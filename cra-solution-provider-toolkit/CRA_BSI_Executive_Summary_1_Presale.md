# Executive Summary - CRA / BSI TR-03183 impact on Presale

**Process:** 1. Presale - Bids, RFP answers, contractual commitments, security claims, support-period commitments, pricing of compliance effort.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_1_Presale.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

Presale has few Critical/High items (4 Critical, 5 High), but they carry the largest commercial exposure: they fix what every offer commits the company to for ten years or more. Bids written today for deliveries after 11 December 2027 must already cover full CRA conformity, a support period that matches the real operating life of airport and government systems, free security updates, ten-year availability of updates and secure-by-default delivery. If these are not priced and contracted now, the company will carry unfunded legal obligations later.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 4 | 5 | 41 | 91 | 451 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 4 | 5 |
| BSI TR-03183-2 v2.1.0 | 0 | 0 |
| BSI TR-03183-3 v1.0.0 | 0 | 0 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 4, M = 5 (S/M/L = small/medium/large).

## Key findings

### 1. CRA conformity is a market-access condition for current bids

- **What the requirements demand:** From 11 Dec 2027 every in-scope product made available on the EU market must meet all CRA requirements; products placed on the market earlier fall under the CRA once they are substantially modified after that date.
- **Why it matters for us:** Public procurement cycles are long, so many bids submitted now will be delivered after the deadline. Extension orders and upgrades of installed legacy systems can amount to a substantial modification.
- **What we must do:** Add a CRA conformity statement and responsibility split to all bid and contract templates; add a CRA readiness and classification check (in scope, default category) to bid/no-bid; screen change requests and extension orders for substantial modification and price the conformity work.
- **Lead role:** Bid Manager (with Contract Manager / Legal)
- **Requirements (2):** Critical: `TR1-007`; High: `TR1-009`

### 2. Support period sized to the real operating life

- **What the requirements demand:** Vulnerability handling with timely security updates during a support period that reflects the expected time in use (generally at least five years); all post-market obligations apply for that whole period.
- **Why it matters for us:** Airport and government systems often stay in operation for ten years or more - far beyond typical warranty or maintenance terms. An under-sized or unpriced support period becomes a legal liability.
- **What we must do:** Set a support-period policy per solution line, state the support end date in every offer, and price long-term security maintenance (PSIRT, monitoring, patching, field roll-out) for the full period.
- **Lead role:** Bid Manager / Product Manager / Contract Manager
- **Requirements (3):** Critical: `TR1-018`; High: `TR1-029`, `TR1-030`

### 3. Security updates must be free of charge

- **What the requirements demand:** Security updates are provided free of charge unless otherwise agreed with a business user for a tailor-made product.
- **Why it matters for us:** Maintenance models that bill patches will no longer work; the tailor-made exception exists only where it is explicitly agreed.
- **What we must do:** Redesign the pricing model so security-update costs sit in the product price or the base maintenance fee; keep security patches separate from chargeable feature upgrades; use the tailor-made exception only with an explicit, legally reviewed contract clause.
- **Lead role:** Bid Manager / Product Manager
- **Requirements (2):** Critical: `TR1-028-c`, `VH.8a-a`

### 4. Ten-year availability of security updates

- **What the requirements demand:** Security updates must remain available for at least 10 years after the product has been placed on the market, or for the full support period if that is longer.
- **Why it matters for us:** This is a long-tail cost (update repository, archived build environments) that must be priced and committed in contracts.
- **What we must do:** Include the ten-year availability commitment and its cost in offers and contract templates.
- **Lead role:** Bid Manager / Product Manager / Contract Manager
- **Requirements (1):** High: `TR1-031-a`

### 5. Secure-by-default delivery and agreed deviations

- **What the requirements demand:** Solutions are made available with a secure default configuration unless otherwise agreed with a business user for a tailor-made product.
- **Why it matters for us:** Customers often ask for settings that weaken security (legacy protocols, shared accounts, open interfaces); such deviations are acceptable only when agreed for a tailor-made solution.
- **What we must do:** Describe the secure-default baseline in solution descriptions and add a deviation clause with documented customer acceptance to the contract templates.
- **Lead role:** Presales Solution Architect
- **Requirements (1):** High: `ER.2`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Update bid and contract templates: CRA conformity clause, stated support end date, free security updates, ten-year update availability, secure-default deviation clause.<br>Add the CRA classification and substantial-modification check to bid/no-bid and change-request reviews.<br>Brief bid teams on what may and may not be promised (SBOM, PSIRT response times, disclosure). |
| By mid-2027 | Approve a pricing model for long-term, free security maintenance per solution line.<br>Add CRA flow-down clauses to supplier and subcontractor templates used in bids. |
| By 11 Dec 2027 | All offers for deliveries after 11 Dec 2027 commit only to capabilities the delivery processes can prove. |

## Decisions needed

- Support-period policy per solution line (default length and how it is set).
- Pricing approach for free security updates (base fee or product price) and when the tailor-made exception may be used.

## Dependencies on other processes

Needs confirmed capabilities from 5. Maintenance (PSIRT, patch times, advisories), 2. Development (secure defaults) and 3. Integration/Build (EU declaration of conformity, SBOM). Every commitment made in Presale becomes an obligation for 4. Deployment and 5. Maintenance.

## Beyond Critical and High

The 41 Medium items mostly add clauses and answers to the bid library: who provides the operating environment and who carries shared risks, lifecycle responsibility, customer notification under the reporting duty, the update and disclosure model, SBOM deliverables and formats, CE marking and the EU declaration of conformity, and screening of change requests for substantial modification.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (9)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| TR1-007 | Critical | From 11 Dec 2027 all in-scope products made available must meet all CRA requirements | Add an approved answer/clause on 'from 11 Dec 2027 all in-scope products made available must meet all CRA requirements' to the bid library and contract templates; confirm feasibility with the owning process before committing. | Bid Manager (with Contract Manager / Legal) | L |
| TR1-018 | Critical | Handle vulnerabilities with timely updates during a support period reflecting expected use time (minimum five years) | Define a support-period policy per solution (based on expected use time), state the end date in every offer and price security maintenance for the full period. | Bid Manager / Product Manager / Contract Manager | L |
| TR1-028-c | Critical | Security updates generally free of charge unless agreed otherwise for tailor-made business products | Include continuous vulnerability monitoring, security updates and periodic reviews in the maintenance offer and price them for the full support period. | Bid Manager / Product Manager | L |
| VH.8a-a | Critical | Security updates free of charge unless otherwise agreed for tailor-made business products | Describe and price the vulnerability-handling service (monitoring, fixes, advisories) in the maintenance offer. | Bid Manager | L |
| TR1-009 | High | Products placed on the market before 11 Dec 2027 fall under the CRA only after a substantial modification after that date | Add an approved answer/clause on 'products placed on the market before 11 Dec 2027 fall under the CRA only after a substantial modification after that date' to the bid library and contract templates; confirm feasibility with the owning process before committing. | Bid Manager (with Contract Manager / Legal) | M |
| TR1-029 | High | Post-market obligations must be upheld during the support period based on expected duration of use | Define a support-period policy per solution (based on expected use time), state the end date in every offer and price security maintenance for the full period. | Bid Manager / Product Manager / Contract Manager | M |
| TR1-030 | High | The support period is generally at least five years | Define a support-period policy per solution (based on expected use time), state the end date in every offer and price security maintenance for the full period. | Bid Manager / Product Manager / Contract Manager | M |
| TR1-031-a | High | Keep security updates available for at least 10 years after placing on the market (or the support period if longer) | Define a support-period policy per solution (based on expected use time), state the end date in every offer and price security maintenance for the full period. | Bid Manager / Product Manager / Contract Manager | M |
| ER.2 | High | Secure-by-default configuration unless otherwise agreed for tailor-made business products | Answer RFP security requirements from the solution's Annex I applicability statement; treat customer-requested deviations as contract items. | Presales Solution Architect | M |
