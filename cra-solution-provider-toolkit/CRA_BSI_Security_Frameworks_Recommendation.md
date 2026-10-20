# Security Frameworks for Implementing the Key CRA / BSI TR-03183 Requirements

**Context:** solution provider acting as CRA manufacturer; default-category solutions for governments and airports.  
**Basis:** the Critical and High requirements in the six impact workbooks (`CRA_BSI_Impact_1_Presale.xlsx` to `CRA_BSI_Impact_6_Decommissioning.xlsx`) and the six executive summaries (`CRA_BSI_Executive_Summary_*.md`).  
**Date:** 18 Oct 2026. The status of the harmonised standards reflects public information up to July 2026.

## Recommendation in short

Use a small core of frameworks and map everything else to it. For a manufacturer supplying airports and governments, five are recommended:

1. **IEC 62443 as the main security framework for products and services.** The relevant parts are 4-1 (secure development lifecycle), 4-2 (component security requirements), 3-2 and 3-3 (system risk assessment and system requirements) and 2-4 (integration and maintenance service providers).
2. **ISO/IEC 27001 as the management system around it.** It covers governance, suppliers, incidents and records, and government and airport tenders often require it anyway.
3. **ISO/IEC 30111, ISO/IEC 29147, the FIRST PSIRT Services Framework and CSAF for vulnerability handling and disclosure.** TR-03183-3 is built on these: it cites ISO/IEC 30111 and 29147, CSAF (ISO/IEC 20153), ETSI TR 103 838 and RFC 9116.
4. **TR-03183-2 with CycloneDX 1.6 or SPDX 3.0.1, SLSA and OpenChain (ISO/IEC 5230 and 18974) for the supply chain.** These cover the SBOM, build integrity and due diligence on open-source components.
5. **The CRA harmonised standards (EN 40000 series) as the end target.** Only standards cited in the Official Journal of the EU give a presumption of conformity. Status from the most recent public information found:
   - In March 2026, prEN 40000-1-1, -1-2 and -1-3 had finished public enquiry and were in the approval stage.
   - A July 2026 commentary expects -1-3 (vulnerability handling) to be cited first.
   - -1-4 (generic security requirements) is still being drafted.
   - The Commission has moved the 2026 drafting deadlines back by two months.
   - No citation of any of them could be confirmed yet; check the Official Journal before relying on one.

## Why IEC 62443 should be the main framework

- **4-1 matches the Critical items closely:**
  - SR-1 (product security context) covers the risk context (TR1-116).
  - SR-2 (threat model) covers threat identification (RH_RA.1.1.2).
  - SM-9 and SM-10 (externally supplied components) cover due diligence (TR1-021).
  - SVV-1 to SVV-5 cover security testing (VH.3).
  - DM-1 to DM-6 cover vulnerability handling (VH.1 to VH.6).
  - SUM-1 to SUM-5 cover security updates (VH.7, VH.8).
  - SG-2 (defence in depth expected from the environment) covers the operating-environment items (TR1-189 to TR1-191).
  - SG-4 (secure disposal) covers data removal (ER.14).
- **4-2 covers most of Annex I Part I(2).** Its seven foundational requirements are:
  - identification and authentication
  - use control and audit logging
  - integrity
  - confidentiality, including CR 4.2 information persistence (data removal)
  - restricted data flow
  - response to events
  - availability, including DoS protection and least functionality
- **Buyers know it and it can be certified.** Critical-infrastructure customers widely recognise it, and certification is available through ISASecure or IECEE.

For pure web or IT software, add OWASP ASVS for the technical requirements.

## Which framework fits each of the most important requirements

| Requirement area | Best fit | Note |
|---|---|---|
| Art. 14 reporting (applies since 11 Sep 2026) | TR-1 §3.6 directly; ISO/IEC 27035; NIS2 Implementing Regulation (EU) 2024/2690 | No framework has the 24h / 72h / 14-day / one-month workflow. TR-1 itself points to the NIS2 implementing act to define "awareness". |
| PSIRT, CVD policy, reporting channels | ISO/IEC 30111, ISO/IEC 29147, ETSI TR 103 838, FIRST PSIRT Services Framework, RFC 9116 with OpenPGP, CVSS, CSAF 2.0 | The same set TR-3 references |
| Vulnerability handling (Annex I Part II) | IEC 62443-4-1 DM and SUM practices; prEN 40000-1-3 once cited | 40000-1-3 will give the presumption of conformity |
| Risk assessment and applicability statement | TR-1 chapter 5 method (uses ISO 31000 terms), ISO/IEC 27005, IEC 62443-3-2 for OT systems; STRIDE or MITRE ATT&CK for threat modelling | Use one method for all solutions |
| Secure development and testing | IEC 62443-4-1; NIST SSDF (SP 800-218) or BSI TR-03185 as the practice catalogue; OWASP SAMM to measure maturity | TR-03185 is BSI's secure software lifecycle guideline |
| Annex I Part I product requirements | IEC 62443-4-2 for components, 62443-3-3 for systems, OWASP ASVS for web and API, BSI TR-02102 for cryptography | One requirements catalogue per solution type |
| SBOM and supply chain | TR-03183-2, CycloneDX or SPDX, CSAF VEX, SLSA build track and signing, reproducible builds, OpenChain, OpenSSF Scorecard | TR-2 stays the binding target |
| Secure defaults and deployment | CIS Benchmarks or DISA STIGs for hardening; IEC 62443-2-4 for site integration and maintenance | Basis for the installation checklist |
| Technical file, Module A, EU declaration of conformity, CE marking | CRA Annexes V and VII, EU Blue Guide, ISO/IEC 17050-1 | Legal deliverables; no framework replaces them |
| Secure data removal | NIST SP 800-88 or IEEE 2883, IEC 62443-4-2 CR 4.2, IT-Grundschutz CON.6 | For the wipe function and the decommissioning procedure |
| Organisation, suppliers, 10-year records | ISO/IEC 27001 and 27002, ISO/IEC 27036; in Germany, ISO 27001 based on IT-Grundschutz | Also covers what NIS2 customers require of their suppliers |

## What frameworks will not do

- **They don't cover the CRA's commercial and legal items:** the support period, free security updates, ten-year availability, the Art. 14 deadlines, the EU declaration of conformity and CE marking. These come straight from the CRA and TR-1.
- **They give evidence, not a presumption of conformity.** Using IEC 62443, ISO 27001 or the SSDF is not enough on its own. The presumption comes only from harmonised standards cited in the Official Journal, or from a certification scheme the Commission designates. TR-1 mentions EUCC and Common Criteria, but those only pay off if a customer demands certified products.
- **Run one development lifecycle, not three.** Pick 62443-4-1 and use the SSDF, SAMM or TR-03185 only as references mapped onto it.

## Frameworks customers will ask suppliers to follow

- **Airports:** they fall under NIS2, usually as essential entities, and under EASA Part-IS. Their supplier requirements will reference ISO 27001 and IEC 62443.
- **German government:** expect IT-Grundschutz, and C5 for anything hosted in the cloud.
- **Remote maintenance:** if it makes the company a managed service provider, NIS2 may apply to it directly. Worth checking.
- **Radio equipment:** any solution that includes it is already subject to EN 18031-1, -2 and -3 under the Radio Equipment Directive.

## Suggested order

1. **Now:** set up TR-3 with ISO/IEC 30111 and 29147 and the FIRST PSIRT framework, because the reporting duty already applies. Start SBOM tooling to TR-2.
2. **First half of 2027:**
   - run a gap assessment of the development lifecycle against IEC 62443-4-1
   - build a 4-2 / ASVS requirements catalogue per solution type
   - extend the ISO 27001 scope to product security
3. **Once the standards are cited:** map processes and evidence to EN 40000-1-3 first, then to -1-2 and -1-4.

The JRC–ENISA CRA standards mapping (2024) links each Annex I requirement to existing standards and points out the gaps. It is a good starting point for an own mapping.

## Possible next step

Add a column to the six impact workbooks that maps each Critical and High requirement to the matching framework clause.

## Sources

- [CEN-CENELEC "CRA unlocked" webinar slides, March 2026](https://www.cencenelec.eu/media/CEN-CENELEC/Events/Webinars/2026/2026-03-05_cra_unlocked_pt2_stan4cr_slides.pdf)
- [cyberresilienceact.eu – CRA standardisation deadlines pushed back two months](https://www.cyberresilienceact.eu/news/cra-standardisation-deadlines-pushed-back-two-months.html)
- [Compliance & Risks – CRA harmonised standards commentary](https://www.complianceandrisks.com/?p=35186)
- [StandICT – prEN 40000-1-3 Vulnerability handling](https://standict.eu/index.php/standards-repository/cra-sr-m606-pt3-cybersecurity-requirements-products-digital-elements-part-1-3)
- [DIN – prEN 40000 draft page](https://www.din.de/en/getting-involved/standards-committees/nia/drafts/wdc-beuth:din21:398541768)
- [BSI TR-03185 Secure Software Lifecycle](https://www.bsi.bund.de/dok/TR-03185-en)
- [ENISA/JRC – CRA Requirements Standards Mapping](https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping-joint-research-centre-enisa-joint)
