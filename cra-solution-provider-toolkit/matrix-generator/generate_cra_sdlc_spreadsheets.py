"""
Retuned Script to parse BSI TR-03183 requirements and generate five (5) formatted .xlsx files
specifically tailored for solutions classified under the CRA DEFAULT / STANDARD CATEGORY
(Conformity Assessment: Module A - Internal Production Control per Article 24(1) and Annex VI):
1. 01_BSI_CRA_Presale.xlsx
2. 02_BSI_CRA_Development.xlsx
3. 03_BSI_CRA_Build.xlsx
4. 04_BSI_CRA_Deployment.xlsx
5. 05_BSI_CRA_Maintenance_RUN.xlsx
"""

import sys
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

SOURCE_WORKBOOK = "Claude_responses/BSI-TR-03183_CRA_Requirements_SDLC_Tool_Coverage.xlsx"

DOC_MAPPING = {
    "BSI TR-03183-1 v1.0.0": "BSI-TR-03183-1_v1_0_0.md",
    "BSI TR-03183-2 v2.1.0": "BSI-TR-03183-2_v2_1_0.md",
    "BSI TR-03183-3 v1.0.0": "BSI-TR-03183-3_v1_0_0.md",
    "BSI TR-03183-H v1.1.0": "BSI-TR-03183-H_v1_1_0.md"
}

DOC_SHORT = {
    "BSI TR-03183-1 v1.0.0": "TR-03183-1",
    "BSI TR-03183-2 v2.1.0": "TR-03183-2",
    "BSI TR-03183-3 v1.0.0": "TR-03183-3",
    "BSI TR-03183-H v1.1.0": "TR-03183-H"
}

PHASE_CONFIGS = [
    {
        "filename": "01_BSI_CRA_Presale.xlsx",
        "phase_name": "Presale",
        "sheet_title": "01 Presale (Default Category)",
        "source_phases": ["Presales and Product Definition"],
        "extra_reqs": [
            "TR2-001", "TR2-002", "TR2-003", "TR2-005", "TR2-014", "TR2-015",
            "TR3-001", "TR3-008", "TR3-013", "TR3-040", "TR3-045", "TR3-050"
        ],
        "desc": "Default Category Scoping, Module A self-assessment sizing, contractual terms, CRA support SLAs, SBOM delivery & CVD disclosure terms"
    },
    {
        "filename": "02_BSI_CRA_Development.xlsx",
        "phase_name": "Development",
        "sheet_title": "02 Dev (Default Category)",
        "source_phases": ["Requirements Engineering and Security Architecture", "Development"],
        "extra_reqs": [],
        "desc": "Default Category secure-by-design architecture, tailored threat modeling (STRIDE), secure coding, internal SAST gates, component selection"
    },
    {
        "filename": "03_BSI_CRA_Build.xlsx",
        "phase_name": "Build",
        "sheet_title": "03 Build (Default Category)",
        "source_phases": ["Build and CI/CD"],
        "extra_reqs": [],
        "desc": "CI/CD pipeline integrity, automated CycloneDX/SPDX SBOM generation, build SCA gating, binary composition, Annex VII Technical File artifact compilation"
    },
    {
        "filename": "04_BSI_CRA_Deployment.xlsx",
        "phase_name": "Deployment",
        "sheet_title": "04 Deploy (Default Category)",
        "source_phases": ["Deployment and Release", "Testing and Security Verification"],
        "extra_reqs": [],
        "desc": "Secure-by-default configuration, hardening, internal DAST & penetration testing verification, Module A EU Declaration of Conformity & CE marking"
    },
    {
        "filename": "05_BSI_CRA_Maintenance_RUN.xlsx",
        "phase_name": "Maintenance_RUN",
        "sheet_title": "05 Run (Default Category)",
        "source_phases": ["Operations and Maintenance", "Vulnerability Handling and End-of-Life"],
        "extra_reqs": [],
        "desc": "Continuous runtime SBOM vulnerability monitoring, automated CSAF/VEX advisories, patch management, mandatory CRA Article 14 24h/72h incident reporting"
    }
]

TOOL_ORDER = [
    ("Threat Analysis / Risk Analysis", "Col G - Threat Analysis / Risk Analysis Coverage"),
    ("DPIA", "Col H - DPIA Coverage"),
    ("SonarQube", "Col I - SonarQube Coverage (SAST / Code Quality)"),
    ("Coverity", "Col J - Coverity Coverage (Deep SAST / C-C++ / Memory & Concurrency)"),
    ("Nexus IQ / Lifecycle (CLM)", "Col K - Nexus IQ CLM Coverage (SCA / License & Policy Governance)"),
    ("Black Duck", "Col L - Black Duck Coverage (SCA / Binary & Snippet Analysis)"),
    ("Dependency-Track", "Col M - Dependency-Track Coverage (Continuous SBOM & VEX Monitoring)"),
    ("OWASP ZAP / Burp Suite", "Col N - OWASP ZAP / Burp Suite Coverage (DAST / Web & API Security)"),
    ("Nessus / Cyberwatch", "Col O - Nessus / Cyberwatch Coverage (Infra & OS Vulnerability Mgmt)"),
    ("Penetration Testing", "Col P - Penetration Testing Coverage (Manual Offensive & Architecture Validation)")
]

def load_data():
    print(f"Loading data from {SOURCE_WORKBOOK}...")
    wb = openpyxl.load_workbook(SOURCE_WORKBOOK, data_only=True)
    ws1 = wb['1 Requirements Register']
    ws2 = wb['2 SDLC Phase Impact']
    ws3 = wb['3 Tool Coverage Matrix']

    # 1. Register data
    reg = {}
    for r in range(2, ws1.max_row + 1):
        req_id = ws1.cell(row=r, column=1).value
        if not req_id:
            continue
        reg[req_id] = {
            "req_id": req_id,
            "orig_id": ws1.cell(row=r, column=2).value,
            "title": ws1.cell(row=r, column=3).value or "",
            "text": ws1.cell(row=r, column=4).value or "",
            "type": ws1.cell(row=r, column=5).value or "",
            "strength": ws1.cell(row=r, column=6).value or "",
            "doc": ws1.cell(row=r, column=7).value or "",
            "section": ws1.cell(row=r, column=8).value or "",
            "page_line": ws1.cell(row=r, column=9).value or "",
            "cra_ref": ws1.cell(row=r, column=12).value or "",
            "std_ref": ws1.cell(row=r, column=13).value or "",
            "control_family": ws1.cell(row=r, column=21).value or ""
        }

    # 2. Phase impact data
    phases = {}
    for r in range(2, ws2.max_row + 1):
        req_id = ws2.cell(row=r, column=1).value
        p_name = ws2.cell(row=r, column=3).value
        if not req_id or not p_name:
            continue
        if req_id not in phases:
            phases[req_id] = {}
        phases[req_id][p_name] = {
            "applicability": ws2.cell(row=r, column=4).value or "Not Applicable",
            "impact_level": ws2.cell(row=r, column=5).value or "Low",
            "rationale": ws2.cell(row=r, column=6).value or "",
            "impact_desc": ws2.cell(row=r, column=7).value or "",
            "activities": ws2.cell(row=r, column=8).value or "",
            "owner": ws2.cell(row=r, column=9).value or "",
            "deliverables": ws2.cell(row=r, column=10).value or "",
            "control_gate": ws2.cell(row=r, column=11).value or "",
            "dependencies": ws2.cell(row=r, column=12).value or "",
            "risks": ws2.cell(row=r, column=13).value or "",
            "acceptance": ws2.cell(row=r, column=14).value or ""
        }

    # 3. Tool coverage
    tools = {}
    for r in range(2, ws3.max_row + 1):
        req_id = ws3.cell(row=r, column=1).value
        tool_name = ws3.cell(row=r, column=2).value
        if not req_id or not tool_name:
            continue
        if req_id not in tools:
            tools[req_id] = {}
        tools[req_id][tool_name] = {
            "classification": ws3.cell(row=r, column=3).value or "None",
            "capability": ws3.cell(row=r, column=4).value or "",
            "how": ws3.cell(row=r, column=5).value or "",
            "limits": ws3.cell(row=r, column=8).value or ""
        }

    print(f"Loaded {len(reg)} requirements, {len(phases)} phase maps, {len(tools)} tool maps.")
    return reg, phases, tools

def format_tool_cell_default(tool_key, tool_info, req_meta):
    if not tool_info:
        return "N/A — Not applicable or unmapped for this requirement under Default Category."
    
    classification = tool_info.get("classification", "None")
    cap = tool_info.get("capability", "").strip()
    how = tool_info.get("how", "").strip()
    limits = tool_info.get("limits", "").strip()

    level_map = {
        "Direct": "Full",
        "Partial": "Partial",
        "Conditional": "Supporting",
        "Indirect": "Supporting",
        "None": "N/A"
    }
    level = level_map.get(classification, "N/A")

    if level == "N/A":
        tool_reasons = {
            "Threat Analysis / Risk Analysis": "Focuses on threat modeling (STRIDE) and risk evaluation; does not perform automated code or runtime verification.",
            "DPIA": "Evaluates GDPR/privacy personal data flows; out of scope for general CRA technical or organizational baseline controls.",
            "SonarQube": "Application SAST and code hygiene; does not analyze compiled binaries without source, perform deep inter-procedural path simulation, or track post-deployment CVEs.",
            "Coverity": "Deep inter-procedural SAST for C/C++/Java/Go; does not analyze third-party open-source components, unbuilt binaries, or runtime infrastructure.",
            "Nexus IQ / Lifecycle (CLM)": "Build-stage SCA policy governance; does not analyze first-party application logic, runtime network traffic, or unmanaged binaries.",
            "Black Duck": "Binary and snippet SCA; does not analyze custom application source code weaknesses or perform active dynamic testing.",
            "Dependency-Track": "Continuous post-build SBOM and VEX monitoring; does not inspect source code quality or perform active network scanning.",
            "OWASP ZAP / Burp Suite": "Dynamic web/API penetration testing; cannot inspect source code, generate SBOMs, or evaluate organizational processes.",
            "Nessus / Cyberwatch": "Infrastructure and host vulnerability management; does not inspect application source code or build manifests.",
            "Penetration Testing": "Manual offensive verification; point-in-time assessment that does not replace continuous CI/CD automated gates."
        }
        specific_reason = tool_reasons.get(tool_key, "Out of scope for this tool/practice.")
        return f"N/A — No direct capability for this requirement. {specific_reason}"

    # Build comprehensive explanation emphasizing Module A Technical File evidence
    parts = []
    if cap and cap != "No relevant capability for this requirement":
        parts.append(cap.rstrip("."))
    if how and how != "Not applicable" and how != "—":
        parts.append(how.rstrip("."))
    if limits and "Informative/definitional text" not in limits and "Tool/process output is" not in limits:
        parts.append(f"Constraint: {limits.rstrip('.')}")

    desc = ". ".join(parts)
    if not desc.endswith("."):
        desc += "."

    # Enhance specific overlapping tools to clearly differentiate their role in Module A self-assessment
    if tool_key == "SonarQube" and level in ["Full", "Partial", "Supporting"]:
        desc += " In Module A, scan reports serve as internal objective evidence verifying clean code standards and blocking PRs on newly introduced CWEs."
    elif tool_key == "Coverity" and level in ["Full", "Partial", "Supporting"]:
        desc += " In Module A, Coverity results provide deep inter-procedural verification for memory safety and concurrency without requiring external certification audits."
    elif tool_key == "Nexus IQ / Lifecycle (CLM)" and level in ["Full", "Partial", "Supporting"]:
        desc += " In Module A, release-stage policy reports provide direct audit evidence that delivered dependencies comply with license and vulnerability baselines."
    elif tool_key == "Black Duck" and level in ["Full", "Partial", "Supporting"]:
        desc += " In Module A, binary and snippet scan reports verify the integrity of embedded third-party libraries for the internal Annex VII Technical File."
    elif tool_key == "Dependency-Track" and level in ["Full", "Partial", "Supporting"]:
        desc += " In Module A, provides continuous post-market monitoring of release SBOMs against NVD/OSV feeds, automatically generating internal CSAF/VEX statements."

    return f"{level} — {desc}"

def retune_impact_for_default(req_id, p_name, orig_impact, p_data_list, meta):
    doc_raw = meta.get("doc", "")
    orig_id = str(meta.get("orig_id", ""))
    is_module_h = ("TR-03183-H" in doc_raw and any(k in orig_id for k in ["108", "109", "110", "111", "112", "114", "117", "118", "B.1", "B.2", "B.3", "B.4", "C.1", "C.2"]))

    # Core Default Category framing
    prefix = ""
    if p_name == "Presale":
        prefix = "Default Category (Module A) Scoping: Solution is classified as Default/Standard PwDE (Article 24(1)), confirming internal production control applies. Third-party Notified Body assessment (Modules B+C / H) is NOT required, eliminating external audit fees and certification lead times. Contractual terms reflect manufacturer self-declaration of conformity, standard CRA warranty, and support period SLAs."
    elif p_name == "Development":
        prefix = "Default Category Engineering Impact: Architecture and threat modeling (STRIDE) follow the tailored risk-based approach of TR-03183-1 Section 5. Internal SAST quality gates (SonarQube/Coverity) and secure coding rules enforce Annex I Essential Requirements under internal engineering ownership, compiling design evidence for the Annex VII Technical Documentation."
    elif p_name == "Build":
        prefix = "Default Category Build Automation: Automated CI/CD pipeline generates and signs machine-readable SBOMs (CycloneDX 1.6+ / SPDX 3.0.1+) and enforces SCA policy gates (Nexus IQ / Black Duck). Build artifacts and provenance checksums are archived in the internal Annex VII Technical File (retained for 10 years) without requiring external witness audits."
    elif p_name == "Deployment":
        prefix = "Default Category Pre-Market Verification: Solution undergoes internal DAST (OWASP ZAP / Burp), configuration hardening audit (Nessus/Cyberwatch), and penetration testing verification. Internal Product Security / Engineering sign-off executes the EU Declaration of Conformity (Module A) and authorizes CE marking without third-party certificate dependencies."
    elif p_name == "Maintenance_RUN":
        prefix = "Default Category Post-Market Operations: Continuous runtime SBOM monitoring (Dependency-Track), CVE triage, and CSAF/VEX advisories are executed via internal PSIRT/CSIRT. Mandatory CRA Article 14 reporting (24h early warning / 72h notification to CSIRT/ENISA) FULLY APPLIES under manufacturer direct responsibility, with no recurring Notified Body surveillance audits."

    if is_module_h:
        module_h_note = " [Default Category Note: Formal third-party Notified Body quality system certification (Module H) is NOT legally mandated for this solution. Internal ISMS (ISO/IEC 27001) controls are applied as voluntary internal engineering best practices to substantiate the Module A self-assessment file.]"
        return f"Impact Level: Low to Medium. {prefix}{module_h_note} {orig_impact}"
    
    return f"{prefix} {orig_impact}"

def retune_dependencies_for_default(p_name, orig_deps):
    if p_name == "Presale":
        cascades = "Module A Lifecycle Flow: Upstream market sizing establishes Default category classification; cascades downstream into Development (internal security-by-design & threat models), Build (automated CI/CD SBOM & SCA toolchains), Deployment (internal verification & CE declaration), and Maintenance/RUN (internal PSIRT support commitments)."
    elif p_name == "Development":
        cascades = "Module A Lifecycle Flow: Sourced from Presale Default category baseline; cascades downstream into Build (automated SAST/SCA quality gates) and Deployment (secure configuration templates & internal compliance records)."
    elif p_name == "Build":
        cascades = "Module A Lifecycle Flow: Ingests Development source code and manifests; outputs signed release artifacts and SBOMs for Deployment verification and establishes the baseline for continuous Maintenance/RUN monitoring."
    elif p_name == "Deployment":
        cascades = "Module A Lifecycle Flow: Verifies signed Build outputs; executes internal pre-market testing sign-off, applies CE marking, and establishes active security contact endpoints for Maintenance/RUN operations."
    elif p_name == "Maintenance_RUN":
        cascades = "Module A Lifecycle Flow: Ingests Build SBOMs for daily automated CVE monitoring; feeds identified post-market vulnerabilities back into Development for patch creation and triggers mandatory CRA Article 14 notifications when actively exploited."

    if orig_deps and orig_deps != "—":
        return f"{cascades} Cross-phase links: {orig_deps}"
    return cascades

def retune_remediation_for_default(p_name, orig_rem, meta):
    doc_raw = meta.get("doc", "")
    orig_id = str(meta.get("orig_id", ""))
    is_module_h = ("TR-03183-H" in doc_raw and any(k in orig_id for k in ["108", "109", "110", "111", "112", "114", "117", "118", "B.1", "B.2", "B.3", "B.4", "C.1", "C.2"]))

    if is_module_h:
        return (
            "Default Category Remediation Strategy (Module A):\n"
            "Action: Apply internal quality and security engineering processes aligned with ISO/IEC 27001 / ISO 9001 principles. Formal Notified Body Module H application, site inspection, and approval are not required.\n"
            "Deliverables & Audit Evidence: Internal process documentation, SDLC governance policies, and engineering verification records integrated into the Annex VII Technical File.\n"
            "Control Gate: Internal Product Security / Quality Management review and sign-off (no external Notified Body gate).\n"
            "Responsible Role: Lead Security Architect / Head of Engineering."
        )

    # General Module A adjustment to control gates and deliverables
    retuned = orig_rem.replace("Notified body approval", "Internal Product Security sign-off")
    retuned = retuned.replace("notified body", "internal engineering authority")
    retuned += f"\nModule A Verification: Artifacts are compiled into the internal CRA Annex VII Technical Documentation, retained for 10 years by the manufacturer."
    return retuned

def generate_phase_workbook_default(cfg, reg, phases, tools):
    fname = cfg["filename"]
    p_name = cfg["phase_name"]
    src_phases = cfg["source_phases"]
    extra_reqs = set(cfg.get("extra_reqs", []))
    sheet_title = cfg["sheet_title"]
    phase_desc = cfg["desc"]

    print(f"\n==========================================")
    print(f"Generating Retuned {fname} for phase: {p_name} [DEFAULT CATEGORY]")
    print(f"Description: {phase_desc}")
    print(f"==========================================")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title

    # Header styling: Dark Navy
    NAVY = "1B365D"
    WHITE = "FFFFFF"
    BORDER_COLOR = "D9D9D9"

    header_font = Font(name="Calibri", size=11, bold=True, color=WHITE)
    header_fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    data_font = Font(name="Calibri", size=10, color="000000")
    data_align = Alignment(horizontal="left", vertical="top", wrap_text=True)
    
    thin_border = Border(
        left=Side(style="thin", color=BORDER_COLOR),
        right=Side(style="thin", color=BORDER_COLOR),
        top=Side(style="thin", color=BORDER_COLOR),
        bottom=Side(style="thin", color=BORDER_COLOR)
    )

    alt_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    headers = [
        "Requirement ID",
        "Source Document",
        "Requirement Summary",
        "Impact on Current Phase",
        "Cross-Phase Dependencies",
        "Remediation & Implementation Strategy"
    ] + [t[1].split(" - ")[1] for t in TOOL_ORDER]

    ws.row_dimensions[1].height = 42
    for col_idx, h_text in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    # Select requirements that apply to this phase
    applicable_req_ids = []
    for req_id, p_map in phases.items():
        is_app = False
        for sp in src_phases:
            if sp in p_map and p_map[sp]["applicability"] in ["Applicable", "Conditional", "To Be Determined"]:
                is_app = True
                break
        if not is_app and req_id in extra_reqs:
            is_app = True
        if is_app:
            applicable_req_ids.append(req_id)

    print(f"Total applicable requirements for {p_name} [Default Category]: {len(applicable_req_ids)}")

    # Sort requirements logically: TR1, TR2, TR3, TRH
    def sort_key(rid):
        prefix = rid[:3]
        order = {"TR1": 1, "TR2": 2, "TR3": 3, "TRH": 4}
        try:
            num = int(rid.split("-")[1])
        except:
            num = 0
        return (order.get(prefix, 9), num)

    applicable_req_ids.sort(key=sort_key)

    row_num = 2
    for req_id in applicable_req_ids:
        meta = reg.get(req_id, {})
        doc_raw = meta.get("doc", "")
        doc_md = DOC_MAPPING.get(doc_raw, doc_raw)
        doc_short = DOC_SHORT.get(doc_raw, "BSI-TR")
        orig_id = meta.get("orig_id", "")
        section = meta.get("section", "")
        title = meta.get("title", "")
        text = meta.get("text", "")
        strength = meta.get("strength", "MUST")
        cra_ref = meta.get("cra_ref", "")

        # Col A - Requirement ID
        col_a_id = f"{doc_short} Sec {orig_id} [{req_id}]"

        # Col B - Source Document
        col_b_doc = doc_md

        # Col C - Requirement Summary
        norm_verb = "MUST"
        if "SHOULD" in strength.upper():
            norm_verb = "SHOULD"
        elif "SHALL" in strength.upper():
            norm_verb = "SHALL"
        elif "MAY" in strength.upper():
            norm_verb = "MAY"
        elif "CRA" in strength.upper():
            norm_verb = "SHALL"

        col_c_summary = f"[{norm_verb}] {title}. {text}"
        if cra_ref and cra_ref != "—":
            col_c_summary += f" (CRA Reference: {cra_ref})"

        # Synthesize Phase Impact, Cross-Phase Dependencies, Remediation
        p_data_list = []
        for sp in src_phases:
            if req_id in phases and sp in phases[req_id]:
                p_data_list.append(phases[req_id][sp])

        if not p_data_list and req_id in extra_reqs:
            sp_first = list(phases[req_id].keys())[0] if req_id in phases else None
            if sp_first:
                p_data_list.append(phases[req_id][sp_first])

        # Col D - Impact on Current Phase (Retuned for Default Category)
        impact_rationales = [pd.get("rationale", "").strip() for pd in p_data_list if pd.get("rationale")]
        impact_descs = [pd.get("impact_desc", "").strip() for pd in p_data_list if pd.get("impact_desc")]
        raw_impact = " ".join([r for r in impact_rationales if "phase not applicable" not in r.lower()] + 
                              [d for d in impact_descs if "none: this requirement does not affect" not in d.lower()])
        col_d_impact = retune_impact_for_default(req_id, p_name, raw_impact, p_data_list, meta)

        # Col E - Cross-Phase Dependencies (Retuned for Default Category)
        dep_parts = [pd.get("dependencies", "").strip() for pd in p_data_list if pd.get("dependencies") and pd.get("dependencies") != "—"]
        raw_deps = "; ".join(set(dep_parts))
        col_e_deps = retune_dependencies_for_default(p_name, raw_deps)

        # Col F - Remediation & Implementation Strategy (Retuned for Default Category)
        acts = [pd.get("activities", "").strip() for pd in p_data_list if pd.get("activities") and pd.get("activities") != "—"]
        delivs = [pd.get("deliverables", "").strip() for pd in p_data_list if pd.get("deliverables") and pd.get("deliverables") != "—"]
        gates = [pd.get("control_gate", "").strip() for pd in p_data_list if pd.get("control_gate") and pd.get("control_gate") != "—"]
        owners = [pd.get("owner", "").strip() for pd in p_data_list if pd.get("owner") and pd.get("owner") != "—"]

        rem_parts = []
        if acts:
            rem_parts.append("Action: " + "; ".join(acts))
        else:
            rem_parts.append(f"Action: Establish and enforce internal {p_name} procedure meeting the normative requirements of {doc_short} Sec {orig_id}.")

        if delivs:
            rem_parts.append("Deliverables & Audit Evidence: " + "; ".join(delivs))
        else:
            rem_parts.append("Deliverables & Audit Evidence: Documented process specification, verified review records, and technical compliance artifacts.")

        if gates:
            rem_parts.append("Control Gate: " + "; ".join(gates))
        else:
            rem_parts.append("Control Gate: Internal engineering/security review sign-off and mandatory compliance approval before phase completion.")

        if owners:
            rem_parts.append("Responsible Role: " + ", ".join(set(owners)))

        raw_rem = "\n\n".join(rem_parts)
        col_f_rem = retune_remediation_for_default(p_name, raw_rem, meta)

        # Cols G to P - Tooling columns (Retuned for Default Category)
        tool_cells = []
        req_tools = tools.get(req_id, {})
        for tool_key, col_header in TOOL_ORDER:
            t_info = req_tools.get(tool_key, None)
            t_cell = format_tool_cell_default(tool_key, t_info, meta)
            tool_cells.append(t_cell)

        # Assemble full row
        full_row = [
            col_a_id,
            col_b_doc,
            col_c_summary,
            col_d_impact,
            col_e_deps,
            col_f_rem
        ] + tool_cells

        ws.row_dimensions[row_num].height = 100
        is_even = (row_num % 2 == 0)

        for col_idx, val in enumerate(full_row, start=1):
            cell = ws.cell(row=row_num, column=col_idx, value=val)
            cell.font = data_font
            cell.alignment = data_align
            cell.border = thin_border
            if is_even:
                cell.fill = alt_fill

        row_num += 1

    # Freeze panes at A2
    ws.freeze_panes = "A2"

    # Set auto-filter
    ws.auto_filter.ref = ws.dimensions

    # Enable gridlines
    ws.views.sheetView[0].showGridLines = True

    # Set column widths
    col_widths = {
        "A": 24, # Requirement ID
        "B": 24, # Source Document
        "C": 48, # Requirement Summary
        "D": 48, # Impact on Current Phase
        "E": 42, # Cross-Phase Dependencies
        "F": 48, # Remediation Strategy
        "G": 38, # Threat Analysis
        "H": 38, # DPIA
        "I": 38, # SonarQube
        "J": 38, # Coverity
        "K": 38, # Nexus IQ
        "L": 38, # Black Duck
        "M": 38, # Dependency-Track
        "N": 38, # OWASP ZAP / Burp
        "O": 38, # Nessus / Cyberwatch
        "P": 38  # Penetration Testing
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Add a secondary Executive Dashboard tab tuned for Default Category
    dash_ws = wb.create_sheet(title="Executive Summary & Stats")
    dash_ws.views.sheetView[0].showGridLines = True
    dash_ws.column_dimensions["A"].width = 34
    dash_ws.column_dimensions["B"].width = 54

    dash_ws.cell(row=1, column=1, value="EU Cyber Resilience Act (CRA) Compliance Register").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
    dash_ws.cell(row=2, column=1, value=f"CRA Product Classification: DEFAULT / STANDARD CATEGORY (Article 24(1))").font = Font(name="Calibri", size=12, bold=True, color="000000")
    dash_ws.cell(row=3, column=1, value=f"Conformity Assessment Route: Module A (Internal Production Control / Self-Assessment per Annex VI)").font = Font(name="Calibri", size=11, bold=True, color="2E75B6")
    dash_ws.cell(row=4, column=1, value=f"SDLC Lifecycle Phase: {p_name} | Scope: {phase_desc}").font = Font(name="Calibri", size=10, italic=True)

    dash_stats = [
        ("Total Applicable Requirements in Phase", len(applicable_req_ids)),
        ("CRA Conformity Assessment Procedure", "Module A (Internal Production Control) — No third-party Notified Body audit required"),
        ("Technical Documentation Obligation", "CRA Annex VII Technical Documentation File (retained for 10 years by manufacturer)"),
        ("Source: BSI TR-03183-1 (General Requirements)", sum(1 for rid in applicable_req_ids if rid.startswith("TR1"))),
        ("Source: BSI TR-03183-2 (SBOM Specification)", sum(1 for rid in applicable_req_ids if rid.startswith("TR2"))),
        ("Source: BSI TR-03183-3 (Vulnerability Reporting)", sum(1 for rid in applicable_req_ids if rid.startswith("TR3"))),
        ("Source: BSI TR-03183-H (Harmonized / ISO 27001)", sum(1 for rid in applicable_req_ids if rid.startswith("TRH"))),
        ("Static Code Analysis (SAST)", "SonarQube (clean code / quality gates) & Coverity (deep C/C++ memory safety) for Annex VII evidence"),
        ("Software Composition Analysis (SCA)", "Nexus IQ (build-stage policy gating) & Black Duck (binary/snippet inspection) for SBOM generation"),
        ("Continuous Post-Market Monitoring", "Dependency-Track (continuous runtime SBOM & NVD/OSV correlation with CSAF/VEX generation)"),
        ("Pre-Release Dynamic & Offensive Testing", "OWASP ZAP / Burp Suite (DAST) & Internal Penetration Testing for pre-market verification"),
        ("Infrastructure Vulnerability Management", "Nessus / Cyberwatch (pre-deployment image hardening & post-market infrastructure scans)"),
        ("Mandatory CRA Article 14 Reporting", "24h early warning / 72h full notification to national CSIRT & ENISA (fully binding on Default Category)")
    ]

    r_idx = 6
    for label, val in dash_stats:
        c1 = dash_ws.cell(row=r_idx, column=1, value=label)
        c2 = dash_ws.cell(row=r_idx, column=2, value=str(val))
        c1.font = Font(name="Calibri", size=10, bold=True)
        c2.font = Font(name="Calibri", size=10)
        c1.border = thin_border
        c2.border = thin_border
        r_idx += 1

    wb.save(fname)
    print(f"Successfully generated: {fname} ({len(applicable_req_ids)} requirement rows) [DEFAULT CATEGORY / MODULE A]")

def main():
    reg, phases, tools = load_data()
    for cfg in PHASE_CONFIGS:
        generate_phase_workbook_default(cfg, reg, phases, tools)
    print("\nAll 5 SDLC Phase Workbooks retuned successfully for CRA DEFAULT CATEGORY (Module A)!")

if __name__ == "__main__":
    main()
