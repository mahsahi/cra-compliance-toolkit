# EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
## Post-Exercise Assessment Report (PEAR): Operation DarkFrame

**Exercise Identifier:** `DRILL-2026-CRA-ALPHA`  
**Date Executed:** `2026-10-12T14:44:35Z`  
**Target Product Evaluated:** `SecureEdge Gateway 5000 (SEG-5000)` (Firmware `v3.4.0`)  
**Vulnerability Tested:** `CVE-2026-49120` (CVSS `10.0` Critical)  
**Lead CSIRT Jurisdiction:** `CSIRT-IE (Ireland)`  

---

### 1. Executive Summary & Audit Certification

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        POST-EXERCISE AUDIT DETERMINATION                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ AUDIT OUTCOME:         PASS                                                   │
│ OVERALL SCORE:         60/60 (100.0%)                                         │
│ STATUTORY STATUS:      CERTIFIED AUDIT READY — 100% STATUTORY COMPLIANCE      │
│ STATUTORY BASELINE:    Regulation (EU) 2024/2847, Articles 13, 14, 16; Annex I Part II │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Chronological Tactical Performance Matrix

| Simulation Inject | Decision | Audit Status | Legal & Technical Rationale |
|---|:---:|:---:|---|
| Inject 1: Threat Intelligence Alert & Telemetry Ingress | `B` | **PASS** | Correct statutory application: Legal awareness requires confirmation of both a product vulnerability AND active exploitation in the wild (Article 14(2)). |
| Inject 2: Lead CSIRT Statutory Jurisdiction Determination | `B` | **PASS** | Correct: Article 14(7) establishes jurisdiction based on the manufacturer's Main Establishment. CSIRT-IE coordinates with affected CSIRTs (BSI, ANSSI) via ENISA SRP. |
| Inject 3: Article 14(2)(a) 24-Hour Early Warning & Delayed Dissemination | `B` | **PASS** | Correct: Delegated Regulation (EU) 2026/881 empowers manufacturers to request delayed dissemination to protect systemic cybersecurity during patch engineering. |
| Inject 4: CVD Intake Coordination & Ethical Researcher Safe Harbor | `B` | **PASS** | Correct: ISO/IEC 29147 standard practice; preserves legal safe harbor, coordinates disclosure date, and protects customers. |
| Inject 5: Article 14(8) Proportional Customer Security Advisory | `B` | **PASS** | Correct: Article 14(8) mandates proportional user notification providing actionable mitigations without assisting malicious attackers. |
| Inject 6: Hotfix Engineering, Upstream Sharing (Art 13(6)) & Final Report | `B` | **PASS** | Correct: Fully satisfies Annex I Part II(2) free updates, Article 13(6) upstream sharing, Annex I Part II(6) CSAF advisories, and Article 14(2)(c) Final Report. |

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
