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
font_kpi_num = Font(name=FONT_FAMILY, size=18, bold=True, color="0F2537")
font_kpi_label = Font(name=FONT_FAMILY, size=8.5, bold=True, color="4A5568")

fill_dark_navy = PatternFill(start_color="0F2537", end_color="0F2537", fill_type="solid")
fill_header_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
fill_header_slate = PatternFill(start_color="2C5282", end_color="2C5282", fill_type="solid")
fill_section_ice = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
fill_card_bg = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

fill_full = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
fill_partial = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
fill_none = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
fill_crit = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
font_crit = Font(name=FONT_FAMILY, size=9, bold=True, color="991B1B")
fill_high = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid")
font_high = Font(name=FONT_FAMILY, size=9, bold=True, color="C2410C")

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
        ws.column_dimensions[col_letter].width = max(12, min(max_len + 3, 45))

def build_executive_dashboard(wb, reqs, tool_profiles, lifecycle_mappings, gaps_roadmap):
    print("Building Sheet 0: Executive Dashboard...")
    ws = wb.create_sheet(title="Executive Dashboard", index=0)
    ws.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws.merge_cells("A1:J1")
    ws["A1"] = "EU CYBER RESILIENCE ACT (REGULATION (EU) 2024/2847) — EXECUTIVE COMPLIANCE DASHBOARD"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[1].height = 25
    
    ws.merge_cells("A2:J2")
    ws["A2"] = "Executive Overview, KPI Scorecards, Toolchain Coverage Metrics & Strategic Roadmap | Baseline: Standard Commercial Product with Digital Elements | October 2026"
    ws["A2"].font = font_subtitle
    ws["A2"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[2].height = 18

    # KPI Block Cards (Row 4-6)
    kpi_configs = [
        ("TOTAL CRA OBLIGATIONS", "=COUNTA('CRA Requirements Matrix'!A4:A46)", "Independently assessable legal requirements", "A", "B"),
        ("MANDATORY OBLIGATIONS", '=COUNTIF(\'CRA Requirements Matrix\'!F4:F46, "*Mandatory*")', "Strict baseline statutory requirements", "C", "C"),
        ("CONDITIONAL CLAUSES", '=COUNTIF(\'CRA Requirements Matrix\'!F4:F46, "*Conditional*")', "Tailored B2B / context-specific clauses", "D", "D"),
        ("ARTICLE 14 REPORTING DUTY", "LIVE (11 Sept 2026)", "MANDATORY & ENFORCEABLE RIGHT NOW", "E", "F"),
        ("CRITICAL REMEDIATION GAPS", '=COUNTIF(\'CRA Requirements Matrix\'!AC4:AC46, "Critical*")', "Immediate compliance priority items", "G", "H"),
        ("RESIDUAL GOVERNANCE GAPS", "=COUNTA('Compliance Gaps & Roadmap'!A4:A23)", "Gaps requiring non-tool policies / legal SOPs", "I", "J")
    ]

    ws.row_dimensions[4].height = 16
    ws.row_dimensions[5].height = 28
    ws.row_dimensions[6].height = 16

    for title, formula_val, desc, col_start, col_end in kpi_configs:
        c1, c2 = f"{col_start}4", f"{col_end}4"
        c3, c4 = f"{col_start}5", f"{col_end}5"
        c5, c6 = f"{col_start}6", f"{col_end}6"
        
        if col_start != col_end:
            ws.merge_cells(f"{c1}:{c2}")
            ws.merge_cells(f"{c3}:{c4}")
            ws.merge_cells(f"{c5}:{c6}")
        
        cell_lbl = ws[c1]
        cell_lbl.value = title
        cell_lbl.font = font_kpi_label
        cell_lbl.alignment = Alignment(horizontal="center", vertical="center")
        cell_lbl.fill = fill_card_bg
        cell_lbl.border = Border(top=Side(style="medium", color="0F2537"), left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"))
        
        cell_val = ws[c3]
        cell_val.value = formula_val
        cell_val.font = font_kpi_num
        cell_val.alignment = Alignment(horizontal="center", vertical="center")
        cell_val.fill = fill_card_bg
        cell_val.border = Border(left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"))
        if title == "ARTICLE 14 REPORTING DUTY":
            cell_val.font = Font(name=FONT_FAMILY, size=13, bold=True, color="991B1B")
            cell_val.fill = fill_crit
        elif title == "CRITICAL REMEDIATION GAPS":
            cell_val.font = Font(name=FONT_FAMILY, size=18, bold=True, color="991B1B")
            cell_val.fill = fill_crit

        cell_desc = ws[c5]
        cell_desc.value = desc
        cell_desc.font = Font(name=FONT_FAMILY, size=7.5, italic=True, color="64748B")
        cell_desc.alignment = Alignment(horizontal="center", vertical="center")
        cell_desc.fill = fill_card_bg
        cell_desc.border = Border(bottom=Side(style="medium", color="0F2537"), left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"))

    # Section 1: Executive Summary
    curr_row = 8
    ws.merge_cells(f"A{curr_row}:J{curr_row}")
    ws[f"A{curr_row}"] = "1. EXECUTIVE REGULATORY CONTEXT & STRATEGIC MANDATE"
    ws[f"A{curr_row}"].font = font_section
    ws[f"A{curr_row}"].fill = fill_dark_navy
    ws[f"A{curr_row}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[curr_row].height = 22
    curr_row += 1

    narrative = (
        "On 20 November 2024, the European Union published Regulation (EU) 2024/2847 (Cyber Resilience Act — CRA; OJ L, 2024/2847), "
        "establishing a mandatory horizontal regulatory framework for products with digital elements (PDEs) placed on the EU single market. "
        "Unlike voluntary security certifications (ISO 27001, SOC 2), the CRA enforces direct product-level essential requirements (Annex I), "
        "continuous vulnerability handling, and statutory administrative fines of up to €15,000,000 or 2.5% of global turnover.\n\n"
        "CRITICAL ENFORCEMENT TIMELINE DISTINCTION (AS OF OCTOBER 2026):\n"
        "• LIVE TODAY (Statutory Duty since 11 September 2026): Article 14 incident and actively exploited vulnerability reporting is fully live and "
        "enforceable right now via the ENISA Single Reporting Platform (SRP). It applies retroactively to all products currently in use on the EU market.\n"
        "• TARGET DATE (11 December 2027): General application of Annex I essential requirements, conformity assessment (Module A/B/C/H), CE marking, "
        "and technical documentation (Annex VII) becomes mandatory for all market placements.\n\n"
        "CORE ARCHITECTURAL FINDING:\n"
        "Automated security tools (SAST, SCA, DAST, Container Scanning) provide vital technical detection and evidence generation for ~28% of CRA requirements. "
        "However, more than 50% of CRA obligations represent non-tool organizational, legal, and operational duties—including statutory CSIRT reporting, "
        "Coordinated Vulnerability Disclosure (CVD), minimum 5-year support periods, 10-year update archives, Annex VII dossiers, and EU Declarations of Conformity."
    )
    ws.merge_cells(f"A{curr_row}:J{curr_row+4}")
    ws[f"A{curr_row}"] = narrative
    ws[f"A{curr_row}"].font = font_cell
    ws[f"A{curr_row}"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws[f"A{curr_row}"].fill = fill_white
    for r in range(curr_row, curr_row+5):
        for c in range(1, 11):
            ws.cell(row=r, column=c).border = border_thin
    curr_row += 6

    # Section 2: Security Toolchain Scorecard Rollup
    ws.merge_cells(f"A{curr_row}:J{curr_row}")
    ws[f"A{curr_row}"] = "2. SECURITY TOOLCHAIN COVERAGE SCORECARD (DYNAMIC SYNCHRONIZATION WITH SHEET 2)"
    ws[f"A{curr_row}"].font = font_section
    ws[f"A{curr_row}"].fill = fill_dark_navy
    ws[f"A{curr_row}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[curr_row].height = 22
    curr_row += 1

    headers_sc = [
        "Security Tool / Activity", "Tool Category", "Total Reqs",
        "Full Coverage", "Full %", "Partial Coverage", "Partial %",
        "Direct Tech Contribution %", "None % (Gaps)", "Primary Lifecycle Phase Focus"
    ]
    ws.row_dimensions[curr_row].height = 24
    for c_idx, h in enumerate(headers_sc, 1):
        cell = ws.cell(row=curr_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header_slate
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin
    curr_row += 1

    for t_idx in range(10):
        src_row = 21 + t_idx
        ws.row_dimensions[curr_row].height = 22
        is_zebra = (t_idx % 2 == 0)
        base_fill = fill_zebra if is_zebra else fill_white

        c1 = ws.cell(row=curr_row, column=1, value=f"='Tool Coverage Summary'!A{src_row}")
        c1.font = font_cell_bold
        c1.alignment = Alignment(horizontal="left", vertical="center")
        c1.fill = base_fill
        c1.border = border_thin

        c2 = ws.cell(row=curr_row, column=2, value=f"='Tool Coverage Summary'!B{src_row}")
        c2.font = font_cell
        c2.alignment = Alignment(horizontal="center", vertical="center")
        c2.fill = base_fill
        c2.border = border_thin

        c3 = ws.cell(row=curr_row, column=3, value=f"='Tool Coverage Summary'!B{src_row}")
        c3.font = font_cell
        c3.alignment = Alignment(horizontal="center", vertical="center")
        c3.fill = base_fill
        c3.border = border_thin

        c4 = ws.cell(row=curr_row, column=4, value=f"='Tool Coverage Summary'!C{src_row}")
        c4.font = font_cell_bold
        c4.alignment = Alignment(horizontal="center", vertical="center")
        c4.fill = fill_full
        c4.border = border_thin

        c5 = ws.cell(row=curr_row, column=5, value=f"='Tool Coverage Summary'!D{src_row}")
        c5.font = font_cell_bold
        c5.number_format = "0.0%"
        c5.alignment = Alignment(horizontal="center", vertical="center")
        c5.fill = fill_full
        c5.border = border_thin

        c6 = ws.cell(row=curr_row, column=6, value=f"='Tool Coverage Summary'!E{src_row}")
        c6.font = font_cell_bold
        c6.alignment = Alignment(horizontal="center", vertical="center")
        c6.fill = fill_partial
        c6.border = border_thin

        c7 = ws.cell(row=curr_row, column=7, value=f"='Tool Coverage Summary'!F{src_row}")
        c7.font = font_cell_bold
        c7.number_format = "0.0%"
        c7.alignment = Alignment(horizontal="center", vertical="center")
        c7.fill = fill_partial
        c7.border = border_thin

        c8 = ws.cell(row=curr_row, column=8, value=f"='Tool Coverage Summary'!I{src_row}")
        c8.font = font_cell_bold
        c8.number_format = "0.0%"
        c8.alignment = Alignment(horizontal="center", vertical="center")
        c8.fill = base_fill
        c8.border = border_thin

        c9 = ws.cell(row=curr_row, column=9, value=f"='Tool Coverage Summary'!H{src_row}")
        c9.font = font_cell
        c9.number_format = "0.0%"
        c9.alignment = Alignment(horizontal="center", vertical="center")
        c9.fill = fill_none
        c9.border = border_thin

        c10 = ws.cell(row=curr_row, column=10, value=f"='Tool Coverage Summary'!J{src_row}")
        c10.font = font_cell
        c10.alignment = Alignment(horizontal="center", vertical="center")
        c10.fill = base_fill
        c10.border = border_thin

        curr_row += 1

    # Scorecard Average Row
    ws.row_dimensions[curr_row].height = 25
    c_avg1 = ws.cell(row=curr_row, column=1, value="Toolchain Portfolio Average")
    c_avg1.font = font_cell_bold
    c_avg1.alignment = Alignment(horizontal="left", vertical="center")
    c_avg1.fill = fill_section_ice
    c_avg1.border = border_double_bottom

    ws.cell(row=curr_row, column=2, value="Multi-Layered").font = font_cell_bold
    ws.cell(row=curr_row, column=2).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=2).fill = fill_section_ice
    ws.cell(row=curr_row, column=2).border = border_double_bottom

    ws.cell(row=curr_row, column=3, value=43).font = font_cell_bold
    ws.cell(row=curr_row, column=3).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=3).fill = fill_section_ice
    ws.cell(row=curr_row, column=3).border = border_double_bottom

    ws.cell(row=curr_row, column=4, value=f"=AVERAGE(D{curr_row-10}:D{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=4).number_format = "0.0"
    ws.cell(row=curr_row, column=4).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=4).fill = fill_section_ice
    ws.cell(row=curr_row, column=4).border = border_double_bottom

    ws.cell(row=curr_row, column=5, value=f"=AVERAGE(E{curr_row-10}:E{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=5).number_format = "0.0%"
    ws.cell(row=curr_row, column=5).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=5).fill = fill_section_ice
    ws.cell(row=curr_row, column=5).border = border_double_bottom

    ws.cell(row=curr_row, column=6, value=f"=AVERAGE(F{curr_row-10}:F{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=6).number_format = "0.0"
    ws.cell(row=curr_row, column=6).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=6).fill = fill_section_ice
    ws.cell(row=curr_row, column=6).border = border_double_bottom

    ws.cell(row=curr_row, column=7, value=f"=AVERAGE(G{curr_row-10}:G{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=7).number_format = "0.0%"
    ws.cell(row=curr_row, column=7).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=7).fill = fill_section_ice
    ws.cell(row=curr_row, column=7).border = border_double_bottom

    ws.cell(row=curr_row, column=8, value=f"=AVERAGE(H{curr_row-10}:H{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=8).number_format = "0.0%"
    ws.cell(row=curr_row, column=8).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=8).fill = fill_section_ice
    ws.cell(row=curr_row, column=8).border = border_double_bottom

    ws.cell(row=curr_row, column=9, value=f"=AVERAGE(I{curr_row-10}:I{curr_row-1})").font = font_cell_bold
    ws.cell(row=curr_row, column=9).number_format = "0.0%"
    ws.cell(row=curr_row, column=9).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=9).fill = fill_section_ice
    ws.cell(row=curr_row, column=9).border = border_double_bottom

    ws.cell(row=curr_row, column=10, value="Integrated SDLC Toolchain").font = font_cell_bold
    ws.cell(row=curr_row, column=10).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=curr_row, column=10).fill = fill_section_ice
    ws.cell(row=curr_row, column=10).border = border_double_bottom
    curr_row += 2

    # Section 3: Lifecycle Phase Readiness Breakdown
    ws.merge_cells(f"A{curr_row}:J{curr_row}")
    ws[f"A{curr_row}"] = "3. LIFECYCLE PHASE READINESS & CONTROL GATE ROLLUP"
    ws[f"A{curr_row}"].font = font_section
    ws[f"A{curr_row}"].fill = fill_dark_navy
    ws[f"A{curr_row}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[curr_row].height = 22
    curr_row += 1

    headers_lc = [
        "Lifecycle Phase", "Mandatory Action Count", "Key Governance Gates",
        "Primary Supporting Tools / Processes", "Mandatory Regulatory Deliverables",
        "Estimated Toolchain Coverage Level", "Residual Governance Gap Areas",
        "Lead Responsible Stakeholders", "Statutory Deadline Cadence", "Audit Risk Level"
    ]
    ws.row_dimensions[curr_row].height = 24
    for c_idx, h in enumerate(headers_lc, 1):
        cell = ws.cell(row=curr_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header_slate
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin
    curr_row += 1

    lc_summary_data = [
        ("Presales and Product Planning", "6 Actions", "Gate 0 (Scope) & Gate 1 (Claims)", "TARA, Scope Questionnaire, OpenSSF", "Classification Record, 5-Yr Support Statement", "Low (~15% - Analytical / Business)", "Product classification, support pricing, marketing gating", "Presales Lead, Product VP, Legal", "Prior to bid / proposal", "High"),
        ("Development", "12 Actions", "Sprint Security Gates & DPIA Approval", "Coverity, SonarQube, TARA, DPIA", "Threat Model, IAM Matrix, Crypto Spec, DPIA", "Medium (~50% - SAST / DAST)", "Living risk updates, data minimisation, secure defaults", "Lead Architect, DevSecOps Lead", "Daily / Sprint cadence", "Medium"),
        ("Build and Release", "8 Actions", "Build Gates 1-3 & Release Gates 1-5", "Black Duck, Nexus IQ, Sigstore, Pentest", "CycloneDX SBOM, Pentest Report, VEX Record", "High (~75% - Automated SCA/SAST)", "HSM code signing, release gating, CAB substantial checks", "DevSecOps Lead, Release Manager", "Per release build", "High"),
        ("Deployment and Delivery", "8 Actions", "Compliance Gates 1-2 & Delivery Gate", "Annex VII Builder, EU DoC Workflow", "Annex VII Dossier, Signed EU DoC, CE Mark", "Low (~10% - Pure Legal/Conformity)", "Dossier assembly, DoC execution, 10-yr compliance vault", "CEO, Compliance Officer, Quality", "Prior to first customer ship", "Critical"),
        ("Maintenance and RUN", "10 Actions", "Operational Gates & Statutory Clocks", "Dependency-Track, Cyberwatch, ENISA SRP", "Article 14 CSIRT Reports, CSAF Advisories", "Medium (~40% - Continuous CVEs)", "24h/72h ENISA SRP filings, 10-yr patch archive, CVD inbox", "CISO, PSIRT Lead, Legal Counsel", "Continuous (24h/72h statutory)", "Critical")
    ]

    for p_name, a_cnt, g_cnt, t_sup, deliv, cov, gaps_desc, owners, timing, risk in lc_summary_data:
        ws.row_dimensions[curr_row].height = 30
        vals = [p_name, a_cnt, g_cnt, t_sup, deliv, cov, gaps_desc, owners, timing, risk]
        for c_idx, val in enumerate(vals, 1):
            cell = ws.cell(row=curr_row, column=c_idx, value=val)
            cell.font = font_cell
            cell.border = border_thin
            if c_idx == 1:
                cell.font = font_cell_bold
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 10:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if val == "Critical":
                    cell.fill = fill_crit
                    cell.font = font_crit
                elif val == "High":
                    cell.fill = fill_high
                    cell.font = font_high
            else:
                cell.alignment = Alignment(horizontal="center" if c_idx in [2, 3, 6, 9] else "left", vertical="center", wrap_text=True)
        curr_row += 1

    curr_row += 1
    # Section 4: Strategic Recommendations
    ws.merge_cells(f"A{curr_row}:J{curr_row}")
    ws[f"A{curr_row}"] = "4. STRATEGIC COMPLIANCE ROADMAP RECOMMENDATIONS FOR CISO & ARCHITECTS"
    ws[f"A{curr_row}"].font = font_section
    ws[f"A{curr_row}"].fill = fill_dark_navy
    ws[f"A{curr_row}"].alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[curr_row].height = 22
    curr_row += 1

    recs = [
        ("1. IMMEDIATE ACTION (LIVE STATUTORY DUTY — Q4 2026)",
         "Operationalize Article 14 Reporting Runbook immediately. Ensure corporate ENISA Single Reporting Platform (SRP) accounts are active with Primary/Secondary Assigned Representatives (EU Login / FIDO2). Train PSIRT on the 24h Early Warning, 72h Notification, and 14-day Final Report statutory clocks. Deploy RFC 9116 security.txt on all web properties."),
        ("2. SDLC TOOLCHAIN INTEGRATION & GATING (H1 2027)",
         "Integrate automated SBOM generation (CycloneDX/SPDX) into CI/CD pipelines using Black Duck / Nexus IQ and connect to Dependency-Track for continuous post-market monitoring. Enforce Quality Gates in SonarQube/Coverity breaking builds on unresolved Critical vulnerabilities. Deploy HSM-backed artifact signing (Sigstore/Cosign)."),
        ("3. CONFORMITY ASSESSMENT & CE MARKING DOSSIER (H2 2027)",
         "Compile the formal Annex VII Technical Documentation Dossier consolidating threat models (TARA), risk assessments, test reports, and SBOMs. If product is Important Class I/II under IR (EU) 2025/2392, engage accredited Notified Body immediately. Finalize Annex II user security guides, execute signed EU DoC, and affix CE mark prior to 11 Dec 2027.")
    ]

    for title_r, text_r in recs:
        ws.merge_cells(f"A{curr_row}:B{curr_row}")
        ws[f"A{curr_row}"] = title_r
        ws[f"A{curr_row}"].font = font_cell_bold
        ws[f"A{curr_row}"].alignment = Alignment(horizontal="left", vertical="top")
        ws[f"A{curr_row}"].fill = fill_section_ice
        ws[f"A{curr_row}"].border = border_thin
        ws.cell(row=curr_row, column=2).border = border_thin

        ws.merge_cells(f"C{curr_row}:J{curr_row}")
        ws[f"C{curr_row}"] = text_r
        ws[f"C{curr_row}"].font = font_cell
        ws[f"C{curr_row}"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws.row_dimensions[curr_row].height = 36
        for c in range(3, 11):
            ws.cell(row=curr_row, column=c).border = border_thin
        curr_row += 1

    # Freeze Panes
    ws.freeze_panes = "A4"

    # Widths
    custom_widths = {
        "A": 26, "B": 22, "C": 14, "D": 14, "E": 14, "F": 16,
        "G": 14, "H": 22, "I": 15, "J": 30
    }
    auto_fit_columns(ws, custom_widths=custom_widths)
    print("Executive Dashboard built successfully.")
