# EU Cyber Resilience Act (CRA) — Regulation (EU) 2024/2847
## Product Risk Classification & Conformity Route Dossier

**Dossier Reference:** `CRA-CLASS-20261012164008`  
**Date of Assessment:** `2026-10-12T14:40:08Z`  
**Evaluated Product:** `SmartEdge Telemetry Hub 400`  
**Manufacturer / Vendor:** `Industrial Logic BV`  

---

### 1. Executive Summary & Statutory Determination

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STATUTORY CLASSIFICATION RESULT                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ PRODUCT RISK TIER:     CLASS_I                                                │
│ STATUTORY STATUS:      Important Product with Digital Elements — Class I (Annex III) │
│ LEGAL BASIS:           Article 7(1) & Annex III                               │
│ NOTIFIED BODY STATUS:  MANDATORY THIRD-PARTY AUDIT REQUIRED                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

**Declared Intended Purpose:**  
> Industrial telemetry ingestion, local sensor protocol conversion, and cloud MQTT egress

---

### 2. Category Screening Results

* **Annex III (Class I) Triggers Identified (1):**  
  vpn_function
* **Annex IV (Class II) Triggers Identified (0):**  
  *None (Passed negative screening)*
* **Article 8 Critical Designation:** NO

---

### 3. Statutory Conformity Assessment Routing (Article 32)

#### Permitted Conformity Assessment Modules:
- **Module A (BLOCKED) (Annex VIII):** DISQUALIFIED
  * *Notified Body Required:* NO (Self-Assessment)
  * *Statutory Condition:* Module A cannot be used because harmonised standards are absent, partial, or unverified.
- **Module B + Module C (EU-Type Examination + Conformity to Type) (Annex IX & X):** STANDARD NOTIFIED BODY ROUTE
  * *Notified Body Required:* YES
  * *Statutory Condition:* Notified Body examines technical dossier and issues EU-Type Examination Certificate.
- **Module H (Full Quality Assurance) (Annex XI):** ORGANISATIONAL CERTIFICATION ROUTE
  * *Notified Body Required:* YES
  * *Statutory Condition:* Notified Body audits and approves manufacturer quality management system and secure SDLC.

#### Commercial & Operational Impact:
* **Direct Compliance Cost Estimate:** `€50,000 – €150,000 (Notified Body fees + audit prep)`
* **Certification Lead Time Impact:** `6 – 9 Months (Notified Body queue & laboratory testing)`
* **Harmonised Standards Presumption Applied:** `NO (Standardisation Request M/60x status: No standards cited in OJEU as of late 2026)`

---

### 4. Boundary Analysis & Architectural De-Scoping

> [!TIP]
> **Architectural Recommendation:** VPN De-Scoping: If VPN tunnel is used solely for the device's own telemetry/management, convert to outbound mTLS client session. Remove generic routing/split-tunneling for third-party traffic to avoid Annex III(5) Class I classification.


### 5. Presales & Governance Verification Sign-Off

| Review Gate | Verification Status | Responsible Authority | Sign-Off Date |
|---|:---:|---|:---:|
| **Technical Boundary Review** | **VERIFIED** | Lead Product Security Architect | _________ |
| **Legal / Intended Purpose Review** | **VERIFIED** | Regulatory Compliance Counsel | _________ |
| **Commercial Bid Approval** | **APPROVED** | Presales / Commercial Director | _________ |
