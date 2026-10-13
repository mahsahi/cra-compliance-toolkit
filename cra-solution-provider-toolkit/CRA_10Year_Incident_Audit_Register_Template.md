# CRA 10-Year Statutory Incident & Triage Audit Register
**Document Ref:** `AUDIT-LEDGER-TEMPLATE-v1.0`  
**Governing Standard:** `SEC-PRO-CRA-001` §7 · Regulation (EU) 2024/2847 Art. 13(10), 14, 53  
**Legal Obligation:** Mandatory 10-Year Evidentiary Record Retention for all Security Events (Reportable and Non-Reportable)

---

> [!IMPORTANT]
> **Audit Rule:** Under CRA Article 13(10) and Article 14, manufacturers must retain technical documentation, incident triage assessments, and notification records for **at least 10 years after the product has been placed on the market or for the support period (whichever is longer)**.
> Every event ingested by PSIRT—including non-reportable false alarms and non-exploitable findings—must have a row in this ledger.

---

## 1. Master Event Ledger Column Schema

| Column Index | Field Name | Type | Description | Mandatory Evidence Link |
|---|---|---|---|---|
| **COL-01** | `Event_ID` | String | Unique tracking code: `EVT-YYYY-[BU]-[SEQ]` | Triage ticket / JIRA key |
| **COL-02** | `Ingress_Vector` | Enum | `CERT_Advisory` \| `Customer_SOC` \| `CVD_Hacker` \| `Internal_Scan` \| `Supplier_SLA` | Raw inbound message / EML |
| **COL-03** | `T0_Arrival_UTC` | ISO-8601 | Exact timestamp information reached the company (server receive time) | Email header / log timestamp |
| **COL-04** | `System_ID` | String | Target product asset ID from Systems Register | `SYS-MYBU-SEG5000` |
| **COL-05** | `Vulnerability_CVE` | String | CVE-YYYY-NNNNN or "N/A - Security Incident" | Advisory URL |
| **COL-06** | `Q1_Supplied` | Boolean | Did we supply the product? (Yes/No) | Contract ref / inventory match |
| **COL-07** | `Q2_Manufacturer` | Boolean | Are we the manufacturer / brand placer? (Yes/No) | DoC / Legal entity register |
| **COL-08** | `Q3_Exploited` | Boolean | Credible active exploitation confirmed? (Yes/No) | KEV list / IoC report / cert |
| **COL-09** | `Q4_Exploitable` | Boolean | Exploitable in our build & configuration? (Yes/No) | Signed NEDR document link |
| **COL-10** | `Q5_Severe_Incident` | Boolean | Severe impact or malicious code execution? (Yes/No) | Incident severity dossier |
| **COL-11** | `Reportable_Status` | Enum | `REPORTABLE` (Art 14) \| `NON_REPORTABLE` | Automated 5-question evaluation |
| **COL-12** | `Target_20h_Internal` | ISO-8601 | Internal buffer milestone (`T0 + 20 hours`) | Calendar trigger |
| **COL-13** | `Early_Warning_24h` | ISO-8601 | Statutory deadline (`T0 + 24 hours`) | Regulatory deadline |
| **COL-14** | `EW_Filed_UTC` | ISO-8601 | Actual timestamp Early Warning submitted to SRP | SRP submission screenshot |
| **COL-15** | `EW_SRP_Ref` | String | ENISA SRP transmission reference number | SRP confirmation ticket |
| **COL-16** | `Cust_Notif_24h_Due` | ISO-8601 | Statutory customer alert deadline (`T0 + 24 hours`) | Art. 14(8) customer advisory |
| **COL-17** | `Cust_Notif_Sent_UTC` | ISO-8601 | Actual customer broadcast timestamp | Mail delivery / portal receipt |
| **COL-18** | `Notif_72h_Due` | ISO-8601 | Statutory detailed notification deadline (`T0 + 72 hours`) | Regulatory deadline |
| **COL-19** | `Notif_72h_Filed_UTC`| ISO-8601 | Actual timestamp Detailed Notification submitted | SRP confirmation ticket |
| **COL-20** | `Workaround_Available`| ISO-8601 | Timestamp workaround or hotfix released (starts 14d clock) | Advisory release note |
| **COL-21** | `Final_Report_Due` | ISO-8601 | `Workaround + 14 days` (Vuln) or `72h Notif + 1 month` (Inc) | Statutory deadline |
| **COL-22** | `Final_Report_Filed` | ISO-8601 | Actual final report submission timestamp | SRP confirmation ticket |
| **COL-23** | `Upstream_Notified` | Boolean | FOSS / COTS maintainer informed? (Art. 13(5)) | Email confirmation hash |
| **COL-24** | `Retention_Expiry` | ISO-8601 | 10 years from resolution (`T0 + 10 years`) | WORM vault retention tag |
| **COL-25** | `WORM_Archive_URI` | URI | Immutable cloud vault path containing all evidence | S3 / Azure WORM archive link |

---

## 2. Example Ledger Data (CSV / JSON Interchangeable)

```csv
Event_ID,Ingress_Vector,T0_Arrival_UTC,System_ID,CVE,Reportable,EW_24h_Due,EW_Filed_UTC,EW_Ref,Cust_Notif_Sent,Final_Report_Due,Final_Filed_UTC,WORM_URI
EVT-2026-MYBU-0001,CERT_Advisory,2026-10-12T02:00:00Z,SYS-MYBU-SEG5000,CVE-2026-49120,REPORTABLE,2026-10-13T02:00:00Z,2026-10-12T14:00:00Z,ENISA-SRP-2026-88192,2026-10-12T18:00:00Z,2026-10-26T18:00:00Z,2026-10-20T11:00:00Z,s3://cra-worm/2026/EVT-0001/
EVT-2026-MYBU-0002,Supplier_SLA,2026-10-14T09:15:00Z,SYS-MYBU-STH400,CVE-2026-31990,NON_REPORTABLE,N/A,N/A,N/A,N/A,N/A,N/A,s3://cra-worm/2026/EVT-0002/
```

---

## 3. Mandatory Evidentiary Package per Ledger Row

For every entry in the register, an immutable evidentiary package folder must be generated and hashed:

```
s3://cra-worm/YYYY/[Event_ID]/
├── 01_raw_ingress_proof.eml                ── Inbound email with full internet headers proving T0
├── 02_triage_decision_record.json          ── 5-question automated decision record and signatures
├── 03_signed_nedr_record.pdf (if Q4=No)    ── Signed Technical Non-Exploitability Record
├── 04_enisa_early_warning_payload.json     ── Payload submitted at T+12h
├── 05_enisa_early_warning_screenshot.png   ── Screenshot of SRP confirmation dialog
├── 06_customer_advisory_broadcast.eml      ── Copy of Article 14(8) customer notification
├── 07_enisa_72h_detailed_payload.json      ── Payload submitted at T+32h
├── 08_enisa_72h_screenshot.png             ── Screenshot of SRP detailed filing
├── 09_workaround_release_announcement.pdf  ── Advisory with date establishing 14-day clock
├── 10_enisa_14d_final_payload.json         ── Final report submitted to ENISA SRP
├── 11_upstream_maintainer_notice.eml       ── Proof of code sharing / disclosure to upstream
└── sha256sums.txt                          ── Cryptographic checksums of all package artifacts
```
