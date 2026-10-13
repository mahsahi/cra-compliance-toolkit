#!/usr/bin/env python3
"""
EU Cyber Resilience Act (CRA) — RFC 9116 security.txt Generator & Validator Tool
Regulatory Baseline: Regulation (EU) 2024/2847, Annex I Part II(3) & Part II(4); Annex II Point 2.

This tool generates and validates RFC 9116 compliant security.txt files configured
to satisfy CRA vulnerability intake, public contact point, and CSAF advisory mandates.
"""

import argparse
import datetime
import re
import sys
from typing import Dict, List, Tuple


def generate_security_txt(
    domain: str,
    contact_email: str,
    intake_url: str,
    policy_url: str,
    pgp_url: str,
    languages: str = "en, fr, de",
    csaf_url: str = None,
    expiry_days: int = 365,
) -> str:
    """Generates an RFC 9116 compliant security.txt string with CRA directives."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expiry = now + datetime.timedelta(days=expiry_days)
    expiry_str = expiry.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if not csaf_url:
        csaf_url = f"https://{domain}/.well-known/csaf/provider-metadata.json"

    lines = [
        "# RFC 9116 Coordinated Vulnerability Disclosure Specification",
        "# EU Cyber Resilience Act (Regulation (EU) 2024/2847) Compliance",
        f"# Generated: {now.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        f"Contact: mailto:{contact_email}",
    ]
    if intake_url:
        lines.append(f"Contact: {intake_url}")

    lines.extend([
        f"Expires: {expiry_str}",
        f"Encryption: {pgp_url}",
        f"Preferred-Languages: {languages}",
        f"Canonical: https://{domain}/.well-known/security.txt",
        f"Policy: {policy_url}",
        f"CSAF: {csaf_url}",
        f"Acknowledgments: https://{domain}/security/hall-of-fame",
        "",
    ])

    return "\n".join(lines)


def validate_security_txt(content: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validates a security.txt file against RFC 9116 rules and CRA Annex I Part II obligations.
    Returns (is_valid, errors, warnings).
    """
    errors = []
    warnings = []

    directives: Dict[str, List[str]] = {}
    for line_no, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"Line {line_no}: Malformed directive (missing colon): '{line}'")
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        directives.setdefault(key, []).append(val)

    # Check mandatory RFC 9116 directive: Contact
    if "Contact" not in directives or not directives["Contact"]:
        errors.append("RFC 9116 / CRA Annex I Part II(4) Violation: Mandatory 'Contact:' directive is missing.")
    else:
        for contact in directives["Contact"]:
            if not (contact.startswith("mailto:") or contact.startswith("https://") or contact.startswith("tel:")):
                errors.append(f"Contact URI must begin with 'mailto:', 'https://', or 'tel:': '{contact}'")

    # Check mandatory RFC 9116 directive: Expires
    if "Expires" not in directives or not directives["Expires"]:
        errors.append("RFC 9116 Violation: Mandatory 'Expires:' directive is missing.")
    else:
        expires_val = directives["Expires"][0]
        # Parse ISO 8601
        try:
            # Handles 2027-10-12T00:00:00.000Z or similar
            clean_date = expires_val.replace("Z", "+00:00")
            exp_dt = datetime.datetime.fromisoformat(clean_date)
            now = datetime.datetime.now(datetime.timezone.utc)
            if exp_dt < now:
                errors.append(f"RFC 9116 Violation: 'Expires:' date has already passed: {expires_val}")
            elif exp_dt > now + datetime.timedelta(days=366):
                warnings.append(f"RFC 9116 Warning: 'Expires:' duration exceeds recommended 1-year window ({expires_val}).")
        except Exception as e:
            errors.append(f"RFC 9116 Violation: Invalid 'Expires:' format (must be RFC 3339 / ISO 8601): {expires_val}")

    # Check CRA-recommended directives
    if "Policy" not in directives:
        warnings.append("CRA Annex I Part II(3) Recommendation: 'Policy:' directive linking to CVD policy is missing.")
    if "Encryption" not in directives:
        warnings.append("CRA Best Practice: 'Encryption:' directive linking to PGP/GPG key is missing.")
    if "CSAF" not in directives:
        warnings.append("CRA Annex I Part II(6) Recommendation: 'CSAF:' directive linking to CSAF provider metadata is missing.")
    if "Canonical" not in directives:
        warnings.append("RFC 9116 Recommendation: 'Canonical:' URL directive is missing.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="EU Cyber Resilience Act (CRA) RFC 9116 security.txt Generator & Validator"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate subcommand
    gen_p = subparsers.add_parser("generate", help="Generate a compliant security.txt file")
    gen_p.add_argument("--domain", required=True, help="Corporate or product domain (e.g., example.com)")
    gen_p.add_argument("--email", required=True, help="Security contact email (e.g., security@example.com)")
    gen_p.add_argument("--intake-url", default="", help="Web intake form URL")
    gen_p.add_argument("--policy-url", required=True, help="Public CVD policy URL")
    gen_p.add_argument("--pgp-url", required=True, help="Public PGP key URL")
    gen_p.add_argument("--languages", default="en, fr, de", help="Preferred languages (default: 'en, fr, de')")
    gen_p.add_argument("--csaf-url", default=None, help="CSAF provider metadata URL")
    gen_p.add_argument("--expiry-days", type=int, default=365, help="Days until expiry (default: 365)")
    gen_p.add_argument("--output", default=None, help="Output file path (default: stdout)")

    # Validate subcommand
    val_p = subparsers.add_parser("validate", help="Validate an existing security.txt file")
    val_p.add_argument("file", help="Path to security.txt file to validate")

    args = parser.parse_args()

    if args.command == "generate":
        txt = generate_security_txt(
            domain=args.domain,
            contact_email=args.email,
            intake_url=args.intake_url,
            policy_url=args.policy_url,
            pgp_url=args.pgp_url,
            languages=args.languages,
            csaf_url=args.csaf_url,
            expiry_days=args.expiry_days,
        )
        if args.output:
            with open(args.output, "w") as f:
                f.write(txt)
            print(f"[+] Successfully wrote CRA-compliant security.txt to {args.output}")
        else:
            print(txt)

    elif args.command == "validate":
        try:
            with open(args.file, "r") as f:
                content = f.read()
        except Exception as e:
            print(f"[-] Error opening file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        is_valid, errors, warnings = validate_security_txt(content)

        print("=" * 70)
        print(f"RFC 9116 & CRA ANNEX I PART II AUDIT REPORT: {args.file}")
        print("=" * 70)

        if errors:
            print(f"[-] ERRORS ({len(errors)}):")
            for err in errors:
                print(f"    • {err}")
        else:
            print("[+] PASS: All mandatory RFC 9116 directives satisfied.")

        if warnings:
            print(f"\n[!] WARNINGS & CRA RECOMMENDATIONS ({len(warnings)}):")
            for w in warnings:
                print(f"    • {w}")
        else:
            print("[+] No warnings. Full CRA and RFC 9116 recommendations met.")

        print("-" * 70)
        if is_valid:
            print("[✓] RESULT: VALID & CRA-COMPLIANT RFC 9116 security.txt")
            sys.exit(0)
        else:
            print("[✗] RESULT: NON-COMPLIANT (Corrections Required)")
            sys.exit(1)


if __name__ == "__main__":
    main()
