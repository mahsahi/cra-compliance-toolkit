# EU Cyber Resilience Act (CRA) — Solution Provider Operational Toolkit

This directory contains the complete, audit-ready compliance framework, operational runbooks, legal contract templates, technical gating tools, and comprehensive compliance matrices developed to align Solution Providers with **Regulation (EU) 2024/2847 (Cyber Resilience Act - CRA)**.

---

## 📂 Toolkit Structure & Deliverables Matrix

| File / Component | Type | Legal Citation | Purpose & Scope |
|---|---|---|---|
| [`CRA_Group_Master_Procedure_SEC_PRO_CRA_001.md`](./CRA_Group_Master_Procedure_SEC_PRO_CRA_001.md) | Group Master Procedure | Reg (EU) 2024/2847 Full Scope; Art. 13, 14, 22, 53 | **Enterprise CRA Incident & Governance Standard (`SEC-PRO-CRA-001`):** Master standard governing multi-BU coordination, single-SRP legal entity accounts, formal RACI, configuration change invalidation, substantial modification rules, and MSA defense. |
| [`CRA_Reporting_Procedure.md`](./CRA_Reporting_Procedure.md) | Business Unit SOP | Article 14 Live Law (11 Sept 2026) | **MYBU Simplified CRA Reporting Procedure:** Pragmatic field-level SOP for rapid intake, 5-question triage, 20-hour internal safety target, and emergency customer notifications. Subordinate to `SEC-PRO-CRA-001`. |
| [`CRA_Non_Exploitability_Determination_Record_Template.md`](./CRA_Non_Exploitability_Determination_Record_Template.md) | Evidentiary Record Template | Art. 14(2), Annex I Part II; `SEC-PRO-CRA-001` §4 | **Signed Technical Non-Exploitability Determination Record (NEDR):** Legally defensible template and schema (`cra_non_exploitability_record_schema.json`) documenting Q4 "not exploitable" decisions with call graph proof and configuration locks. |
| [`CRA_Delivered_Systems_and_Object_Register_Template.md`](./CRA_Delivered_Systems_and_Object_Register_Template.md) | Inventory Register | Art. 13(1), 13(5), 13(8), 14 | **Delivered Systems & CRA Object Register Template:** Master inventory schema and sample (`cra_delivered_systems_sample.json`) tracking delivered products, firmware baselines, customer deployments, member states, and CycloneDX SBOM links. |
| [`CRA_10Year_Incident_Audit_Register_Template.md`](./CRA_10Year_Incident_Audit_Register_Template.md) | Statutory Retention Ledger | Art. 13(10), 14, 53 | **10-Year Statutory Incident & Triage Audit Register:** 25-column master ledger template tracking every security event from T0 arrival to final report, WORM archival, and 10-year retention tags. |
| [`CRA_Tabletop_Simulation_Drill_Runbook.md`](./CRA_Tabletop_Simulation_Drill_Runbook.md) | Tabletop Simulation Runbook | Art. 13, 14, 16; Annex I Part II; Del. Reg 2026/881 | **Tabletop Incident Simulation Drill ("Operation DarkFrame"):** Master scenario and tactical inject runbook testing 24h Early Warning, delayed dissemination grounds, Lead CSIRT determination (CSIRT-IE), CVD intake, Art. 14(8) workaround advisories, and 14-day Final Reports. |
| [`cra_drill_simulator.py`](./cra_drill_simulator.py) | CLI Simulation Engine | Art. 14(2), 14(4), 14(8); Annex I Part II | **Interactive Tabletop Drill Simulator:** CLI engine walking incident teams through chronological injects, testing tactical decision gates, scoring compliance (0-100%), and generating Post-Exercise Assessment Reports (PEAR). |
| [`cra_tabletop_drill_execution_record.json`](./cra_tabletop_drill_execution_record.json) | Audit Record | Schema & Art. 13, 53 | **Certified Tabletop Drill Execution Record:** Schema-validated simulation log (`DRILL-2026-CRA-ALPHA`) modeling zero-day RCE response with 100% on-time milestone achievements. |
| [`CRA_Tabletop_Drill_PEAR_Report.md`](./CRA_Tabletop_Drill_PEAR_Report.md) | Post-Exercise Audit Report | Article 13 & ISMS Governance | **Post-Exercise Assessment Report (PEAR):** Executive audit certification document evaluating tactical performance, legal awareness precision, and upstream patch sharing. |
| [`enisa_srp_early_warning_simulated.json`](./enisa_srp_early_warning_simulated.json) | SRP Payload Sample | Art. 14(2)(a), Del. Reg 2026/881 | Simulated 24-Hour Early Warning transmission payload with delayed dissemination request. |
| [`enisa_srp_detailed_notification_simulated.json`](./enisa_srp_detailed_notification_simulated.json) | SRP Payload Sample | Art. 14(2)(b) | Simulated 72-Hour Detailed Notification payload with root cause, CWE-122, and TLP:AMBER+STRICT grading. |
| [`enisa_srp_final_report_simulated.json`](./enisa_srp_final_report_simulated.json) | SRP Payload Sample | Art. 14(2)(c), Art. 13(6) | Simulated 14-Day Final Report payload documenting corrective OTA patch release and upstream code sharing. |
| [`CRA_Class_I_Class_II_Boundary_Assessment_Guide.md`](./CRA_Class_I_Class_II_Boundary_Assessment_Guide.md) | Boundary Assessment Guide | Art. 7, 8, 24, 32; Annex III, IV, VIII–XI | **Class I & Class II Boundary Assessment Guide:** Definitive analysis of Annex III (18 Class I categories) and Annex IV (9 Class II categories), 7 high-risk boundary battlegrounds, conformity routing engine (Modules A, B+C, H), the 2026/2027 Harmonised Standards Cliff, and architectural de-scoping strategies. |
| [`cra_classification_engine.py`](./cra_classification_engine.py) | CLI Automation Engine | Art. 7, 8, 32; Annex III, IV | **Product Risk Tier & Conformity Routing Engine:** CLI tool evaluating product architectures against all 27 Annex III/IV categories, computing risk tiers, calculating Notified Body mandates, estimating cost/time impacts, and emitting audit dossiers. |
| [`CRA_Classification_Dossier_Sample.md`](./CRA_Classification_Dossier_Sample.md) | Audit Record | Section 15.4 Framework | Example boundary classification dossier (`SmartEdge Telemetry Hub 400`) demonstrating VPN de-scoping to preserve Default Category Module A status. |
| [`CRA_Annex_VII_Technical_Documentation_and_EU_DoC_Blueprint.md`](./CRA_Annex_VII_Technical_Documentation_and_EU_DoC_Blueprint.md) | Technical Dossier Blueprint | Art. 13(10), 28, 29, 31; Annex II, V, VII, VIII | **Annex VII Technical Documentation File (TDF) & EU DoC:** Turnkey 10-section technical documentation assembly blueprint, bilingual Annex V EU Declaration of Conformity template, CE marking drawing specifications, Module A change control SOP, and 10-year WORM archival rules. |
| [`CRA_Coordinated_Vulnerability_Disclosure_and_Advisory_Policy.md`](./CRA_Coordinated_Vulnerability_Disclosure_and_Advisory_Policy.md) | Enterprise Security Policy | Annex I Part II (Points 1–8); Art. 13, 14 | **CVD, CSIRT & Security Advisory Policy:** ISO/IEC 29147 & 30111 compliant Coordinated Vulnerability Disclosure policy, ethical hacker Legal Safe Harbor, RFC 9116 `security.txt` standard, CSAF 2.0 / OpenVEX advisory pipelines, 48h/90d SLAs, and Art. 14 dual-track triggers. |
| [`cra_security_txt_tool.py`](./cra_security_txt_tool.py) | CLI Automation Tool | RFC 9116, Annex I Part II(4) | **RFC 9116 `security.txt` Generator & Validator:** CLI tool to generate and audit compliant `/.well-known/security.txt` files with CRA contact points, PGP keys, policy links, and CSAF endpoints. |
| [`cra_csaf_advisory_tool.py`](./cra_csaf_advisory_tool.py) | CLI Automation Tool | Annex I Part II(6), OASIS CSAF 2.0 | **CSAF 2.0 & OpenVEX Generator & Validator:** CLI tool creating schema-compliant OASIS CSAF 2.0 JSON advisories and OpenVEX v0.2.0 exploitability statements with CRA free-update notices. |
| [`CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix.xlsx`](./CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix.xlsx) | Excel Workbook (Audit Ready) | Reg (EU) 2024/2847, Annex I, VII, VIII, Art. 13, 14 | **Master Compliance & Tool Coverage Matrix:** 6-sheet workbook featuring 43 traceable requirements across 31 standardized columns, evaluating 10 security tools/activities, mapping 44 lifecycle controls, identifying 20 governance gaps, and providing an Executive KPI Dashboard. |
| [`CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix_Guide.md`](./CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix_Guide.md) | Executive Guide & Report | Reg (EU) 2024/2847 | **Matrix Architecture & Assessment Guide:** Comprehensive companion report detailing workbook architecture, quantitative tool coverage scorecards, lifecycle control gates, residual gaps, and compliance roadmap. |
| [`matrix-generator/`](./matrix-generator/) | Python Build Engine | OpenPyXL Pipeline | **Matrix Generator Pipeline:** Modular Python compilation scripts and JSON datasets (`all_reqs.json`, `tool_profiles.json`, etc.) allowing continuous regeneration and customization of the Excel matrix workbook. |
| [`CRA_Placing_and_Making_Available_Market_Lifecycle.md`](./CRA_Placing_and_Making_Available_Market_Lifecycle.md) | Legal & Lifecycle Analysis | Art. 3(21), 3(22), 3(30), 4(3), 13(8), 13(10), 14, 21, 22 | **Market Placement & Lifecycle Guide:** Definitive legal analysis of "Placing on the Market" vs. "Making Available" across 9 lifecycle phases, 14 mandatory legal distinctions, 15-scenario decision matrix, worked timelines, decision tree, and SDLC release-gate checklist. |
| [`CRA_Default_Category_Vendor_Lifecycle_Guide.md`](./CRA_Default_Category_Vendor_Lifecycle_Guide.md) | Vendor Operational Guide | Module A (Annex VIII), Annex I, VII, V | **Default Category Playbook:** Comprehensive end-to-end handbook for vendors that sell, develop, build, deploy, and support standard products under 100% in-house Module A internal production control. |
| [`CRA_Open_Source_and_COTS_Integration_Guide.md`](./CRA_Open_Source_and_COTS_Integration_Guide.md) | Component Compliance Guide | Art. 13(5), 13(6), 14(2), Annex I Part II | **FOSS & COTS Integration Guide:** Detailed obligations for integrating third-party and open-source software into standard solutions across Sell, Develop, Build, Deploy, and RUN maintenance (due diligence, reachability, upstream sharing, abandonware). |
| [`CRA_Solution_Provider_Lifecycle_Requirements.md`](./CRA_Solution_Provider_Lifecycle_Requirements.md) | Policy & Assessment | Full Reg (EU) 2024/2847 | **Core Master Deliverable:** Comprehensive requirements and business process impact assessment mapping regulatory obligations across all 6 lifecycle stages (Presales to Decommissioning). |
| [`CRA_Article_14_Reporting_Operational_Runbook.md`](./CRA_Article_14_Reporting_Operational_Runbook.md) | Operational Procedure | Art. 14, 15–17, Del. Reg 2026/881 | **Phase 1 Priority (Live Law):** Binding incident response runbook, ENISA Single Reporting Platform (SRP) procedures, 24h/72h notification countdowns, and standard forms. |
| [`cra_article14_deadlines.py`](./cra_article14_deadlines.py) | CLI Automation Tool | Art. 14(2), 14(4), 14(8) | **Statutory Deadline Calculator, Triage Gate & Drill Validator:** Computes statutory countdowns, executes MYBU 5-question rapid triage with 20h buffer enforcement, and validates drill logs. |
| [`CRA_Contractual_Templates_and_Addenda.md`](./CRA_Contractual_Templates_and_Addenda.md) | Legal Documentation | Art. 13(5), 13(8), 21, 22 | **Phase 2 Contract Package:** Schedule A (Customer CRA Addendum with 5-year support warranty), Schedule B (Supplier 12-Hour Emergency Notification SLA and SBOM covenants), and Schedule C (Bespoke Software). |
| [`cra_presales_gate.py`](./cra_presales_gate.py) | CLI Automation Tool | Art. 2, 3, 21, 22, 32 | **Presales Gating Engine:** Interactive and batch qualification CLI tool scoring role archetypes (A–E), product risk tiers (Default, Class I, Class II, Critical), and generating formal bid risk dossiers. |
| [`cra_ci_pipeline_gate.py`](./cra_ci_pipeline_gate.py) | CI/CD Quality Gate | Annex I, II & Art. 14 | **Phase 3 Build Gate:** Automates CycloneDX SBOM generation, SCA reachability analysis, Article 14 KEV active exploit screening, OpenVEX document emission, and blocking build gates. |
| [`cra_compliance_gate_workflow.yml`](./cra_compliance_gate_workflow.yml) | CI/CD Pipeline Config | GitHub Actions | Reusable GitHub Actions workflow for PR gating and release compliance archiving. |

---

## ⚡ Quickstart & Operational Usage

### 1. Rapid Article 14 Incident Triage (MYBU Procedure & SEC-PRO-CRA-001)
Evaluate the 5-question statutory decision gate, compute the internal 20-hour buffer, and emit certified audit records:

```bash
# Reportable in-the-wild zero-day triage
python3 cra_article14_deadlines.py triage \
  --product "SecureEdge Gateway 5000" \
  --event-id "EVT-2026-MYBU-0042" \
  --t0 "2026-10-12T14:00:00+02:00" \
  --q1-supplied yes \
  --q2-manufacturer yes \
  --q3-exploited yes \
  --q4-exploitable yes \
  --out-json triage_record.json \
  --out-md triage_summary.md

# Non-exploitable finding requiring signed NEDR justification
python3 cra_article14_deadlines.py triage \
  --product "SmartEdge Telemetry Hub 400" \
  --event-id "EVT-2026-MYBU-0043" \
  --t0 "2026-10-12T14:00:00+02:00" \
  --q1-supplied yes \
  --q2-manufacturer yes \
  --q3-exploited yes \
  --q4-exploitable no \
  --q4-justification "Vulnerable symbol heap_alloc_daemon() in libproto is unreachable in production build (CONFIG_DEBUG_TRACE=0 hardcoded and stripped; verified by static call graph and HIL fuzzing)" \
  --out-json triage_non_exploitable.json
```

### 2. Execute Tabletop Incident Simulation Drill ("Operation DarkFrame")
Run an interactive or automated drill testing the Article 14 ENISA SRP notification pipeline, CVD triage, and hotfix release:

```bash
# Interactive mode (step-by-step incident injects)
python3 cra_drill_simulator.py

# Automated golden-path mode (audit certification)
python3 cra_drill_simulator.py --automated \
  --out-json drill_results.json \
  --out-md drill_pear_report.md

# Validate drill record schema with deadline tool
python3 cra_article14_deadlines.py drill cra_tabletop_drill_execution_record.json
```

### 3. Product Risk Classification & Conformity Routing
Evaluate a solution against Annex III and IV categories and compute Notified Body mandates:

```bash
# List all 27 statutory Annex III & IV categories
python3 cra_classification_engine.py --list-categories

# Evaluate a product and generate audit dossier
python3 cra_classification_engine.py \
  --product "SmartEdge Telemetry Hub 400" \
  --vendor "Industrial Logic BV" \
  --purpose "Industrial telemetry ingestion, protocol conversion, and MQTT egress" \
  --class-1 vpn_function \
  --out-json classification.json \
  --out-md classification_dossier.md
```

### 4. Generate & Audit RFC 9116 `security.txt`
```bash
# Generate compliant security.txt file
python3 cra_security_txt_tool.py generate \
  --domain "company.com" \
  --email "security@company.com" \
  --intake-url "https://company.com/security/report" \
  --policy-url "https://company.com/security/cvd-policy" \
  --pgp-url "https://company.com/security/pgp.asc" \
  --output security.txt

# Audit and validate existing security.txt
python3 cra_security_txt_tool.py validate security.txt
```

### 5. Generate CSAF 2.0 & OpenVEX Security Advisories
```bash
# Create CSAF 2.0 JSON security advisory
python3 cra_csaf_advisory_tool.py create-csaf \
  --id "COMPANY-SA-2026-001" \
  --title "Buffer Overflow in Network Daemon" \
  --cve "CVE-2026-49120" \
  --cvss 9.6 \
  --cvss-vector "CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H" \
  --vendor "SecureEdge Technologies" \
  --product "SEG-5000" \
  --fixed-version "3.4.1" \
  --summary "Heap buffer overflow in network framing parser." \
  --fix-url "https://download.company.com/updates/SEG-5000-v3.4.1.bin" \
  --out csaf-advisory.json

# Validate CSAF 2.0 JSON file
python3 cra_csaf_advisory_tool.py validate-csaf csaf-advisory.json

# Create companion OpenVEX exploitability document
python3 cra_csaf_advisory_tool.py create-vex \
  --id "VEX-2026-001" \
  --cve "CVE-2026-49120" \
  --purl "pkg:generic/secureedge/seg-5000@3.4.1" \
  --status fixed \
  --out openvex.json
```

### 6. Calculate Article 14 Statutory Deadlines
Article 14 is **live statutory law since 11 September 2026**. Deadlines begin strictly upon establishing legal awareness:

```bash
# Calculate statutory deadlines for an Actively Exploited Vulnerability (Art 14(2))
python3 cra_article14_deadlines.py calc \
  --type vulnerability \
  --awareness 2026-10-12T14:00:00+02:00 \
  --mitigation-available 2026-10-16T18:00:00+02:00

# Validate a semi-annual tabletop reporting drill log
python3 cra_article14_deadlines.py drill cra_tabletop_drill_execution_record.json
```

### 7. Presales Gating & Solution Role Qualification
```bash
# Interactive mode (step-by-step questionnaire)
python3 cra_presales_gate.py

# Automated batch mode
python3 cra_presales_gate.py \
  --batch \
  --project "Cloud-Connected Micro-Gateway" \
  --client "Telecom Corp EU" \
  --has-digital --has-network --own-brand --class-1 \
  --support-years 5 \
  --out-md CRA_Presales_Gate_Sample.md \
  --out-json cra_presales_gate_sample.json
```

### 8. CI/CD Build Pipeline Quality Gate
```bash
python3 cra_ci_pipeline_gate.py \
  --repo . \
  --output-dir build/cra-artifacts \
  --fail-on CRITICAL
```
