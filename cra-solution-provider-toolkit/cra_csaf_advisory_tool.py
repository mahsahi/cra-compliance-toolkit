#!/usr/bin/env python3
"""
EU Cyber Resilience Act (CRA) — CSAF 2.0 & OpenVEX Advisory Generator and Validator Tool
Regulatory Baseline: Regulation (EU) 2024/2847, Annex I Part II, Points (2), (6), and (7).

This tool creates and validates machine-readable security advisories conforming to:
1. OASIS Common Security Advisory Framework (CSAF) v2.0
2. OpenVEX v0.2.0 (Vulnerability Exploitability eXchange)
"""

import argparse
import datetime
import json
import os
import sys
from typing import Dict, List, Tuple


def generate_csaf_advisory(
    advisory_id: str,
    title: str,
    cve: str,
    cvss_score: float,
    cvss_vector: str,
    cwe_id: str,
    cwe_name: str,
    vendor_name: str,
    product_name: str,
    cpe: str,
    affected_version: str,
    fixed_version: str,
    summary: str,
    fix_url: str,
) -> Dict:
    """Generates an OASIS CSAF 2.0 JSON structure fulfilling CRA Annex I Part II(6) mandates."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    severity = "INFO"
    if cvss_score >= 9.0:
        severity = "CRITICAL"
    elif cvss_score >= 7.0:
        severity = "HIGH"
    elif cvss_score >= 4.0:
        severity = "MEDIUM"
    elif cvss_score > 0.0:
        severity = "LOW"

    product_id = f"CSAFPID-{product_name.replace(' ', '-').upper()}-{fixed_version}"

    csaf_doc = {
        "document": {
            "category": "csaf_security_advisory",
            "csaf_version": "2.0",
            "title": title,
            "tracking": {
                "id": advisory_id,
                "current_release_date": now_iso,
                "initial_release_date": now_iso,
                "status": "final",
                "version": "1.0.0",
                "generator": {
                    "engine": {
                        "name": "CRA CSAF Advisory Tool",
                        "version": "1.0.0",
                    }
                },
            },
            "publisher": {
                "category": "vendor",
                "name": vendor_name,
                "namespace": f"https://www.{vendor_name.lower().replace(' ', '')}.com",
                "contact_details": f"security@{vendor_name.lower().replace(' ', '')}.com",
            },
            "notes": [
                {
                    "category": "summary",
                    "title": "Advisory Summary",
                    "text": summary,
                },
                {
                    "category": "legal_disclaimer",
                    "title": "CRA Regulatory Notice",
                    "text": (
                        "This security advisory is issued pursuant to Regulation (EU) 2024/2847 "
                        "(Cyber Resilience Act), Annex I, Part II, Point 6."
                    ),
                },
            ],
            "references": [
                {
                    "category": "self",
                    "summary": "Canonical Security Advisory URL",
                    "url": f"https://www.{vendor_name.lower().replace(' ', '')}.com/security/advisories/{advisory_id}",
                }
            ],
        },
        "product_tree": {
            "branches": [
                {
                    "category": "vendor",
                    "name": vendor_name,
                    "branches": [
                        {
                            "category": "product_name",
                            "name": product_name,
                            "product": {
                                "name": f"{product_name} {affected_version}",
                                "product_id": product_id,
                                "product_identification_helper": {
                                    "cpe": cpe,
                                },
                            },
                        }
                    ],
                }
            ]
        },
        "vulnerabilities": [
            {
                "cve": cve,
                "title": title,
                "cwe": {
                    "id": cwe_id,
                    "name": cwe_name,
                },
                "scores": [
                    {
                        "cvss_v3": {
                            "version": "3.1",
                            "vectorString": cvss_vector,
                            "baseScore": cvss_score,
                            "baseSeverity": severity,
                        }
                    }
                ],
                "product_status": {
                    "known_affected": [
                        product_id,
                    ]
                },
                "remediations": [
                    {
                        "category": "vendor_fix",
                        "details": (
                            f"Upgrade {product_name} to version {fixed_version} or later. "
                            "Pursuant to CRA Annex I Part II(2), this security update is provided free of charge."
                        ),
                        "url": fix_url,
                    }
                ],
            }
        ],
    }
    return csaf_doc


def generate_openvex_statement(
    advisory_id: str,
    cve: str,
    product_purl: str,
    status: str,
    justification: str = "",
    impact_statement: str = "",
) -> Dict:
    """Generates an OpenVEX v0.2.0 document."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    stmt = {
        "vulnerability": {
            "name": cve,
        },
        "products": [
            {
                "@id": product_purl,
            }
        ],
        "status": status,
    }
    if status == "not_affected":
        if justification:
            stmt["justification"] = justification
        if impact_statement:
            stmt["impact_statement"] = impact_statement

    vex_doc = {
        "@context": "https://openvex.dev/ns/v0.2.0",
        "@id": f"https://openvex.io/doc/2026/{advisory_id}",
        "author": "PSIRT Regulatory Office",
        "role": "Product Security Incident Response Team",
        "timestamp": now_iso,
        "version": 1,
        "statements": [stmt],
    }
    return vex_doc


def validate_csaf_advisory(data: Dict) -> Tuple[bool, List[str], List[str]]:
    """Validates a CSAF 2.0 JSON against CRA Annex I Part II requirements."""
    errors = []
    warnings = []

    doc = data.get("document", {})
    if not doc:
        errors.append("CSAF Root Error: Missing top-level 'document' object.")
        return False, errors, warnings

    if doc.get("csaf_version") != "2.0":
        errors.append(f"CSAF Version Error: Expected '2.0', found '{doc.get('csaf_version')}'")

    if doc.get("category") != "csaf_security_advisory":
        warnings.append(f"CSAF Category: Found '{doc.get('category')}', expected 'csaf_security_advisory'")

    # Tracking
    tracking = doc.get("tracking", {})
    if not tracking.get("id"):
        errors.append("CSAF Tracking Error: Missing 'id' in tracking object.")
    if tracking.get("status") not in ["final", "interim"]:
        warnings.append(f"CSAF Status: '{tracking.get('status')}' is not 'final' or 'interim'")

    # Publisher
    publisher = doc.get("publisher", {})
    if not publisher.get("name") or not publisher.get("namespace"):
        errors.append("CSAF Publisher Error: Missing 'name' or 'namespace' in publisher object.")

    # Vulnerabilities
    vulns = data.get("vulnerabilities", [])
    if not vulns:
        errors.append("CRA Annex I Part II(6) Violation: Document contains no 'vulnerabilities' array.")
    else:
        for idx, v in enumerate(vulns):
            cve = v.get("cve")
            if not cve:
                warnings.append(f"Vulnerability #{idx+1}: Missing CVE identifier.")
            scores = v.get("scores", [])
            if not scores:
                warnings.append(f"Vulnerability #{idx+1}: Missing CVSS score object.")
            rems = v.get("remediations", [])
            if not rems:
                errors.append(f"Vulnerability #{idx+1} CRA Violation: Missing remediation guidance (Annex I Part II(2)).")
            else:
                has_fix = any(r.get("category") == "vendor_fix" for r in rems)
                if not has_fix:
                    warnings.append(f"Vulnerability #{idx+1}: No remediation categorized as 'vendor_fix'.")

    return len(errors) == 0, errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="EU Cyber Resilience Act (CRA) CSAF 2.0 & OpenVEX Advisory Generator and Validator"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate CSAF
    gen_csaf = subparsers.add_parser("create-csaf", help="Create a CRA-compliant CSAF 2.0 JSON advisory")
    gen_csaf.add_argument("--id", required=True, help="Advisory ID (e.g., ADVISORY-2026-001)")
    gen_csaf.add_argument("--title", required=True, help="Advisory title")
    gen_csaf.add_argument("--cve", required=True, help="CVE identifier (e.g., CVE-2026-12345)")
    gen_csaf.add_argument("--cvss", type=float, required=True, help="CVSS base score (e.g., 8.8)")
    gen_csaf.add_argument("--cvss-vector", required=True, help="CVSS vector string")
    gen_csaf.add_argument("--cwe-id", default="CWE-119", help="CWE ID (default: CWE-119)")
    gen_csaf.add_argument("--cwe-name", default="Improper Restriction of Operations within the Bounds of a Memory Buffer", help="CWE name")
    gen_csaf.add_argument("--vendor", required=True, help="Vendor name")
    gen_csaf.add_argument("--product", required=True, help="Product name")
    gen_csaf.add_argument("--cpe", default="cpe:2.3:a:vendor:product:*:*:*:*:*:*:*:*", help="Product CPE")
    gen_csaf.add_argument("--affected-version", default="< 2.0.0", help="Affected version range")
    gen_csaf.add_argument("--fixed-version", required=True, help="Fixed version string")
    gen_csaf.add_argument("--summary", required=True, help="Summary description of vulnerability")
    gen_csaf.add_argument("--fix-url", required=True, help="URL to download security update free of charge")
    gen_csaf.add_argument("--out", default=None, help="Output JSON path")

    # Generate OpenVEX
    gen_vex = subparsers.add_parser("create-vex", help="Create an OpenVEX v0.2.0 document")
    gen_vex.add_argument("--id", required=True, help="Advisory or VEX ID")
    gen_vex.add_argument("--cve", required=True, help="CVE identifier")
    gen_vex.add_argument("--purl", required=True, help="Product package URL (purl)")
    gen_vex.add_argument("--status", choices=["fixed", "not_affected", "affected", "under_investigation"], required=True, help="Vulnerability status")
    gen_vex.add_argument("--justification", default="", help="Justification if not_affected")
    gen_vex.add_argument("--impact", default="", help="Impact statement if not_affected")
    gen_vex.add_argument("--out", default=None, help="Output JSON path")

    # Validate CSAF
    val_csaf = subparsers.add_parser("validate-csaf", help="Validate a CSAF 2.0 JSON file")
    val_csaf.add_argument("file", help="Path to CSAF JSON file")

    args = parser.parse_args()

    if args.command == "create-csaf":
        doc = generate_csaf_advisory(
            advisory_id=args.id,
            title=args.title,
            cve=args.cve,
            cvss_score=args.cvss,
            cvss_vector=args.cvss_vector,
            cwe_id=args.cwe_id,
            cwe_name=args.cwe_name,
            vendor_name=args.vendor,
            product_name=args.product,
            cpe=args.cpe,
            affected_version=args.affected_version,
            fixed_version=args.fixed_version,
            summary=args.summary,
            fix_url=args.fix_url,
        )
        json_str = json.dumps(doc, indent=2)
        if args.out:
            with open(args.out, "w") as f:
                f.write(json_str)
            print(f"[+] Wrote CSAF 2.0 JSON advisory to {args.out}")
        else:
            print(json_str)

    elif args.command == "create-vex":
        doc = generate_openvex_statement(
            advisory_id=args.id,
            cve=args.cve,
            product_purl=args.purl,
            status=args.status,
            justification=args.justification,
            impact_statement=args.impact,
        )
        json_str = json.dumps(doc, indent=2)
        if args.out:
            with open(args.out, "w") as f:
                f.write(json_str)
            print(f"[+] Wrote OpenVEX v0.2.0 document to {args.out}")
        else:
            print(json_str)

    elif args.command == "validate-csaf":
        with open(args.file, "r") as f:
            data = json.load(f)
        is_valid, errors, warnings = validate_csaf_advisory(data)
        print("=" * 70)
        print(f"CSAF 2.0 & CRA ANNEX I PART II AUDIT: {args.file}")
        print("=" * 70)
        if errors:
            print(f"[-] ERRORS ({len(errors)}):")
            for e in errors:
                print(f"    • {e}")
        else:
            print("[+] PASS: All mandatory CSAF 2.0 and CRA elements present.")

        if warnings:
            print(f"\n[!] WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"    • {w}")
        print("-" * 70)
        if is_valid:
            print("[✓] RESULT: VALID CSAF 2.0 ADVISORY")
            sys.exit(0)
        else:
            print("[✗] RESULT: INVALID CSAF ADVISORY")
            sys.exit(1)


if __name__ == "__main__":
    main()
