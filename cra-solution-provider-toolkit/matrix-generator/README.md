# CRA Matrix Workbook Generator Engine

This directory contains the Python generation pipeline that compiles the **CRA Compliance Requirements and Security Tool Coverage Matrix** Excel workbook (`CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix.xlsx`).

---

## 🛠️ Architecture & Pipeline Flow

The build engine uses `openpyxl` with strict typography, cell styling, palette themes, and Excel formula generation:

```
all_reqs.json (43 Requirements across 31 Columns)
tool_profiles.json (10 Security Tools / Activities Analysis)
lifecycle_mappings.json (44 Lifecycle Controls & Approval Gates)
gaps_roadmap.json (20 Governance & Policy Compliance Gaps)
sources_data.json (Statutory References, Harmonised Standards, Assumptions)
                    │
                    ▼
          run_complete_build.py
                    │
      ┌─────────────┼─────────────┬─────────────┬─────────────┐
      ▼             ▼             ▼             ▼             ▼
cra_dashboard.py  cra_sheet1.py cra_sheet2.py cra_sheet3.py cra_sheet4.py cra_sheet5.py
(Sheet 0: Exec)   (Sheet 1: Reqs)(Sheet 2: Tools)(Sheet 3: SDLC)(Sheet 4: Gaps)(Sheet 5: Refs)
                    │
                    ▼
CRA_Compliance_Requirements_and_Security_Tool_Coverage_Matrix.xlsx
```

---

## 🚀 How to Run

To regenerate or modify the Excel matrix workbook:

```bash
# Ensure openpyxl is installed
pip install openpyxl

# Run the complete workbook compilation
python3 run_complete_build.py
```

The output workbook will be generated in this directory and can be copied to the toolkit root.
