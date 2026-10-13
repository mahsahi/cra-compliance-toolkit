# BSI TR-03183 tool coverage: executive summary

Oct 13, 2026 · @Mahmoud SAHI

Of 465 non-informative requirements in BSI TR-03183 Parts 1, 2, 3 and H, the 10 listed tools and processes cover 61 directly; 19 critical gaps sit in CRA Article 14 reporting and vulnerability-handling processes that no tool performs. Figures measure what the tools can contribute, not compliance.

## What was analysed

All four documents were read in full and split into 561 requirement rows, each quoted word for word (or labelled as a summary) with a PDF page and Markdown line reference.

| Document | Version | Mandatory | Conditional | Recommendation | Informative | Externally referenced | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TR-03183-1 General requirements | 1.0.0 | 35 | 5 | 22 | 42 | 73 | 177 |
| TR-03183-2 SBOM | 2.1.0 | 36 | 15 | 18 | 20 | 1 | 90 |
| TR-03183-3 Vulnerability reports | 1.0.0 | 90 | 16 | 50 | 6 | 0 | 162 |
| TR-03183-H Module H | 1.1.0 | 26 | 8 | 16 | 28 | 54 | 132 |
| **Total** |  | **187** | **44** | **106** | **96** | **128** | **561** |

"Externally referenced" rows restate CRA text (for example the Annex I ER and VH requirements) or pull in ISO/IEC 27001, 27002 or ISO 9001 clauses. Each requirement is assessed against 8 lifecycle phases and 10 tools or processes: SonarQube, Nexus IQ, penetration testing, Nessus/Cyberwatch, DPIA, threat/risk analysis, Dependency-Track, Black Duck, Coverity and ZAP/Burp.

## Coverage at a glance

&#91;embedded content: Workbook sheet 3 (Tool Coverage Matrix) · 465 non-informative requirements × 10 tools or processes\]

Conditional coverage depends on add-ons, in-house source code or the product exposing a web or host surface. Combining tools still leaves the organisational TR-3 rules and Article 14 reporting uncovered.

## Main findings

TR-03183-3 is the weakest-covered part: 62 of the 83 requirements with no tool or process mapping are its organisational rules.

| Best coverage of a requirement | Requirements (of 465 non-informative) |
| --- | --- |
| At least one direct mapping | 61 |
| Partial or conditional only | 226 |
| Indirect only | 95 |
| No meaningful tool or process | 83 |

- **Vulnerability intake (TR-3).** PSIRT/CSIRT roles, CVD policy content, case handling and response times need a process, not a scanner. ZAP/Burp and penetration testing check the public pages and the anonymous form only partly; no listed tool validates security.txt fields or its OpenPGP signature.
- **SBOM (TR-2).** No listed tool is documented to produce a conformant SBOM out of the box. CycloneDX 1.6+ or SPDX 3.0.1+ export is unconfirmed, no tool adds BSI's executable/archive/structured properties, Sonatype exports carry a truncated SHA-1 and embed vulnerability data, and Dependency-Track cannot read SPDX. A build-time enrichment step and a validator are needed.
- **Risk method (TR-1, TR-H).** Threat/risk analysis is the strongest process, with 44 direct mappings.
- **Known vulnerabilities.** Nexus IQ, Black Duck and Dependency-Track directly cover "no known exploitable vulnerabilities" (ER.1) and component and vulnerability identification (VH.1).
- **Overlap.** One SBOM generator plus Dependency-Track for monitoring is usually enough. Coverity and SonarQube overlap on static analysis but suit different languages; DAST and penetration testing complement each other.
- **Manual work.** 276 requirements can be assessed mainly by manual or documentary review.

## Critical gaps

19 of the 408 gap rows are critical: CRA obligations that already apply or block market access, and that no listed tool can perform. The rest split into 170 High, 162 Medium and 57 Low.

| Gap area | CRA reference | Workbook rows | What is missing |
| --- | --- | --- | --- |
| Reporting of actively exploited vulnerabilities and severe incidents (24 h early warning, 72 h notification, final reports) via the single reporting platform | Article 14 (applies since 11 Sep 2026) | TR1-004, TR1-019 to TR1-025 | Reporting playbook, 24/7 on-call, platform access, deadline tracking and decision log |
| Public disclosure of fixed vulnerabilities | Annex I Part II (4) | TR1-167, TRH-101 | Advisory process and CSAF tooling |
| CVD policy, sharing of vulnerability information, contact address | Annex I Part II (5)-(6) | TR1-168 to TR1-170, TRH-102 to TRH-104 | Published CVD policy, intake channel, upstream reporting procedure |
| Security updates disseminated without delay, free of charge, with advisory messages | Annex I Part II (8) | TR1-173, TR1-174, TRH-107 | Release timing records, pricing terms, advisory messages to users |

Priority is rule-based (CRA obligation with no coverage = Critical); effort estimates and organisational status are left for the organisation to fill in.

## Completeness and limitations

Every capitalised MUST, SHALL and SHOULD in TR-1 and TR-2 falls inside an extracted row; the remaining keyword hits in TR-3, TR-H and lower-case TR-1 text are definitions, list introductions or informative explanations, each listed with its reason in the workbook.

- **Recovered from the official PDFs.** The Markdown conversions dropped TR-2 Tables 2-6 (the SBOM data fields) and garbled TR-2 Tables 7-12, TR-1's Annex B and risk tables, and TR-H's tables and "fi"/"fl" letter pairs. Each recovered row says so.
- **Not analysable.** TR-1's chapter 7 controls are not in the document (BSI provides them on request). TR-H cites a TR-1 "chapter 8" that does not exist. ISO/IEC 27001, 27002, ISO 9001, TR-03116-4 and the RFCs are referenced but not provided.
- **46 open questions** are flagged, including BSI citation slips and three conflicts with the CRA: TR-3's 90-day disclosure deadline versus the CRA's disclose-after-fix rule, TR-1 calling third-party assessment "voluntary" for class I products, and TR-1's FOSS exclusion wording.
- **Tool capabilities** come from vendor documentation read on 2026-10-13; exact SBOM format versions need confirming against installed releases.
- **Not a compliance verdict.** No organisation's implementation status was assessed; every status reads "TBD". BSI TR-03183 itself gives no presumption of conformity with the CRA.

## Sources

Full detail (requirement register, lifecycle impact, tool matrix, gap plan, evidence mapping and methodology) is in the workbook BSI-TR-03183\_CRA\_Requirements\_SDLC\_Tool\_Coverage.xlsx.

- [BSI TR-03183 Parts 1, 2, 3 and H](https://bsi.bund.de/dok/TR-03183-en): TR-03183-1 v1.0.0, TR-03183-2 v2.1.0, TR-03183-3 v1.0.0, TR-03183-H v1.1.0
- [Dependency-Track documentation](https://docs.dependencytrack.org/)
- [Sonatype Lifecycle: CycloneDX](https://help.sonatype.com/en/cyclonedx.html)
- [SonarQube Advanced Security: viewing dependencies](https://docs.sonarsource.com/sonarqube-server/advanced-security/viewing-dependencies)
- [Black Duck: CycloneDX data fields](https://docs.blackduck.com/r/blackduck/latest/black-duck-documentation/cyclonedx-data-fields.html)
- [Cyberwatch: scan Docker images on a Harbor registry](https://docs.cyberwatch.com/help/en/use_assets/harbor_scan)
