# Executive Summary - CRA / BSI TR-03183 impact on Solution Integration / Build

**Process:** 3. Solution Integration / Build - Assembling own and third-party components, build pipeline, per-release SBOM, hardening, technical documentation, conformity evidence.  
**Basis:** 592 atomic requirements from BSI TR-03183-1 v1.0.0, BSI TR-03183-2 v2.1.0, BSI TR-03183-3 v1.0.0, assessed in `CRA_BSI_Impact_3_Integration_Build.xlsx`.  
**Role:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Date:** 18 Oct 2026 - CRA reporting obligations have applied since 11 Sep 2026; all other obligations apply from 11 Dec 2027.  
**Status:** draft for management review.

## Bottom line

Integration/Build turns development output into a product that may legally be placed on the market (9 Critical, 50 High). For every version it needs a complete technical file (Annex VII), a release gate that proves Annex I Part I conformity and the absence of known exploitable vulnerabilities, the internal-control conformity assessment with EU declaration of conformity and CE marking, and a per-version SBOM. BSI TR-03183-2 raises the SBOM bar well above the CRA minimum.

## Impact at a glance

| Critical | High | Medium | Low | Nil | Total |
|---:|---:|---:|---:|---:|---:|
| 9 | 50 | 97 | 102 | 334 | 592 |

| Source document | Critical | High |
|---|---:|---:|
| BSI TR-03183-1 v1.0.0 | 7 | 37 |
| BSI TR-03183-2 v2.1.0 | 2 | 13 |
| BSI TR-03183-3 v1.0.0 | 0 | 0 |

- **Critical:** Legal non-compliance or market-access risk if not addressed; needs a new capability, tool, role or organisational change.
- **High:** Significant change to an existing process, new deliverables or roles, notable effort or cost.
- **Effort of the Critical/High items** (workbook column Effort): L = 9, M = 50 (S/M/L = small/medium/large).

## Key findings

### 1. Technical file per version

- **What the requirements demand:** Before placing on the market: general description, design/development/production and vulnerability-handling processes, production and monitoring processes, the risk assessment with the Annex I applicability statement, and test reports - available to market surveillance authorities on request.
- **Why it matters for us:** Without a complete technical file the product may not be placed on the market; it is a new deliverable for every version.
- **What we must do:** Create a technical-file template mapped to Annex VII and the TR-1 assessment report and make it a release-gate item.
- **Lead role:** CRA Compliance Manager / Technical Documentation Lead
- **Requirements (15):** Critical: `TR1-022-a`, `TR1-094`; High: `TR1-022-b`, `TR1-071`, `TR1-095`, `TR1-096`, `TR1-097`, `TR1-098`, `TR1-099`, `TR1-145-b`, `TR1-146`, `RH_RT.1.1.2-a`, `RH_RT.1.1.2-b`, `TR1-154-b`, `RH_DOC.1-a`

### 2. Conformity assessment, EU declaration of conformity and CE marking

- **What the requirements demand:** Carry out the conformity assessment (Module A internal control for default-category solutions), draw up the EU declaration of conformity and affix the CE marking - now also for commercially distributed software; Part I conformity must be demonstrated before release.
- **Why it matters for us:** These are new legal documents with a management signatory; software deliveries need a CE-marking method (documentation, website or the product itself).
- **What we must do:** Define the internal-control procedure, EU declaration template, signatory and CE-marking method for software and appliances; block releases without them.
- **Lead role:** CRA Compliance Manager (management signatory)
- **Requirements (9):** Critical: `TR1-024`, `TR1-025-a`; High: `TR1-004`, `TR1-007`, `TR1-025-b`, `TR1-064`, `TR1-065`, `TR1-117-a`, `ER.0`

### 3. Per-version SBOM to BSI TR-03183-2

- **What the requirements demand:** A separate SBOM for every software version, part of the technical documentation and generated from build information: valid CycloneDX >= 1.6 or SPDX >= 3.0.1; executables and archives listed as components; recursive dependency resolution down to the first component outside the scope of delivery; SHA-512 hashes; executable property; CPE or purl identifiers; new versions for altered components and their parents; reproducible builds so hashes identify components unambiguously.
- **Why it matters for us:** The CRA asks only for top-level dependencies; TR-2 goes much further. Package-level scanners do not deliver this, so tooling and pipeline work are needed.
- **What we must do:** Choose and pin the SBOM tool chain, implement build-time SBOM generation with post-processing and validation against TR-2, and start reproducible builds for the main products.
- **Lead role:** Build & Release Manager (DevSecOps)
- **Requirements (18):** Critical: `TR1-022-c`, `VH.1a`, `TR2-005`, `TR2-011`; High: `VH.1`, `TR2-008`, `TR2-013-a`, `TR2-013-b`, `TR2-016`, `TR2-020`, `TR2-039-b`, `TR2-041`, `TR2-048`, `TR2-057-a`, `TR2-059`, `TR2-060`, `TR2-066`, `TR2-104`

### 4. Release security gate and hardening

- **What the requirements demand:** No known exploitable vulnerabilities in release artefacts, secure default configuration, update capability, integrity protection, limited attack surface, exploit mitigation, effective security tests that verify the controls, and only approved third-party components.
- **Why it matters for us:** Each release made available after 11 Dec 2027 must pass these checks; the release gate is where conformity is proven.
- **What we must do:** Add vulnerability scanning, hardening checks, artefact signing and security-test results to the release gate.
- **Lead role:** Build & Release Manager
- **Requirements (10):** Critical: `ER.1`; High: `TR1-021`, `TR1-067`, `RH_RT.1.3-b`, `ER.2`, `ER.4`, `ER.7-a`, `ER.11`, `ER.12`, `VH.3`

### 5. Patch pipeline and user documentation

- **What the requirements demand:** Security updates built without delay and, where technically feasible, separately from feature releases, with secure distribution; Annex II user information per release, guidance on shared risks, and a transparent description of what the customer environment must provide.
- **Why it matters for us:** Patch builds for older versions fail without archived, reproducible build environments; user information is a mandatory release deliverable.
- **What we must do:** Maintain security-only patch branches and archived build environments; create a security-guide template that is produced for every release.
- **Lead role:** Build & Release Manager
- **Requirements (7):** High: `TR1-023-a`, `TR1-028-b`, `RH_RT.1.2.2-b`, `TR1-191`, `VH.2a-a`, `VH.2a-b`, `VH.7`

## Priorities

| When | Actions |
|---|---|
| Now (Q4 2026) | Technical-file template (Annex VII and TR-1 assessment report) and release-gate definition.<br>SBOM tool-chain decision (CycloneDX 1.6 / SPDX 3.0.1) and a pilot pipeline.<br>Vulnerability scanning of release artefacts. |
| By mid-2027 | Per-version SBOM with the TR-2 fields in all pipelines; reproducible builds for the main products.<br>EU declaration template and signatory; security-guide template; security-only patch branches. |
| By 11 Dec 2027 | Every release made available after 11 Dec 2027 has a complete technical file, SBOM, EU declaration of conformity and CE marking. |

## Decisions needed

- SBOM tool chain and target format.
- Who signs the EU declaration of conformity and how CE marking is applied to software.

## Dependencies on other processes

Assembles inputs from 2. Development (risk assessment, tests, components); hands SBOM, documentation, declaration and packages to 4. Deployment; feeds SBOMs and patch builds to 5. Maintenance; archives records for 6. Decommissioning.

## Beyond Critical and High

The 97 Medium items are mostly further SBOM data fields and structure rules (component granularity, level of detail, references to other BOMs, licences), the steps and assessment report of the TR-1 self-assessment procedure, risk-treatment evidence and supplier due diligence.

## Assumptions behind the ratings

Ratings assume that CRA-specific capabilities (product PSIRT, published CVD policy, per-release SBOM pipeline, ENISA reporting procedure, CRA technical file and EU declaration of conformity) do not exist yet; where one already exists, the impact is lower. Solutions are assumed to be in CRA scope (not exclusively for national security or defence, not designed to process classified information, not certified under Regulation (EU) 2018/1139), the company is not a microenterprise, and customer operators are skilled IT/OT professionals. Requirements that BSI TR-03183 adds beyond the CRA are rated on effort and customer expectations. The full list is on the Method sheet of the workbook.

## Annex - all Critical and High items (59)

Requirement texts are short summaries; the verbatim text, rationale and evidence are in the workbook.

| Req ID | Impact | Requirement (summary) | Required change / action | Owner | Effort |
|---|---|---|---|---|---|
| TR1-022-a | Critical | Draw up the technical documentation (Art. 31, Annex VII) demonstrating compliance | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | L |
| TR1-022-c | Critical | The technical documentation must include an SBOM | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | L |
| TR1-024 | Critical | Carry out conformity assessment procedures (self-assessment or notified body) | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | L |
| TR1-025-a | Critical | Draw up an EU declaration of conformity once compliance is demonstrated | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | L |
| TR1-094 | Critical | Draw up technical documentation before placing on the market (Art. 31) | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | L |
| ER.1 | Critical | Be made available without known exploitable vulnerabilities | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | L |
| VH.1a | Critical | Draw up an SBOM in a commonly used machine-readable format covering at least top-level dependencies | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | L |
| TR2-005 | Critical | Compiling an SBOM is mandatory under the CRA | Generate the SBOM at build/link time, validate it against TR-03183-2 and the format schema, and archive one SBOM per software version. | Build & Release Manager (DevSecOps) | L |
| TR2-011 | Critical | Generate a separate SBOM for each software version | Generate the SBOM at build/link time, validate it against TR-03183-2 and the format schema, and archive one SBOM per software version. | Build & Release Manager (DevSecOps) | L |
| TR1-004 | High | Commercially distributed software is now subject to CE marking | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | M |
| TR1-007 | High | From 11 Dec 2027 all in-scope products made available must meet all CRA requirements | Add a pipeline or release-gate check / documentation step for 'from 11 Dec 2027 all in-scope products made available must meet all CRA requirements' and archive the result with the release. | Build & Release Manager / Technical Documentation Lead | M |
| TR1-021 | High | Apply due diligence when integrating third-party components including open source | Verify signatures/checksums of third-party artefacts and pull them only from approved sources. | Build & Release Manager | M |
| TR1-022-b | High | The technical documentation must include the cybersecurity risk assessment | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-023-a | High | Provide Annex II information and instructions incl. single point of contact for vulnerability reporting | Create an Annex II-aligned security-guide template and produce it for every release. | Technical Documentation Lead | M |
| TR1-025-b | High | Affix the CE marking | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | M |
| TR1-028-b | High | Address found vulnerabilities including by providing security updates | Run security patch releases through the same SBOM/documentation gates as full releases. | Build & Release Manager | M |
| TR1-064 | High | Only products meeting Part I may be placed on the market | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | M |
| TR1-065 | High | Part I conformity has to be demonstrated beforehand | Set up the internal-control conformity procedure as a release gate, sign the EU DoC per version and apply the CE marking. | CRA Compliance Manager (management signatory) | M |
| TR1-067 | High | A vulnerability handling process must be in place before placing on the market to avoid known exploitable vulnerabilities | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | M |
| TR1-071 | High | Provide all conformity information and documentation to market surveillance authorities on reasoned request | Keep the technical file of every version retrievable within days, in paper or electronic form, with a request-handling procedure. | CRA Compliance Manager | M |
| TR1-095 | High | General description incl. intended purpose, software versions, Annex II information, hardware photos | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-096 | High | Description of design, development, production and vulnerability handling processes | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-097 | High | Information on production and monitoring processes and their validation | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-098 | High | Cybersecurity risk assessment incl. applicability of Annex I Part I | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-099 | High | Test reports verifying Part I conformity and the vulnerability handling processes (Part II) | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-117-a | High | Products may only be made available if they meet Annex I Part I when properly installed, maintained, used and updated | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | M |
| TR1-145-b | High | Document the applicable Annex I Part I (2) requirements | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| TR1-146 | High | Document and justify why an unaddressed essential requirement is not applicable | Include control verification results in the release evidence. | QA Lead / Build & Release Manager | M |
| RH_RT.1.1.2-a | High | Select and document applicable Annex I Part I (2) requirements based on the selected controls | Include control verification results in the release evidence. | QA Lead / Build & Release Manager | M |
| RH_RT.1.1.2-b | High | Document and justify non-applicable Annex I Part I (2) requirements | Include control verification results in the release evidence. | QA Lead / Build & Release Manager | M |
| RH_RT.1.2.2-b | High | Provide sufficient guidance documenting shared risks and expected user mitigations | Create an Annex II-aligned security-guide template and produce it for every release. | Technical Documentation Lead | M |
| RH_RT.1.3-b | High | Verify effectiveness and correctness of controls in accordance with the risk | Include control verification results in the release evidence. | QA Lead / Build & Release Manager | M |
| TR1-154-b | High | The documented risk assessment shall be included in the technical documentation | Create a technical-file template mapped to Annex VII and the TR-1 assessment report, and assemble it per release as a release-gate item. | CRA Compliance Manager / Technical Documentation Lead | M |
| RH_DOC.1-a | High | Document the risk-assessment results comprehensively | File the current risk assessment with each release. | Technical Documentation Lead | M |
| TR1-191 | High | Delegation includes a transparent description of the expectations and the means to meet them | Create an Annex II-aligned security-guide template and produce it for every release. | Technical Documentation Lead | M |
| ER.0 | High | Products shall ensure an appropriate level of cybersecurity based on the risks | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | M |
| ER.2 | High | Secure-by-default configuration unless otherwise agreed for tailor-made business products | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | M |
| ER.4 | High | Ensure vulnerabilities can be addressed through security updates | Produce signed update packages; keep security patches separate from feature releases. | Build & Release Manager | M |
| ER.7-a | High | Protect integrity of data, commands, programs and configuration against unauthorised modification | Check cryptographic and data-protection defaults in the release gate. | Build & Release Manager | M |
| ER.11 | High | Be designed, developed and produced to limit attack surfaces | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | M |
| ER.12 | High | Reduce incident impact using exploitation mitigation mechanisms | Verify the property in the release pipeline (configuration/hardening checks) and file the evidence. | Build & Release Manager | M |
| VH.1 | High | Identify and document vulnerabilities and components contained in products | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | M |
| VH.2a-a | High | Address and remediate vulnerabilities without delay, incl. security updates | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | M |
| VH.2a-b | High | Provide security updates separately from functionality updates where technically feasible | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | M |
| VH.3 | High | Apply effective and regular security tests and reviews | Provide the pipeline capability (scans, packaging, SBOM, signing) for it. | Build & Release Manager | M |
| VH.7 | High | Provide mechanisms to securely distribute updates so vulnerabilities are fixed in time | Produce signed update packages; keep security patches separate from feature releases. | Build & Release Manager | M |
| TR2-008 | High | An SBOM must contain the minimum information of section 5 | Generate the SBOM at build/link time, validate it against TR-03183-2 and the format schema, and archive one SBOM per software version. | Build & Release Manager (DevSecOps) | M |
| TR2-013-a | High | Any altered component must get a new software version | Generate the SBOM at build/link time, validate it against TR-03183-2 and the format schema, and archive one SBOM per software version. | Build & Release Manager (DevSecOps) | M |
| TR2-013-b | High | For delivery item SBOMs all depending parent components also get a new version | Generate the SBOM at build/link time, validate it against TR-03183-2 and the format schema, and archive one SBOM per software version. | Build & Release Manager (DevSecOps) | M |
| TR2-016 | High | Logical components, executable files and archive files must be represented as components | Implement and test this rule in the SBOM generation/merge step; add sample-based checks to the release gate. | Build & Release Manager (DevSecOps) | M |
| TR2-020 | High | List the component used by the linker, even if alternatives exist | Implement and test this rule in the SBOM generation/merge step; add sample-based checks to the release gate. | Build & Release Manager (DevSecOps) | M |
| TR2-039-b | High | SBOMs must be valid CycloneDX >= 1.6 or SPDX >= 3.0.1 | Pin SBOM generator and schema versions, validate every SBOM against the schema, and track TR-03183-2 versions (six-month transition). | Build & Release Manager (DevSecOps) | M |
| TR2-041 | High | Resolve dependencies recursively on each path down to the first component outside the scope of delivery | Implement and test this rule in the SBOM generation/merge step; add sample-based checks to the release gate. | Build & Release Manager (DevSecOps) | M |
| TR2-048 | High | The SBOM must contain the information available during the build process | Implement and test this rule in the SBOM generation/merge step; add sample-based checks to the release gate. | Build & Release Manager (DevSecOps) | M |
| TR2-057-a | High | Field 'Dependencies on other components' (direct dependencies / contained components) | Configure the SBOM generator/post-processor to fill this field (BSI taxonomy where the format has no native field) and add a validation rule that fails the release when it is missing. | Build & Release Manager (DevSecOps) | M |
| TR2-059 | High | Field 'Hash value of the deployable component' as SHA-512 | Configure the SBOM generator/post-processor to fill this field (BSI taxonomy where the format has no native field) and add a validation rule that fails the release when it is missing. | Build & Release Manager (DevSecOps) | M |
| TR2-060 | High | Field 'Executable property' (executable / non-executable) | Configure the SBOM generator/post-processor to fill this field (BSI taxonomy where the format has no native field) and add a validation rule that fails the release when it is missing. | Build & Release Manager (DevSecOps) | M |
| TR2-066 | High | Field 'Other unique identifiers' such as CPE or purl | Configure the SBOM generator/post-processor to fill this field (BSI taxonomy where the format has no native field) and add a validation rule that fails the release when it is missing. | Build & Release Manager (DevSecOps) | M |
| TR2-104 | High | Employ reproducible builds so hash values identify components unambiguously | Implement the practice in the pipeline and verify it per release (e.g. rebuild-and-compare hashes, signature verification). | Build & Release Manager (DevSecOps) | M |
