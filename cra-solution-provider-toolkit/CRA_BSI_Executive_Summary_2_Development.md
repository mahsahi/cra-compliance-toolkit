# Executive Summary - CRA / BSI TR-03183 impact on Solution Development

**Process:** 2. Solution Development - Secure design, coding, dependency and component management, SBOM generation, security testing.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_2_Development.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

Development carries the core of the CRA product obligations (14 Critical, 58 High). Every solution needs a documented cybersecurity risk assessment that drives its design, the applicable Annex I essential requirements built in by design, a structured security-testing programme, and documented due diligence for every third-party and open-source component. These must work as systematic, repeatable capabilities before any version is made available after 11 December 2027.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 14 | 58 | 103 | 114 | 303 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 14 | 54 |
| BSI TR-03183-2 v2.1.0 | 0 | 3 |
| BSI TR-03183-3 v1.0.0 | 0 | 1 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 14, M = 58 (S/M/L = small/medium/large).

## Key findings

### 1. A documented risk assessment becomes the basis of every design

- **What the requirements demand:** Per solution: define the risk context, identify assets and threats, analyse likelihood and impact, evaluate the risks against acceptance criteria, document the results comprehensively for the technical documentation and update them when the risk context changes.
- **Why it matters for us:** The risk assessment is a legal prerequisite and the evidence base for the technical file; without one method and template it cannot be produced consistently across solutions.
- **What we must do:** Adopt one risk-assessment method and template (TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2 for airport OT), apply it to every solution and reusable platform component, and train the architects.
- **Lead role:** Security Architect
- **Requirements (16):** Critical: `TR1-108-a`, `RH_RA.1.1.1`, `RH_RA.1.1.2`, `RH_DOC.1-a`; High: `TR1-015`, `TR1-022-b`, `TR1-069`, `TR1-096`, `TR1-098`, `TR1-108-b`, `TR1-116`, `RH_RA.1.2`, `RH_RA.1.3`, `TR1-154-a`, `RH_DOC.1-b`, `RH_UPD.1-a`

### 2. Risk treatment and the Annex I applicability statement

- **What the requirements demand:** Select and implement controls that reduce each risk to an acceptable level; map them to Annex I Part I (2) and justify every requirement treated as not applicable; share risks with suppliers or users only when they are able and obliged to treat them and within the users' foreseeable expectations.
- **Why it matters for us:** The applicability statement is core conformity evidence; its justifications (for example no automatic updates in change-controlled airport environments) must hold up with market surveillance.
- **What we must do:** Build a control catalogue mapped to the essential requirements (ER.x) and an applicability-statement template; record the treatment decision for each risk.
- **Lead role:** Security Architect
- **Requirements (12):** Critical: `RH_RT.1.1.1-a`, `RH_RT.1.1.2-a`, `RH_RT.1.1.2-b`, `RH_RT.1.3-a`; High: `TR1-142`, `RH_RT.1.1.1-b`, `TR1-145-a`, `TR1-146`, `RH_RT.1.2.1`, `RH_RT.1.2.2-a`, `TR1-152`, `RH_UPD.1-b`

### 3. Annex I essential requirements built in by design

- **What the requirements demand:** No known exploitable vulnerabilities at release; secure by default; fixable through security updates (automatic where applicable); access control with authentication/IAM and reporting of possible unauthorised access; encryption and integrity protection; data minimisation; resilience including against DoS; limited attack surface; exploit mitigation; security logging; reset and permanent data removal.
- **Why it matters for us:** Only solutions that meet Annex I Part I may be placed on the market from 11 Dec 2027; gaps in existing solutions need roadmap time now.
- **What we must do:** Define a product security baseline per essential requirement, run a gap analysis per solution and plan gap closure before 11 Dec 2027.
- **Lead role:** Security Architect / Development Lead
- **Requirements (27):** Critical: `ER.0`, `ER.1`, `ER.2`, `ER.4`; High: `TR1-007`, `TR1-013`, `TR1-020`, `TR1-064`, `TR1-070`, `TR1-107`, `TR1-117-a`, `ER.3a`, `ER.4a`, `ER.5`, `ER.5a`, `ER.5b`, `ER.6`, `ER.7-a`, `TR1-192`, `ER.9`, `ER.9a`, `ER.11`, `ER.11a`, `ER.12`, `ER.13`, `ER.13a`, `ER.14-a`

### 4. Security testing and fast vulnerability fixing

- **What the requirements demand:** Effective and regular security testing that verifies the controls; a vulnerability-handling process already before release; fixes without delay; analysis of whether a flagged subcomponent actually affects the product; fixes ready within the TR-3 90-day public-disclosure window; secure update delivery.
- **Why it matters for us:** Security testing is an essential requirement, and fix capacity for all supported release lines decides whether disclosure and patch deadlines can be met.
- **What we must do:** Run SAST and software-composition analysis in CI, DAST and penetration tests per release, keep maintenance branches buildable, and set fix lead-time targets by severity.
- **Lead role:** Development Lead
- **Requirements (10):** Critical: `VH.3`; High: `TR1-028-b`, `TR1-067`, `TR1-099`, `RH_RT.1.3-b`, `VH.1`, `VH.2a-a`, `VH.7`, `TR2-004`, `TR3-4.4.10a-a`

### 5. Third-party components, SBOM hygiene and licences

- **What the requirements demand:** Documented due diligence before integrating commercial and open-source components; an SBOM covering at least the top-level dependencies; a new version for every altered component; SPDX licence identifiers; sharing own fixes of third-party components with their maintainers.
- **Why it matters for us:** Solutions integrate many third-party parts; without an approval process neither the SBOM nor vulnerability monitoring can be trusted.
- **What we must do:** Introduce a component approval process and supplier register, software-composition and licence scanning, a versioning policy and a legally cleared upstream-contribution process.
- **Lead role:** Software Architect / Open Source Program Office
- **Requirements (7):** Critical: `TR1-021`; High: `TR1-052`, `TR1-125-b`, `TR1-147-b`, `VH.1a`, `TR2-013-a`, `TR2-071-a`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Adopt the risk-assessment method and template and pilot it on one or two flagship solutions.<br>Introduce SAST and software-composition analysis in CI and a component approval process.<br>Define the product security baseline per essential requirement (start with secure defaults and updates). |
| By mid-2027 | Risk assessments and applicability statements for every solution to be sold after 11 Dec 2027.<br>Gap-closure roadmap per solution; penetration-test programme; versioning and licence policy. |
| By 11 Dec 2027 | All Critical gaps closed and evidenced in the technical file for every version made available after 11 Dec 2027. |

## Decisions needed

- Risk-assessment method and tooling (one standard for all solutions).
- Budget and roadmap capacity to close essential-requirement gaps before 11 Dec 2027.

## Dependencies on other processes

Takes intended use and operating environment from 1. Presale; delivers the risk assessment, applicability statement, test reports and SBOM inputs to 3. Integration/Build; supplies fixes and impact analysis to 5. Maintenance.

## Beyond Critical and High

The 103 Medium items are mostly risk-method details (risk context, acceptance and decision criteria, treatment and update rules), SBOM licence information, further technical-documentation inputs, operating-environment expectations and security-update design details.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (72)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| TR1-021 | Critical | Apply due diligence when integrating third-party components including open source | Introduce a component approval process with due-diligence criteria and a register of approved components and suppliers. | Software Architect / Open Source Program Office | L |
| TR1-108-a | Critical | Undertake a cybersecurity risk assessment of each product | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | L |
| RH_RA.1.1.1 | Critical | Identify all assets of the product | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | L |
| RH_RA.1.1.2 | Critical | Identify the threats to the assets and the affected components | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | L |
| RH_RT.1.1.1-a | Critical | Select controls that reduce evaluated risks to an acceptable level | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | L |
| RH_RT.1.1.2-a | Critical | Select and document applicable Annex I Part I (2) requirements based on the selected controls | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | L |
| RH_RT.1.1.2-b | Critical | Document and justify non-applicable Annex I Part I (2) requirements | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | L |
| RH_RT.1.3-a | Critical | Implement the selected controls | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | L |
| RH_DOC.1-a | Critical | Document the risk-assessment results comprehensively | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | L |
| ER.0 | Critical | Products shall ensure an appropriate level of cybersecurity based on the risks | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | L |
| ER.1 | Critical | Be made available without known exploitable vulnerabilities | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | L |
| ER.2 | Critical | Secure-by-default configuration unless otherwise agreed for tailor-made business products | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | L |
| ER.4 | Critical | Ensure vulnerabilities can be addressed through security updates | Design and implement the update mechanism with integrity protection, notification and deferral; justify non-applicable parts (e.g. automatic installation in change-controlled sites). | Software Architect | L |
| VH.3 | Critical | Apply effective and regular security tests and reviews | Provide fixes, analysis and test capacity for the vulnerability-handling process. | Development Lead | L |
| TR1-007 | High | From 11 Dec 2027 all in-scope products made available must meet all CRA requirements | Add 'from 11 Dec 2027 all in-scope products made available must meet all CRA requirements' to the secure-design checklist and definition of done; implement and test it. | Development Lead / Security Architect | M |
| TR1-013 | High | Integrate cybersecurity into planning, design, development and maintenance from the outset | Anchor the obligation in the SDL policy: security requirements, threat modelling, secure coding, security testing gates. | Head of Engineering / Security Architect | M |
| TR1-015 | High | Implement the essential requirements based on a risk assessment considering intended purpose and foreseeable use | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| TR1-020 | High | Ensure products meet Annex I based on a per-product risk assessment and treatment | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| TR1-022-b | High | The technical documentation must include the cybersecurity risk assessment | Produce design, risk-assessment and test documents in the agreed templates as part of the definition of done. | Development Lead / Security Architect | M |
| TR1-028-b | High | Address found vulnerabilities including by providing security updates | Reserve engineering capacity for post-market fixes and risk-assessment updates. | Development Lead | M |
| TR1-052 | High | Share own fixes for third-party components with their maintainer, machine-readable where appropriate | Introduce a component approval process with due-diligence criteria and a register of approved components and suppliers. | Software Architect / Open Source Program Office | M |
| TR1-064 | High | Only products meeting Part I may be placed on the market | Deliver evidence per Annex I requirement to the conformity assessment. | Development Lead | M |
| TR1-067 | High | A vulnerability handling process must be in place before placing on the market to avoid known exploitable vulnerabilities | Provide fixes, analysis and test capacity for the vulnerability-handling process. | Development Lead | M |
| TR1-069 | High | Part I (1) requires an appropriate level of cybersecurity based on a risk assessment | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| TR1-070 | High | Part I (2) requirements have to be implemented based on the risk assessment where applicable | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| TR1-096 | High | Description of design, development, production and vulnerability handling processes | Produce design, risk-assessment and test documents in the agreed templates as part of the definition of done. | Development Lead / Security Architect | M |
| TR1-098 | High | Cybersecurity risk assessment incl. applicability of Annex I Part I | Produce design, risk-assessment and test documents in the agreed templates as part of the definition of done. | Development Lead / Security Architect | M |
| TR1-099 | High | Test reports verifying Part I conformity and the vulnerability handling processes (Part II) | Produce design, risk-assessment and test documents in the agreed templates as part of the definition of done. | Development Lead / Security Architect | M |
| TR1-107 | High | Design, develop and produce products per Annex I Part I for an appropriate cybersecurity level based on the risks | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| TR1-108-b | High | Take the risk-assessment outcome into account in planning, design, development, production, delivery and maintenance | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| TR1-116 | High | Define the cybersecurity risk context of the product | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| TR1-117-a | High | Products may only be made available if they meet Annex I Part I when properly installed, maintained, used and updated | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| TR1-125-b | High | Exercise due diligence for integrated third-party components (Art. 13(5)) | Introduce a component approval process with due-diligence criteria and a register of approved components and suppliers. | Software Architect / Open Source Program Office | M |
| RH_RA.1.2 | High | Analyse the risks for likelihood and potential impact | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| RH_RA.1.3 | High | Evaluate whether the analysed risks can be accepted | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| TR1-142 | High | Meet Annex I Part I (1) by designing, developing and producing for an appropriate level of cybersecurity | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| RH_RT.1.1.1-b | High | Include the selected controls in the product design | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| TR1-145-a | High | Meet the applicable Annex I Part I (2) requirements based on the risk assessment | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| TR1-146 | High | Document and justify why an unaddressed essential requirement is not applicable | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| TR1-147-b | High | Exercise due diligence when integrating components | Introduce a component approval process with due-diligence criteria and a register of approved components and suppliers. | Software Architect / Open Source Program Office | M |
| RH_RT.1.2.1 | High | When sharing risks with suppliers, ensure they are obliged/required/able and willing to treat them | Introduce a component approval process with due-diligence criteria and a register of approved components and suppliers. | Software Architect / Open Source Program Office | M |
| RH_RT.1.2.2-a | High | Risks shared with users must be within their foreseeable expectations | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| TR1-152 | High | Controls incorporated into the design have to be implemented | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| RH_RT.1.3-b | High | Verify effectiveness and correctness of controls in accordance with the risk | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| TR1-154-a | High | The risk assessment shall be documented | Produce design, risk-assessment and test documents in the agreed templates as part of the definition of done. | Development Lead / Security Architect | M |
| RH_DOC.1-b | High | The documentation covers risk context, evaluated risks with controls, shared risks and applicable requirements | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| RH_UPD.1-a | High | Update the risk assessment when the risk context changes | Embed this step in a documented risk-assessment method and template (e.g. TR-1 chapter 5, ISO/IEC 27005, IEC 62443-3-2) used for every solution and reusable component. | Security Architect | M |
| RH_UPD.1-b | High | Treat new unaccepted risks | Record the treatment decision per risk (control, sharing, acceptance) and verify the implemented controls. | Security Architect | M |
| ER.3a | High | Including the possibility to reset the product to its original state | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.4a | High | Automatic security updates within an appropriate timeframe enabled by default, where applicable | Design and implement the update mechanism with integrity protection, notification and deferral; justify non-applicable parts (e.g. automatic installation in change-controlled sites). | Software Architect | M |
| ER.5 | High | Ensure protection from unauthorised access by appropriate control mechanisms | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.5a | High | Including authentication, identity or access management systems | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.5b | High | And report on possible unauthorised access | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.6 | High | Protect confidentiality of data at rest and in transit with state-of-the-art encryption | Design, implement and test the protection; record it in the applicability statement. | Security Architect | M |
| ER.7-a | High | Protect integrity of data, commands, programs and configuration against unauthorised modification | Design, implement and test the protection; record it in the applicability statement. | Security Architect | M |
| TR1-192 | High | Process only data adequate, relevant and limited to the intended purpose (data minimisation) | Design, implement and test the protection; record it in the applicability statement. | Security Architect | M |
| ER.9 | High | Protect availability of essential and basic functions, also after an incident | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.9a | High | Including resilience and mitigation measures against denial-of-service attacks | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.11 | High | Be designed, developed and produced to limit attack surfaces | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.11a | High | Including external interfaces | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.12 | High | Reduce incident impact using exploitation mitigation mechanisms | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.13 | High | Provide security information by recording and monitoring relevant internal activity | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.13a | High | Including access to or modification of data, services or functions | Implement the requirement where applicable, record the design decision and test evidence, otherwise justify non-applicability in the applicability statement. | Security Architect / Development Lead | M |
| ER.14-a | High | Provide secure and easy permanent removal of all data and settings | Design, implement and test the protection; record it in the applicability statement. | Security Architect | M |
| VH.1 | High | Identify and document vulnerabilities and components contained in products | Provide fixes, analysis and test capacity for the vulnerability-handling process. | Development Lead | M |
| VH.1a | High | Draw up an SBOM in a commonly used machine-readable format covering at least top-level dependencies | Provide fixes, analysis and test capacity for the vulnerability-handling process. | Development Lead | M |
| VH.2a-a | High | Address and remediate vulnerabilities without delay, incl. security updates | Provide fixes, analysis and test capacity for the vulnerability-handling process. | Development Lead | M |
| VH.7 | High | Provide mechanisms to securely distribute updates so vulnerabilities are fixed in time | Design and implement the update mechanism with integrity protection, notification and deferral; justify non-applicable parts (e.g. automatic installation in change-controlled sites). | Software Architect | M |
| TR2-004 | High | Analyse how potentially affected subcomponents are used to decide whether the product is affected, as part of vulnerability handling | Provide reachability and exploitability analysis for components flagged by monitoring within the triage SLA. | Development Lead / Security Architect | M |
| TR2-013-a | High | Any altered component must get a new software version | Enforce lock files and declared dependencies in all repositories; generate a source SBOM in CI for early checks. | Development Lead | M |
| TR2-071-a | High | Name licences by SPDX licence identifiers or expressions | Introduce licence scanning (SPDX identifiers, ScanCode LicenseDB fallback, LicenseRef- for unknown licences) and a clearing workflow for every new component. | Open Source Compliance Officer / Development Lead | M |
| TR3-4.4.10a-a | High | Publicly disclose validated and verified vulnerabilities within 90 days unless fixed before placing on the market | Set fix lead-time targets by severity that fit inside the 90-day disclosure window. | Development Lead | M |
