import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT_FAMILY = "Segoe UI"
font_title = Font(name=FONT_FAMILY, size=15, bold=True, color="0F2537")
font_subtitle = Font(name=FONT_FAMILY, size=9.5, italic=True, color="4A5568")
font_section = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
font_header = Font(name=FONT_FAMILY, size=9.5, bold=True, color="FFFFFF")
font_cell = Font(name=FONT_FAMILY, size=9, color="1A202C")
font_cell_bold = Font(name=FONT_FAMILY, size=9, bold=True, color="1A202C")

fill_dark_navy = PatternFill(start_color="0F2537", end_color="0F2537", fill_type="solid")
fill_header_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
fill_header_slate = PatternFill(start_color="2C5282", end_color="2C5282", fill_type="solid")
fill_section_ice = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

fill_full = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
fill_partial = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
fill_none = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")

border_thin = Border(left=Side(style="thin", color="CBD5E1"),
                     right=Side(style="thin", color="CBD5E1"),
                     top=Side(style="thin", color="CBD5E1"),
                     bottom=Side(style="thin", color="CBD5E1"))

border_double_bottom = Border(left=Side(style="thin", color="CBD5E1"),
                              right=Side(style="thin", color="CBD5E1"),
                              top=Side(style="thin", color="CBD5E1"),
                              bottom=Side(style="double", color="0F2537"))

def auto_fit_columns(ws, custom_widths=None):
    if custom_widths is None:
        custom_widths = {}
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        if col_letter in custom_widths:
            ws.column_dimensions[col_letter].width = custom_widths[col_letter]
            continue
        max_len = 0
        for cell in col:
            if cell.row in [1, 2]:
                continue
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(12, min(max_len + 3, 50))

def build_tool_summary(wb, tool_profiles):
    print("Building Sheet 2: Tool Coverage Summary...")
    ws = wb.create_sheet(title="Tool Coverage Summary")
    ws.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws.merge_cells("A1:L1")
    ws["A1"] = "SECURITY TOOLCHAIN COVERAGE EVALUATION & STATISTICAL GAP ANALYSIS"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[1].height = 25
    
    ws.merge_cells("A2:L2")
    ws["A2"] = "Assessment of 10 Security Products & Activities against Regulation (EU) 2024/2847 | Denominator: 43 Evaluated CRA Requirements"
    ws["A2"].font = font_subtitle
    ws["A2"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[2].height = 18

    # Section 1 Header
    ws.merge_cells("A4:L4")
    ws["A4"] = "TABLE A: TOOL CAPABILITIES, OPERATING MODELS & REGULATORY PROFILES"
    ws["A4"].font = font_section
    ws["A4"].fill = fill_dark_navy
    ws["A4"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[4].height = 24

    headers_a = [
        "Tool / Activity Name", "Operating Model / Category", "Primary Security Purpose",
        "Relevant CRA Requirements Supported", "Lifecycle Phases Supported",
        "Direct Capabilities & Technical Strengths", "Coverage Limitations & Regulatory Blind Spots",
        "Required Integrations, Setup & Config", "Evidence & Deliverables Generated",
        "Complementary Controls & Activities Required", "Toolchain Overlaps & Synergies",
        "Residual Toolchain Gaps"
    ]
    
    ws.row_dimensions[5].height = 26
    for col_idx, h in enumerate(headers_a, 1):
        cell = ws.cell(row=5, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header_navy
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin

    for idx, t in enumerate(tool_profiles, start=6):
        ws.row_dimensions[idx].height = 60
        is_zebra = (idx % 2 == 0)
        base_fill = fill_zebra if is_zebra else fill_white
        
        vals = [
            t["name"], t["category"], t["purpose"], t["requirements"],
            t["lifecycle"], t["capabilities"], t["limitations"],
            t["integrations"], t["evidence"], t["complementary"],
            t["overlaps"], t["gaps"]
        ]
        
        for c_idx, val in enumerate(vals, 1):
            cell = ws.cell(row=idx, column=c_idx, value=val)
            cell.font = font_cell
            cell.border = border_thin
            cell.fill = base_fill
            if c_idx == 1:
                cell.font = font_cell_bold
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif c_idx in [2, 4, 5]:
                cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # Section 2: Quantitative Metrics Table
    row_sec2 = 18
    ws.merge_cells(f"A{row_sec2}:K{row_sec2}")
    ws[f"A{row_sec2}"] = "TABLE B: QUANTITATIVE TOOL COVERAGE METRICS & STATISTICAL SUMMARY (EXCEL FORMULAS)"
    ws[f"A{row_sec2}"].font = font_section
    ws[f"A{row_sec2}"].fill = fill_dark_navy
    ws[f"A{row_sec2}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[row_sec2].height = 24

    ws.merge_cells(f"A{row_sec2+1}:K{row_sec2+1}")
    ws[f"A{row_sec2+1}"] = "Methodology: Evaluated across all 43 traceable CRA requirements. Excludes Non-Applicable requirements from denominator. Formulas dynamically reference 'CRA Requirements Matrix'."
    ws[f"A{row_sec2+1}"].font = font_subtitle
    ws[f"A{row_sec2+1}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[row_sec2+1].height = 18

    headers_b = [
        "Tool / Activity Name", "Total Applicable Reqs (Denominator)",
        "Full Coverage Count", "Full Coverage %",
        "Partial Coverage Count", "Partial Coverage %",
        "None Coverage Count", "None Coverage %",
        "Direct Technical Contribution %", "Primary Lifecycle Focus",
        "Operational Methodology & Scoping Assumptions"
    ]

    header_row_b = row_sec2 + 2
    ws.row_dimensions[header_row_b].height = 26
    for col_idx, h in enumerate(headers_b, 1):
        cell = ws.cell(row=header_row_b, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header_slate
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin

    tool_col_mapping = [
        ("SonarQube", "Q", "Development, Build and Release", "Automated code quality & SAST gating in CI/CD for first-party code."),
        ("Nexus IQ Lifecycle / CLM", "R", "Development, Build, RUN", "SCA package manager scanning; policy enforcement for open source libraries."),
        ("Penetration Testing", "S", "Development, Build, RUN", "Offensive security verification of running product builds & APIs."),
        ("Vulnerability Scanning (Nessus / Cyberwatch)", "T", "Build, Deployment, RUN", "Infrastructure, OS, daemon, and CIS configuration hardening auditing."),
        ("Data Protection Impact Assessment (DPIA)", "U", "Planning, Development", "GDPR Art 35 privacy assessment; addresses data minimisation & rights."),
        ("Threat Analysis & Risk Analysis (TARA)", "V", "Planning, Design, RUN", "Foundational engineering process deriving Annex VII risk assessment."),
        ("Dependency-Track", "W", "Build, Deployment, RUN", "Continuous SBOM ingestion & post-market vulnerability monitoring."),
        ("Black Duck", "X", "Development, Build, RUN", "Enterprise SCA, binary analysis, and SPDX/CycloneDX SBOM generation."),
        ("Coverity", "Y", "Development, Build", "Deep static analysis for memory safety & defects in C/C++/Java/Go."),
        ("OWASP ZAP / Burp Suite", "Z", "Development, Build, Deployment", "Dynamic application & API security testing against exposed endpoints.")
    ]

    start_data_b = header_row_b + 1
    for idx, (tname, c_letter, l_focus, notes) in enumerate(tool_col_mapping, start=start_data_b):
        ws.row_dimensions[idx].height = 28
        is_zebra = (idx % 2 == 0)
        base_fill = fill_zebra if is_zebra else fill_white

        ws.cell(row=idx, column=1, value=tname).font = font_cell_bold
        ws.cell(row=idx, column=1).alignment = Alignment(horizontal="left", vertical="center")
        ws.cell(row=idx, column=1).fill = base_fill
        ws.cell(row=idx, column=1).border = border_thin

        # Denominator (43)
        ws.cell(row=idx, column=2, value=43).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=idx, column=2).font = font_cell
        ws.cell(row=idx, column=2).fill = base_fill
        ws.cell(row=idx, column=2).border = border_thin

        # Full count formula
        f_formula = f'=COUNTIF(\'CRA Requirements Matrix\'!{c_letter}$4:{c_letter}$46, "Full")'
        cell_full_cnt = ws.cell(row=idx, column=3, value=f_formula)
        cell_full_cnt.alignment = Alignment(horizontal="center", vertical="center")
        cell_full_cnt.font = font_cell_bold
        cell_full_cnt.fill = fill_full
        cell_full_cnt.border = border_thin

        # Full % formula
        cell_full_pct = ws.cell(row=idx, column=4, value=f"=C{idx}/B{idx}")
        cell_full_pct.alignment = Alignment(horizontal="center", vertical="center")
        cell_full_pct.number_format = "0.0%"
        cell_full_pct.font = font_cell_bold
        cell_full_pct.fill = fill_full
        cell_full_pct.border = border_thin

        # Partial count formula
        p_formula = f'=COUNTIF(\'CRA Requirements Matrix\'!{c_letter}$4:{c_letter}$46, "Partial")'
        cell_part_cnt = ws.cell(row=idx, column=5, value=p_formula)
        cell_part_cnt.alignment = Alignment(horizontal="center", vertical="center")
        cell_part_cnt.font = font_cell_bold
        cell_part_cnt.fill = fill_partial
        cell_part_cnt.border = border_thin

        # Partial % formula
        cell_part_pct = ws.cell(row=idx, column=6, value=f"=E{idx}/B{idx}")
        cell_part_pct.alignment = Alignment(horizontal="center", vertical="center")
        cell_part_pct.number_format = "0.0%"
        cell_part_pct.font = font_cell_bold
        cell_part_pct.fill = fill_partial
        cell_part_pct.border = border_thin

        # None count formula
        n_formula = f'=COUNTIF(\'CRA Requirements Matrix\'!{c_letter}$4:{c_letter}$46, "None")'
        cell_none_cnt = ws.cell(row=idx, column=7, value=n_formula)
        cell_none_cnt.alignment = Alignment(horizontal="center", vertical="center")
        cell_none_cnt.font = font_cell
        cell_none_cnt.fill = fill_none
        cell_none_cnt.border = border_thin

        # None % formula
        cell_none_pct = ws.cell(row=idx, column=8, value=f"=G{idx}/B{idx}")
        cell_none_pct.alignment = Alignment(horizontal="center", vertical="center")
        cell_none_pct.number_format = "0.0%"
        cell_none_pct.font = font_cell
        cell_none_pct.fill = fill_none
        cell_none_pct.border = border_thin

        # Direct Technical Contribution %
        cell_contrib = ws.cell(row=idx, column=9, value=f"=(C{idx}+E{idx})/B{idx}")
        cell_contrib.alignment = Alignment(horizontal="center", vertical="center")
        cell_contrib.number_format = "0.0%"
        cell_contrib.font = font_cell_bold
        cell_contrib.fill = base_fill
        cell_contrib.border = border_thin

        # Lifecycle focus
        cell_lf = ws.cell(row=idx, column=10, value=l_focus)
        cell_lf.alignment = Alignment(horizontal="center", vertical="center")
        cell_lf.font = font_cell
        cell_lf.fill = base_fill
        cell_lf.border = border_thin

        # Notes
        cell_notes = ws.cell(row=idx, column=11, value=notes)
        cell_notes.alignment = Alignment(horizontal="left", vertical="center")
        cell_notes.font = font_cell
        cell_notes.fill = base_fill
        cell_notes.border = border_thin

    # Summary Average Row
    summary_row = start_data_b + len(tool_col_mapping)
    ws.row_dimensions[summary_row].height = 30
    
    ws.cell(row=summary_row, column=1, value="Toolchain Average").font = font_cell_bold
    ws.cell(row=summary_row, column=1).alignment = Alignment(horizontal="left", vertical="center")
    ws.cell(row=summary_row, column=1).fill = fill_section_ice
    ws.cell(row=summary_row, column=1).border = border_double_bottom

    ws.cell(row=summary_row, column=2, value=43).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=2).font = font_cell_bold
    ws.cell(row=summary_row, column=2).fill = fill_section_ice
    ws.cell(row=summary_row, column=2).border = border_double_bottom

    ws.cell(row=summary_row, column=3, value=f"=AVERAGE(C{start_data_b}:C{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=3).font = font_cell_bold
    ws.cell(row=summary_row, column=3).number_format = "0.0"
    ws.cell(row=summary_row, column=3).fill = fill_section_ice
    ws.cell(row=summary_row, column=3).border = border_double_bottom

    ws.cell(row=summary_row, column=4, value=f"=AVERAGE(D{start_data_b}:D{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=4).font = font_cell_bold
    ws.cell(row=summary_row, column=4).number_format = "0.0%"
    ws.cell(row=summary_row, column=4).fill = fill_section_ice
    ws.cell(row=summary_row, column=4).border = border_double_bottom

    ws.cell(row=summary_row, column=5, value=f"=AVERAGE(E{start_data_b}:E{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=5).font = font_cell_bold
    ws.cell(row=summary_row, column=5).number_format = "0.0"
    ws.cell(row=summary_row, column=5).fill = fill_section_ice
    ws.cell(row=summary_row, column=5).border = border_double_bottom

    ws.cell(row=summary_row, column=6, value=f"=AVERAGE(F{start_data_b}:F{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=6).font = font_cell_bold
    ws.cell(row=summary_row, column=6).number_format = "0.0%"
    ws.cell(row=summary_row, column=6).fill = fill_section_ice
    ws.cell(row=summary_row, column=6).border = border_double_bottom

    ws.cell(row=summary_row, column=7, value=f"=AVERAGE(G{start_data_b}:G{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=7).font = font_cell_bold
    ws.cell(row=summary_row, column=7).number_format = "0.0"
    ws.cell(row=summary_row, column=7).fill = fill_section_ice
    ws.cell(row=summary_row, column=7).border = border_double_bottom

    ws.cell(row=summary_row, column=8, value=f"=AVERAGE(H{start_data_b}:H{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=8).font = font_cell_bold
    ws.cell(row=summary_row, column=8).number_format = "0.0%"
    ws.cell(row=summary_row, column=8).fill = fill_section_ice
    ws.cell(row=summary_row, column=8).border = border_double_bottom

    ws.cell(row=summary_row, column=9, value=f"=AVERAGE(I{start_data_b}:I{summary_row-1})").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=9).font = font_cell_bold
    ws.cell(row=summary_row, column=9).number_format = "0.0%"
    ws.cell(row=summary_row, column=9).fill = fill_section_ice
    ws.cell(row=summary_row, column=9).border = border_double_bottom

    ws.cell(row=summary_row, column=10, value="Integrated SDLC Toolchain").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=summary_row, column=10).font = font_cell_bold
    ws.cell(row=summary_row, column=10).fill = fill_section_ice
    ws.cell(row=summary_row, column=10).border = border_double_bottom

    ws.cell(row=summary_row, column=11, value="Combined toolchain provides layered Defense-in-Depth across source code, dependencies, and runtime.").alignment = Alignment(horizontal="left", vertical="center")
    ws.cell(row=summary_row, column=11).font = font_cell_bold
    ws.cell(row=summary_row, column=11).fill = fill_section_ice
    ws.cell(row=summary_row, column=11).border = border_double_bottom

    # Freeze Panes at row 6
    ws.freeze_panes = "A6"

    # Widths
    custom_widths = {
        "A": 26, "B": 24, "C": 35, "D": 35, "E": 28, "F": 45,
        "G": 45, "H": 35, "I": 35, "J": 35, "K": 35, "L": 35
    }
    auto_fit_columns(ws, custom_widths=custom_widths)
    print("Sheet 2 built successfully.")
