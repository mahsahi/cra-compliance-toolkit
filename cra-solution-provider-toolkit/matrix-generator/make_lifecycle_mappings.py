import json

lifecycle_mappings = [
    # PHASE 1: PRESALES AND PRODUCT PLANNING
    {
        "cra_ref": "Art 2(1), Art 3(1), Art 3(12)–(17)",
        "phase": "Presales and Product Planning",
        "action": "Execute CRA Statutory Scope and Economic Operator Role Assessment",
        "role": "Presales Lead, Solution Architect, Legal Counsel",
        "tool_process": "Statutory Applicability Questionnaire & Decision Tree",
        "input_output": "Input: Product concept, deployment topology, contractual delivery model. Output: Formal Scope Determination Record & Economic Operator Role Classification (Manufacturer vs Integrator vs Distributor).",
        "evidence": "Signed Scope & Role Determination Record (02-scope-decision.json / PDF)",
        "gate": "Presales Gate 0: Bid submission or project charter freeze blocked until CRA role is formally identified."
    },
    {
        "cra_ref": "Art 7, Art 8; Annexes III, IV; IR (EU) 2025/2392",
        "phase": "Presales and Product Planning",
        "action": "Classify Product into Default, Important Class I/II, or Critical Category",
        "role": "Lead Product Security Architect, Compliance Officer",
        "tool_process": "CRA Product Classification Matrix & IR 2025/2392 Technical Analysis",
        "input_output": "Input: Core functionality, operating environment, network integration specs. Output: Product Tier Classification Record and Conformity Route Selection (Module A vs B+C vs H).",
        "evidence": "Product Classification Decision Dossier; Notified Body Engagement Strategy (if Class I/II)",
        "gate": "Architecture Gate 1: Solution design freeze blocked if Notified Body budget and timeline are not provisioned for Class I/II."
    },
    {
        "cra_ref": "Art 13(8); Annex II, point 8; Guidance Pt 133",
        "phase": "Presales and Product Planning",
        "action": "Determine and Contractually Commit to Guaranteed Product Security Support Period",
        "role": "Business Unit VP, Product Manager, Finance Lead",
        "tool_process": "Multi-Year Engineering Sustaining Cost Model & Product Lifecycle Policy",
        "input_output": "Input: Customer expected operational lifetime, hardware component lifecycle. Output: Formal Support Period Statement (minimum 5 years unless shorter lifetime justified) and Sustaining Budget Model.",
        "evidence": "Executive Support Period Determination Statement; Multi-Year Maintenance Budget Plan",
        "gate": "Commercial Gate: Contract signature or proposal delivery blocked without explicit calendar support period commitment."
    },
    {
        "cra_ref": "Art 13(2), Annex II point 1; Guidance Pt 139",
        "phase": "Presales and Product Planning",
        "action": "Gating and Alignment of Marketing Claims, Tender Responses, and Intended Purpose",
        "role": "Product Marketing Lead, Presales Architect, Legal Counsel",
        "tool_process": "Marketing Claims Review Checklist & Intended Use Definition SOP",
        "input_output": "Input: Marketing collateral, technical datasheets, RFP responses. Output: Approved Datasheet & Contractual Scope of Intended Purpose preventing unintended category escalation.",
        "evidence": "Approved Product Datasheet; Legal Marketing Review Sign-off Record",
        "gate": "Presales Gate 1: Public brochure publication or RFP submission blocked until claims match tested intended use."
    },
    {
        "cra_ref": "Art 13(5); Recitals 33–36",
        "phase": "Presales and Product Planning",
        "action": "Presales Cybersecurity Screening of Commercial Off-the-Shelf (COTS) and Open-Source Components",
        "role": "Procurement Lead, Lead Solution Architect",
        "tool_process": "Vendor Due Diligence Questionnaire & Open-Source Health Evaluation (OpenSSF)",
        "input_output": "Input: Proposed third-party hardware, software libraries, and SaaS modules. Output: Vendor CRA Readiness Evaluation & Approved Component Selection Matrix.",
        "evidence": "Vendor Cybersecurity Due Diligence Assessment Dossier; Open-Source Selection Log",
        "gate": "Procurement Gate: Third-party component procurement blocked if vendor lacks CE mark or CRA support commitments."
    },
    {
        "cra_ref": "Art 13(2)–(4); Annex I Part I point (1)",
        "phase": "Presales and Product Planning",
        "action": "Establish Initial Concept Cybersecurity Risk Assessment and Security Objectives",
        "role": "Lead Security Architect, Systems Engineer",
        "tool_process": "Threat Analysis and Risk Analysis (TARA) Concept Phase (STRIDE / PASTA)",
        "input_output": "Input: High-level solution topology, data flow diagrams, asset register. Output: Initial Cybersecurity Risk Register and Baseline Security Requirements Specification.",
        "evidence": "Concept Phase Cybersecurity Risk Assessment Document; High-Level Threat Model",
        "gate": "Planning Gate: Transition to detailed engineering blocked without approved Concept Risk Assessment."
    },

    # PHASE 2: DEVELOPMENT
    {
        "cra_ref": "Art 13(2)–(4); Annex VII point 1(b)",
        "phase": "Development",
        "action": "Conduct Comprehensive Threat Modeling and Living Cybersecurity Risk Assessment",
        "role": "Lead Security Architect, Product Security Engineer",
        "tool_process": "Threat Analysis and Risk Analysis (TARA) (IriusRisk / Threat Dragon / STRIDE)",
        "input_output": "Input: Detailed microservice architecture, API interfaces, network protocols. Output: Detailed Threat Model, Attack Trees, and Security Requirements Backlog.",
        "evidence": "Annex VII Cybersecurity Risk Assessment Dossier; Threat Model Architecture Schemas; Security Epics in Jira",
        "gate": "Design Review Gate: Detailed design approval blocked until all identified threat vectors have mapped security user stories."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(d)",
        "phase": "Development",
        "action": "Implement Robust Identity, Authentication, and Role-Based Access Controls (IAM)",
        "role": "Backend Engineer, IAM Architect",
        "tool_process": "Centralized IAM Framework (OAuth 2.0 / OIDC), Coverity, SonarQube",
        "input_output": "Input: Identity requirements, RBAC specifications. Output: Enforced authentication middleware, Argon2 password hashing, short-lived tokens, RBAC guards.",
        "evidence": "IAM Implementation Architecture; Unit & Integration Auth Test Suites; SAST Auth Scan Clean Report",
        "gate": "Sprint Review Gate: PR merge blocked if API route lacks authenticated context or authorization checks."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(e), (2)(f)",
        "phase": "Development",
        "action": "Implement Cryptographic Protections for Data Confidentiality and Integrity",
        "role": "Cryptographic Engineer, Platform Developer",
        "tool_process": "Standard Crypto Libraries (OpenSSL FIPS, libsodium), Coverity, SonarQube",
        "input_output": "Input: Data classification matrix, sensitive data flows. Output: TLS 1.3 enforced transport, AES-256-GCM / ChaCha20 encryption at rest, KMS key management.",
        "evidence": "Cryptographic Architecture & Key Management Plan; SAST Secret & Cryptography Scan Reports",
        "gate": "Static Analysis Gate: Zero hardcoded secrets, zero ECB mode, zero deprecated ciphers allowed in codebase."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(g)",
        "phase": "Development",
        "action": "Execute Data Protection Impact Assessment (DPIA) and Implement Data Minimisation",
        "role": "Data Protection Officer (DPO), Lead Software Architect",
        "tool_process": "Data Protection Impact Assessment (DPIA) Process & Privacy Schema Reviews",
        "input_output": "Input: User data ingestion points, telemetry payloads. Output: Formally approved DPIA dossier, telemetry opt-out switches, automated data pruning routines.",
        "evidence": "Approved DPIA Assessment Dossier; GDPR Art 30 Register; Telemetry Configuration Spec",
        "gate": "Privacy Gate: Product release blocked without DPO approval and verifiable telemetry opt-out mechanism."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(b)",
        "phase": "Development",
        "action": "Engineer Secure Default Configurations and Factory Reset Mechanics",
        "role": "Firmware Engineer, Systems Architect",
        "tool_process": "CIS Benchmark Hardening Scripts, Nessus / Cyberwatch, Unit Testing",
        "input_output": "Input: System services list, configuration templates. Output: Hardened default OS/firmware images, zero default passwords, automated factory reset routine.",
        "evidence": "Hardening Automation Scripts (Ansible); Factory Reset Test Verification Record",
        "gate": "Hardening Gate: Default build must boot with zero open unneeded ports and enforce credential change on first boot."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(j)",
        "phase": "Development",
        "action": "Prune External Interfaces and Reduce Software/Hardware Attack Surfaces",
        "role": "Systems Engineer, Embedded Lead",
        "tool_process": "TARA, Port Scanning (Nmap/Nessus), Distroless Base Containers",
        "input_output": "Input: System port and interface inventory. Output: Minimal container images, disabled JTAG/UART/debug shells, stripped debug symbols.",
        "evidence": "Interface & Port Baseline Inventory; Build Compiler Hardening Specification",
        "gate": "Interface Gate: Presence of undocumented listening ports or active debug interfaces breaks release build."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(k)",
        "phase": "Development",
        "action": "Implement Exploit Mitigations and Memory Safety Protections in Code",
        "role": "Senior Software Engineer, Platform Lead",
        "tool_process": "Coverity Deep Static Analysis, Compiler Hardening Flags (`checksec`)",
        "input_output": "Input: C/C++/Java/Go source code. Output: Memory-safe code constructs, compiled binaries with ASLR, DEP, Stack Canaries, and RELRO enabled.",
        "evidence": "`checksec` Binary Hardening Verification Report; Coverity Zero-Critical-Defect Scan Log",
        "gate": "Compiler Security Gate: All release binaries must achieve 100% compliance on ASLR, NX, Stack Canary, and Full RELRO."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(h)",
        "phase": "Development",
        "action": "Architect Denial-of-Service Resilience and Rate-Limiting Controls",
        "role": "Backend Architect, Infrastructure Lead",
        "tool_process": "API Gateway Throttling, OWASP ZAP, Locust / k6 Stress Testing",
        "input_output": "Input: Expected transaction traffic patterns. Output: Token-bucket rate limiting, request size limits, connection timeouts, circuit breakers.",
        "evidence": "DoS Resilience Design Spec; Stress & Rate-Limiting Automated Test Reports",
        "gate": "Resilience Gate: Simulated traffic flood at 5x normal peak must degrade gracefully without crashing core daemon."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(l)",
        "phase": "Development",
        "action": "Implement Standardized Security Event Logging and Audit Subsystem",
        "role": "Security Engineer, Backend Developer",
        "tool_process": "Structured Logging Framework, SonarQube, Coverity",
        "input_output": "Input: Security event taxonomy (auth, privilege, config changes). Output: Tamper-resistant, timestamped audit logs with log sanitization filtering.",
        "evidence": "Security Logging Specification; Unit Tests Verifying PII/Secret Scrubbing from Logs",
        "gate": "Audit Gate: Automated tests verify zero passwords/keys written to logs and 100% of auth failures produce audit events."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(m)",
        "phase": "Development",
        "action": "Implement Cryptographic Data Sanitization and Decommissioning Capabilities",
        "role": "Firmware Engineer, Cloud Architect",
        "tool_process": "NIST SP 800-88 Sanitization Automation, Cryptographic Erasure Modules",
        "input_output": "Input: Storage medium architecture, cloud tenant structures. Output: Cryptographic wipe mechanism scrubbing encryption keys and de-registering cloud services.",
        "evidence": "Data Sanitization Architecture; NIST SP 800-88 Wipe Verification Test Report",
        "gate": "Decommissioning Gate: Post-wipe forensic block scan verifies zero recoverable user data or keys."
    },
    {
        "cra_ref": "Annex I, Part II, point (5), (6); Art 13(19)",
        "phase": "Development",
        "action": "Establish Coordinated Vulnerability Disclosure (CVD) Policy and Intake Channels",
        "role": "CISO, PSIRT Lead, Legal Counsel",
        "tool_process": "ISO/IEC 29147 CVD Framework & RFC 9116 `security.txt` Deployment",
        "input_output": "Input: Organizational contact channels, PGP keys. Output: Published CVD policy document, public `security.txt` file, monitored `security@` inbox.",
        "evidence": "Approved CVD Policy Document; Deployed `security.txt` File URL; Public PGP Key in Registry",
        "gate": "Governance Gate: Placing on market blocked without live, verified vulnerability intake channel."
    },
    {
        "cra_ref": "Annex I, Part II, point (8); Art 13(10)",
        "phase": "Development",
        "action": "Architect Release Branching for Free Security Updates and Feature Decoupling",
        "role": "Release Engineering Lead, Lead Architect",
        "tool_process": "Git Dual-Track Branching Model (LTS Security vs Feature Branches)",
        "input_output": "Input: Product release roadmap. Output: Independent maintenance branches allowing isolated backporting of security patches without bundling paid features.",
        "evidence": "Release Branching Strategy Spec; CI/CD Multi-Branch Automated Build Configuration",
        "gate": "Branching Gate: Verify security patches compile and release from LTS branch without incorporating feature branch deltas."
    },

    # PHASE 3: BUILD AND RELEASE
    {
        "cra_ref": "Annex I, Part II, point (1); Art 13(24)",
        "phase": "Build and Release",
        "action": "Automate Machine-Readable SBOM Generation in CI/CD Pipeline",
        "role": "DevSecOps Lead, Release Manager",
        "tool_process": "Black Duck Detect, Nexus IQ CLM, cdxgen / Syft, Dependency-Track",
        "input_output": "Input: Compiled build artifacts, package lockfiles, container images. Output: Cryptographically signed CycloneDX / SPDX machine-readable SBOM files.",
        "evidence": "Generated SBOM Files (CycloneDX JSON / SPDX XML); CI/CD SBOM Generation Build Logs",
        "gate": "Build Gate 1: CI/CD build fails if machine-readable SBOM is missing, invalid, or fails schema validation."
    },
    {
        "cra_ref": "Art 13(5); Annex I Part I point (2)(a)",
        "phase": "Build and Release",
        "action": "Execute Automated Software Composition Analysis (SCA) Quality Gate",
        "role": "DevSecOps Engineer, Security QA",
        "tool_process": "Nexus IQ Lifecycle / Black Duck / Dependency-Track",
        "input_output": "Input: Build dependencies. Output: Component vulnerability and license compliance report with automated pass/fail decision.",
        "evidence": "SCA Policy Compliance Scan Report; Dependency License Audit Report",
        "gate": "Build Gate 2: CI/CD pipeline breaks on any Critical/High known CVE in dependencies lacking approved VEX justification."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(a); Annex I Part II point (3)",
        "phase": "Build and Release",
        "action": "Execute Automated Static Code Security Analysis (SAST) Quality Gate",
        "role": "DevSecOps Engineer, Lead Developer",
        "tool_process": "Coverity Deep SAST, SonarQube Enterprise",
        "input_output": "Input: Application source code. Output: SAST defect scan report and Quality Gate status.",
        "evidence": "SonarQube Quality Gate Status Record; Coverity Pre-Release Defect Audit Report",
        "gate": "Build Gate 3: Pull request merge and build artifact promotion blocked on any unresolved Critical SAST security defect."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(a), (2)(f); Annex VII",
        "phase": "Build and Release",
        "action": "Enforce Cryptographic Code Signing and Build Pipeline Integrity (SLSA)",
        "role": "DevSecOps Lead, Platform Security Lead",
        "tool_process": "Hardware HSM Code Signing, Sigstore / Cosign, SLSA Provenance",
        "input_output": "Input: Compiled release binaries, container images, SBOMs. Output: Cryptographically signed artifacts and signed in-toto SLSA provenance metadata.",
        "evidence": "Artifact Cryptographic Signatures (.sig); HSM Signing Audit Logs; SLSA Provenance Attestations",
        "gate": "Release Gate 1: Release artifact staging blocked if binary signature or SLSA provenance attestation fails verification."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(b), (2)(j); Annex I Part II point (3)",
        "phase": "Build and Release",
        "action": "Conduct Automated Container Image and OS Hardening Vulnerability Scans",
        "role": "DevSecOps Engineer, Infrastructure Security Lead",
        "tool_process": "Nessus / Cyberwatch, Trivy, CIS Benchmark Audit Scripts",
        "input_output": "Input: Release container images, appliance virtual disks. Output: Image vulnerability and configuration compliance report.",
        "evidence": "Container Image Scan Report; CIS Benchmark Compliance Audit Scorecard",
        "gate": "Release Gate 2: Promotion blocked on any OS/container Critical CVE or CIS Benchmark hardening score below 90%."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(a), (2)(d); Annex I Part II point (3)",
        "phase": "Build and Release",
        "action": "Execute Automated Dynamic Application Security Testing (DAST) on Staging Target",
        "role": "Security QA Engineer, DevSecOps Lead",
        "tool_process": "OWASP ZAP / Burp Suite Enterprise (Automated API / Web Scans)",
        "input_output": "Input: Deployed staging environment, OpenAPI specs. Output: Dynamic vulnerability scan report (injection, auth, headers).",
        "evidence": "DAST Automated Scan Reports (HTML/JSON); API Security Test Run Logs",
        "gate": "Release Gate 3: Release blocked on unaddressed High/Critical DAST findings on exposed endpoints."
    },
    {
        "cra_ref": "Annex I, Part II, point (3); Art 13(2)",
        "phase": "Build and Release",
        "action": "Execute Independent Pre-Release Penetration Testing and Retesting",
        "role": "Third-Party Penetration Testing Team, PSIRT Lead",
        "tool_process": "Manual & Automated Penetration Testing, Burp Suite, Exploit Frameworks",
        "input_output": "Input: Staging environment, documentation, source access (gray box). Output: Formal Penetration Testing Report and Retest Verification Certificate.",
        "evidence": "Final Penetration Testing Report (Executive & Technical); Remediation Retest Verification Sign-off",
        "gate": "Release Gate 4: Commercial release blocked until all Critical/High pentest findings are remediated and retested."
    },
    {
        "cra_ref": "Art 3(30), Art 21, Art 22; Guidance Pt 110–132",
        "phase": "Build and Release",
        "action": "Execute Substantial Modification Change Control Screening Gate",
        "role": "Change Advisory Board (CAB) Chair, Security Architect, Compliance Officer",
        "tool_process": "Substantial Modification Assessment Checklist & Architectural Delta Review",
        "input_output": "Input: Release changelog, architectural diffs, threat model delta. Output: Formal Substantial Modification Determination (Non-substantial patch vs Substantial new product).",
        "evidence": "CAB Substantial Modification Screening Record; Release Governance Sign-off",
        "gate": "Release Gate 5: If change is deemed substantial, release cannot proceed under existing CE mark; routes to new conformity assessment."
    },

    # PHASE 4: DEPLOYMENT AND DELIVERY
    {
        "cra_ref": "Art 13(11), Art 31; Annex VII",
        "phase": "Deployment and Delivery",
        "action": "Compile and Formally Finalize Annex VII Technical Documentation Dossier",
        "role": "Regulatory Compliance Lead, Lead Systems Architect",
        "tool_process": "Annex VII Compliance Dossier Builder & Evidence Repository",
        "input_output": "Input: Architecture specs, risk assessments, test reports, SBOMs, user instructions. Output: Complete, verified Annex VII Technical Documentation Dossier.",
        "evidence": "Final Annex VII Technical Documentation Dossier (PDF/Archive); Executive Engineering Sign-off",
        "gate": "Compliance Gate 1: Product placing on the market strictly blocked without completed, approved Annex VII dossier."
    },
    {
        "cra_ref": "Art 7, Art 8, Art 32; Annexes VIII–XI",
        "phase": "Deployment and Delivery",
        "action": "Execute Statutory Conformity Assessment Procedure (Module A / B+C / H)",
        "role": "Compliance Officer, Notified Body (if Class I/II), VP Engineering",
        "tool_process": "Internal Production Control (Module A) or Notified Body Audit Dossier",
        "input_output": "Input: Annex VII Technical Documentation. Output: Internal Conformity Assessment Report (Module A) or EU Type-Examination / Quality System Certificate (Module B+C/H).",
        "evidence": "Conformity Assessment Report; Notified Body Certificate (if Class I/II); Audit Protocol",
        "gate": "Compliance Gate 2: Market delivery blocked without valid conformity assessment report or Notified Body certificate."
    },
    {
        "cra_ref": "Art 13(13), Art 28; Annex V",
        "phase": "Deployment and Delivery",
        "action": "Draw Up and Execute the Formal EU Declaration of Conformity (DoC)",
        "role": "Managing Director / CEO, VP Engineering, Legal Counsel",
        "tool_process": "EU DoC Legal Template & Executive Signature Authorization Workflow",
        "input_output": "Input: Completed conformity assessment and Annex VII dossier. Output: Signed, legally binding EU Declaration of Conformity.",
        "evidence": "Signed EU Declaration of Conformity (Annex V PDF); Board Signatory Resolution",
        "gate": "Legal Gate: Affixing CE mark or delivering commercial units blocked until EU DoC is executed."
    },
    {
        "cra_ref": "Art 13(15)–(17), Arts 29–30",
        "phase": "Deployment and Delivery",
        "action": "Affix CE Marking, Traceability Numbers, and Manufacturer Identification",
        "role": "Hardware Packaging Lead, Software Release Engineer",
        "tool_process": "Packaging Inspection, Software UI 'About' Screen Verification",
        "input_output": "Input: Approved artwork, software UI builds. Output: Visible, legible, indelible CE mark, manufacturer name/address, model/batch number on device or software UI.",
        "evidence": "Packaging Artwork Proofs; Software UI Screenshot Records; Inbound Inspection Sign-off",
        "gate": "Dispatch Gate: Factory shipment or download portal release blocked if CE marking or identification is missing or incorrect."
    },
    {
        "cra_ref": "Art 13(18); Annex II",
        "phase": "Deployment and Delivery",
        "action": "Deliver Annex II Instructions for Use and Technical Security Information to Users",
        "role": "Technical Publications Lead, Customer Delivery Engineer",
        "tool_process": "Customer Documentation Portal, Electronic Delivery System, Packaging Leaflet",
        "input_output": "Input: Annex II user security guide, deployment hardening specs. Output: User manual supplied with product in required Union languages.",
        "evidence": "Delivered User Manual (PDF / Print); Customer Portal URL; Translation Certification Records",
        "gate": "Delivery Gate: Handover to customer blocked if user manual lacks support period end date or CVD contact details."
    },
    {
        "cra_ref": "Annex I, Part II, point (7)",
        "phase": "Deployment and Delivery",
        "action": "Ensure Cryptographically Protected Distribution Channels for Software Delivery",
        "role": "DevOps Infrastructure Lead, Security Operations",
        "tool_process": "TLS 1.3 CDN, Signed Package Repositories, Client Verification Daemons",
        "input_output": "Input: Signed release binaries. Output: Authenticated, encrypted download channel preventing tampering or man-in-the-middle attacks.",
        "evidence": "Download Infrastructure TLS Configuration Audit; Repository Signature Verification Logs",
        "gate": "Infrastructure Gate: Insecure HTTP or unauthenticated delivery endpoints strictly disabled."
    },
    {
        "cra_ref": "Art 13(12), Art 31(3)",
        "phase": "Deployment and Delivery",
        "action": "Archive Technical Documentation and EU DoC into 10-Year Compliance Vault",
        "role": "Corporate Compliance Archivist, Legal Counsel",
        "tool_process": "Enterprise Compliance Document Management System (Immutable Archive)",
        "input_output": "Input: Final Annex VII dossier, signed DoC, test reports. Output: Secure, indexed archive record locked under 10-year retention hold.",
        "evidence": "Compliance Archive Deposit Receipt; WORM Storage Retention Lock Verification",
        "gate": "Archiving Gate: Formal release sign-off requires confirmation of archive deposit."
    },
    {
        "cra_ref": "Arts 17–20",
        "phase": "Deployment and Delivery",
        "action": "Execute Commercial Distributor and Importer Compliance Verification Handover",
        "role": "Channel Operations Lead, Supply Chain Director",
        "tool_process": "Partner Compliance Portal & Distributor Audit Checklist",
        "input_output": "Input: Executed partner agreements, delivery shipments. Output: Verified distributor compliance record ensuring product remains unaltered in transit.",
        "evidence": "Distributor Compliance Audit Record; Partner Master Agreement CRA Addenda",
        "gate": "Channel Gate: Shipments to distributors blocked if partner has not signed CRA compliance addendum."
    },

    # PHASE 5: MAINTENANCE AND RUN
    {
        "cra_ref": "Art 13(7); Annex I Part II point (1)–(3)",
        "phase": "Maintenance and RUN",
        "action": "Execute Continuous Post-Market Vulnerability Monitoring across All Deployed Versions",
        "role": "PSIRT Lead, Security Operations Analyst",
        "tool_process": "Dependency-Track, Black Duck, Continuous NVD/OSV Threat Feeds, Nessus",
        "input_output": "Input: Deployed product SBOM inventory, daily CVE feeds. Output: Automated vulnerability alerts, triage tickets, and exploitability evaluations.",
        "evidence": "Dependency-Track Daily Alert Feeds; Weekly PSIRT Triage Records; Vulnerability Triage Dashboard",
        "gate": "Operational Gate: Newly disclosed CVEs matching product SBOM must be triaged within 24 hours of notification."
    },
    {
        "cra_ref": "Art 14(1)–(3), Art 16; Del Reg 2026/881",
        "phase": "Maintenance and RUN",
        "action": "Execute Statutory Reporting of Actively Exploited Vulnerabilities via ENISA SRP",
        "role": "CISO, PSIRT Incident Commander, Legal Counsel",
        "tool_process": "Article 14 Operational Runbook & ENISA Single Reporting Platform (SRP)",
        "input_output": "Input: Confirmed evidence of active exploitation. Output: 24h Early Warning, 72h Detailed Notification, and 14-day Final Report submitted to CSIRT and ENISA.",
        "evidence": "ENISA SRP Submission Receipts; Incident Awareness Timestamp Records; Final Technical Dossiers",
        "gate": "Statutory Clock Gate: Mandatory 24-hour Early Warning submitted to CSIRT/ENISA from the instant of awareness."
    },
    {
        "cra_ref": "Art 14(3)–(5), Art 16",
        "phase": "Maintenance and RUN",
        "action": "Execute Statutory Reporting of Severe Product Security Incidents via ENISA SRP",
        "role": "CISO, Head of SOC, Legal Counsel",
        "tool_process": "Article 14 Operational Runbook & ENISA Single Reporting Platform (SRP)",
        "input_output": "Input: Incident severely impacting PDE security. Output: 24h Early Warning, 72h Notification, and 1-month Final Report submitted to CSIRT and ENISA.",
        "evidence": "ENISA SRP Incident Receipts; SOC Triage Records; Final Root-Cause Analysis Dossiers",
        "gate": "Statutory Clock Gate: Mandatory 24-hour Early Warning submitted to CSIRT/ENISA upon incident awareness."
    },
    {
        "cra_ref": "Art 14(8); Annex I Part II point (4)",
        "phase": "Maintenance and RUN",
        "action": "Disseminate Emergency Security Advisories and Mitigations to Affected Users",
        "role": "PSIRT Lead, VP Customer Support, Communications Director",
        "tool_process": "Customer Emergency Advisory Broadcast Platform, In-App Alerts, Security Portal",
        "input_output": "Input: Active exploit details, interim mitigation guidance. Output: Direct customer notification bulletins and actionable mitigation instructions.",
        "evidence": "Customer Advisory Broadcast Transmissions; Mitigation Bulletin Web Page; Customer Ticket Logs",
        "gate": "Communications Gate: Advisory dispatched to users without undue delay following confirmation of active exploitation."
    },
    {
        "cra_ref": "Annex I, Part II, point (2); Art 13(10)",
        "phase": "Maintenance and RUN",
        "action": "Develop, Test, and Distribute Vulnerability Remediation Security Patches Without Delay",
        "role": "Sustaining Engineering Lead, DevSecOps Lead, PSIRT",
        "tool_process": "Emergency CI/CD Patch Pipeline, Automated Regression Suites, HSM Code Signing",
        "input_output": "Input: Vulnerability root cause. Output: Cryptographically signed standalone security patch and updated SBOM.",
        "evidence": "Patch Release Artifacts; Automated Regression Test Logs; Updated CycloneDX SBOM; Release Notes",
        "gate": "Patch Release Gate: Critical security patch released within 7-14 calendar days of triage confirmation."
    },
    {
        "cra_ref": "Annex I, Part II, point (4)",
        "phase": "Maintenance and RUN",
        "action": "Publish Standardized Public Security Advisories (CSAF 2.0)",
        "role": "PSIRT Lead, Technical Writer",
        "tool_process": "CSAF 2.0 Advisory Generator & Public Security Portal",
        "input_output": "Input: Remediated CVE details, CVSS scores, fixed versions. Output: Published security advisory in CSAF 2.0 JSON and HTML formats.",
        "evidence": "Published CSAF Advisory Files (JSON); Public Advisory Web URLs; RSS Feed Updates",
        "gate": "Advisory Gate: Public advisory published synchronously with or immediately following patch availability."
    },
    {
        "cra_ref": "Annex I, Part I, point (2)(c); Annex I Part II point (7)",
        "phase": "Maintenance and RUN",
        "action": "Deliver Automatic Security Updates with User Notification and Opt-Out Controls",
        "role": "Operations Lead, Release Manager",
        "tool_process": "OTA / Background Update Daemon, Dual-Partition Rollback Protection",
        "input_output": "Input: Verified security patch. Output: Automated background installation on client fleets with deferral/opt-out options.",
        "evidence": "Fleet Update Telemetry Dashboard; Update Success/Failure Logs; Rollback Trigger Logs",
        "gate": "Deployment Gate: Automatic deployment staged across canary groups prior to 100% rollout."
    },
    {
        "cra_ref": "Art 13(9)",
        "phase": "Maintenance and RUN",
        "action": "Deposit Released Security Patches into Mandatory 10-Year Public Update Archive",
        "role": "Release Engineering Lead, Cloud Infrastructure Lead",
        "tool_process": "Immutable Public Patch Repository (WORM Storage / S3 Glacier)",
        "input_output": "Input: Released patch binaries and release notes. Output: Immutable public download archive accessible for ≥10 years from market placement.",
        "evidence": "Immutable Storage Deposit Log; Patch Archive Public URL; Periodic Integrity Check Reports",
        "gate": "Archival Gate: Every released security patch automatically deposited and locked in 10-year archive."
    },
    {
        "cra_ref": "Art 13(7), Art 31(2); Guidance Pt 147",
        "phase": "Maintenance and RUN",
        "action": "Continuously Update Living Cybersecurity Risk Assessment and Technical Documentation",
        "role": "Product Security Architect, Regulatory Compliance Officer",
        "tool_process": "Living TARA Risk Register & Technical Documentation Management System",
        "input_output": "Input: Post-market vulnerability trends, new attack vectors, customer incident data. Output: Updated Cybersecurity Risk Assessment and Annex VII dossier addenda.",
        "evidence": "Updated Risk Assessment Revisions; Annual Risk Review Sign-off Records; Annex VII Addenda",
        "gate": "Annual Review Gate: Executive review and re-certification of risk assessment every 12 months during RUN."
    },
    {
        "cra_ref": "Art 13(8), Art 13(22); Annex II point 8",
        "phase": "Maintenance and RUN",
        "action": "Execute End-of-Support (EOS) Notice and Decommissioning Governance",
        "role": "Product Manager, VP Customer Support, Legal Counsel",
        "tool_process": "Product Lifecycle Portal, Customer Direct Notices, Code Escrow Procedure",
        "input_output": "Input: Impending end of declared support period. Output: Advance customer notice (minimum 6 months), public lifecycle update, final data erasure guidance.",
        "evidence": "Advance End-of-Support Notices to Customers; Market Surveillance Authority Notifications; Final Decommissioning Advisory",
        "gate": "EOS Gate: Vulnerability monitoring and reporting cannot terminate until declared calendar EOS date arrives and notice is satisfied."
    }
]

with open('lifecycle_mappings.json', 'w') as f:
    json.dump(lifecycle_mappings, f, indent=2)

print(f"Lifecycle mappings saved: {len(lifecycle_mappings)} actions across 5 phases.")
