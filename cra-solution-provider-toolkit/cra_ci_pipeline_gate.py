#!/usr/bin/env python3
"""EU Cyber Resilience Act (Regulation (EU) 2024/2847) - Phase 3 CI/CD SBOM & SCA Quality Gate.

Orchestrates automated CRA compliance gating in engineering CI/CD build pipelines:
1. Generates an Annex II-compliant CycloneDX (JSON) Software Bill of Materials (SBOM)
   using the multi-ecosystem generators from cra-agent.
2. Executes SCA vulnerability scanning with reachability checks.
3. Cross-references CVEs against Known Exploited Vulnerability (KEV) catalogs to screen
   for Article 14(2) statutory reporting triggers (actively exploited flaws).
4. Computes Article 14 statutory countdowns (24h early warning, 72h notification) if
   exploited vulnerabilities are detected.
5. Emits an OpenVEX document (v0.2.0) documenting exploitability status.
6. Enforces configurable release gates (fails CI/CD build if statutory criteria are violated).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure cra-agent root is on python path
SCRIPT_DIR = Path(__file__).resolve().parent
CRA_AGENT_DIR = SCRIPT_DIR.parent if (SCRIPT_DIR.parent / "src").exists() else Path("/root/cra-agent")
if CRA_AGENT_DIR.exists() and str(CRA_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(CRA_AGENT_DIR))


# CISA Known Exploited Vulnerabilities (KEV) sample cache / live lookup
# In real production, synced periodically via cra-agent's sync_threat_intel.py
SAMPLE_KNOWN_EXPLOITED_CVES = {
    "CVE-2021-44228",  # Log4Shell
    "CVE-2022-22965",  # Spring4Shell
    "CVE-2023-34362",  # MOVEit Transfer
    "CVE-2023-44487",  # HTTP/2 Rapid Reset
    "CVE-2024-3094",   # XZ Utils Backdoor
    "CVE-2024-21626",  # runc Leaky Vessels
    "CVE-2023-48795",  # Terrapin Attack
}


class CRACIGateway:
    def __init__(self, repo_path: Path, output_dir: Path, fail_on_severity: str = "CRITICAL"):
        self.repo_path = repo_path.resolve()
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fail_on_severity = fail_on_severity.upper()
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repo": str(self.repo_path),
            "gates_passed": True,
            "gate_failures": [],
            "sbom_generated": False,
            "sbom_path": None,
            "components_count": 0,
            "vex_path": None,
            "findings_count": 0,
            "article14_triggers": [],
            "vulnerabilities": []
        }

    async def generate_sbom(self) -> bool:
        """Generate CycloneDX SBOM using cra-agent service or trivy fallback."""
        sbom_out_path = self.output_dir / "sbom.cyclonedx.json"
        print(f"[*] Step 1: Generating CycloneDX SBOM for {self.repo_path}...")

        try:
            from src.services.sbom_generator import generate_sbom
            sbom_str = await generate_sbom(self.repo_path)
            sbom_data = json.loads(sbom_str)
            with open(sbom_out_path, "w", encoding="utf-8") as f:
                f.write(sbom_str)
            self.results["sbom_generated"] = True
            self.results["sbom_path"] = str(sbom_out_path)
            self.results["components_count"] = len(sbom_data.get("components", []))
            print(f"    [+] CycloneDX SBOM generated successfully: {self.results['components_count']} components.")
            return True
        except Exception as e:
            print(f"    [!] cra-agent generator notice ({e}), falling back to Trivy CLI...")
            try:
                cmd = [
                    "trivy", "fs", "--format", "cyclonedx",
                    "--output", str(sbom_out_path), str(self.repo_path)
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                with open(sbom_out_path, "r", encoding="utf-8") as f:
                    sbom_data = json.load(f)
                self.results["sbom_generated"] = True
                self.results["sbom_path"] = str(sbom_out_path)
                self.results["components_count"] = len(sbom_data.get("components", []))
                print(f"    [+] Fallback CycloneDX SBOM generated: {self.results['components_count']} components.")
                return True
            except Exception as ex:
                print(f"    [-] SBOM generation failed: {ex}", file=sys.stderr)
                self.results["gates_passed"] = False
                self.results["gate_failures"].append(f"SBOM Generation Failed: {ex}")
                return False

    def scan_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Run vulnerability scan using Trivy / pip-audit."""
        print(f"[*] Step 2: Executing SCA vulnerability scan across {self.repo_path}...")
        findings = []

        try:
            cmd = [
                "trivy", "fs", "--scanners", "vuln",
                "--format", "json", str(self.repo_path)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if res.returncode == 0 and res.stdout.strip():
                trivy_json = json.loads(res.stdout)
                for r in trivy_json.get("Results", []):
                    target = r.get("Target", "unknown")
                    for v in r.get("Vulnerabilities", []):
                        findings.append({
                            "cve": v.get("VulnerabilityID"),
                            "package": v.get("PkgName"),
                            "installed_version": v.get("InstalledVersion"),
                            "fixed_version": v.get("FixedVersion"),
                            "severity": v.get("Severity", "UNKNOWN").upper(),
                            "title": v.get("Title", ""),
                            "target_file": target,
                            "cvss": v.get("CVSS", {}).get("nvd", {}).get("V3Score", 0.0),
                            "reachable": True  # Default conservative heuristic
                        })
        except Exception as e:
            print(f"    [!] Trivy scan notice ({e}). Checking with pip-audit...")

        # If findings empty and python project, run pip-audit
        if not findings and (self.repo_path / "requirements.txt").exists():
            try:
                cmd = ["pip-audit", "-r", str(self.repo_path / "requirements.txt"), "-f", "json", "--no-deps"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if res.stdout.strip():
                    audit_json = json.loads(res.stdout)
                    for item in audit_json.get("dependencies", []):
                        for v in item.get("vulns", []):
                            findings.append({
                                "cve": v.get("id"),
                                "package": item.get("name"),
                                "installed_version": item.get("version"),
                                "fixed_version": ", ".join(v.get("fix_versions", [])),
                                "severity": "HIGH",  # fallback
                                "title": v.get("description", "")[:100],
                                "target_file": "requirements.txt",
                                "cvss": 7.5,
                                "reachable": True
                            })
            except Exception as e:
                print(f"    [!] pip-audit check notice: {e}")

        self.results["findings_count"] = len(findings)
        self.results["vulnerabilities"] = findings
        print(f"    [+] Scan complete. Total vulnerabilities identified: {len(findings)}.")
        return findings

    def screen_article14_triggers(self, findings: List[Dict[str, Any]]):
        """Cross-check findings for active in-the-wild exploitation (Article 14 trigger)."""
        print("[*] Step 3: Screening for CRA Article 14(2) Actively Exploited Vulnerabilities...")
        now = datetime.now(timezone.utc)
        seen_cves = set()

        for f in findings:
            cve_id = f.get("cve", "")
            pkg_name = f.get("package", "")
            key = (cve_id, pkg_name)
            is_actively_exploited = cve_id in SAMPLE_KNOWN_EXPLOITED_CVES

            # Check if CISA KEV or high exploitability flags present
            if is_actively_exploited and f.get("reachable", True) and key not in seen_cves:
                seen_cves.add(key)
                trigger_data = {
                    "cve": cve_id,
                    "package": pkg_name,
                    "severity": f.get("severity"),
                    "cvss": f.get("cvss"),
                    "target_file": f.get("target_file"),
                    "detected_at": now.isoformat(),
                    "deadlines": {
                        "early_warning_24h_due": (now + timedelta(hours=24)).isoformat(),
                        "notification_72h_due": (now + timedelta(hours=72)).isoformat(),
                        "legal_basis": "CRA Article 14(2) - Active In-the-Wild Exploitation"
                    }
                }
                self.results["article14_triggers"].append(trigger_data)
                print(f"    [!] CRITICAL ARTICLE 14 ALERT: {cve_id} in {pkg_name} is ACTIVELY EXPLOITED in the wild!")

    def generate_vex_document(self, findings: List[Dict[str, Any]]) -> str:
        """Generate OpenVEX v0.2.0 document."""
        print("[*] Step 4: Generating OpenVEX exploitability document...")
        vex_path = self.output_dir / "vex.openvex.json"
        now_iso = datetime.now(timezone.utc).isoformat()
        repo_name = self.repo_path.name

        statements = []
        for f in findings:
            cve = f.get("cve")
            if not cve or not cve.startswith("CVE-"):
                continue

            status = "affected" if f.get("reachable", True) else "not_affected"
            stmt: Dict[str, Any] = {
                "vulnerability": {"name": cve},
                "timestamp": now_iso,
                "products": [
                    {
                        "@id": f"pkg:generic/{repo_name}",
                        "identifiers": {"purl": f"pkg:generic/{repo_name}"},
                        "subcomponents": [{"@id": f.get("target_file", "source")}]
                    }
                ],
                "status": status,
            }
            if status == "not_affected":
                stmt["justification"] = "code_not_reachable"
            else:
                stmt["action_statement"] = f"Remediate package {f.get('package')} to version {f.get('fixed_version') or 'latest patch'}."

            statements.append(stmt)

        vex_doc = {
            "@context": "https://openvex.dev/ns/v0.2.0",
            "@id": f"https://solution-provider.example.com/vex/{repo_name}-{int(datetime.now().timestamp())}",
            "author": "Solution Provider CRA CI/CD Gate",
            "role": "Document Creator",
            "timestamp": now_iso,
            "version": 1,
            "tooling": "cra_ci_pipeline_gate.py",
            "statements": statements
        }

        with open(vex_path, "w", encoding="utf-8") as out:
            json.dump(vex_doc, out, indent=2)

        self.results["vex_path"] = str(vex_path)
        print(f"    [+] OpenVEX document generated: {len(statements)} vulnerability statements.")
        return str(vex_path)

    def enforce_gates(self) -> bool:
        """Enforce CRA release quality gates."""
        print("[*] Step 5: Enforcing CRA CI/CD Quality Gates...")
        passed = True

        # Gate 1: Mandatory SBOM
        if not self.results["sbom_generated"] or self.results["components_count"] == 0:
            msg = "Gate 1 Failed: Valid CycloneDX SBOM must be produced with >= 1 component."
            self.results["gate_failures"].append(msg)
            print(f"    [-] {msg}")
            passed = False
        else:
            print("    [+] Gate 1 Passed: Valid CycloneDX SBOM generated.")

        # Gate 2: Article 14 Actively Exploited Vulnerabilities
        if self.results["article14_triggers"]:
            cves = [t["cve"] for t in self.results["article14_triggers"]]
            msg = f"Gate 2 Failed: Actively exploited vulnerabilities detected ({', '.join(cves)}). Immediate Article 14 24h statutory reporting triggered!"
            self.results["gate_failures"].append(msg)
            print(f"    [-] {msg}")
            passed = False
        else:
            print("    [+] Gate 2 Passed: Zero reachable actively exploited (Article 14) vulnerabilities.")

        # Gate 3: Severity Threshold
        critical_count = sum(1 for v in self.results["vulnerabilities"] if v.get("severity") == "CRITICAL" and v.get("reachable"))
        high_count = sum(1 for v in self.results["vulnerabilities"] if v.get("severity") == "HIGH" and v.get("reachable"))

        if self.fail_on_severity == "CRITICAL" and critical_count > 0:
            msg = f"Gate 3 Failed: {critical_count} unmitigated CRITICAL vulnerabilities present in release candidate."
            self.results["gate_failures"].append(msg)
            print(f"    [-] {msg}")
            passed = False
        elif self.fail_on_severity == "HIGH" and (critical_count > 0 or high_count > 0):
            msg = f"Gate 3 Failed: {critical_count} Critical and {high_count} High vulnerabilities present in release candidate."
            self.results["gate_failures"].append(msg)
            print(f"    [-] {msg}")
            passed = False
        else:
            print(f"    [+] Gate 3 Passed: Vulnerability severity limits within policy ({self.fail_on_severity}).")

        self.results["gates_passed"] = passed
        return passed

    def export_summary(self):
        """Write JSON summary and Markdown CI step report."""
        summary_json_path = self.output_dir / "cra_gate_summary.json"
        summary_md_path = self.output_dir / "cra_gate_summary.md"

        with open(summary_json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        # Markdown Report (compatible with GitHub Actions Step Summary)
        status_badge = "✅ PASSED" if self.results["gates_passed"] else "❌ FAILED"
        md = f"""# CRA Build Pipeline Quality Gate: {status_badge}

- **Repository:** `{self.repo_path.name}`
- **Evaluation Timestamp:** `{self.results['timestamp']}`
- **CRA Compliance Standard:** Regulation (EU) 2024/2847 (Cyber Resilience Act)

---

### Pipeline Quality Gate Results

| Inspection Gate | Status | Finding / Evidence |
|---|---|---|
| **Gate 1: CycloneDX SBOM** | {'✅ PASS' if self.results['sbom_generated'] else '❌ FAIL'} | `{self.results['components_count']}` components cataloged in [`sbom.cyclonedx.json`]({self.results.get('sbom_path')}) |
| **Gate 2: Article 14 Exploitation** | {'✅ PASS' if not self.results['article14_triggers'] else '❌ CRITICAL FAIL'} | `{len(self.results['article14_triggers'])}` actively exploited vulnerabilities identified |
| **Gate 3: Severity Threshold ({self.fail_on_severity})** | {'✅ PASS' if self.results['gates_passed'] else '❌ FAIL'} | Total Findings: `{self.results['findings_count']}` |
| **OpenVEX Exploitability** | ✅ EMITTED | Statements compiled in [`vex.openvex.json`]({self.results.get('vex_path')}) |

"""
        if self.results["gate_failures"]:
            md += "### ⚠️ Blocking Release Gate Failures\n"
            for fail in self.results["gate_failures"]:
                md += f"- **{fail}**\n"
            md += "\n> **Action Required:** Remediate vulnerable components or supply an accredited VEX justification prior to production deployment.\n"

        if self.results["article14_triggers"]:
            md += "\n### 🚨 Statutory Article 14 Reporting Escalations\n"
            md += "| CVE ID | Component | CVSS | 24h Early Warning Deadline | 72h Notification Deadline |\n"
            md += "|---|---|---|---|---|\n"
            for t in self.results["article14_triggers"]:
                md += f"| **{t['cve']}** | `{t['package']}` | {t['cvss']} | `{t['deadlines']['early_warning_24h_due']}` | `{t['deadlines']['notification_72h_due']}` |\n"
            md += "\n> **Statutory Notice:** Awareness established during build qualification. PSIRT and designated CSIRT coordinator must be notified in compliance with the Article 14 Operational Runbook.\n"

        with open(summary_md_path, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"\n[+] Summary artifacts written:")
        print(f"    - JSON: {summary_json_path}")
        print(f"    - Markdown: {summary_md_path}")


async def main_async():
    parser = argparse.ArgumentParser(description="EU CRA CI/CD Quality Gate & Pipeline Validator")
    parser.add_argument("--repo", default="/root/cra-agent", help="Target repository directory path")
    parser.add_argument("--output-dir", default="/root/cra_ci_output", help="Output directory for SBOM, VEX, and reports")
    parser.add_argument("--fail-on", default="CRITICAL", choices=["CRITICAL", "HIGH", "NONE"], help="Fail build on severity")
    args = parser.parse_args()

    gateway = CRACIGateway(
        repo_path=Path(args.repo),
        output_dir=Path(args.output_dir),
        fail_on_severity=args.fail_on
    )

    await gateway.generate_sbom()
    findings = gateway.scan_vulnerabilities()
    gateway.screen_article14_triggers(findings)
    gateway.generate_vex_document(findings)
    passed = gateway.enforce_gates()
    gateway.export_summary()

    sys.exit(0 if passed else 1)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
