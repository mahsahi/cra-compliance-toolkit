# Executive Summary - CRA / BSI TR-03183 impact on Solution Maintenance (RUN)

**Process:** 5. Solution Maintenance (RUN) - Vulnerability monitoring and handling, security updates, coordinated vulnerability disclosure, incident and vulnerability reporting, SBOM updates, support period.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_5_Maintenance_RUN.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

Maintenance (RUN) carries the largest and most urgent load (26 Critical, 63 High). CRA Art. 14 reporting has applied since 11 September 2026 - also to solutions installed years ago - and needs a process that can deliver a 24-hour early warning, a 72-hour notification and a final report through ENISA's single reporting platform to the coordinating CSIRT and ENISA. From 11 December 2027 RUN must also operate the full vulnerability-handling lifecycle of Annex I Part II and the PSIRT, CVD and public intake channels described in BSI TR-03183-3.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 26 | 63 | 119 | 169 | 215 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 20 | 34 |
| BSI TR-03183-2 v2.1.0 | 1 | 6 |
| BSI TR-03183-3 v1.0.0 | 5 | 23 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 24, M = 63, S = 2 (S/M/L = small/medium/large).

## Key findings

### 1. Art. 14 reporting - in force now

- **What the requirements demand:** Report actively exploited vulnerabilities and severe incidents to the coordinating CSIRT and ENISA simultaneously: early warning within 24 hours of awareness, notification within 72 hours, final report within 14 days after a fix or mitigation is available (vulnerabilities) or within one month (incidents); select the corresponding national CSIRT and coordinate mitigations and schedules with it.
- **Why it matters for us:** This duty already applies, including to the whole installed base; a missed deadline is a direct legal breach.
- **What we must do:** Set up an interim reporting capability immediately: named reporters and deputies, access to the single reporting platform, report templates, awareness criteria, 24/7 escalation and one rehearsal.
- **Lead role:** PSIRT Lead / Compliance Officer
- **Requirements (23):** Critical: `TR1-005`, `TR1-006`, `TR1-032-a`, `TR1-032-b`, `TR1-033`, `TR1-034-a`, `TR1-035`, `TR1-038`, `TR1-040`, `TR1-042`, `TR1-045`, `TR3-007`, `TR3-4.4.2a`; High: `TR1-008`, `TR1-034-b`, `TR1-036`, `TR1-041-a`, `TR1-041-b`, `TR1-043`, `TR1-046`, `TR3-008`, `TR3-4.4.2b-a`, `TR3-4.4.2b-b`

### 2. PSIRT organisation, CVD policy and public intake channels

- **What the requirements demand:** Create internal PSIRT and CSIRT roles divided among several people with cover for absences; publish and enforce a CVD policy (confidential handling, no criminal charges against good-faith reporters, response within five and detailed feedback within ten working days, no single analyst closes a report); provide a contact address, a central reporting web page, a web form, a security.txt (RFC 9116) and a public security information website; record all measures, test procedures and test results.
- **Why it matters for us:** A CVD policy and a reporting contact are CRA essential requirements; the PSIRT is also the engine of the reporting duty.
- **What we must do:** Approve a PSIRT charter and staffing, publish the CVD policy and security pages, and test and record the reporting channels regularly.
- **Lead role:** PSIRT Lead (Legal reviews policy wording)
- **Requirements (23):** Critical: `VH.5`, `VH.6a`, `TR3-4.3.1a`, `TR3-4.3.4a`, `TR3-022`; High: `VH.6`, `TR3-003`, `TR3-005`, `TR3-016`, `TR3-019`, `TR3-4.1.1a`, `TR3-020`, `TR3-021`, `TR3-4.3.1b`, `TR3-4.3.1f`, `TR3-4.3.1m`, `TR3-4.3.3a-a`, `TR3-4.4.4a`, `TR3-4.4.4c`, `TR3-4.4.4d`, `TR3-4.4.7g`, `TR3-4.4.8a-a`, `TR3-4.4.8b`

### 3. SBOM-based vulnerability monitoring and remediation

- **What the requirements demand:** Monitor every supported release for vulnerabilities throughout the support period, using its per-version SBOM; analyse whether a flagged subcomponent affects the product; remediate without delay with security updates, separately from feature updates where feasible; report vulnerabilities in third-party components to their maintainers.
- **Why it matters for us:** Monitoring is impossible without accurate per-version SBOMs (CPE/purl) and a map of which version runs at which site.
- **What we must do:** Load all released SBOMs into a monitoring tool, define triage and fix targets by severity, and set up an upstream reporting route.
- **Lead role:** PSIRT Lead
- **Requirements (17):** Critical: `TR1-028-a`, `TR1-028-b`, `VH.1`, `VH.2a-a`, `TR2-004`; High: `TR1-051`, `TR1-067`, `TR1-068`, `TR1-117-b`, `ER.1`, `VH.1a`, `VH.2a-b`, `TR2-005`, `TR2-006-a`, `TR2-011`, `TR2-066`, `TR3-001`

### 4. Security updates, advisories and public disclosure

- **What the requirements demand:** Distribute updates securely and without delay, free of charge (unless agreed otherwise for a tailor-made product), with advisory messages and update notifications; keep updates available for at least ten years; publish fixed vulnerabilities as CSAF advisories (including VEX); disclose validated vulnerabilities within 90 days (TR-3).
- **Why it matters for us:** Public disclosure and free updates are new for many B2B providers and touch the confidentiality expectations of government and airport customers.
- **What we must do:** Operate an update distribution service (online and offline), an advisory/CSAF publication process and a long-term update repository.
- **Lead role:** PSIRT Lead
- **Requirements (13):** Critical: `VH.4-a`, `VH.7`, `VH.8`; High: `TR1-028-c`, `TR1-031-a`, `ER.4`, `ER.4c`, `VH.8a-a`, `VH.8a-b`, `TR2-003`, `TR2-092`, `TR3-006`, `TR3-4.4.10a-a`

### 5. Support period, post-market review and change control

- **What the requirements demand:** Uphold all obligations for the full support period; review cybersecurity regularly; update the risk assessment when new vulnerabilities or threats appear; screen changes for substantial modification; keep essential functions available after incidents; cooperate with market surveillance authorities.
- **Why it matters for us:** Long support periods multiply the number of release lines that must be maintained in parallel.
- **What we must do:** Keep a support-period register per release, plan capacity per release line, and add the review and the substantial-modification check to change management.
- **Lead role:** PSIRT Lead / Product Security Officer
- **Requirements (13):** High: `TR1-009`, `TR1-011`, `TR1-018`, `TR1-026`, `TR1-027`, `TR1-029`, `TR1-066`, `TR1-072`, `TR1-156`, `TR1-158`, `RH_UPD.1-a`, `RH_UPD.1-b`, `ER.9`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Interim Art. 14 reporting capability: reporters, single reporting platform access, templates, awareness criteria, 24/7 escalation, rehearsal.<br>Select and document the corresponding national CSIRT; complete the installed-base register.<br>Approve the PSIRT charter and staffing. |
| By mid-2027 | Publish the CVD policy, security page, security.txt and report web form; start SBOM-based monitoring.<br>Advisory/CSAF publication process and update distribution for online and segregated sites. |
| By 11 Dec 2027 | Full Annex I Part II lifecycle in operation for all solutions made available after 11 Dec 2027, with free security updates and a ten-year update repository. |

## Decisions needed

- PSIRT headcount (several people per role, deputies, on-call).
- Disclosure stance towards government and airport customers (public advisories, 90-day rule).

## Dependencies on other processes

Relies on 3. Integration/Build (SBOMs, patch builds), 2. Development (impact analysis, fixes), 4. Deployment (installed base, roll-out) and 1. Presale (contract clauses on notification, free updates and support periods).

## Beyond Critical and High

The 119 Medium items detail the security.txt fields, PSIRT/CSIRT organisation, the content of the vulnerability-reporting web page and web form, anonymous reporting, CVD principles and disclosure rules, the security information website, SBOM data-field maintenance, and updates of the technical documentation and risk assessment.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (89)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| TR1-005 | Critical | CRA Art. 14 reporting obligations start on 11 September 2026 | Set up an interim reporting capability immediately: name reporters and deputies, register on the single reporting platform, prepare templates, define awareness criteria and a 24/7 escalation path; rehearse once. | PSIRT Lead / Service Delivery Manager | L |
| TR1-006 | Critical | The reporting obligations also apply to products already placed on the market | Build or complete the installed-base register for all delivered solutions still in operation and link it to the PSIRT reporting procedure. | PSIRT Lead / Service Delivery Manager | L |
| TR1-028-a | Critical | Monitor the product for vulnerabilities throughout the support period | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | L |
| TR1-028-b | Critical | Address found vulnerabilities including by providing security updates | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | L |
| TR1-032-a | Critical | Report actively exploited vulnerabilities upon becoming aware of them | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-032-b | Critical | Report severe incidents affecting product security upon becoming aware of them | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-033 | Critical | Notify CSIRT and ENISA simultaneously via the single reporting platform | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-034-a | Critical | Early warning within 24 hours of awareness of an actively exploited vulnerability | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-035 | Critical | Detailed vulnerability notification within 72 hours | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-038 | Critical | Final report within 14 days after a corrective or mitigating measure is available | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-040 | Critical | Early warning within 24 hours of awareness of a severe incident | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-042 | Critical | Detailed incident notification within 72 hours | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-045 | Critical | Final incident report within one month incl. severity, impact, root cause and mitigations | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | L |
| VH.1 | Critical | Identify and document vulnerabilities and components contained in products | Implement, document and operate: identify and document vulnerabilities and components contained in products. | PSIRT Lead | L |
| VH.2a-a | Critical | Address and remediate vulnerabilities without delay, incl. security updates | Implement, document and operate: address and remediate vulnerabilities without delay, incl. security updates. | PSIRT Lead | L |
| VH.4-a | Critical | Once a security update is available, publicly disclose information about fixed vulnerabilities | Implement, document and operate: once a security update is available, publicly disclose information about fixed vulnerabilities. | PSIRT Lead | L |
| VH.5 | Critical | Put in place and enforce a coordinated vulnerability disclosure policy | Implement, document and operate: put in place and enforce a coordinated vulnerability disclosure policy. | PSIRT Lead | L |
| VH.6a | Critical | Provide a contact address for reporting vulnerabilities | Implement, document and operate: provide a contact address for reporting vulnerabilities. | PSIRT Lead | L |
| VH.7 | Critical | Provide mechanisms to securely distribute updates so vulnerabilities are fixed in time | Operate update distribution and track installation status per site. | Service Delivery Manager | L |
| VH.8 | Critical | Disseminate available security updates without delay | Implement, document and operate: disseminate available security updates without delay. | PSIRT Lead | L |
| TR2-004 | Critical | Analyse how potentially affected subcomponents are used to decide whether the product is affected, as part of vulnerability handling | Triage every SBOM-based match, record the exploitability decision, and publish product status as CSAF/VEX linked to SBOM component identifiers. | PSIRT Lead | L |
| TR3-007 | Critical | Select the corresponding national CSIRT among those designated as CVD coordinator in the Member State | select the corresponding national CSIRT among those designated as CVD coordinator in the Member State - document it in the PSIRT notification procedure and keep a case log. | PSIRT Lead / Compliance Officer | S |
| TR3-4.3.1a | Critical | Create at least two roles: PSIRT and CSIRT | Establish PSIRT (products, incl. RDPS) and CSIRT (corporate infrastructure) with charter, named members, deputies and management mandate. | CISO / PSIRT Lead | L |
| TR3-4.3.4a | Critical | Create a central web page for vulnerability reporting | Publish the central vulnerability reporting page (contacts, keys, web form, CVD policy link) and link it from the home page. | PSIRT Lead with Web/IT team | M |
| TR3-022 | Critical | The CVD policy must fulfil at least all requirements of section 4.4 | Draft, approve (Legal, management) and publish the CVD policy covering every 4.4.x item; assign an owner and review cycle. | PSIRT Lead (Legal reviews policy wording) | L |
| TR3-4.4.2a | Critical | Notify the corresponding national CSIRT without undue delay of actively exploited vulnerabilities in products or own infrastructure | Implement the actively-exploited-vulnerability notification procedure (awareness criteria, 24h/72h/14-day timeline, single reporting platform account, CSIRT contact, approvals) and rehearse it. | PSIRT Lead / Compliance Officer | L |
| TR1-008 | High | Art. 14 obligations apply to all in-scope products placed on the market before 11 Dec 2027 | Embed 'Art. 14 obligations apply to all in-scope products placed on the market before 11 Dec 2027' in the PSIRT / vulnerability-handling procedure and service-management tooling. | PSIRT Lead / Service Delivery Manager | M |
| TR1-009 | High | Products placed on the market before 11 Dec 2027 fall under the CRA only after a substantial modification after that date | Embed 'products placed on the market before 11 Dec 2027 fall under the CRA only after a substantial modification after that date' in the PSIRT / vulnerability-handling procedure and service-management tooling. | PSIRT Lead / Service Delivery Manager | M |
| TR1-011 | High | A substantial modification exists if type and purpose change in a way not foreseen in the initial risk assessment | Add a substantial-modification check (type/purpose change vs. initial risk assessment) to change management for all installed solutions. | PSIRT Lead / Service Delivery Manager | M |
| TR1-018 | High | Handle vulnerabilities with timely updates during a support period reflecting expected use time (minimum five years) | Plan PSIRT and engineering capacity per supported release line until its support end date. | Service Delivery Manager / PSIRT Lead | M |
| TR1-026 | High | Systematically document and regularly review cybersecurity aspects during the support period | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | M |
| TR1-027 | High | The review includes updating the risk assessment and addressing new risks | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | M |
| TR1-028-c | High | Security updates generally free of charge unless agreed otherwise for tailor-made business products | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | M |
| TR1-029 | High | Post-market obligations must be upheld during the support period based on expected duration of use | Plan PSIRT and engineering capacity per supported release line until its support end date. | Service Delivery Manager / PSIRT Lead | M |
| TR1-031-a | High | Keep security updates available for at least 10 years after placing on the market (or the support period if longer) | Plan PSIRT and engineering capacity per supported release line until its support end date. | Service Delivery Manager / PSIRT Lead | M |
| TR1-034-b | High | The early warning should name the Member States where the product is made available | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-036 | High | The 72-hour notification should include product info, nature of exploit, mitigations and user guidance | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-041-a | High | The incident early warning includes whether unlawful or malicious acts are suspected | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-041-b | High | The incident early warning should name the Member States where the product is available | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-043 | High | The incident notification should include product info, nature, mitigations and user guidance | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-046 | High | Awareness starts when there is a reasonable degree of certainty | Implement the reporting procedure: awareness criteria, 24h / 72h / 14-day (vulnerability) and 24h / 72h / one-month (incident) timelines, platform accounts, templates, approvals and 24/7 escalation; rehearse it. | PSIRT Lead / Compliance Officer | M |
| TR1-051 | High | Report vulnerabilities found in third-party components to their manufacturer or maintainer | Monitor supplier advisories and end-of-life dates; report found vulnerabilities upstream and track responses. | PSIRT Lead | M |
| TR1-066 | High | Part II applies from placing on the market for the entire support period | Plan PSIRT and engineering capacity per supported release line until its support end date. | Service Delivery Manager / PSIRT Lead | M |
| TR1-067 | High | A vulnerability handling process must be in place before placing on the market to avoid known exploitable vulnerabilities | Implement, document and operate: a vulnerability handling process must be in place before placing on the market to avoid known exploitable vulnerabilities. | PSIRT Lead | M |
| TR1-068 | High | Part II requires identifying, addressing and remediating vulnerabilities | Implement, document and operate: Part II requires identifying, addressing and remediating vulnerabilities. | PSIRT Lead | M |
| TR1-072 | High | Cooperate with market surveillance authorities on measures to eliminate risks | Define an authority-request and corrective-action procedure (single point of contact, escalation, recall decision). | Compliance Officer / PSIRT Lead | M |
| TR1-117-b | High | The manufacturer's processes must comply with the essential requirements | Implement, document and operate: the manufacturer's processes must comply with the essential requirements. | PSIRT Lead | M |
| TR1-156 | High | Update the risk assessment as appropriate during the support period | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | M |
| TR1-158 | High | Trigger: a new vulnerability becomes known | Operate SBOM-based continuous vulnerability monitoring, periodic security reviews and remediation for all supported releases. | PSIRT Lead / Product Security Officer | M |
| RH_UPD.1-a | High | Update the risk assessment when the risk context changes | Trigger risk-assessment updates from PSIRT cases and threat intelligence. | Product Security Officer | M |
| RH_UPD.1-b | High | Treat new unaccepted risks | Treat post-market risks via fixes, mitigations or documented acceptance. | Product Security Officer | M |
| ER.1 | High | Be made available without known exploitable vulnerabilities | Check in regression and post-market reviews that updates do not weaken the property. | PSIRT Lead / QA Lead | M |
| ER.4 | High | Ensure vulnerabilities can be addressed through security updates | Operate update distribution and track installation status per site. | Service Delivery Manager | M |
| ER.4c | High | Through notification of available updates to users | Operate update distribution and track installation status per site. | Service Delivery Manager | M |
| ER.9 | High | Protect availability of essential and basic functions, also after an incident | Check in regression and post-market reviews that updates do not weaken the property. | PSIRT Lead / QA Lead | M |
| VH.1a | High | Draw up an SBOM in a commonly used machine-readable format covering at least top-level dependencies | Implement, document and operate: draw up an SBOM in a commonly used machine-readable format covering at least top-level dependencies. | PSIRT Lead | M |
| VH.2a-b | High | Provide security updates separately from functionality updates where technically feasible | Implement, document and operate: provide security updates separately from functionality updates where technically feasible. | PSIRT Lead | M |
| VH.6 | High | Facilitate sharing information about potential vulnerabilities in the product and its third-party components | Implement, document and operate: facilitate sharing information about potential vulnerabilities in the product and its third-party components. | PSIRT Lead | M |
| VH.8a-a | High | Security updates free of charge unless otherwise agreed for tailor-made business products | Implement, document and operate: security updates free of charge unless otherwise agreed for tailor-made business products. | PSIRT Lead | M |
| VH.8a-b | High | Accompany security updates with advisory messages incl. actions to take | Implement, document and operate: accompany security updates with advisory messages incl. actions to take. | PSIRT Lead | M |
| TR2-003 | High | Exchange vulnerability information and impact via security advisories (CSAF) or VEX | Triage every SBOM-based match, record the exploitability decision, and publish product status as CSAF/VEX linked to SBOM component identifiers. | PSIRT Lead | M |
| TR2-005 | High | Compiling an SBOM is mandatory under the CRA | Load every released SBOM into the vulnerability monitoring tool; publish updated/corrected SBOMs with patch releases. | PSIRT Lead | M |
| TR2-006-a | High | The CRA obliges manufacturers to continuously operate a vulnerability handling process | Establish and document the vulnerability handling chain: intake, triage, fix, release, secure distribution, installation tracking. | PSIRT Lead | M |
| TR2-011 | High | Generate a separate SBOM for each software version | Load every released SBOM into the vulnerability monitoring tool; publish updated/corrected SBOMs with patch releases. | PSIRT Lead | M |
| TR2-066 | High | Field 'Other unique identifiers' such as CPE or purl | Use the field in monitoring/matching rules; correct and re-issue SBOMs where the data is wrong. | PSIRT Lead | M |
| TR2-092 | High | Distribute vulnerability information as CSAF (incl. VEX profile) | Triage every SBOM-based match, record the exploitability decision, and publish product status as CSAF/VEX linked to SBOM component identifiers. | PSIRT Lead | M |
| TR3-001 | High | The vulnerability handling process must cover creation, release, secure distribution and installation of updates or other mitigations | Establish and document the vulnerability handling chain: intake, triage, fix, release, secure distribution, installation tracking. | PSIRT Lead | M |
| TR3-003 | High | Prepare holistic internal CVD processes across departments, contact options and channels | Write into the CVD policy / PSIRT procedure and apply in case handling: prepare holistic internal CVD processes across departments, contact options and channels. | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-005 | High | Publish the contact options and the CVD policy for external communication | Implement on the corporate website: publish the contact options and the CVD policy for external communication; include it in the quarterly security.txt/contact check. | PSIRT Lead with Web/IT team | M |
| TR3-006 | High | Publish security advisories on the manufacturer website in CSAF format | publish security advisories on the manufacturer website in CSAF format - define the disclosure workflow, deadlines and approvals. | PSIRT Lead | M |
| TR3-008 | High | Determine the corresponding CSIRT according to CRA Art. 14(7) (main establishment) | determine the corresponding CSIRT according to CRA Art. 14(7) (main establishment) - document it in the PSIRT notification procedure and keep a case log. | PSIRT Lead / Compliance Officer | S |
| TR3-016 | High | Record the implemented measures, all test procedures and all test results | Keep an evidence register: implemented measures, test procedures and test results for the reporting channels. | PSIRT Lead | M |
| TR3-019 | High | Make security-related information easily accessible to the public | Implement on the corporate website: make security-related information easily accessible to the public; include it in the quarterly security.txt/contact check. | PSIRT Lead with Web/IT team | M |
| TR3-4.1.1a | High | Operate a website that publicly provides security-related information about the manufacturer and its products | Implement on the corporate website: operate a website that publicly provides security-related information about the manufacturer and its products; include it in the quarterly security.txt/contact check. | PSIRT Lead with Web/IT team | M |
| TR3-020 | High | Create a security.txt according to RFC 9116 and make it available on the website | Implement on the corporate website: create a security.txt according to RFC 9116 and make it available on the website; include it in the quarterly security.txt/contact check. | PSIRT Lead with Web/IT team | M |
| TR3-021 | High | Organise the response process for vulnerability reports in advance | Set up and document: organise the response process for vulnerability reports in advance. | CISO / PSIRT Lead | M |
| TR3-4.3.1b | High | PSIRT and CSIRT must not be one person; split across several individuals (unless microenterprise) | Set up and document: PSIRT and CSIRT must not be one person; split across several individuals (unless microenterprise). | CISO / PSIRT Lead | M |
| TR3-4.3.1f | High | PSIRT is the first contact and covers vulnerability handling of products and services | Set up and document: PSIRT is the first contact and covers vulnerability handling of products and services. | CISO / PSIRT Lead | M |
| TR3-4.3.1m | High | Provide sufficient resources for absences and to guarantee CVD response times | Set up and document: provide sufficient resources for absences and to guarantee CVD response times. | CISO / PSIRT Lead | M |
| TR3-4.3.3a-a | High | Set up a web form for vulnerability reports as a contact option | Build the report web form with a secure back-end into PSIRT case tooling; no trackers; anonymous submission possible. | PSIRT Lead with Web/IT team | M |
| TR3-4.4.2b-a | High | Inform the CSIRT about all new information, mitigation measures and their schedules | inform the CSIRT about all new information, mitigation measures and their schedules - document it in the PSIRT notification procedure and keep a case log. | PSIRT Lead / Compliance Officer | M |
| TR3-4.4.2b-b | High | Coordinate mitigation measures and schedules with the CSIRT | coordinate mitigation measures and schedules with the CSIRT - document it in the PSIRT notification procedure and keep a case log. | PSIRT Lead / Compliance Officer | M |
| TR3-4.4.4a | High | Treat each incoming report confidentially to the extent permitted by law | Write into the CVD policy / PSIRT procedure and apply in case handling: treat each incoming report confidentially to the extent permitted by law. | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.4c | High | Respond to each report or update within the guaranteed response times | Write into the CVD policy / PSIRT procedure and apply in case handling: respond to each report or update within the guaranteed response times. | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.4d | High | No criminal charges against good-faith reporters who comply with the policy | Write into the CVD policy / PSIRT procedure and apply in case handling: no criminal charges against good-faith reporters who comply with the policy. | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.7g | High | Treat all reports to the best extent and ensure no single analyst can close a report | Write into the CVD policy / PSIRT procedure and apply in case handling: treat all reports to the best extent and ensure no single analyst can close a report. | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.8a-a | High | Give a simple response within five working days (not for anonymous reports) | Write into the CVD policy / PSIRT procedure and apply in case handling: give a simple response within five working days (not for anonymous reports). | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.8b | High | Give detailed feedback after analysis within ten working days (not for anonymous reports) | Write into the CVD policy / PSIRT procedure and apply in case handling: give detailed feedback after analysis within ten working days (not for anonymous reports). | PSIRT Lead (Legal reviews policy wording) | M |
| TR3-4.4.10a-a | High | Publicly disclose validated and verified vulnerabilities within 90 days unless fixed before placing on the market | publicly disclose validated and verified vulnerabilities within 90 days unless fixed before placing on the market - define the disclosure workflow, deadlines and approvals. | PSIRT Lead | M |
