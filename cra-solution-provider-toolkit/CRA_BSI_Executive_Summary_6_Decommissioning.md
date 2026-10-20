# Executive Summary - CRA / BSI TR-03183 impact on Solution Decommissioning

**Process:** 6. Solution Decommissioning - End-of-support notification, secure data removal, retention of documentation and records, final customer communication.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_6_Decommissioning.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

Decommissioning has the fewest Critical/High items (1 Critical, 4 High), but one is a new product capability: verified, permanent removal of all data and settings, plus secure transfer of data to successor systems. Several obligations also outlive each installation: the end of the support period ends vulnerability handling and needs timely customer notice, and security updates and technical documentation must stay available for at least ten years.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 14 | 17 | 556 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 1 | 4 |
| BSI TR-03183-2 v2.1.0 | 0 | 0 |
| BSI TR-03183-3 v1.0.0 | 0 | 0 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 1, M = 4 (S/M/L = small/medium/large).

## Key findings

### 1. Secure data removal and secure data transfer

- **What the requirements demand:** Users must be able to remove all data and settings securely, easily and permanently; where data can be transferred to other products or systems, the transfer must be secure.
- **Why it matters for us:** Government and airport customers typically require proof of deletion at contract end; without a verified wipe function and procedure the solution does not meet the requirement.
- **What we must do:** Specify the wipe function with Development (including backups, logs and keys), define a verified decommissioning procedure with a deletion certificate, and offer a secure export for migration.
- **Lead role:** Service Delivery Manager / Data Protection Officer
- **Requirements (2):** Critical: `ER.14-a`; High: `ER.14-b`

### 2. End of support managed against the support period

- **What the requirements demand:** The support period reflects the time the product is expected to be in use; its end is the end of vulnerability handling with security updates.
- **Why it matters for us:** Customers must know in time when monitoring and updates stop, so they can plan replacement.
- **What we must do:** Track support end dates per installation and send end-of-support notices with migration options well in advance.
- **Lead role:** Customer Success Manager / Service Delivery Manager
- **Requirements (1):** High: `TR1-018`

### 3. Obligations that outlive the installation

- **What the requirements demand:** Security updates and the technical documentation must remain available for at least 10 years after the product has been placed on the market, or for the full support period if that is longer.
- **Why it matters for us:** Decommissioning a customer installation must not delete update repositories or technical files.
- **What we must do:** Set up a retention schedule and archive for technical files, SBOMs, EU declarations and update packages.
- **Lead role:** Customer Success Manager / Service Delivery Manager
- **Requirements (2):** High: `TR1-031-a`, `TR1-031-b`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Record support end dates for all installed solutions.<br>Specify the secure data-removal function and the decommissioning procedure. |
| By mid-2027 | Retention schedule and archive for documentation and update packages.<br>End-of-support notification template and deletion certificate. |
| By 11 Dec 2027 | Every solution made available after 11 Dec 2027 offers verified data removal and a documented decommissioning path. |

## Decisions needed

- Retention system and owner for the ten-year records.

## Dependencies on other processes

Depends on 2. Development for the wipe and export functions, 3. Integration/Build for archives, 5. Maintenance for support-period tracking and 1. Presale for exit and data-return commitments.

## Beyond Critical and High

The 14 Medium items cover lifecycle responsibility at the end of support, support-period communication, availability of the technical documentation to market surveillance, reset to the original state, and protection of access rights, confidential data and minimised data at exit.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (5)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| ER.14-a | Critical | Provide secure and easy permanent removal of all data and settings | Provide and execute a verified data-wipe and secure data-transfer procedure and issue a deletion certificate to the customer. | Service Delivery Manager / Data Protection Officer | L |
| TR1-018 | High | Handle vulnerabilities with timely updates during a support period reflecting expected use time (minimum five years) | Notify customers well before the support end date and plan migration or decommissioning. | Customer Success Manager / Service Delivery Manager | M |
| TR1-031-a | High | Keep security updates available for at least 10 years after placing on the market (or the support period if longer) | Notify customers well before the support end date and plan migration or decommissioning. | Customer Success Manager / Service Delivery Manager | M |
| TR1-031-b | High | Keep technical documentation available for at least 10 years (or the support period if longer) | Retain technical files for at least 10 years after placing on the market (or the support period if longer) with a retrieval procedure. | Records / Documentation Manager | M |
| ER.14-b | High | Where data can be transferred to other products or systems, ensure this is done securely | Provide and execute a verified data-wipe and secure data-transfer procedure and issue a deletion certificate to the customer. | Service Delivery Manager / Data Protection Officer | M |
