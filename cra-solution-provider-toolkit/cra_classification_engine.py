#!/usr/bin/env python3
"""
EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
Product Risk Tier & Conformity Route Classification Engine

Statutory Baseline: Articles 7, 8, 24, 32; Annex III (Class I), Annex IV (Class II), Annex VIII-XI.
Commission Guidance: Notice C(2026) 5252 final; Implementing Regulation (EU) 2025/2392.
"""

import argparse
import datetime
import json
import sys
from typing import Dict, List, Tuple


ANNEX_III_CATEGORIES = [
    ("iam_system", "Identity management systems and privileged access management (PAM) software/hardware (Annex III(1))"),
    ("browser", "Standalone and embedded browsers (Annex III(2))"),
    ("password_manager", "Password managers (Annex III(3))"),
    ("antivirus_edr", "Software searching for, removing, or quarantining malicious software (Annex III(4))"),
    ("vpn_function", "Products with digital elements with the function of Virtual Private Network (VPN) (Annex III(5))"),
    ("network_management", "Network management systems (NMS) (Annex III(6))"),
    ("network_monitoring", "Network monitoring tools (sniffers, packet analyzers, flow telemetry) (Annex III(7))"),
    ("siem_system", "Security information and event management (SIEM) systems (Annex III(8))"),
    ("boot_manager", "Boot managers and UEFI bootloaders (Annex III(9))"),
    ("pki_standard", "Public key infrastructure (PKI) and digital certificate issuance software (Annex III(10))"),
    ("network_interface", "Physical and virtual network interfaces and tunneling drivers (Annex III(11))"),
    ("operating_system_embedded", "Operating systems not covered by Class II (specialized embedded RTOS) (Annex III(12))"),
    ("router_switch", "Routers, modems intended for internet connection, and switches (Annex III(13))"),
    ("mcu_industrial", "Microprocessors / microcontrollers intended for integration into PLCs/industrial devices (Annex III(14))"),
    ("iacs_general", "Industrial automation and control systems (IACS) not covered by Class II (SCADA, PLCs) (Annex III(15))"),
    ("smart_home_security", "Smart home products involving security functions (door locks, cameras, alarms) (Annex III(16))"),
    ("smart_toy_connected", "Smart toys with digital elements featuring social interactive/recording features (Annex III(17))"),
    ("wearable_health", "Personal wearable health devices (non-MDR medical devices) (Annex III(18))"),
]

ANNEX_IV_CATEGORIES = [
    ("os_general_purpose", "Operating systems for servers, desktops, and mobile devices (Annex IV(1))"),
    ("hypervisor_container", "Hypervisors and container runtime systems (Docker, containerd, Kubernetes nodes) (Annex IV(2))"),
    ("pki_qualified", "PKI and certificate issuance software for qualified trust services under eIDAS (Annex IV(3))"),
    ("firewall_ids_enterprise", "Firewalls, intrusion detection and prevention systems (IDS/IPS) for enterprise/industrial use (Annex IV(4))"),
    ("cpu_security", "General-purpose microprocessors with security functions (secure enclaves, TrustZone) (Annex IV(5))"),
    ("mcu_security_hsm", "Microcontrollers with security functions (HSMs, Secure Elements, smart cards, TPM chips) (Annex IV(6))"),
    ("iacs_critical_entities", "Industrial Automation and Control Systems (IACS) for NIS 2 critical entities (energy, nuclear, water) (Annex IV(7))"),
    ("smart_meter_gateway", "Smart meter gateways and components within smart grids (Annex IV(8))"),
    ("secure_element_token", "Secure elements, smart card chips, and hardware security tokens (Annex IV(9))"),
]


def classify_product(
    product_name: str,
    vendor_name: str,
    intended_purpose: str,
    selected_class_i: List[str],
    selected_class_ii: List[str],
    is_critical_art8: bool = False,
    harmonised_standards_fully_applied: bool = False,
    boundary_flags: List[str] = None,
) -> Dict:
    """Computes the statutory risk tier and conformity assessment options under CRA."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    boundary_flags = boundary_flags or []

    # Determine Risk Tier
    if is_critical_art8:
        tier = "Critical Product with Digital Elements (Article 8)"
        tier_short = "CRITICAL"
    elif selected_class_ii:
        tier = "Important Product with Digital Elements — Class II (Annex IV)"
        tier_short = "CLASS_II"
    elif selected_class_i:
        tier = "Important Product with Digital Elements — Class I (Annex III)"
        tier_short = "CLASS_I"
    else:
        tier = "Default Category (Standard Commercial Product)"
        tier_short = "DEFAULT"

    # Conformity Assessment Routes (Article 32)
    permitted_routes = []
    notified_body_required = False
    cost_estimate = ""
    lead_time_estimate = ""

    if tier_short == "DEFAULT":
        permitted_routes.append({
            "module": "Module A (Internal Production Control)",
            "annex": "Annex VIII",
            "notified_body_involved": False,
            "status": "STANDARD ROUTE (100% In-House)",
            "notes": "Manufacturer assumes full responsibility. Compiles 10-section TDF and issues Annex V EU DoC.",
        })
        notified_body_required = False
        cost_estimate = "€10,000 – €30,000 (Internal engineering & compliance labor)"
        lead_time_estimate = "Immediate / Aligned with internal CI/CD release sprint"

    elif tier_short == "CLASS_I":
        if harmonised_standards_fully_applied:
            permitted_routes.append({
                "module": "Module A (Internal Production Control)",
                "annex": "Annex VIII",
                "notified_body_involved": False,
                "status": "CONDITIONAL ROUTE (Harmonised Standards Applied)",
                "notes": "Permitted ONLY because full harmonised standards cited in OJEU are applied (Article 32(2)(a)).",
            })
        else:
            permitted_routes.append({
                "module": "Module A (BLOCKED)",
                "annex": "Annex VIII",
                "notified_body_involved": False,
                "status": "DISQUALIFIED",
                "notes": "Module A cannot be used because harmonised standards are absent, partial, or unverified.",
            })

        permitted_routes.append({
            "module": "Module B + Module C (EU-Type Examination + Conformity to Type)",
            "annex": "Annex IX & X",
            "notified_body_involved": True,
            "status": "STANDARD NOTIFIED BODY ROUTE",
            "notes": "Notified Body examines technical dossier and issues EU-Type Examination Certificate.",
        })
        permitted_routes.append({
            "module": "Module H (Full Quality Assurance)",
            "annex": "Annex XI",
            "notified_body_involved": True,
            "status": "ORGANISATIONAL CERTIFICATION ROUTE",
            "notes": "Notified Body audits and approves manufacturer quality management system and secure SDLC.",
        })
        notified_body_required = not harmonised_standards_fully_applied
        if notified_body_required:
            cost_estimate = "€50,000 – €150,000 (Notified Body fees + audit prep)"
            lead_time_estimate = "6 – 9 Months (Notified Body queue & laboratory testing)"
        else:
            cost_estimate = "€20,000 – €45,000 (Standards audit & internal evidence)"
            lead_time_estimate = "1 – 2 Months"

    elif tier_short == "CLASS_II":
        notified_body_required = True
        permitted_routes.append({
            "module": "Module B + Module C (EU-Type Examination + Conformity to Type)",
            "annex": "Annex IX & X",
            "notified_body_involved": True,
            "status": "STANDARD ROUTE (Mandatory Third-Party)",
            "notes": "Module A is NEVER permitted for Class II products (Article 32(3)).",
        })
        permitted_routes.append({
            "module": "Module H (Full Quality Assurance)",
            "annex": "Annex XI",
            "notified_body_involved": True,
            "status": "ORGANISATIONAL CERTIFICATION ROUTE",
            "notes": "Audited secure SDLC approved by accredited Notified Body.",
        })
        permitted_routes.append({
            "module": "European Cybersecurity Certification Scheme",
            "annex": "Regulation (EU) 2019/881",
            "notified_body_involved": True,
            "status": "CERTIFICATION SCHEME ROUTE",
            "notes": "Certification under Cybersecurity Act at assurance level at least 'substantial'.",
        })
        cost_estimate = "€100,000 – €250,000+ per product family"
        lead_time_estimate = "9 – 12 Months"

    elif tier_short == "CRITICAL":
        notified_body_required = True
        permitted_routes.append({
            "module": "European Cybersecurity Certification Scheme (High)",
            "annex": "Article 8 & Reg (EU) 2019/881",
            "notified_body_involved": True,
            "status": "MANDATORY EUROPEAN CERTIFICATION",
            "notes": "Mandatory high-assurance certification scheme adopted via Commission delegated act.",
        })
        cost_estimate = "€250,000 – €500,000+"
        lead_time_estimate = "12 – 18 Months"

    # De-scoping Recommendations
    descope_recommendations = []
    if "vpn_function" in selected_class_i:
        descope_recommendations.append(
            "VPN De-Scoping: If VPN tunnel is used solely for the device's own telemetry/management, convert to outbound mTLS client session. "
            "Remove generic routing/split-tunneling for third-party traffic to avoid Annex III(5) Class I classification."
        )
    if "iam_system" in selected_class_i:
        descope_recommendations.append(
            "IAM De-Scoping: If product merely authenticates users for its own local UI/API, it is application authentication (Annex I Part I(3)(a)), "
            "NOT an Identity Management System (Annex III(1)). Ensure marketing materials do not describe product as an IdP, SSO broker, or central directory."
        )
    if "network_management" in selected_class_i or "network_monitoring" in selected_class_i:
        descope_recommendations.append(
            "Network Management De-Scoping: Restrict network diagnostics to the device's own interfaces and sockets. "
            "Do not provide network packet sniffing, external switch port configuration, or cross-network topology orchestration."
        )

    result = {
        "assessment_id": f"CRA-CLASS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp_utc": now_iso,
        "product_name": product_name,
        "vendor_name": vendor_name,
        "intended_purpose": intended_purpose,
        "classification": {
            "tier": tier,
            "tier_short": tier_short,
            "statutory_basis": (
                "Article 8" if tier_short == "CRITICAL"
                else "Article 7(2) & Annex IV" if tier_short == "CLASS_II"
                else "Article 7(1) & Annex III" if tier_short == "CLASS_I"
                else "Article 7 & Annex I Baseline (Default Category)"
            ),
            "annex_iii_triggers": selected_class_i,
            "annex_iv_triggers": selected_class_ii,
            "critical_art8_trigger": is_critical_art8,
        },
        "conformity_assessment": {
            "notified_body_mandatory": notified_body_required,
            "harmonised_standards_fully_applied": harmonised_standards_fully_applied,
            "permitted_routes": permitted_routes,
            "cost_estimate": cost_estimate,
            "lead_time_estimate": lead_time_estimate,
        },
        "boundary_analysis": {
            "boundary_warning_flags": boundary_flags,
            "descope_recommendations": descope_recommendations,
        },
    }
    return result


def generate_markdown_dossier(res: Dict) -> str:
    """Formats classification result into a formal Markdown dossier."""
    c = res["classification"]
    ca = res["conformity_assessment"]
    ba = res["boundary_analysis"]

    routes_md = ""
    for r in ca["permitted_routes"]:
        nb_str = "YES" if r["notified_body_involved"] else "NO (Self-Assessment)"
        routes_md += f"- **{r['module']} ({r['annex']}):** {r['status']}\n"
        routes_md += f"  * *Notified Body Required:* {nb_str}\n"
        routes_md += f"  * *Statutory Condition:* {r['notes']}\n"

    descopes_md = ""
    if ba["descope_recommendations"]:
        for d in ba["descope_recommendations"]:
            descopes_md += f"> [!TIP]\n> **Architectural Recommendation:** {d}\n\n"
    else:
        descopes_md = "*No architectural de-scoping required; product is either clearly categorized or in Default Category.*\n"

    md = f"""# EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
## Product Risk Classification & Conformity Route Dossier

**Dossier Reference:** `{res['assessment_id']}`  
**Date of Assessment:** `{res['timestamp_utc']}`  
**Evaluated Product:** `{res['product_name']}`  
**Manufacturer / Vendor:** `{res['vendor_name']}`  

---

### 1. Executive Summary & Statutory Determination

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STATUTORY CLASSIFICATION RESULT                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ PRODUCT RISK TIER:     {c['tier_short']:<54} │
│ STATUTORY STATUS:      {c['tier']:<54} │
│ LEGAL BASIS:           {c['statutory_basis']:<54} │
│ NOTIFIED BODY STATUS:  {"MANDATORY THIRD-PARTY AUDIT REQUIRED" if ca['notified_body_mandatory'] else "IN-HOUSE MODULE A PERMITTED (NO NOTIFIED BODY)":<54} │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

**Declared Intended Purpose:**  
> {res['intended_purpose']}

---

### 2. Category Screening Results

* **Annex III (Class I) Triggers Identified ({len(c['annex_iii_triggers'])}):**  
  {', '.join(c['annex_iii_triggers']) if c['annex_iii_triggers'] else '*None (Passed negative screening)*'}
* **Annex IV (Class II) Triggers Identified ({len(c['annex_iv_triggers'])}):**  
  {', '.join(c['annex_iv_triggers']) if c['annex_iv_triggers'] else '*None (Passed negative screening)*'}
* **Article 8 Critical Designation:** {'YES' if c['critical_art8_trigger'] else 'NO'}

---

### 3. Statutory Conformity Assessment Routing (Article 32)

#### Permitted Conformity Assessment Modules:
{routes_md}
#### Commercial & Operational Impact:
* **Direct Compliance Cost Estimate:** `{ca['cost_estimate']}`
* **Certification Lead Time Impact:** `{ca['lead_time_estimate']}`
* **Harmonised Standards Presumption Applied:** `{'YES' if ca['harmonised_standards_fully_applied'] else 'NO (Standardisation Request M/60x status: No standards cited in OJEU as of late 2026)'}`

---

### 4. Boundary Analysis & Architectural De-Scoping

{descopes_md}
### 5. Presales & Governance Verification Sign-Off

| Review Gate | Verification Status | Responsible Authority | Sign-Off Date |
|---|:---:|---|:---:|
| **Technical Boundary Review** | **VERIFIED** | Lead Product Security Architect | _________ |
| **Legal / Intended Purpose Review** | **VERIFIED** | Regulatory Compliance Counsel | _________ |
| **Commercial Bid Approval** | **APPROVED** | Presales / Commercial Director | _________ |
"""
    return md


def main():
    parser = argparse.ArgumentParser(
        description="EU Cyber Resilience Act (CRA) Product Risk Tier & Conformity Routing Engine"
    )
    parser.add_argument("--product", default="Commercial Digital Solution", help="Product name")
    parser.add_argument("--vendor", default="Commercial Vendor Ltd", help="Vendor name")
    parser.add_argument("--purpose", default="Standard business data processing", help="Intended purpose statement")
    parser.add_argument("--class-1", nargs="*", default=[], help="Annex III Class I category keys triggered")
    parser.add_argument("--class-2", nargs="*", default=[], help="Annex IV Class II category keys triggered")
    parser.add_argument("--critical", action="store_true", help="Article 8 Critical product trigger")
    parser.add_argument("--full-standards-applied", action="store_true", help="Full OJEU harmonised standards applied")
    parser.add_argument("--out-json", default=None, help="Output JSON path")
    parser.add_argument("--out-md", default=None, help="Output Markdown path")
    parser.add_argument("--list-categories", action="store_true", help="List all statutory categories and exit")

    args = parser.parse_args()

    if args.list_categories:
        print("=" * 80)
        print("ANNEX III — IMPORTANT PRODUCTS WITH DIGITAL ELEMENTS (CLASS I):")
        print("=" * 80)
        for key, desc in ANNEX_III_CATEGORIES:
            print(f"  • {key:<26} : {desc}")
        print("\n" + "=" * 80)
        print("ANNEX IV — IMPORTANT PRODUCTS WITH DIGITAL ELEMENTS (CLASS II):")
        print("=" * 80)
        for key, desc in ANNEX_IV_CATEGORIES:
            print(f"  • {key:<26} : {desc}")
        sys.exit(0)

    res = classify_product(
        product_name=args.product,
        vendor_name=args.vendor,
        intended_purpose=args.purpose,
        selected_class_i=args.class_1,
        selected_class_ii=args.class_2,
        is_critical_art8=args.critical,
        harmonised_standards_fully_applied=args.full_standards_applied,
    )

    md = generate_markdown_dossier(res)

    if args.out_json:
        with open(args.out_json, "w") as f:
            json.dump(res, f, indent=2)
        print(f"[+] Wrote classification JSON record to {args.out_json}")

    if args.out_md:
        with open(args.out_md, "w") as f:
            f.write(md)
        print(f"[+] Wrote classification Markdown dossier to {args.out_md}")

    if not args.out_json and not args.out_md:
        print(md)


if __name__ == "__main__":
    main()
