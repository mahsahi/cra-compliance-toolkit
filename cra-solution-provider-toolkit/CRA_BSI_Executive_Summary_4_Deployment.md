# Executive Summary - CRA / BSI TR-03183 impact on Solution Deployment

**Process:** 4. Solution Deployment - Delivery and installation at the customer, secure default configuration, user and security instructions, update mechanism, handover of SBOM and documentation.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_4_Deployment.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

From 11 December 2027 every solution handed over to a customer must be conformant as installed (1 Critical, 17 High). Deployment must deliver a secure-by-default, fully patched installation with the Annex II information and CE marking, agree who provides which part of the operating environment, and put every site on a secure update path - usually inside segregated airport or government networks under customer change control.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 1 | 17 | 44 | 53 | 477 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 1 | 16 |
| BSI TR-03183-2 v2.1.0 | 0 | 0 |
| BSI TR-03183-3 v1.0.0 | 0 | 1 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 1, M = 17 (S/M/L = small/medium/large).

## Key findings

### 1. Secure-by-default, fully patched installations

- **What the requirements demand:** The solution is made available without known exploitable vulnerabilities and with a secure default configuration (deviations only when agreed for a tailor-made product); it must meet Annex I Part I when properly installed, protect against unauthorised access, encrypt data at rest and in transit and keep essential functions available.
- **Why it matters for us:** Installing outdated images or accepting insecure settings requested on site would make the delivered solution non-conformant.
- **What we must do:** Create a secure installation and commissioning checklist (current patched versions, unique credentials and IAM integration, keys, certificates and TLS, high-availability and recovery set-up where needed) and a documented deviation process.
- **Lead role:** Deployment Manager
- **Requirements (6):** Critical: `ER.2`; High: `TR1-117-a`, `ER.1`, `ER.5`, `ER.6`, `ER.9`

### 2. Handover package: Annex II information, security guidance and CE marking

- **What the requirements demand:** Every delivery comes with the Annex II information and instructions (including the single point of contact for vulnerability reports), guidance on shared risks and the mitigations expected from operators, and the CE marking.
- **Why it matters for us:** This is a mandatory part of making the product available, and it defines what the customer's operators are responsible for.
- **What we must do:** Define a standard handover package and have the customer confirm its receipt.
- **Lead role:** Deployment Manager
- **Requirements (4):** High: `TR1-023-a`, `TR1-023-b`, `TR1-025-b`, `RH_RT.1.2.2-b`

### 3. Shared responsibility for the operating environment

- **What the requirements demand:** Provide the environment that the integrated components expect (for example hardened OS, network segmentation, physical protection) in full, or delegate it to the customer with a transparent description of the expectations and the means to meet them.
- **Why it matters for us:** At airports and in government the customer's IT often runs the platform; unclear delegation leaves gaps that fall back on the manufacturer.
- **What we must do:** Record the environment split per site in the statement of work and the handover documentation.
- **Lead role:** Deployment Manager
- **Requirements (3):** High: `TR1-189-a`, `TR1-190`, `TR1-191`

### 4. Updates and patches reaching the sites

- **What the requirements demand:** Vulnerabilities must be fixable through security updates; updates are distributed securely and disseminated without delay; the vulnerability-handling process covers the installation of updates at the sites.
- **Why it matters for us:** Segregated networks and change windows make field roll-out the bottleneck of every patch timeline.
- **What we must do:** Define remote and offline update procedures, align them with customer change windows and plan field-service capacity.
- **Lead role:** Deployment Manager
- **Requirements (5):** High: `ER.4`, `VH.2a-a`, `VH.7`, `VH.8`, `TR3-001`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Build the installed-base register (customer, site, Member State, installed version) - also needed for the reporting duty that has applied since 11 Sep 2026.<br>Draft the secure installation checklist and the deviation process. |
| By mid-2027 | Standard handover package (Annex II information, security guidance, shared risks, declaration and CE).<br>Update roll-out procedures for online and segregated sites. |
| By 11 Dec 2027 | All installations after 11 Dec 2027 are conformant, secure by default and on a secure update path. |

## Decisions needed

- Field-service capacity and process for patch roll-out under customer change control.

## Dependencies on other processes

Receives releases, SBOM, documentation and the EU declaration of conformity from 3. Integration/Build; carries out commitments made in 1. Presale; provides installed-base data and patch roll-out for 5. Maintenance.

## Beyond Critical and High

The 44 Medium items include handing over the EU declaration of conformity and transparency information, site data that supports Art. 14 reporting on vulnerabilities and incidents, shared-risk guidance for operators, access-control and attack-surface settings at installation, and screening of site changes for substantial modification.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (18)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| ER.2 | Critical | Secure-by-default configuration unless otherwise agreed for tailor-made business products | Configure and verify the property during commissioning; document any customer-requested deviation. | Deployment Manager | L |
| TR1-023-a | High | Provide Annex II information and instructions incl. single point of contact for vulnerability reporting | Hand over the security guide / Annex II information with every delivery and record receipt. | Deployment Manager | M |
| TR1-023-b | High | The product must be accompanied by the Annex II information (paper or electronic) | Hand over the security guide / Annex II information with every delivery and record receipt. | Deployment Manager | M |
| TR1-025-b | High | Affix the CE marking | Check CE marking and EU DoC availability at handover. | Deployment Manager | M |
| TR1-117-a | High | Products may only be made available if they meet Annex I Part I when properly installed, maintained, used and updated | Configure and verify the property during commissioning; document any customer-requested deviation. | Deployment Manager | M |
| RH_RT.1.2.2-b | High | Provide sufficient guidance documenting shared risks and expected user mitigations | Hand over the security guide / Annex II information with every delivery and record receipt. | Deployment Manager | M |
| TR1-189-a | High | Provide the environment expected by integrated components in full | Brief the operator on shared risks and required mitigations at handover. | Deployment Manager | M |
| TR1-190 | High | When delegating, enable the next user to meet the expectations | Hand over the security guide / Annex II information with every delivery and record receipt. | Deployment Manager | M |
| TR1-191 | High | Delegation includes a transparent description of the expectations and the means to meet them | Hand over the security guide / Annex II information with every delivery and record receipt. | Deployment Manager | M |
| ER.1 | High | Be made available without known exploitable vulnerabilities | Configure and verify the property during commissioning; document any customer-requested deviation. | Deployment Manager | M |
| ER.4 | High | Ensure vulnerabilities can be addressed through security updates | Configure the update channel (online/offline), notification and deferral per site policy at commissioning. | Deployment Manager | M |
| ER.5 | High | Ensure protection from unauthorised access by appropriate control mechanisms | Configure and verify the property during commissioning; document any customer-requested deviation. | Deployment Manager | M |
| ER.6 | High | Protect confidentiality of data at rest and in transit with state-of-the-art encryption | Set up site keys/certificates and data-retention settings at commissioning and record them. | Deployment Manager | M |
| ER.9 | High | Protect availability of essential and basic functions, also after an incident | Configure and verify the property during commissioning; document any customer-requested deviation. | Deployment Manager | M |
| VH.2a-a | High | Address and remediate vulnerabilities without delay, incl. security updates | Apply the resulting updates/instructions at customer sites. | Field Service Manager | M |
| VH.7 | High | Provide mechanisms to securely distribute updates so vulnerabilities are fixed in time | Configure the update channel (online/offline), notification and deferral per site policy at commissioning. | Deployment Manager | M |
| VH.8 | High | Disseminate available security updates without delay | Apply the resulting updates/instructions at customer sites. | Field Service Manager | M |
| TR3-001 | High | The vulnerability handling process must cover creation, release, secure distribution and installation of updates or other mitigations | Define remote and offline update procedures aligned with customer change windows. | Deployment / Field Service Manager | M |
