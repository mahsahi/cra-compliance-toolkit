# CRA Delivered Systems & CRA Object Register Template
**Document Ref:** `REG-TEMPLATE-v1.0`  
**Governing Standard:** `SEC-PRO-CRA-001` §3 · Reg (EU) 2024/2847 Art. 13(1), 13(5), 13(8), 14  
**Operational Objective:** Fulfill Section 10 Actions 4 & 5 of the MYBU Procedure (System Register & SBOM Inventory)

---

## 1. Overview & Regulatory Purpose

Under the EU Cyber Resilience Act (CRA), a solution provider or manufacturer cannot meet the 24-hour Article 14 incident reporting window or conduct rapid reachability triage without an up-to-date **System of Record** mapping every delivered product, hardware SKU, operating software version, customer environment, and Software Bill of Materials (SBOM).

This register serves as the authoritative inventory to answer within minutes:
1. *Did we supply this product?* (Question 1)
2. *Are we the manufacturer or system integrator?* (Question 2)
3. *What exact firmware/OS build is running in customer environments?* (Question 4)
4. *Which EU Member States have active customer deployments?* (SRP Early Warning Field)
5. *Which Lead CSIRT has geographic jurisdiction over our legal entity?*

---

## 2. Delivered Systems Master Schema

Each product or system delivered to customers must be registered with the following mandatory attributes:

| Field | Description & Syntax | Regulatory Citation |
|---|---|---|
| `system_id` | Unique internal asset identifier (e.g., `SYS-MYBU-SEG5000`) | Art. 13(1) |
| `commercial_name` | Public marketing & contract name (e.g., *SecureEdge Gateway 5000*) | Art. 13(14) |
| `product_type` | `hardware_appliance` \| `embedded_system` \| `on_prem_software` \| `hybrid_edge` | Annex I |
| `cra_risk_tier` | `default` (Module A) \| `class_i` (Annex III) \| `class_ii` (Annex IV) | Art. 7, 8, Annex III/IV |
| `manufacturer_entity` | Name of European Corporate Legal Entity placing the product on the market | Art. 3(21), 13(14) |
| `legal_entity_vat_eori` | VAT / EORI number of the European manufacturer entity | Art. 13(14) |
| `lead_csirt` | Designated Lead CSIRT (e.g., `CSIRT-IE`, `NCSC-NL`, `BSI-DE`) | Art. 14(3), 14(7) |
| `market_placement_date` | First date placed on the European market (`YYYY-MM-DD`) | Art. 3(22) |
| `support_end_date` | End of support & patch obligation period (minimum 5 years from placement) | Art. 13(8) |
| `current_firmware_version` | Active supported firmware / application release (e.g., `v3.4.0`) | Art. 13(10) |
| `sbom_uri` | Canonical link to CycloneDX 1.6 / SPDX 3.0 SBOM repository | Art. 13(5), Annex VII |
| `customer_deployments` | List of customers, installation environments, and EU Member States | Art. 14(2)(a) |
| `external_interfaces` | List of external network ports, protocols, and ingress paths | Annex I Part I |
| `responsible_blco` | Name and 24/7 contact of Business Line Compliance Officer | §5 MYBU Proc |
| `technical_psirt_lead` | Name and contact of designated product security lead | §5 MYBU Proc |

---

## 3. Machine-Readable JSON Schema (`cra_systems_register.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CRA Delivered Systems Register",
  "type": "object",
  "required": ["registry_version", "business_unit", "updated_utc", "systems"],
  "properties": {
    "registry_version": { "type": "string" },
    "business_unit": { "type": "string" },
    "updated_utc": { "type": "string", "format": "date-time" },
    "systems": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "system_id",
          "commercial_name",
          "cra_risk_tier",
          "manufacturer_entity",
          "lead_csirt",
          "support_end_date",
          "current_firmware_version",
          "sbom_uri",
          "member_states_deployed"
        ],
        "properties": {
          "system_id": { "type": "string" },
          "commercial_name": { "type": "string" },
          "cra_risk_tier": { "type": "string", "enum": ["default", "class_i", "class_ii", "critical"] },
          "manufacturer_entity": { "type": "string" },
          "legal_entity_vat": { "type": "string" },
          "lead_csirt": { "type": "string" },
          "support_end_date": { "type": "string", "format": "date" },
          "current_firmware_version": { "type": "string" },
          "sbom_uri": { "type": "string" },
          "member_states_deployed": {
            "type": "array",
            "items": { "type": "string", "minLength": 2, "maxLength": 2 }
          },
          "customers": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "customer_name": { "type": "string" },
                "deployment_id": { "type": "string" },
                "country": { "type": "string" },
                "installed_firmware": { "type": "string" },
                "emergency_contact": { "type": "string" }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## 4. Maintenance & Continuous Update SOP

1. **New Product Delivery**: Upon executing customer handoff / acceptance or first shipment, the Project Manager / SDM must file a System Registration Ticket with the BLCO within 5 business days.
2. **Firmware / Patch Release**: Every OTA release, maintenance patch, or hotfix automatically updates the `current_firmware_version` and SBOM pointer via the CI/CD pipeline gate.
3. **Decommissioning & End of Support**: When a system reaches `support_end_date`, formal customer notification is preserved for 10 years, and the status changes to `archived_supported_closed`.
