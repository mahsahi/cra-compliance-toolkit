# EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
# Tabletop Incident Simulation Drill Runbook: "Operation DarkFrame"

**Drill Identifier:** `DRILL-2026-CRA-ALPHA`  
**Classification:** Tabletop Exercise Runbook & Incident Response Drill Record  
**Regulatory Baseline:** Regulation (EU) 2024/2847, Articles 13, 14, 16; Annex I Part II (Points 2, 3, 5, 6, 7); Delegated Regulation (EU) 2026/881  
**Exercise Scenario:** In-the-wild active exploitation of an unauthenticated remote zero-day heap buffer overflow (`CVE-2026-49120`) in `SecureEdge Gateway 5000 (SEG-5000)` firmware v3.4.0  
**Enforcement Status:** Article 14 is **Live Statutory Law** (in effect across all EU Member States since 11 September 2026)

---

## 1. Exercise Architecture & Governance

### 1.1 Objective & Scope
The purpose of this exercise is to rigorously test, evaluate, and certify our organization's operational readiness to execute the mandatory multi-track obligations under the **EU Cyber Resilience Act (CRA)** within statutorily binding timelines:
1. **Article 14(2)(a) 24-Hour Early Warning:** Formulation, legal justification for delayed dissemination under Delegated Regulation (EU) 2026/881, and submission to the **ENISA Single Reporting Platform (SRP)**.
2. **Article 14(7) CSIRT Jurisdiction:** Statutory determination of the lead CSIRT coordinator (Main Establishment rule).
3. **Annex I Part II(3) Coordinated Vulnerability Disclosure (CVD):** Dual-track coordination with an external ethical security researcher reporting a companion proof-of-concept under RFC 9116 and Legal Safe Harbor.
4. **Article 14(8) Proportional Customer Security Advisory:** Distribution of machine-readable CSAF 2.0 / OpenVEX workarounds without disclosing exploit weaponization details.
5. **Article 14(2)(b) 72-Hour Detailed Notification:** Transmission of technical analysis, CVSS vectors, and sensitivity markings (TLP:AMBER+STRICT) to ENISA SRP.
6. **Annex I Part II(2) & (5) Emergency Hotfix Engineering & Distribution:** Pre-release verification, Ed25519 signing, and free OTA distribution of firmware v3.4.1.
7. **Article 13(6) Upstream Notification:** Sharing patch code with upstream open-source maintainers.
8. **Article 14(2)(c) 14-Day Final Report:** Concluding post-mortem and mitigation dossier submission to ENISA SRP.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CHRONOLOGICAL DRILL TIMELINE CLOCK                              │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│  T+00:00     │   T+02:00    │   T+18:00    │   T+30:00    │   T+60:00    │   T+120:00  │
│ Telemetry    │ Awareness    │ Early Warning│ CVD Intake & │ Detailed Not.│ Hotfix Out  │
│ Alert        │ Signed       │ to ENISA SRP │ Workaround   │ to ENISA SRP │ & Final Rep │
│ (Inject 1)   │ (Inject 2)   │ (Inject 3)   │ (Inject 4)   │ (Inject 5)   │ (Inject 6)  │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴─────────────┘
```

---

### 1.2 Exercise Roles & Incident Command Structure

| Drill Role | Primary Responsibility | Incumbent / Assigned Lead |
|---|---|---|
| **Incident Commander (IC)** | Directs technical containment; approves public and customer communications; coordinates executive briefing. | Chief Information Security Officer (CISO) |
| **PSIRT Technical Lead** | Oversees vulnerability reproduction, root-cause debugging, hotfix development, and regression verification. | Product Security Engineering Lead |
| **Regulatory & Legal Lead** | Verifies statutory deadlines; assesses delayed dissemination criteria; signs formal ENISA SRP submissions. | General Counsel / Chief Compliance Officer |
| **Product Architecture Lead** | Determines affected firmware releases, hardware variants, and cloud RDPS dependencies; assesses reachability. | Principal Solutions Architect |
| **Communications Lead** | Drafts customer advisories (CSAF 2.0 / OpenVEX), coordinates customer portal distribution, and manages PR. | VP Product Marketing & Customer Support |
| **Exercise Facilitator / White Cell** | Delivers chronological injects, evaluates adherence to statutory SLAs, and logs performance. | Independent Compliance Auditor |

---

## 2. Chronological Scenario Injects & Tactical Workflows

---

### INJECT 1 — Detection & Anomaly Ingress
**Drill Time:** `Day 1, 08:00:00 CET (T+00:00)`  
**Source:** Threat Intelligence Feed (CERT-EU) & Tier-1 Automotive Customer SOC (Munich, Germany)

```
[INCOMING THREAT INTELLIGENCE INJECT]
FROM: CERT-EU Early Warning Network & Enterprise Customer SOC
SUBJECT: URGENT: Anomalous Reverse Shell Traffic from SEG-5000 Edge Gateways
DETAILS: 
A Tier-1 enterprise customer in Germany detected anomalous outbound TCP connections 
from multiple SEG-5000 gateways on corporate subnets connecting to unknown external IPs 
in Eastern Europe. 

Packet captures show unauthenticated HTTP POST requests to port 8443 (/api/v1/network/frame) 
containing an oversized JSON payload that crashes the 'netframed' daemon, followed immediately 
by an interactive shell invocation. 
CERT-EU reports that similar artifacts were observed targeting edge hardware in France and Ireland.
```

#### Incident Team Tactical Action:
1. **08:15 CET:** PSIRT on-call engineer escalates to CISO and Product Security Engineering Lead.
2. **08:30 CET:** Emergency War Room convened; triage investigation initiated.
3. **09:15 CET:** Product Engineering confirms that `netframed` in firmware v3.4.0 contains an unchecked `memcpy()` buffer allocation in the multipart payload parser.
4. **09:45 CET:** Reverse engineering of customer PCAP confirms arbitrary memory overwrite leading to remote code execution (RCE) without authentication.

---

### INJECT 2 — The Legal Awareness Gate
**Drill Time:** `Day 1, 10:00:00 CET (T+02:00)`  
**Statutory Trigger:** Establishing Legal Awareness under Article 14(2)

> [!IMPORTANT]
> **The Awareness Legal Standard (Article 14(2)):**  
> Under Article 14(2), the statutory clock does NOT start when an unconfirmed alert is first received (08:00 CET). It starts strictly at the moment the manufacturer **establishes awareness** that:
> 1. A vulnerability exists in its product with digital elements, AND
> 2. The vulnerability is being **actively exploited in the wild**.
>
> At **10:00 CET**, technical verification confirmed both criteria. The Legal Awareness Determination Record must be formally executed immediately.

#### Operational Deliverable: Awareness Determination Record (`AWARE-2026-0042`)
* **Awareness Timestamp:** `2026-10-12T10:00:00+02:00`
* **Vulnerability Title:** Remote Heap Buffer Overflow in SEG-5000 NetFrame Parser
* **Assigned CVE:** `CVE-2026-49120` (CNA Reservation)
* **CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` (**Base Score: 10.0 Critical**)
* **Exploitation Status:** **ACTIVELY EXPLOITED IN THE WILD (Confirmed)**
* **Lead CSIRT Determination (Article 14(7)):**  
  * Manufacturer's main establishment where strategic cybersecurity decisions are taken is in **Dublin, Ireland**.  
  * **Designated Lead CSIRT:** **CSIRT-IE (National CSIRT of Ireland)**.
* **Statutory Countdown Clocks Initiated:**
  * **Article 14(2)(a) 24-Hour Early Warning Due:** `2026-10-13T10:00:00+02:00`
  * **Article 14(2)(b) 72-Hour Detailed Notification Due:** `2026-10-15T10:00:00+02:00`
  * **Article 14(2)(c) Final Report Due:** $\le 14\text{ Days}$ after corrective patch release.

---

### INJECT 3 — Article 14(2)(a) Early Warning & Delayed Dissemination
**Drill Time:** `Day 1, 22:00:00 CET (T+12:00)` (12 Hours Ahead of Statutory 24h Deadline)  
**Channel:** ENISA Single Reporting Platform (SRP) (`portal.cra-srp.enisa.europa.eu`)

The Regulatory Lead and CISO formulate the Early Warning dossier:

#### Statutory Requirements Checked (Article 14(2)(a)):
1. Identification of the product with digital elements (`SecureEdge Gateway 5000`, firmware v3.4.0).
2. General nature of the actively exploited vulnerability (Remote Heap Buffer Overflow in administrative API).
3. Member States where the product is known to be placed or made available (Germany, France, Ireland, Netherlands).
4. **Invocation of Delayed Dissemination (Delegated Regulation (EU) 2026/881):**  
   * The manufacturer formally requests the recipient CSIRTs and ENISA to **temporarily withhold wider dissemination** of vulnerability details.  
   * *Statutory Ground:* Immediate public disclosure prior to patch availability would expose thousands of operational edge gateways across European industrial infrastructure to automated exploitation before mitigations can be applied.

#### Simulated ENISA SRP Early Warning Payload (`enisa_srp_early_warning_simulated.json`)
```json
{
  "report_type": "article_14_2_a_early_warning",
  "statutory_basis": "Regulation (EU) 2024/2847, Article 14(2)(a)",
  "submission_timestamp": "2026-10-12T20:00:00Z",
  "awareness_timestamp": "2026-10-12T08:00:00Z",
  "manufacturer": {
    "name": "SecureEdge Technologies Ltd",
    "country_of_establishment": "IE",
    "lead_csirt": "CSIRT-IE",
    "contact_email": "psirt-lead@secureedge.com",
    "contact_phone": "+353-1-496-0120"
  },
  "product": {
    "commercial_name": "SecureEdge Gateway 5000",
    "model_number": "SEG-5000",
    "affected_versions": ["3.4.0", "3.3.2", "3.3.1"],
    "cpe": "cpe:2.3:o:secureedge:seg-5000_firmware:*:*:*:*:*:*:*:*"
  },
  "vulnerability_event": {
    "cve_id": "CVE-2026-49120",
    "general_nature": "Unauthenticated Remote Heap Buffer Overflow in network framing daemon (netframed)",
    "active_exploitation_confirmed": true,
    "known_exploited_member_states": ["DE", "FR", "IE", "NL"]
  },
  "delayed_dissemination_request": {
    "requested": true,
    "legal_basis": "Delegated Regulation (EU) 2026/881, Article 2",
    "justification": "Mitigation and firmware patch are actively under engineering. Public disclosure prior to patch release will induce severe systemic security risks across critical industrial customer networks."
  }
}
```

---

### INJECT 4 — Parallel CVD Researcher Intake & Article 14(8) Workaround Advisory
**Drill Time:** `Day 2, 14:00:00 CET (T+28:00)`  
**Channel:** Encrypted Intake Inbox (`security@secureedge.com` via RFC 9116 `security.txt`)

```
[RESEARCHER INTAKE INJECT]
FROM: researcher@redteam-security.org (PGP Encrypted)
TO: security@secureedge.com
SUBJECT: Zero-Day RCE in SEG-5000 netframed (PoC attached)
DETAILS:
Hello PSIRT team,
I have discovered a critical heap overflow in your netframed binary on port 8443. 
Attached is my advisory draft and a Python exploit script achieving reliable root shell. 
I am planning full public disclosure in 14 days. Please confirm receipt under your CVD policy.
```

#### Dual-Track Tactical Coordination:
1. **Researcher Safe Harbor & Embargo Alignment:**
   * Within **2 hours** (at 16:00 CET), PSIRT responds to researcher confirming receipt under the **Ethical Researcher Legal Safe Harbor**.
   * PSIRT informs researcher that the vulnerability is actively exploited in the wild and subject to European statutory coordination under CRA Article 14.
   * Negotiate an aligned disclosure embargo tied to hotfix release (T+96 hours).
2. **Article 14(8) Proportional Customer Security Advisory:**
   * Under **Article 14(8)**, the manufacturer must inform users of the PDE about the incident/vulnerability **without undue delay** and provide corrective workarounds.
   * *Crucial Compliance Principle:* The advisory must inform customers of the risk and provide defensive workarounds **WITHOUT exposing the vulnerability mechanism or PoC payload**.
   * *Technical Workaround Issued via Authenticated Portal:*
     ```bash
     # Emergency Workaround Script for SEG-5000 Customers:
     # Restrict port 8443 administrative access to trusted management subnets only
     iptables -I INPUT -p tcp --dport 8443 ! -s 10.0.0.0/8 -j DROP
     ```

---

### INJECT 5 — Article 14(2)(b) 72-Hour Detailed Notification Submission
**Drill Time:** `Day 3, 16:00:00 CET (T+54:00)` (18 Hours Ahead of Statutory 72h Deadline)  
**Channel:** ENISA Single Reporting Platform (SRP)

The PSIRT completes root-cause forensics and submits the Detailed Notification:

#### Detailed Notification Elements Transmitted:
* **Root-Cause Analysis:** CWE-122 (Heap-based Buffer Overflow) in `parse_frame_header()` due to integer truncation on frame length field.
* **Exploit Vector Analysis:** Attackers send fragmented packets with invalid length offsets, triggering heap corruption and overwriting function pointers.
* **Sensitivity Grading:** **TLP:AMBER+STRICT** (Restricted strictly to authorized CSIRTs and incident handling personnel).
* **Mitigation Status:** Engineering hotfix v3.4.1 compiled; undergoing automated regression testing in CI/CD pipeline.

---

### INJECT 6 — Hotfix Release, Pre-Release Testing, Secure OTA & 14-Day Final Report
**Drill Time:** `Day 5, 12:00:00 CET (T+98:00)`  
**Channel:** Secure OTA Pipeline & ENISA SRP

#### 1. Pre-Release Security Verification Gate (Annex I Part II(8))
* Unit test suite executed with AddressSanitizer (`ASan`) and `Valgrind`: Zero memory leaks, buffer boundaries strictly validated.
* Re-test against researcher PoC and customer PCAP: All exploit payloads cleanly rejected with HTTP 400 Bad Request.
* Full automated regression pass: Zero regressions in core telemetry functionality.

#### 2. Cryptographic Firmware Sealing (Annex I Part II(5))
```bash
# 1. Sign firmware image using offline hardware Ed25519 root key
sign-firmware-release --key /opt/pki/ed25519-release-root.key \
  --image seg-5000-v3.4.1.bin \
  --out-sig seg-5000-v3.4.1.bin.sig

# 2. Re-generate CycloneDX SBOM and OpenVEX document
python3 cra_csaf_advisory_tool.py create-vex \
  --id "VEX-2026-0042" \
  --cve "CVE-2026-49120" \
  --purl "pkg:generic/secureedge/seg-5000@3.4.1" \
  --status "fixed" \
  --out openvex.json
```

#### 3. Free Patch Distribution (Annex I Part II(2))
* Firmware v3.4.1 deployed to global OTA delivery cluster.
* All registered SEG-5000 units receive automated update notification with free-of-charge download entitlement.

#### 4. Mandatory Upstream Sharing (Article 13(6))
* The framing parser utilized a modified fork of the open-source library `libframenet`.
* Pursuant to **Article 13(6)**, the PSIRT submits a sanitized git patch and pull request to the upstream project maintainer on GitHub under coordinated disclosure.

#### 5. Article 14(2)(c) Final Report Submission to ENISA SRP
* Submitted at **T+120 hours** (substantially ahead of the statutory 14-day limit following mitigation availability).
* Summarizes final root-cause analysis, total affected units worldwide (14,200 devices), customer patch uptake statistics, and threat actor attribution indicators.

---

## 3. Evaluation Rubric & Compliance Audit Scoring

The drill performance is scored against four statutory CRA evaluation dimensions:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TABLETOP DRILL EVALUATION SCORECARD                             │
├───────────────────────────────┬────────────┬─────────────┬─────────────────────────────┤
│ Evaluation Dimension          │ Max Points │ Score Award │ Performance Finding         │
├───────────────────────────────┼────────────┼─────────────┼─────────────────────────────┤
│ 1. Statutory Deadline Control │     30     │     30      │ Early Warning (T+12h vs 24h)│
│                               │            │             │ Detailed Not. (T+54h vs 72h)│
│                               │            │             │ Final Report (T+5d vs 14d)  │
├───────────────────────────────┼────────────┼─────────────┼─────────────────────────────┤
│ 2. Legal Grounding & Justif.  │     25     │     25      │ Awareness accurately logged │
│                               │            │             │ Reg 2026/881 grounds cited  │
│                               │            │             │ CSIRT-IE jurisdiction sound │
├───────────────────────────────┼────────────┼─────────────┼─────────────────────────────┤
│ 3. CVD & Customer Handling    │     25     │     25      │ RFC 9116 intake responded 2h│
│                               │            │             │ Art 14(8) workaround issued │
│                               │            │             │ CSAF 2.0 / OpenVEX emitted  │
├───────────────────────────────┼────────────┼─────────────┼─────────────────────────────┤
│ 4. Technical Patch Integrity  │     20     │     20      │ Pre-release ASan testing OK │
│                               │            │             │ Ed25519 signing verified    │
│                               │            │             │ Free OTA delivery validated │
│                               │            │             │ Art 13(6) upstream patch sent│
├───────────────────────────────┼────────────┼─────────────┼─────────────────────────────┤
│ TOTAL AUDIT SCORE             │    100     │    100      │ RATING: EXCELLENT / PASS    │
└───────────────────────────────┴────────────┴─────────────┴─────────────────────────────┘
```

---

## 4. Post-Exercise Action Items & Continuous Improvement

1. **SIEM Webhook Integration:** Automate early warning draft generation directly from SIEM active-exploit detection rules to shave 2 hours off triage.
2. **CSIRT-IE Secure Portal Token Rotation:** Ensure secondary PAR and SAR tokens for ENISA SRP authentication are audited every 90 days.
3. **Tabletop Drill Frequency:** Mandate semi-annual simulation drills pursuant to internal ISMS policies and Article 13 compliance governance.
