#!/usr/bin/env python3
"""EU Cyber Resilience Act (Regulation (EU) 2024/2847) & GDPR Dual-Track Reporting Calculator.

Computes statutory reporting milestones:
- Cyber Resilience Act (CRA Art. 14):
    * Early warning: within 24 hours of awareness (ENISA SRP & Lead CSIRT)
    * User advisory: within 24 hours of awareness (Art. 14(8))
    * Detailed notification: within 72 hours of awareness (ENISA SRP)
    * Final report: within 14 days of fix/workaround (vuln) or 1 month (incident)
- General Data Protection Regulation (GDPR Art. 33/34):
    * Personal Data Breach to DPA: within 72 hours of awareness
    * Processor-to-Controller Alert: without undue delay (contractual 24-48h SLA)

Features:
- calc: Calculate statutory deadlines from ISO-8601 awareness timestamp.
- triage: Execute MYBU / SEC-PRO-CRA-001 5-question triage + GDPR data breach gate,
          enforcing the 20-hour internal buffer target, customer notification SLAs,
          DPA parallel deadlines, and producing audit-ready JSON/Markdown records.
- drill: Validate Tabletop Drill logs against the CRA drill reporting schema.
"""

import argparse
import calendar
import json
import os
import sys
from datetime import datetime, timedelta


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO-8601 timestamp and verify presence of timezone offset."""
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError(f"Timestamp {ts!r} has no UTC offset; statutory clocks must be timezone-aware.")
    return d


def add_one_month(d: datetime) -> datetime:
    """Add exactly one calendar month to a datetime object, clamping to month end."""
    year, month = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
    day = min(d.day, calendar.monthrange(year, month)[1])
    return d.replace(year=year, month=month, day=day)


def compute_deadlines(
    kind: str,
    awareness: datetime,
    mitigation: datetime | None = None,
    notification_submitted: datetime | None = None,
) -> dict:
    """Compute statutory reporting milestones from awareness timestamp."""
    early_warning = awareness + timedelta(hours=24)
    notification_due = awareness + timedelta(hours=72)

    result = {
        "event_type": kind,
        "legal_basis": "Regulation (EU) 2024/2847 (Cyber Resilience Act) - Article 14",
        "enforcement_status": "Statutory Law (In effect since 11 September 2026)",
        "platform": "ENISA Single Reporting Platform (https://portal.cra-srp.enisa.europa.eu)",
        "timestamps": {
            "awareness": awareness.isoformat(),
            "early_warning_due": early_warning.isoformat(),
            "notification_due": notification_due.isoformat(),
        },
        "deadlines_summary": {
            "early_warning_24h": {
                "deadline": early_warning.isoformat(),
                "legal_reference": "Article 14(2)(a)" if kind == "vulnerability" else "Article 14(4)(a)",
                "action": "Submit product identity, general nature of event, EU Member States affected, and optional delay request.",
            },
            "notification_72h": {
                "deadline": notification_due.isoformat(),
                "legal_reference": "Article 14(2)(b)" if kind == "vulnerability" else "Article 14(4)(b)",
                "action": "Submit detailed vulnerability/exploit or incident data, mitigation measures, and sensitivity grading.",
            },
        },
        "user_notification_rule": {
            "legal_reference": "Article 14(8)",
            "timing": "Without undue delay following awareness (statutory target <= 24h)",
            "format": "Machine-readable (CSAF 2.0 / CycloneDX) and human-readable",
        },
    }

    if kind == "vulnerability":
        result["final_report_rule"] = {
            "legal_reference": "Article 14(2)(c)",
            "rule": "No later than 14 calendar days after a corrective or mitigating measure is made available.",
        }
        if mitigation:
            final_due = mitigation + timedelta(days=14)
            result["timestamps"]["mitigation_available"] = mitigation.isoformat()
            result["timestamps"]["final_report_due"] = final_due.isoformat()
            result["deadlines_summary"]["final_report_14d"] = {
                "deadline": final_due.isoformat(),
                "status": "Calculated from patch release timestamp",
            }
        else:
            result["timestamps"]["final_report_due"] = None
            result["deadlines_summary"]["final_report_14d"] = {
                "status": "Pending patch release (--mitigation-available parameter)",
            }
    else:  # incident
        result["final_report_rule"] = {
            "legal_reference": "Article 14(4)(c)",
            "rule": "Within 1 calendar month after the submission of the 72-hour incident notification.",
        }
        if notification_submitted:
            final_due = add_one_month(notification_submitted)
            result["timestamps"]["notification_submitted"] = notification_submitted.isoformat()
            result["timestamps"]["final_report_due"] = final_due.isoformat()
            result["deadlines_summary"]["final_report_1m"] = {
                "deadline": final_due.isoformat(),
                "status": "Calculated from 72h notification submission timestamp",
            }
        else:
            est_due = add_one_month(notification_due)
            result["timestamps"]["final_report_due"] = None
            result["timestamps"]["final_report_planning_estimate"] = est_due.isoformat()
            result["deadlines_summary"]["final_report_1m"] = {
                "planning_estimate": est_due.isoformat(),
                "note": "Estimate assumes notification submitted at 72-hour limit. Supply --notification-submitted for actual deadline.",
            }

    return result


def evaluate_triage(
    event_id: str,
    product_name: str,
    t0: datetime,
    q1_supplied: bool,
    q2_manufacturer: bool,
    q3_exploited: bool | None,
    q4_exploitable: bool | None,
    q4_justification: str | None,
    q5_severe_incident: bool | None,
    q6_data_breached: bool | None = None,
    lead_csirt: str = "CSIRT-IE",
    lead_dpa: str = "Data Protection Commission (Ireland)",
    business_unit: str = "MYBU",
) -> dict:
    """Execute the 5-Question decision triage + GDPR Data Breach Gate under CRA Art. 14, GDPR Art. 33, and SEC-PRO-CRA-001.

    Decision Rules:
    - CRA Reportable if: (Q1 and Q2 and Q3 and Q4) OR (Q1 and Q2 and Q5)
    - GDPR Reportable if: Q6 is True (Personal Data Compromised)
    - Buffer Rule: Internal filing target is T0 + 20 hours (4h safety buffer before 24h statutory cliff)
    """
    is_vuln_reportable = bool(q1_supplied and q2_manufacturer and q3_exploited and q4_exploitable)
    is_incident_reportable = bool(q1_supplied and q2_manufacturer and q5_severe_incident)
    cra_reportable = is_vuln_reportable or is_incident_reportable
    gdpr_reportable = bool(q6_data_breached)

    target_20h = t0 + timedelta(hours=20)
    early_warning_24h = t0 + timedelta(hours=24)
    customer_notif_24h = t0 + timedelta(hours=24)
    detailed_notif_72h = t0 + timedelta(hours=72)
    gdpr_dpa_72h = t0 + timedelta(hours=72)

    branch = "vulnerability" if is_vuln_reportable else ("incident" if is_incident_reportable else "none")

    # Assess findings
    findings = []
    if not q1_supplied:
        findings.append("Q1=No: Product not supplied by us. CRA obligations do not attach.")
    if not q2_manufacturer:
        findings.append("Q2=No: Entity is not the manufacturer/brand-placer. Pass upstream to manufacturer.")
    if q3_exploited is False:
        findings.append("Q3=No: Vulnerability has no credible evidence of in-the-wild exploitation. CVSS alone does not trigger Art 14.")
    if q4_exploitable is False:
        if not q4_justification or len(q4_justification.strip()) < 15:
            findings.append("CRITICAL AUDIT RISK: Q4=No requires a documented, signed technical justification (NEDR record under §9).")
        else:
            findings.append(f"Q4=No substantiated: {q4_justification.strip()} (Signed NEDR required)")
    if q5_severe_incident is False:
        findings.append("Q5=No: Incident does not meet the Article 14(4) severe impact or malicious code execution threshold.")

    if gdpr_reportable:
        findings.append(
            "PARALLEL REGULATORY DUTY: Personal data breach confirmed under GDPR Art. 33. "
            "Filing on the ENISA Single Reporting Platform does NOT satisfy GDPR. "
            "A separate filing to the competent Data Protection Authority (DPA) is mandatory within 72 hours."
        )

    # Next actions
    next_actions = []
    if cra_reportable:
        next_actions.extend([
            f"[CRA INTERNAL] File Early Warning to ENISA SRP before internal buffer: {target_20h.isoformat()}",
            f"[CRA STATUTORY ⚖️] ENISA SRP Early Warning hard cliff: {early_warning_24h.isoformat()}",
            f"[CRA STATUTORY ⚖️] Disseminate Article 14(8) Proportional Customer Security Advisory: {customer_notif_24h.isoformat()}",
            f"[CRA STATUTORY ⚖️] Submit 72-Hour Detailed Notification to ENISA SRP: {detailed_notif_72h.isoformat()}",
        ])
    else:
        next_actions.extend([
            "Archive negative CRA determination in 10-Year Incident Ledger",
            "If Q4=No, execute signed Technical Non-Exploitability Determination Record (NEDR)",
            "Notify upstream maintainer under Article 13(5) if component is third-party/FOSS",
        ])

    if gdpr_reportable:
        next_actions.extend([
            f"[GDPR STATUTORY ⚖️] Submit Personal Data Breach Notification to Lead DPA ({lead_dpa}): {gdpr_dpa_72h.isoformat()}",
            "[GDPR / B2B] If acting as Data Processor, notify Customer Data Controller without undue delay",
            "[GDPR] Convene emergency Data Protection Officer (DPO) and Legal breach committee",
        ])

    next_actions.append("[AUDIT] Retain T0 email headers, triage record, DPA receipts, and SRP screenshots for 10 years in WORM vault")

    record = {
        "event_id": event_id,
        "product_name": product_name,
        "business_unit": business_unit,
        "lead_csirt": lead_csirt,
        "lead_dpa": lead_dpa,
        "t0_arrival_utc": t0.isoformat(),
        "triage_completed_utc": datetime.now(t0.tzinfo).isoformat(),
        "questions_evaluated": {
            "q1_product_supplied": q1_supplied,
            "q2_manufacturer_entity": q2_manufacturer,
            "q3_vulnerability_actively_exploited": q3_exploited,
            "q4_vulnerability_exploitable_in_our_build": q4_exploitable,
            "q5_severe_incident_or_malicious_code": q5_severe_incident,
            "q6_personal_data_breached": gdpr_reportable,
        },
        "determination": {
            "cra_reportable": cra_reportable,
            "gdpr_reportable": gdpr_reportable,
            "overall_reportable": cra_reportable or gdpr_reportable,
            "cra_governing_branch": branch,
            "cra_legal_basis": "Regulation (EU) 2024/2847 Art. 14(2)" if branch == "vulnerability" else (
                "Regulation (EU) 2024/2847 Art. 14(4)" if branch == "incident" else "CRA Scope Exclusion"
            ),
            "gdpr_legal_basis": "Regulation (EU) 2016/679 Art. 33" if gdpr_reportable else "None (No Personal Data Breach)",
            "findings_summary": findings,
            "q4_non_exploitability_justification": q4_justification if q4_exploitable is False else None,
        },
        "statutory_timelines": {
            "cra_internal_target_20h": target_20h.isoformat() if cra_reportable else None,
            "cra_early_warning_srp_24h": early_warning_24h.isoformat() if cra_reportable else None,
            "cra_customer_advisory_24h": customer_notif_24h.isoformat() if cra_reportable else None,
            "cra_detailed_notification_srp_72h": detailed_notif_72h.isoformat() if cra_reportable else None,
            "gdpr_dpa_notification_72h": gdpr_dpa_72h.isoformat() if gdpr_reportable else None,
            "cra_final_report_rule": (
                "T+14 calendar days from hotfix OR workaround release"
                if branch == "vulnerability"
                else ("T+1 calendar month from 72h notification submission" if branch == "incident" else None)
            ),
        },
        "mandatory_next_actions": next_actions,
    }

    return record


def validate_drill_log(file_path: str) -> bool:
    """Validate a JSON tabletop drill log file."""
    if not os.path.exists(file_path):
        print(f"[-] Error: File not found: {file_path}", file=sys.stderr)
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = ["drill_id", "scenario_type", "scenario", "awareness_timestamp", "deadlines", "steps", "outcome"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"[-] Validation Failed: Missing required root keys: {missing}", file=sys.stderr)
        return False

    if not data.get("fictional", False):
        print("[-] Validation Warning: 'fictional' must be true for simulated drills to avoid live platform confusion.", file=sys.stderr)

    steps = data.get("steps", [])
    print(f"[+] Drill ID: {data.get('drill_id')}")
    print(f"[+] Scenario: {data.get('scenario')}")
    print(f"[+] Outcome: {data.get('outcome')}")
    print(f"[+] Total Drill Steps: {len(steps)}")
    all_on_time = True
    for idx, s in enumerate(steps, start=1):
        status_sym = "[OK]" if s.get("on_time") else "[LATE/MISSING]"
        if not s.get("on_time"):
            all_on_time = False
        print(f"    Step {idx:02d}: {status_sym} {s.get('step')} (Planned by: {s.get('planned_by')})")

    if all_on_time and data.get("outcome") in ("pass", "pass_with_findings"):
        print("[+] Drill Validation Result: SUCCESSFUL & AUDIT READY")
        return True
    else:
        print("[-] Drill Validation Result: FAILED OR FINDINGS REQUIRE REMEDIATION")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="EU CRA Article 14 & GDPR Statutory Reporting Deadline Calculator & Triage Gate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Command: calc
    calc_parser = subparsers.add_parser("calc", help="Calculate statutory deadlines")
    calc_parser.add_argument("--type", choices=["vulnerability", "incident"], required=True, help="Event category")
    calc_parser.add_argument("--awareness", required=True, help="ISO-8601 awareness timestamp with timezone (e.g. 2026-10-12T14:00:00+02:00)")
    calc_parser.add_argument("--mitigation-available", help="ISO-8601 patch/mitigation timestamp (for vulnerabilities)")
    calc_parser.add_argument("--notification-submitted", help="ISO-8601 notification submission timestamp (for incidents)")
    calc_parser.add_argument("--json", action="store_true", help="Output pure JSON")

    # Command: triage / mybu-triage
    triage_parser = subparsers.add_parser("triage", aliases=["mybu-triage"], help="Execute MYBU / SEC-PRO-CRA-001 5-question rapid triage + GDPR gate")
    triage_parser.add_argument("--product", default="Delivered System", help="Commercial product name")
    triage_parser.add_argument("--event-id", default=f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}", help="Event ID")
    triage_parser.add_argument("--t0", "--awareness", dest="t0", required=True, help="T0 arrival timestamp (ISO-8601 with timezone)")
    triage_parser.add_argument("--q1-supplied", choices=["yes", "no"], default="yes", help="Q1: Did we supply the product?")
    triage_parser.add_argument("--q2-manufacturer", choices=["yes", "no"], default="yes", help="Q2: Are we the manufacturer / brand-placer?")
    triage_parser.add_argument("--q3-exploited", choices=["yes", "no"], help="Q3: Is vulnerability actively exploited in the wild?")
    triage_parser.add_argument("--q4-exploitable", choices=["yes", "no"], help="Q4: Is vulnerability exploitable in our build & configuration?")
    triage_parser.add_argument("--q4-justification", help="Technical justification if Q4=no (signed NEDR baseline)")
    triage_parser.add_argument("--q5-severe-incident", choices=["yes", "no"], help="Q5: Severe incident or malicious code execution?")
    triage_parser.add_argument("--data-breached", choices=["yes", "no"], default="no", help="Q6: Was personal data compromised (GDPR Art. 33)?")
    triage_parser.add_argument("--lead-csirt", default="CSIRT-IE", help="Lead CSIRT jurisdiction")
    triage_parser.add_argument("--lead-dpa", default="Data Protection Commission (Ireland)", help="Lead Supervisory Data Protection Authority")
    triage_parser.add_argument("--out-json", help="Path to write JSON triage record")
    triage_parser.add_argument("--out-md", help="Path to write Markdown summary")
    triage_parser.add_argument("--json", action="store_true", help="Print JSON output directly")

    # Command: drill
    drill_parser = subparsers.add_parser("drill", help="Validate a simulation drill record")
    drill_parser.add_argument("file", help="Path to drill record JSON file")

    # Compatibility mode for flat flags
    parser.add_argument("--type", choices=["vulnerability", "incident"], help="Event category (compat)")
    parser.add_argument("--awareness", help="Awareness timestamp (compat)")
    parser.add_argument("--mitigation-available", help="Mitigation timestamp (compat)")
    parser.add_argument("--notification-submitted", help="Notification submitted timestamp (compat)")
    parser.add_argument("--validate-drill", help="Validate drill record file (compat)")

    args = parser.parse_args()

    # Handle flat arguments if subcommands not explicitly used
    if args.validate_drill:
        ok = validate_drill_log(args.validate_drill)
        sys.exit(0 if ok else 1)
    elif args.awareness and args.type:
        dt_aware = parse_timestamp(args.awareness)
        dt_mit = parse_timestamp(args.mitigation_available) if args.mitigation_available else None
        dt_notif = parse_timestamp(args.notification_submitted) if args.notification_submitted else None
        res = compute_deadlines(args.type, dt_aware, dt_mit, dt_notif)
        print(json.dumps(res, indent=2))
        sys.exit(0)
    elif args.command == "calc":
        dt_aware = parse_timestamp(args.awareness)
        dt_mit = parse_timestamp(args.mitigation_available) if args.mitigation_available else None
        dt_notif = parse_timestamp(args.notification_submitted) if args.notification_submitted else None
        res = compute_deadlines(args.type, dt_aware, dt_mit, dt_notif)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("\n=======================================================")
            print(" CRA ARTICLE 14 STATUTORY DEADLINE SUMMARY")
            print("=======================================================")
            print(f" Event Category:        {res['event_type'].upper()}")
            print(f" Awareness Timestamp:   {res['timestamps']['awareness']}")
            print("-------------------------------------------------------")
            print(f" [1] 24H Early Warning: {res['timestamps']['early_warning_due']}")
            print(f" [2] 72H Notification:  {res['timestamps']['notification_due']}")
            if res['timestamps']['final_report_due']:
                print(f" [3] Final Report Due:  {res['timestamps']['final_report_due']}")
            elif "final_report_planning_estimate" in res['timestamps']:
                print(f" [3] Final Report Est:  {res['timestamps']['final_report_planning_estimate']} (Est.)")
            print("=======================================================\n")
        sys.exit(0)
    elif args.command in ("triage", "mybu-triage"):
        dt_t0 = parse_timestamp(args.t0)
        q1 = args.q1_supplied == "yes"
        q2 = args.q2_manufacturer == "yes"
        q3 = True if args.q3_exploited == "yes" else (False if args.q3_exploited == "no" else None)
        q4 = True if args.q4_exploitable == "yes" else (False if args.q4_exploitable == "no" else None)
        q5 = True if args.q5_severe_incident == "yes" else (False if args.q5_severe_incident == "no" else None)
        q6 = args.data_breached == "yes"

        record = evaluate_triage(
            event_id=args.event_id,
            product_name=args.product,
            t0=dt_t0,
            q1_supplied=q1,
            q2_manufacturer=q2,
            q3_exploited=q3,
            q4_exploitable=q4,
            q4_justification=args.q4_justification,
            q5_severe_incident=q5,
            q6_data_breached=q6,
            lead_csirt=args.lead_csirt,
            lead_dpa=args.lead_dpa,
        )

        if args.out_json:
            with open(args.out_json, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2)
            print(f"[+] Wrote triage audit record to {args.out_json}")

        if args.out_md:
            with open(args.out_md, "w", encoding="utf-8") as f:
                f.write(f"# CRA & GDPR Triage Decision Record: {record['event_id']}\n\n")
                f.write(f"- **Product:** {record['product_name']}\n")
                f.write(f"- **T0 Arrival:** {record['t0_arrival_utc']}\n")
                f.write(f"- **CRA Reportable:** **{'YES (Art. 14 Mandatory)' if record['determination']['cra_reportable'] else 'NO (Scope Exclusion)'}**\n")
                f.write(f"- **GDPR Data Breach:** **{'YES (Art. 33 Mandatory)' if record['determination']['gdpr_reportable'] else 'NO'}**\n\n")
                if record['statutory_timelines']:
                    f.write("## Statutory Deadlines\n\n")
                    for k, v in record['statutory_timelines'].items():
                        if v:
                            f.write(f"- **{k}:** `{v}`\n")
                f.write("\n## Findings & Actions\n\n")
                for act in record['mandatory_next_actions']:
                    f.write(f"- {act}\n")
            print(f"[+] Wrote triage markdown report to {args.out_md}")

        if args.json:
            print(json.dumps(record, indent=2))
        else:
            print("\n=======================================================")
            print(" CRA ARTICLE 14 & GDPR DATA BREACH TRIAGE GATE")
            print(" (MYBU Procedure v1.1 / SEC-PRO-CRA-001)")
            print("=======================================================")
            print(f" Event ID:            {record['event_id']}")
            print(f" Target Product:      {record['product_name']}")
            print(f" Ingress T0 (UTC):    {record['t0_arrival_utc']}")
            print("-------------------------------------------------------")
            cra_color = "🔴 REPORTABLE (Art. 14)" if record['determination']['cra_reportable'] else "🟢 NON-REPORTABLE"
            gdpr_color = "🚨 PERSONAL DATA BREACH (GDPR Art. 33)" if record['determination']['gdpr_reportable'] else "🟢 NO DATA BREACH"
            print(f" CRA Status:          {cra_color}")
            print(f" GDPR Status:         {gdpr_color}")
            print(f" CRA Basis:           {record['determination']['cra_legal_basis']}")
            print(f" GDPR Basis:          {record['determination']['gdpr_legal_basis']}")
            print("-------------------------------------------------------")
            print(" DECISION EVALUATION SUMMARY:")
            q = record['questions_evaluated']
            print(f" [Q1] Product Supplied by Us:       {'YES' if q['q1_product_supplied'] else 'NO'}")
            print(f" [Q2] Manufacturer / Brand Placer:  {'YES' if q['q2_manufacturer_entity'] else 'NO'}")
            print(f" [Q3] Actively Exploited in Wild:   {str(q['q3_vulnerability_actively_exploited']).upper()}")
            print(f" [Q4] Exploitable in Our Build:     {str(q['q4_vulnerability_exploitable_in_our_build']).upper()}")
            print(f" [Q5] Severe Incident / Code Exec:  {str(q['q5_severe_incident_or_malicious_code']).upper()}")
            print(f" [Q6] Personal Data Compromised:    {str(q['q6_personal_data_breached']).upper()}")
            print("-------------------------------------------------------")
            st = record['statutory_timelines']
            print(" MANDATORY STATUTORY & INTERNAL COUNTDOWNS:")
            if st['cra_internal_target_20h']:
                print(f"  * [20h CRA Buffer] Internal Early Warning: {st['cra_internal_target_20h']} (Buffer: 4h)")
            if st['cra_early_warning_srp_24h']:
                print(f"  * [24h CRA Legal ⚖️] ENISA SRP Early Warning: {st['cra_early_warning_srp_24h']}")
            if st['cra_customer_advisory_24h']:
                print(f"  * [24h CRA Legal ⚖️] Customer Security Alert:  {st['cra_customer_advisory_24h']}")
            if st['cra_detailed_notification_srp_72h']:
                print(f"  * [72h CRA Legal ⚖️] Detailed SRP Notification: {st['cra_detailed_notification_srp_72h']}")
            if st['gdpr_dpa_notification_72h']:
                print(f"  * [72h GDPR Legal ⚖️] National DPA Breach Filing: {st['gdpr_dpa_notification_72h']} (Lead DPA: {record['lead_dpa']})")
            if st['cra_final_report_rule']:
                print(f"  * [CRA Final Report] {st['cra_final_report_rule']}")
            print("-------------------------------------------------------")
            print(" MANDATORY NEXT ACTIONS:")
            for act in record['mandatory_next_actions']:
                print(f"  * {act}")
            print("=======================================================\n")
        sys.exit(0)
    elif args.command == "drill":
        ok = validate_drill_log(args.file)
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
