import json

sources_data = {
    "regulations": [
        {
            "instrument": "Regulation (EU) 2024/2847 (Cyber Resilience Act - CRA)",
            "official_title": "Regulation (EU) 2024/2847 of the European Parliament and of the Council of 23 October 2024 on horizontal cybersecurity requirements for products with digital elements and amending Regulations (EU) No 168/2013 and (EU) 2019/1020 and Directive (EU) 2020/1828",
            "citation": "OJ L, 2024/2847, 20.11.2024",
            "entry_into_force": "10 December 2024 (20 days post-publication)",
            "applicability_date": "11 December 2027 (general application); 11 September 2026 (Article 14 reporting LIVE); 11 June 2026 (Chapter IV Notified Bodies)",
            "legal_nature": "Binding EU Regulation (Directly applicable in all EU Member States without national transposition)",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402847",
            "notes": "Primary governing Union regulation establishing horizontal cybersecurity requirements for products with digital elements."
        },
        {
            "instrument": "Corrigendum to Regulation (EU) 2024/2847",
            "official_title": "Corrigendum to Regulation (EU) 2024/2847 of the European Parliament and of the Council on horizontal cybersecurity requirements for products with digital elements",
            "citation": "OJ L, 2024/90782, 05.12.2024",
            "entry_into_force": "Immediate upon publication (05 December 2024)",
            "applicability_date": "Applies retroactively to the date of entry into force of the parent Regulation",
            "legal_nature": "Binding Corrigendum",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202490782",
            "notes": "Corrects statutory cross-references in Article 64(10) regarding administrative fines for economic operators."
        },
        {
            "instrument": "Commission Implementing Regulation (EU) 2025/2392",
            "official_title": "Commission Implementing Regulation (EU) 2025/2392 laying down technical descriptions and specifications for categories of important and critical products with digital elements listed in Annexes III and IV",
            "citation": "OJ L, 2025/2392, 01.12.2025",
            "entry_into_force": "21 December 2025",
            "applicability_date": "11 December 2027 (in line with general application of Annexes III and IV)",
            "legal_nature": "Binding Implementing Act",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202502392",
            "notes": "Provides technical descriptions, functional criteria, and scoping boundaries for Class I and Class II important products."
        },
        {
            "instrument": "Commission Delegated Regulation (EU) 2026/881",
            "official_title": "Commission Delegated Regulation (EU) 2026/881 supplementing Regulation (EU) 2024/2847 by specifying grounds and procedural conditions for delayed dissemination of notifications of actively exploited vulnerabilities",
            "citation": "OJ L, 2026/881, 20.04.2026",
            "entry_into_force": "10 May 2026",
            "applicability_date": "11 September 2026 (in line with Article 14 live enforcement)",
            "legal_nature": "Binding Delegated Act",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202600881",
            "notes": "Governs statutory grounds for withholding or delaying dissemination of actively exploited vulnerability notices on cybersecurity grounds."
        }
    ],
    "guidance": [
        {
            "document": "Commission Guidance on the Application of the Cyber Resilience Act, C(2026) 5252 final",
            "issuing_body": "European Commission (Directorate-General for Communications Networks, Content and Technology - DG CNECT)",
            "publication_date": "27 July 2026",
            "status": "Authoritative Commission Interpretative Notice (Non-binding guidance)",
            "key_topics": "Concepts of placing on market, making available, standalone software, substantial modifications, support period calculation, and remote data processing solutions (RDPS).",
            "url": "https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act"
        },
        {
            "document": "European Commission CRA Implementation FAQs (v13)",
            "issuing_body": "European Commission DG CNECT",
            "publication_date": "03 December 2025 (Regularly updated living document)",
            "status": "Informal Commission Q&A Guidance",
            "key_topics": "Clarifications on open source software stewardship, bespoke/tailor-made software, cloud component boundaries, and transitional provisions.",
            "url": "https://ec.europa.eu/commission/presscorner/detail/en/qanda_22_5555"
        },
        {
            "document": "The 'Blue Guide' on the implementation of EU product rules 2022 (Notice 2022/C 247/01)",
            "issuing_body": "European Commission",
            "publication_date": "29 June 2022 (OJ C 247, pp. 1–151)",
            "status": "Foundational Union Harmonisation Reference Guide",
            "key_topics": "Core concepts of New Legislative Framework (NLF): placing on the market, making available, putting into service, manufacturer, importer, distributor, conformity assessment modules.",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52022XC0629(01)"
        }
    ],
    "standards": [
        {
            "standard_ref": "CEN/CENELEC/ETSI Joint Standardisation Request (M/60x)",
            "title": "Standardisation Request to CEN, CENELEC, and ETSI in support of Regulation (EU) 2024/2847",
            "current_status": "MANDATE ISSUED; DRAFTING IN PROGRESS",
            "verified_harmonised_status": "NOT HARMONISED YET (No standard has been formally cited in the Official Journal of the EU under CRA as of October 2026).",
            "relevance": "European Standardisation Organisations are developing harmonised standards covering Annex I Part I and Part II. Once cited in OJ, compliance confers statutory Presumption of Conformity under Article 24.",
            "notes": "Manufacturers cannot currently claim 'Presumption of Conformity' based on CRA harmonised standards until formal publication in OJEU."
        },
        {
            "standard_ref": "EN 50742:2025 / ETSI EN 303 645 v2.1.1",
            "title": "Cyber Security for Consumer Internet of Things: Baseline Requirements",
            "current_status": "Published European Standard (State of the Art)",
            "verified_harmonised_status": "NOT FORMALLY HARMONISED UNDER CRA (CITED UNDER RED 2014/53/EU DELEGATED ACT ONLY)",
            "relevance": "Serves as state-of-the-art technical baseline for IoT default passwords, vulnerability disclosure, software updates, and interface pruning.",
            "notes": "Strongly informs Annex I compliance for connected hardware products; candidate for future CRA harmonisation."
        },
        {
            "standard_ref": "IEC 62443 Series (IEC 62443-4-1:2018 & IEC 62443-4-2:2019)",
            "title": "Security for Industrial Automation and Control Systems — Secure Product Development Lifecycle & Technical Security Requirements",
            "current_status": "Published International Standard (Global Industrial State of the Art)",
            "verified_harmonised_status": "NOT FORMALLY HARMONISED UNDER CRA",
            "relevance": "Primary benchmark for secure development lifecycle (Part 4-1) and component technical security controls (Part 4-2); directly aligns with CRA Annex I and Annex VII.",
            "notes": "Widely recognized by Notified Bodies as state-of-the-art evidence for industrial products and embedded systems."
        },
        {
            "standard_ref": "ISO/IEC 29147:2018 & ISO/IEC 30111:2019",
            "title": "Information Technology — Security Techniques — Vulnerability Disclosure & Vulnerability Handling Processes",
            "current_status": "Published International Standard",
            "verified_harmonised_status": "NOT FORMALLY HARMONISED UNDER CRA (Explicitly cited in CRA Annex I Part II point (5) recitals as reference)",
            "relevance": "Defines the mandatory structure for Coordinated Vulnerability Disclosure (CVD) policies, external intake channels, and PSIRT triage handling.",
            "notes": "Adherence is practically required to satisfy Annex I Part II point (5) and Article 13(19)."
        },
        {
            "standard_ref": "ISO/IEC 27001:2022 & ISO/IEC 27034:2011",
            "title": "Information Security Management Systems (ISMS) & Application Security Framework",
            "current_status": "Published International Standard",
            "verified_harmonised_status": "NOT FORMALLY HARMONISED UNDER CRA",
            "relevance": "Provides organisational governance baseline for secure development environments, code-signing key management, and corporate security policies.",
            "notes": "ISO 27001 certification provides supporting evidence for Module H (Full Quality Assurance) but does NOT prove product-level conformity."
        },
        {
            "standard_ref": "OWASP SAMM v2.0 & ASVS v4.0.3",
            "title": "OWASP Software Assurance Maturity Model & Application Security Verification Standard",
            "current_status": "Industry Best Practice Framework",
            "verified_harmonised_status": "NOT HARMONISED (Industry Technical Guidance)",
            "relevance": "Provides practical verification criteria and automated security test baselines for web applications, APIs, and Secure SDLC maturity.",
            "notes": "Widely utilized to structure DevSecOps pipelines and verify absence of OWASP Top 10 vulnerabilities."
        }
    ],
    "assumptions": [
        {
            "area": "Product Archetype & Baseline Scope",
            "assumption_text": "The analysis assumes a standard commercial product with digital elements (PDE) placed on the EU single market for commercial distribution, consisting of compiled software, embedded firmware, or networked hardware, along with any integrated Remote Data Processing Solutions (RDPS).",
            "regulatory_basis": "Regulation (EU) 2024/2847, Article 2(1) and Article 3(1).",
            "impact_on_findings": "If the product falls under specific statutory exclusions (medical devices under MDR 2017/745, aviation under 2018/1139, or motor vehicles under 2019/2144), sector-specific Union regulations supersede the CRA."
        },
        {
            "area": "Economic Operator Role",
            "assumption_text": "The target organization acts primarily as the Manufacturer under Article 3(13), designing, engineering, packaging, and marketing the product under its own corporate brand or trademark.",
            "regulatory_basis": "Regulation (EU) 2024/2847, Article 3(13) and Article 13.",
            "impact_on_findings": "If acting strictly as a distributor or value-added reseller without altering product security or branding, obligations shift to Articles 19–20 (verifying CE mark, user instructions, and manufacturer details)."
        },
        {
            "area": "Product Classification Tier",
            "assumption_text": "The baseline product is classified as a 'Default' product with digital elements subject to internal production control (Conformity Assessment Module A) unless its core functionality includes standalone firewalls, operating systems, hypervisors, IAM, or PKI, which triggers Important Class I or Class II classification.",
            "regulatory_basis": "Regulation (EU) 2024/2847, Article 7, Article 32, Annex III; IR (EU) 2025/2392.",
            "impact_on_findings": "If classified as Important Class I or II, third-party Notified Body conformity assessment (Module B+C or Module H) becomes mandatory, introducing 6-12 month auditing lead times and Notified Body fees."
        },
        {
            "area": "Remote Data Processing Solutions (RDPS)",
            "assumption_text": "Cloud backends developed by or under the responsibility of the manufacturer, without which the product cannot perform one of its core functions, are treated as an integral part of the product with digital elements and are fully subject to Annex I requirements.",
            "regulatory_basis": "Regulation (EU) 2024/2847, Article 3(2); Commission Guidance C(2026) 5252, Section 8.",
            "impact_on_findings": "Pure third-party multi-tenant SaaS accessed via standard browsers is excluded, but custom companion cloud APIs are strictly in scope."
        },
        {
            "area": "Tailor-Made Bespoke Software",
            "assumption_text": "Custom software engineered under commercial contracts for single enterprise clients is fully in scope of the CRA, with only two narrow permitted contractual deviations: secure default configurations (Annex I Part I point 2(b)) and free security updates (Annex I Part II point 8) may be contractually tailored under Recital 64.",
            "regulatory_basis": "Regulation (EU) 2024/2847, Recital 64; Blue Guide Section 2.2; Commission Guidance C(2026) 5252 Pt 18.",
            "impact_on_findings": "Bespoke enterprise developers must still produce Annex VII technical documentation, conduct risk assessments, affix CE markings, and comply with Article 14 reporting."
        }
    ],
    "uncertainties": [
        {
            "issue": "Substantial Modification Thresholds for Iterative Agile Releases",
            "description": "Determining exactly when continuous CI/CD sprint releases, architectural microservice refactors, or major functional version bumps cross the statutory threshold of a 'substantial modification' under Article 3(30), requiring a formal new placing on the market and updated conformity assessment.",
            "recommended_action": "Establish an internal Change Advisory Board (CAB) regulatory screening checklist aligned with Commission Guidance C(2026) 5252 (Points 110–132); consult Legal Counsel and Notified Body for edge cases."
        },
        {
            "issue": "Notified Body Capacity Bottlenecks across the European Union",
            "description": "With Chapter IV taking effect on 11 June 2026, the number of accredited Notified Bodies for CRA Important Class I and Class II products remains severely constrained across Member States, creating severe audit scheduling bottlenecks ahead of December 2027.",
            "recommended_action": "Initiate preliminary Notified Body procurement inquiries immediately (Q4 2026 / Q1 2027) if product functionality touches Annex III categories."
        },
        {
            "issue": "Interplay Between Article 14 Reporting and National Whistleblower / Defense Carve-Outs",
            "description": "Member State national CSIRTs and judicial authorities may issue divergent instructions regarding delayed dissemination or coordination when an actively exploited vulnerability impacts critical infrastructure under NIS2 Directive (EU) 2022/2555.",
            "recommended_action": "Adhere strictly to the designated CSIRT coordinator hierarchy in Article 14(7) and file delayed dissemination requests formally through the ENISA Single Reporting Platform under Delegated Regulation (EU) 2026/881."
        },
        {
            "issue": "Open Source Software Steward Liability vs Commercial Integrator Liability",
            "description": "While open-source software stewards face lighter regulatory burdens under Article 24, commercial manufacturers integrating open-source libraries into commercial products retain strict, unmitigated legal liability for all vulnerabilities under Article 13(5).",
            "recommended_action": "Never rely on upstream open-source maintainers for CRA compliance; enforce rigorous internal automated SCA scanning (Black Duck/Nexus IQ), continuous SBOM tracking (Dependency-Track), and independent patch backporting capacity."
        }
    ],
    "review_metadata": {
        "date_of_review": "October 2026",
        "regulatory_status": "Article 14 reporting LIVE since 11 September 2026; Annex I and general application mandatory from 11 December 2027.",
        "author": "Principal Product Security Architect & Regulatory Compliance Counsel"
    }
}

with open('sources_data.json', 'w') as f:
    json.dump(sources_data, f, indent=2)

print("Sources data saved successfully.")
