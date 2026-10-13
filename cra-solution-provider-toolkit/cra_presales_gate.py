#!/usr/bin/env python3
"""EU Cyber Resilience Act (Regulation (EU) 2024/2847) - Presales Solution Gating & Role Classification Engine.

Operationalizes Section 15.4 and Sections 3-4 of CRA_Solution_Provider_Lifecycle_Requirements.md:
- Determines CRA Scope & Sectoral Exclusions (Article 2)
- Evaluates Solution Provider Role Archetype (A: Proprietary Manufacturer, B: White-Labeler,
  C: Substantial Modifier, D: Integrator/Distributor, E: Professional Services Operator)
- Classifies Product Risk Tier (Default, Important Class I, Important Class II, Critical)
- Identifies Required Conformity Route (Module A, Module B+C, Module H, or EU Certification)
- Generates Presales Gating Decision (APPROVED, CONDITIONAL, REJECTED, OUT_OF_SCOPE)
- Emits Formal Markdown Bid Dossier and JSON metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --- Classification Catalogs (Annex III & IV) ---
IMPORTANT_CLASS_I_KEYWORDS = [
    "iam", "identity", "access_management", "credential", "password_manager",
    "vpn", "virtual_private_network", "antivirus", "malware",
    "network_management", "siem", "boot_manager", "router", "switch",
    "browser", "smart_home_hub", "smart_lock"
]

IMPORTANT_CLASS_II_KEYWORDS = [
    "operating_system", "os", "hypervisor", "virtualization", "firewall",
    "ips", "ids", "intrusion_prevention", "intrusion_detection",
    "tamper_resistant", "secure_element", "industrial_automation",
    "plc", "scada_controller"
]

CRITICAL_KEYWORDS = [
    "smart_meter_gateway", "biometric_authenticator_hardware",
    "hardware_security_box", "eidas_hardware"
]


class PresalesGatingEngine:
    def __init__(self, project_name: str, client_name: str = "", lead_architect: str = ""):
        self.project_name = project_name
        self.client_name = client_name
        self.lead_architect = lead_architect
        self.answers: Dict[str, Any] = {}
        self.evaluation: Dict[str, Any] = {}

    def run_interactive(self):
        """Run interactive CLI questionnaire."""
        print("\n" + "=" * 70)
        print(" EU CYBER RESILIENCE ACT (REGULATION (EU) 2024/2847)")
        print(" PRESALES SOLUTION GATING & ROLE CLASSIFICATION ENGINE")
        print("=" * 70)
        print(f"Project:        {self.project_name}")
        print(f"Client/Bid:     {self.client_name or 'N/A'}")
        print(f"Lead Architect: {self.lead_architect or os.environ.get('USER', 'Architect')}")
        print("-" * 70)

        # 1. Product Characteristics
        print("\n[SECTION 1: PRODUCT CHARACTERISTICS & DIGITAL ELEMENT TEST]")
        has_digital = self._prompt_bool("Does the deliverable include software, firmware, or an appliance?")
        has_network = False
        has_rdps = False
        if has_digital:
            has_network = self._prompt_bool("Does it have an active data connection (IP, Wi-Fi, BLE, API, USB logical)?")
            has_rdps = self._prompt_bool("Does it connect to an in-house developed cloud backend / companion API (RDPS)?")
        self.answers["has_digital"] = has_digital
        self.answers["has_network"] = has_network
        self.answers["has_rdps"] = has_rdps

        # 2. Sectoral Exclusions
        print("\n[SECTION 2: SECTORAL EXCLUSIONS (ARTICLE 2)]")
        is_military = self._prompt_bool("Is the product exclusively for military, national defence, or state security?")
        is_medical = self._prompt_bool("Is it certified as a Medical Device under Regulation (EU) 2017/745 (MDR) or IVDR?")
        is_automotive = self._prompt_bool("Is it a type-approved automotive system under Regulation (EU) 2019/2144?")
        is_aviation = self._prompt_bool("Is it certified civil aviation equipment under Regulation (EU) 2018/1139?")
        is_pure_saas = self._prompt_bool("Is it a pure cloud SaaS service with NO installed client software or device?")
        self.answers["is_military"] = is_military
        self.answers["is_medical"] = is_medical
        self.answers["is_automotive"] = is_automotive
        self.answers["is_aviation"] = is_aviation
        self.answers["is_pure_saas"] = is_pure_saas

        # 3. Commercial & Branding Model (Articles 13, 21, 22)
        print("\n[SECTION 3: COMMERCIAL & BRANDING MODEL]")
        own_brand = self._prompt_bool("Will the solution be sold, marketed, or packaged under our company's name or trademark?")
        white_label = self._prompt_bool("Are we white-labeling a third-party product under our brand/trademark (Article 21)?")
        distribute_unmodified = self._prompt_bool("Are we distributing a third-party product unmodified with original vendor CE mark?")
        pure_consulting = self._prompt_bool("Is this strictly professional services / configuration advice without product delivery?")
        self.answers["own_brand"] = own_brand
        self.answers["white_label"] = white_label
        self.answers["distribute_unmodified"] = distribute_unmodified
        self.answers["pure_consulting"] = pure_consulting

        # 4. Customization & Modification
        print("\n[SECTION 4: CODE MODIFICATION & ATTACK SURFACE]")
        modifies_code = self._prompt_bool("Are we modifying third-party code, kernels, OS binaries, or custom firmware logic?")
        exposes_surface = self._prompt_bool("Do our modifications expose new network ports, altered protocols, or new threat vectors?")
        changes_purpose = self._prompt_bool("Do our modifications alter the intended purpose assessed by the original vendor?")
        self.answers["modifies_code"] = modifies_code
        self.answers["exposes_surface"] = exposes_surface
        self.answers["changes_purpose"] = changes_purpose

        # 5. Product Functional Categories (Annex III & IV)
        print("\n[SECTION 5: FUNCTIONAL CLASSIFICATION]")
        print("Select all security-critical functions provided by the deliverable:")
        is_class_1 = self._prompt_bool("Does it perform IAM, VPN, SIEM, network management, router, switch, or browser functions?")
        is_class_2 = self._prompt_bool("Does it perform Operating System, hypervisor, firewall, or IDS/IPS functions?")
        is_critical = self._prompt_bool("Is it a smart meter gateway or tamper-resistant cryptographic hardware device?")
        self.answers["is_class_1"] = is_class_1
        self.answers["is_class_2"] = is_class_2
        self.answers["is_critical"] = is_critical

        # 6. Contractual Support Horizon
        print("\n[SECTION 6: LIFECYCLE & SUPPORT COMMITMENTS]")
        bid_years = self._prompt_int("How many years of security maintenance are committed to the client in the bid?", default=5)
        self.answers["bid_support_years"] = bid_years

        self.evaluate()

    def evaluate(self):
        """Perform legal and regulatory assessment based on questionnaire answers."""
        eval_res: Dict[str, Any] = {
            "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
            "in_scope": False,
            "exclusion_reason": None,
            "role_archetype": None,
            "archetype_description": "",
            "product_tier": "Default",
            "conformity_route": "Annex VIII Module A (Internal Production Control)",
            "statutory_support_floor_years": 5,
            "bid_support_years": self.answers.get("bid_support_years", 5),
            "support_compliance": True,
            "gating_decision": "PENDING",
            "risk_factors": [],
            "required_actions": [],
            "bid_cost_implications": []
        }

        # Check Scope
        if not (self.answers.get("has_digital") and (self.answers.get("has_network") or self.answers.get("has_rdps"))):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Deliverable lacks digital elements or logical/physical network connectivity (Article 2(1))."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return

        # Check Sectoral Exclusions
        if self.answers.get("is_military"):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Exclusively military / national defence purpose (Article 2(2))."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return
        if self.answers.get("is_medical"):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Regulated as Medical Device under Regulation (EU) 2017/745 or IVDR (Article 2(3))."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return
        if self.answers.get("is_automotive"):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Type-approved motor vehicle system under Regulation (EU) 2019/2144 (Article 2(4))."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return
        if self.answers.get("is_aviation"):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Civil aviation product certified under Regulation (EU) 2018/1139 (Article 2(5))."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return
        if self.answers.get("is_pure_saas"):
            eval_res["in_scope"] = False
            eval_res["exclusion_reason"] = "Pure cloud SaaS without client-installed digital element or companion RDPS (NIS2 Directive applies)."
            eval_res["gating_decision"] = "OUT_OF_SCOPE"
            self.evaluation = eval_res
            return

        # Deliverable is In Scope
        eval_res["in_scope"] = True

        # Determine Role Archetype
        if self.answers.get("white_label"):
            eval_res["role_archetype"] = "Archetype B (Manufacturer via White-Labeling)"
            eval_res["archetype_description"] = "Marketing 3rd-party PDE under company trademark triggers full Manufacturer status under Article 21."
            eval_res["risk_factors"].append("High Liability: Organization inherits 100% of statutory Manufacturer duties and 5-year patch liabilities.")
            eval_res["bid_cost_implications"].append("Must budget for independent Technical Dossier assembly and 5-year patch SLA insurance.")
        elif self.answers.get("modifies_code") and (self.answers.get("exposes_surface") or self.answers.get("changes_purpose")):
            eval_res["role_archetype"] = "Archetype C (Manufacturer via Substantial Modification)"
            eval_res["archetype_description"] = "Modifying code/configuration to expose new attack surface triggers Article 22 Substantial Modification."
            eval_res["risk_factors"].append("Statutory Reclassification: Organization becomes the legal Manufacturer for the modified solution.")
            eval_res["bid_cost_implications"].append("Conformity assessment required for modified scope prior to commissioning.")
        elif self.answers.get("own_brand"):
            eval_res["role_archetype"] = "Archetype A (Proprietary Manufacturer)"
            eval_res["archetype_description"] = "Organization designs, builds, and places product on market under own brand (Articles 13 & 14)."
            eval_res["bid_cost_implications"].append("Full SSDLC, SBOM, Annex VII documentation, and Article 14 24/7 on-call budgeting.")
        elif self.answers.get("distribute_unmodified"):
            eval_res["role_archetype"] = "Archetype D (Integrator / Distributor)"
            eval_res["archetype_description"] = "Reselling or integrating 3rd-party PDE under original vendor CE mark (Article 19 Distributor duties)."
            eval_res["risk_factors"].append("Distributor Duty: Must verify CE mark, EU DoC, and ensure customer receives user instructions.")
        elif self.answers.get("pure_consulting"):
            eval_res["role_archetype"] = "Archetype E (Professional Services / Managed Operator)"
            eval_res["archetype_description"] = "Advisory and operations only; no PDE placed on market. CRA affects operational handovers."
        else:
            eval_res["role_archetype"] = "Archetype D (Systems Integrator)"
            eval_res["archetype_description"] = "Multi-component integration. Role depends on final trademark and substantial modification screening."

        # Product Risk Tier & Conformity Route
        if self.answers.get("is_critical"):
            eval_res["product_tier"] = "Critical (Annex IV)"
            eval_res["conformity_route"] = "Mandatory European Cybersecurity Certificate (EUCC / CC EAL4+) (Article 32(4))"
            eval_res["risk_factors"].append("Extremely High Cost: External accredited certification mandatory.")
            eval_res["bid_cost_implications"].append("Certification costs typically exceed €80k-€150k with 6-12 month lead times.")
        elif self.answers.get("is_class_2"):
            eval_res["product_tier"] = "Important Class II (Annex III)"
            eval_res["conformity_route"] = "Mandatory Notified Body Assessment (Annex IX Module B+C or Annex X Module H) (Article 32(3))"
            eval_res["risk_factors"].append("Notified Body Mandate: Self-assessment is NOT legally permitted.")
            eval_res["bid_cost_implications"].append("Third-party Notified Body conformity audit fee (€30k-€70k) must be priced into bid.")
        elif self.answers.get("is_class_1"):
            eval_res["product_tier"] = "Important Class I (Annex III)"
            eval_res["conformity_route"] = "Annex VIII Module A (if EN harmonised standards applied in full) OR Notified Body Module B+C"
            eval_res["risk_factors"].append("Standards Dependency: If harmonised standards not fully applied, Notified Body engagement required.")
            eval_res["bid_cost_implications"].append("Budget for CEN/CENELEC/ETSI standard compliance audit.")
        else:
            eval_res["product_tier"] = "Default Tier (Standard Product)"
            eval_res["conformity_route"] = "Annex VIII Module A (Internal Production Control - Self-Assessment)"

        # Check Support Horizon
        if eval_res["bid_support_years"] < 5:
            eval_res["support_compliance"] = False
            eval_res["risk_factors"].append(
                f"Statutory Support Floor Violation: Bid promises {eval_res['bid_support_years']} years, but CRA Article 13(8) mandates at least 5 years unless shorter use is legally justified."
            )
            eval_res["required_actions"].append(
                "Adjust customer quotation to include 5-year security maintenance, or file an Article 13(8) formal justification in the technical dossier."
            )

        # Gating Decision Formulation
        is_manufacturer = "Manufacturer" in eval_res["role_archetype"]
        is_high_tier = eval_res["product_tier"] in ("Important Class II", "Critical")

        if is_manufacturer and is_high_tier:
            eval_res["gating_decision"] = "CONDITIONAL (HIGH REGULATORY OVERHEAD)"
            eval_res["required_actions"].extend([
                "CISO & Legal sign-off required prior to submitting bid proposal.",
                "Mandatory Notified Body audit fees must be included in financial model.",
                "Ensure upstream supplier contracts include 12-hour Article 14 notification SLA (Schedule B).",
                "Execute CRA Customer Compliance Addendum (Schedule A) with enterprise customer."
            ])
        elif is_manufacturer and not eval_res["support_compliance"]:
            eval_res["gating_decision"] = "CONDITIONAL (PRICING ADJUSTMENT REQUIRED)"
            eval_res["required_actions"].append("Align pricing model with 5-year statutory support period floor.")
        elif is_manufacturer:
            eval_res["gating_decision"] = "APPROVED (STANDARD MANUFACTURER SSDLC)"
            eval_res["required_actions"].extend([
                "Execute automated CycloneDX SBOM generation in CI/CD pipeline.",
                "Register product on ENISA Single Reporting Platform roster.",
                "Attach CRA Schedule A Addendum to Master Services Agreement."
            ])
        else:
            eval_res["gating_decision"] = "APPROVED (INTEGRATOR / DISTRIBUTOR SCOPE)"
            eval_res["required_actions"].extend([
                "Verify upstream vendor CE mark and EU Declaration of Conformity.",
                "Ensure contractual demarcation prevents accidental Article 22 reclassification."
            ])

        self.evaluation = eval_res

    def generate_markdown_report(self) -> str:
        """Render formal presales audit dossier in Markdown."""
        ev = self.evaluation
        ts = ev.get("evaluation_timestamp", datetime.now(timezone.utc).isoformat())

        md = f"""# CRA Presales Gating & Role Classification Dossier
**Project / Bid:** {self.project_name}  
**Client / Account:** {self.client_name or 'Commercial Proposal'}  
**Lead Solutions Architect:** {self.lead_architect or 'Solutions Architecture Team'}  
**Evaluation Timestamp:** `{ts}`  
**Regulatory Baseline:** Regulation (EU) 2024/2847 (Cyber Resilience Act)

---

## 1. Presales Gating Summary

| Evaluation Dimension | Assessment Finding | Regulatory Basis |
|---|---|---|
| **CRA Scope Determination** | **{'IN SCOPE' if ev.get('in_scope') else 'OUT OF SCOPE'}** | Article 2(1) Scope Test |
| **Identified Role Archetype** | **{ev.get('role_archetype', 'N/A')}** | Articles 13, 21, 22 |
| **Product Risk Tier** | **{ev.get('product_tier', 'N/A')}** | Annex III & IV Classification |
| **Mandatory Conformity Route** | `{ev.get('conformity_route', 'N/A')}` | Article 32 Conformity Routes |
| **Guaranteed Support Period** | **{ev.get('bid_support_years')} Years** (Statutory Floor: {ev.get('statutory_support_floor_years')} Years) | Article 13(8) & Annex II |
| **PRESALES GATING DECISION** | **{ev.get('gating_decision')}** | Enterprise Bid Policy |

---

## 2. Role Archetype & Scope Details
* **Description:** {ev.get('archetype_description', 'N/A')}
"""
        if not ev.get("in_scope"):
            md += f"\n> **EXCLUSION BASIS:** {ev.get('exclusion_reason')}\n"
            return md

        md += "\n### 3. Key Presales Risk Factors\n"
        if ev.get("risk_factors"):
            for rf in ev["risk_factors"]:
                md += f"- ⚠️ **{rf}**\n"
        else:
            md += "- ✅ No abnormal regulatory risk flags identified for this solution profile.\n"

        md += "\n### 4. Mandatory Presales Action Checklist\n"
        for act in ev.get("required_actions", []):
            md += f"- [ ] {act}\n"

        md += "\n### 5. Bid Costing & Financial Adjustments\n"
        if ev.get("bid_cost_implications"):
            for ci in ev["bid_cost_implications"]:
                md += f"- 💰 **Financial Impact:** {ci}\n"
        else:
            md += "- 💰 Standard internal SSDLC overhead; no external Notified Body audit fees required.\n"

        md += f"""
---

## 6. Presales Sign-Off & Approvals
- **Lead Solutions Architect:** ___________________________  Date: __________
- **CISO / Product Security:** ___________________________  Date: __________
- **Legal & Contracts Lead:** ___________________________   Date: __________
"""
        return md

    def _prompt_bool(self, question: str) -> bool:
        while True:
            resp = input(f"  {question} [y/n]: ").strip().lower()
            if resp in ("y", "yes"):
                return True
            if resp in ("n", "no"):
                return False
            print("    Please answer 'y' or 'n'.")

    def _prompt_int(self, question: str, default: int = 5) -> int:
        while True:
            resp = input(f"  {question} [default: {default}]: ").strip()
            if not resp:
                return default
            try:
                val = int(resp)
                if val > 0:
                    return val
            except ValueError:
                pass
            print("    Please enter a positive integer.")


def main():
    parser = argparse.ArgumentParser(
        description="EU CRA Presales Gating & Solution Role Qualification Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project", default="Enterprise Edge Gateway Solution", help="Project / Solution Name")
    parser.add_argument("--client", default="EU Enterprise Customer", help="Client / Bid Name")
    parser.add_argument("--architect", default="Lead Architect", help="Lead Architect Name")
    parser.add_argument("--batch", action="store_true", help="Run non-interactively using CLI flags")
    parser.add_argument("--has-digital", action="store_true", help="Deliverable includes digital elements")
    parser.add_argument("--has-network", action="store_true", help="Deliverable has network connectivity")
    parser.add_argument("--has-rdps", action="store_true", help="Deliverable connects to companion cloud RDPS")
    parser.add_argument("--own-brand", action="store_true", help="Marketed under company trademark")
    parser.add_argument("--white-label", action="store_true", help="White-labeling 3rd-party product")
    parser.add_argument("--modifies-code", action="store_true", help="Modifies 3rd party code/firmware")
    parser.add_argument("--exposes-surface", action="store_true", help="Exposes new network surface/protocols")
    parser.add_argument("--class-1", action="store_true", help="Important Class I functions (IAM, VPN, etc.)")
    parser.add_argument("--class-2", action="store_true", help="Important Class II functions (OS, Firewall, etc.)")
    parser.add_argument("--critical", action="store_true", help="Critical product functions (Annex IV)")
    parser.add_argument("--support-years", type=int, default=5, help="Years of support promised in bid")
    parser.add_argument("--out-md", help="Path to write Markdown dossier")
    parser.add_argument("--out-json", help="Path to write JSON evaluation")

    args = parser.parse_args()

    engine = PresalesGatingEngine(project_name=args.project, client_name=args.client, lead_architect=args.architect)

    if args.batch:
        engine.answers = {
            "has_digital": args.has_digital or True,
            "has_network": args.has_network or True,
            "has_rdps": args.has_rdps,
            "is_military": False,
            "is_medical": False,
            "is_automotive": False,
            "is_aviation": False,
            "is_pure_saas": False,
            "own_brand": args.own_brand,
            "white_label": args.white_label,
            "distribute_unmodified": not (args.own_brand or args.white_label or args.modifies_code),
            "pure_consulting": False,
            "modifies_code": args.modifies_code,
            "exposes_surface": args.exposes_surface,
            "changes_purpose": False,
            "is_class_1": args.class_1,
            "is_class_2": args.class_2,
            "is_critical": args.critical,
            "bid_support_years": args.support_years,
        }
        engine.evaluate()
    else:
        engine.run_interactive()

    # Output results
    md_content = engine.generate_markdown_report()
    json_content = json.dumps(engine.evaluation, indent=2)

    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[+] Markdown Bid Dossier saved: {args.out_md}")
    else:
        print("\n" + md_content)

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            f.write(json_content)
        print(f"[+] JSON Evaluation saved: {args.out_json}")


if __name__ == "__main__":
    main()
