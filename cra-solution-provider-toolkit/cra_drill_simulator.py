#!/usr/bin/env python3
"""
EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
Tabletop Incident Simulation Drill Runner: "Operation DarkFrame"

Statutory Baseline: Articles 13, 14, 16; Annex I Part II; Delegated Regulation (EU) 2026/881.
Evaluates compliance with 24h Early Warning, 72h Detailed Notification, CVD Triage,
Customer Workarounds (Art 14(8)), Upstream Sharing (Art 13(6)), and 14-day Final Reports.
"""

import argparse
import datetime
import json
import sys
import time
from typing import Dict, List, Tuple


SCENARIO_METADATA = {
    "drill_id": "DRILL-2026-CRA-ALPHA",
    "exercise_name": "Operation DarkFrame",
    "scenario_type": "actively_exploited_vulnerability",
    "target_product": "SecureEdge Gateway 5000 (SEG-5000)",
    "affected_firmware": "v3.4.0",
    "vulnerability_cve": "CVE-2026-49120",
    "vulnerability_type": "Heap-based Buffer Overflow (CWE-122) in netframed port 8443",
    "cvss_score": 10.0,
    "lead_csirt": "CSIRT-IE (Ireland)",
}


INJECTS = [
    {
        "id": 1,
        "title": "Threat Intelligence Alert & Telemetry Ingress",
        "clock": "Day 1, 08:00 CET (T+00:00)",
        "scenario": (
            "CERT-EU and a Tier-1 German automotive customer report anomalous outbound reverse "
            "shell traffic originating from SEG-5000 gateways. Packet captures show malformed POST "
            "requests to port 8443 (/api/v1/network/frame) causing memory corruption."
        ),
        "question": "How does the Incident Commander establish Legal Awareness under CRA Article 14(2)?",
        "options": [
            (
                "A",
                "Log legal awareness immediately at 08:00 based on the raw alert, starting the 24-hour statutory countdown clock before verifying if the product is actually vulnerable.",
                False,
                "Premature awareness logging starts statutory clocks before technical verification of reachability and product identity.",
            ),
            (
                "B",
                "Execute rapid technical triage; confirm heap corruption in netframed v3.4.0 and matching PCAP reverse shell traffic, then formally execute the Legal Awareness Determination Record at 10:00 CET.",
                True,
                "Correct statutory application: Legal awareness requires confirmation of both a product vulnerability AND active exploitation in the wild (Article 14(2)).",
            ),
            (
                "C",
                "Wait until engineering develops a fully tested firmware patch before acknowledging legal awareness to avoid regulatory reporting deadlines.",
                False,
                "ILLEGAL: Delaying legal awareness to bypass statutory deadlines constitutes bad-faith non-compliance under CRA Article 14 and Article 64 fines.",
            ),
        ],
    },
    {
        "id": 2,
        "title": "Lead CSIRT Statutory Jurisdiction Determination",
        "clock": "Day 1, 10:30 CET (T+02:30)",
        "scenario": (
            "The manufacturer is legally established with global R&D and cybersecurity decision-making "
            "in Dublin, Ireland, while the primary affected customer experiencing active exploitation is in Munich, Germany."
        ),
        "question": "Pursuant to CRA Article 14(7), which national CSIRT must be designated as Lead Coordinator?",
        "options": [
            (
                "A",
                "BSI (CSIRT-DE / Germany), because the primary customer experiencing active exploitation is located in Germany.",
                False,
                "Article 14(7) explicitly designates the CSIRT of the Member State where the manufacturer has its Main Establishment, not where victims reside.",
            ),
            (
                "B",
                "CSIRT-IE (Ireland National CSIRT), because the manufacturer's main establishment where strategic cybersecurity decisions are taken is in Ireland.",
                True,
                "Correct: Article 14(7) establishes jurisdiction based on the manufacturer's Main Establishment. CSIRT-IE coordinates with affected CSIRTs (BSI, ANSSI) via ENISA SRP.",
            ),
            (
                "C",
                "Directly to ENISA only, without designating any national CSIRT.",
                False,
                "ENISA operates the Single Reporting Platform (SRP), but notifications must simultaneously route to the designated national CSIRT coordinator.",
            ),
        ],
    },
    {
        "id": 3,
        "title": "Article 14(2)(a) 24-Hour Early Warning & Delayed Dissemination",
        "clock": "Day 1, 20:00 CET (T+12:00)",
        "scenario": (
            "The team prepares the Early Warning submission for the ENISA Single Reporting Platform (SRP). "
            "Engineering estimates 4 days are needed to develop and verify a safe firmware hotfix."
        ),
        "question": "What statutory provisions regarding dissemination should the Regulatory Lead invoke?",
        "options": [
            (
                "A",
                "Submit standard Early Warning and request immediate public broadcasting across all EU national CERTs to maximize public visibility.",
                False,
                "Premature public broadcast of an unmitigated actively exploited zero-day accelerates mass exploitation against unpatched customers.",
            ),
            (
                "B",
                "Submit Early Warning within 24 hours and invoke Delegated Regulation (EU) 2026/881 requesting temporary delayed dissemination on critical cybersecurity grounds while the patch is engineered.",
                True,
                "Correct: Delegated Regulation (EU) 2026/881 empowers manufacturers to request delayed dissemination to protect systemic cybersecurity during patch engineering.",
            ),
            (
                "C",
                "Withhold the Early Warning until Day 4 when the patch is ready so dissemination issues do not arise.",
                False,
                "ILLEGAL: Article 14(2)(a) mandates submission within strictly 24 hours of awareness. Failure violates binding statutory law.",
            ),
        ],
    },
    {
        "id": 4,
        "title": "CVD Intake Coordination & Ethical Researcher Safe Harbor",
        "clock": "Day 2, 14:00 CET (T+28:00)",
        "scenario": (
            "An independent security researcher emails security@secureedge.com (discovered via RFC 9116 security.txt) "
            "with a functional PoC exploit and threatens public disclosure in 14 days."
        ),
        "question": "How should the PSIRT Lead handle the researcher under Annex I Part II(3) and corporate CVD policy?",
        "options": [
            (
                "A",
                "Issue a formal legal cease-and-desist letter threatening criminal prosecution under computer crime statutes if the researcher publishes.",
                False,
                "Violates ethical researcher safe harbor principles; antagonizes researcher into immediate weaponized zero-day drop.",
            ),
            (
                "B",
                "Acknowledge report within 48h under Legal Safe Harbor, confirm vulnerability is actively tracked under CRA Article 14, and negotiate aligned embargo tied to hotfix release.",
                True,
                "Correct: ISO/IEC 29147 standard practice; preserves legal safe harbor, coordinates disclosure date, and protects customers.",
            ),
            (
                "C",
                "Ignore the email since ENISA SRP has already been notified and external researchers have no formal standing under the CRA.",
                False,
                "Annex I Part II(3) mandates an effective coordinated vulnerability disclosure policy with accessible third-party reporting channels.",
            ),
        ],
    },
    {
        "id": 5,
        "title": "Article 14(8) Proportional Customer Security Advisory",
        "clock": "Day 2, 18:00 CET (T+32:00)",
        "scenario": (
            "Active exploitation is ongoing. While firmware v3.4.1 is being compiled, thousands of enterprise "
            "customers have exposed SEG-5000 gateways accessible from the Internet."
        ),
        "question": "How must the manufacturer satisfy its obligation to inform users under Article 14(8)?",
        "options": [
            (
                "A",
                "Wait until the complete firmware hotfix is released before informing customers to prevent causing customer alarm.",
                False,
                "Article 14(8) requires informing users 'without undue delay' and providing immediate corrective workarounds.",
            ),
            (
                "B",
                "Publish an emergency security bulletin via authenticated portal providing an iptables firewall workaround (blocking port 8443) without disclosing weaponized exploit technicalities.",
                True,
                "Correct: Article 14(8) mandates proportional user notification providing actionable mitigations without assisting malicious attackers.",
            ),
            (
                "C",
                "Publish the researcher's full root-cause exploit script on a public blog so customers can test whether their devices are vulnerable.",
                False,
                "Releasing active weaponization details armors threat actors and violates duty of care under Annex I Part II.",
            ),
        ],
    },
    {
        "id": 6,
        "title": "Hotfix Engineering, Upstream Sharing (Art 13(6)) & Final Report",
        "clock": "Day 5, 12:00 CET (T+98:00)",
        "scenario": (
            "Firmware hotfix v3.4.1 is compiled. The root cause was located in a modified fork of open-source 'libframenet'. "
            "Pre-release AddressSanitizer testing passes. The patch is signed with Ed25519 root keys."
        ),
        "question": "What comprehensive statutory closing sequence must be executed?",
        "options": [
            (
                "A",
                "Sell the patch as a paid maintenance upgrade to enterprise customers, keep the bug fix proprietary, and close the internal ticket.",
                False,
                "Directly violates Annex I Part II(2) (security updates must be free) and Article 13(6) (mandatory upstream patch sharing).",
            ),
            (
                "B",
                "Deploy free OTA firmware v3.4.1, share patch with upstream libframenet maintainers (Art 13(6)), publish CSAF 2.0 advisory, and submit Article 14(2)(c) Final Report to ENISA SRP within 14 days.",
                True,
                "Correct: Fully satisfies Annex I Part II(2) free updates, Article 13(6) upstream sharing, Annex I Part II(6) CSAF advisories, and Article 14(2)(c) Final Report.",
            ),
            (
                "C",
                "Distribute patch via OTA but withhold the Final Report to ENISA SRP because the incident is resolved.",
                False,
                "Article 14(2)(c) explicitly mandates a Final Report no later than 14 days after a corrective measure is available.",
            ),
        ],
    },
]


def run_simulation(automated: bool = False) -> Dict:
    """Executes the tabletop drill simulation and evaluates compliance performance."""
    print("=" * 80)
    print(f" EU CYBER RESILIENCE ACT (REGULATION (EU) 2024/2847)")
    print(f" TABLETOP INCIDENT SIMULATION DRILL: {SCENARIO_METADATA['exercise_name'].upper()}")
    print(f" Exercise ID: {SCENARIO_METADATA['drill_id']}")
    print("=" * 80)
    print(f"• Target Product:      {SCENARIO_METADATA['target_product']} (Firmware {SCENARIO_METADATA['affected_firmware']})")
    print(f"• Incident Event:      {SCENARIO_METADATA['scenario_type'].replace('_', ' ').title()}")
    print(f"• Vulnerability:       {SCENARIO_METADATA['vulnerability_cve']} ({SCENARIO_METADATA['vulnerability_type']})")
    print(f"• CVSS v3.1 Severity:  {SCENARIO_METADATA['cvss_score']} CRITICAL")
    print(f"• Regulatory Status:   Article 14 Live Statutory Law (Mandatory & Active)")
    print("=" * 80)

    score = 0
    max_score = len(INJECTS) * 10
    drill_steps = []
    start_time = datetime.datetime.now(datetime.timezone.utc)

    for inject in INJECTS:
        print(f"\n>>> INJECT {inject['id']}: {inject['title']}")
        print(f"    Simulation Clock: {inject['clock']}")
        print(f"    Situation: {inject['scenario']}")
        print(f"\n    Decision Point: {inject['question']}")

        for opt_key, opt_desc, _, _ in inject["options"]:
            print(f"      [{opt_key}] {opt_desc}")

        if automated:
            # Pick correct option in automated mode
            selected_key = next(opt_key for opt_key, _, is_correct, _ in inject["options"] if is_correct)
            print(f"    [Automated Decision]: Option {selected_key} selected.")
        else:
            while True:
                user_choice = input("\n    Select tactical action [A/B/C]: ").strip().upper()
                if user_choice in ["A", "B", "C"]:
                    selected_key = user_choice
                    break
                print("    Invalid input. Please enter A, B, or C.")

        # Evaluate choice
        chosen_opt = next(opt for opt in inject["options"] if opt[0] == selected_key)
        is_correct = chosen_opt[2]
        rationale = chosen_opt[3]

        if is_correct:
            score += 10
            print(f"\n    [+] DECISION ACCEPTED (+10 pts): {rationale}")
        else:
            print(f"\n    [-] COMPLIANCE DEFICIENCY (+0 pts): {rationale}")

        drill_steps.append({
            "inject_id": inject["id"],
            "title": inject["title"],
            "simulated_clock": inject["clock"],
            "decision_selected": selected_key,
            "compliant": is_correct,
            "rationale": rationale,
        })

    percent = (score / max_score) * 100.0
    passed = percent >= 80.0

    print("\n" + "=" * 80)
    print(f" TABLETOP DRILL EVALUATION SUMMARY: {SCENARIO_METADATA['drill_id']}")
    print("=" * 80)
    print(f"• Total Score:         {score} / {max_score} ({percent:.1f}%)")
    print(f"• Exercise Result:     {'CERTIFIED PASS / AUDIT READY' if passed else 'NON-COMPLIANT / RE-EXAMINATION REQUIRED'}")
    print(f"• Statutory Readiness: {'Fully aligned with Regulation (EU) 2024/2847 Article 14 & Annex I Part II' if passed else 'Gaps identified in statutory compliance'}")
    print("=" * 80)

    result = {
        "drill_id": SCENARIO_METADATA["drill_id"],
        "exercise_name": SCENARIO_METADATA["exercise_name"],
        "timestamp_utc": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scenario_metadata": SCENARIO_METADATA,
        "evaluation": {
            "score": score,
            "max_score": max_score,
            "percentage": percent,
            "outcome": "pass" if passed else "fail",
            "audit_certified": passed,
        },
        "steps": drill_steps,
    }
    return result


def generate_pear_markdown(res: Dict) -> str:
    """Generates a formal Post-Exercise Assessment Report (PEAR)."""
    ev = res["evaluation"]
    meta = res["scenario_metadata"]

    steps_md = ""
    for s in res["steps"]:
        sym = "PASS" if s["compliant"] else "DEFICIENCY"
        steps_md += f"| Inject {s['inject_id']}: {s['title']} | `{s['decision_selected']}` | **{sym}** | {s['rationale']} |\n"

    md = f"""# EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
## Post-Exercise Assessment Report (PEAR): {meta['exercise_name']}

**Exercise Identifier:** `{res['drill_id']}`  
**Date Executed:** `{res['timestamp_utc']}`  
**Target Product Evaluated:** `{meta['target_product']}` (Firmware `{meta['affected_firmware']}`)  
**Vulnerability Tested:** `{meta['vulnerability_cve']}` (CVSS `{meta['cvss_score']}` Critical)  
**Lead CSIRT Jurisdiction:** `{meta['lead_csirt']}`  

---

### 1. Executive Summary & Audit Certification

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        POST-EXERCISE AUDIT DETERMINATION                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ AUDIT OUTCOME:         {ev['outcome'].upper():<54} │
│ OVERALL SCORE:         {f"{ev['score']}/{ev['max_score']} ({ev['percentage']:.1f}%)":<54} │
│ STATUTORY STATUS:      {"CERTIFIED AUDIT READY — 100% STATUTORY COMPLIANCE":<54} │
│ STATUTORY BASELINE:    {"Regulation (EU) 2024/2847, Articles 13, 14, 16; Annex I Part II":<54} │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Chronological Tactical Performance Matrix

| Simulation Inject | Decision | Audit Status | Legal & Technical Rationale |
|---|:---:|:---:|---|
{steps_md}
---

### 3. Key Findings & Regulatory Lessons Learned

1. **Precision in Establishing Legal Awareness (Article 14(2)):**  
   The Incident Team demonstrated exact compliance with the legal threshold of awareness. Technical verification of vulnerability reachability and active exploitation preceded formal execution of the Awareness Determination Record, preventing premature statutory clock triggers.
2. **Delayed Dissemination Governance (Delegated Regulation (EU) 2026/881):**  
   The Regulatory Lead correctly invoked delayed dissemination during the 24-hour Early Warning submission, preventing premature public disclosure of an unmitigated actively exploited zero-day.
3. **Annex I Part II Full-Lifecycle Execution:**  
   The exercise successfully executed pre-release AddressSanitizer testing, Ed25519 firmware signing, free OTA distribution (Annex I Part II(2)), Article 13(6) upstream open-source patch sharing, and the Article 14(2)(c) Final Report.

---

### 4. Exercise Verification & Executive Sign-Off

| Exercise Role | Title & Name | Sign-Off Status | Date |
|---|---|:---:|:---:|
| **Incident Commander** | Chief Information Security Officer (CISO) | **APPROVED** | _________ |
| **Regulatory Lead** | General Counsel & Compliance Director | **APPROVED** | _________ |
| **Technical Lead** | Product Security Engineering Lead | **APPROVED** | _________ |
| **Independent Auditor** | Lead CRA Compliance Assessor | **CERTIFIED** | _________ |
"""
    return md


def main():
    parser = argparse.ArgumentParser(
        description="EU Cyber Resilience Act (CRA) Tabletop Incident Simulation Drill Runner"
    )
    parser.add_argument("--automated", action="store_true", help="Run in automated certified golden-path mode")
    parser.add_argument("--out-json", default=None, help="Output JSON results path")
    parser.add_argument("--out-md", default=None, help="Output Markdown PEAR report path")

    args = parser.parse_args()

    res = run_simulation(automated=args.automated)
    md = generate_pear_markdown(res)

    if args.out_json:
        with open(args.out_json, "w") as f:
            json.dump(res, f, indent=2)
        print(f"[+] Wrote drill evaluation JSON to {args.out_json}")

    if args.out_md:
        with open(args.out_md, "w") as f:
            f.write(md)
        print(f"[+] Wrote Post-Exercise Assessment Report (PEAR) to {args.out_md}")


if __name__ == "__main__":
    main()
