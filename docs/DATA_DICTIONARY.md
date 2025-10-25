# SAP SD Sales Analytics - Data Dictionary

## Overview

This document provides detailed field-level descriptions for all SAP SD tables included in the analytics platform.

---

## Master Data Tables

### Customer Master

#### KNA1 - Customer Master General

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| KUNNR | CHAR | 10 | Customer Number (Primary Key) | 0000100234 |
| NAME1 | CHAR | 35 | Customer Name | Acme Industrial Corp |
| LAND1 | CHAR | 3 | Country Key | US |
| PSTLZ | CHAR | 10 | Postal Code | 10001 |
| ORT01 | CHAR | 35 | City | New York |
| STRAS | CHAR | 35 | Street Address | 123 Main Street |
| KTOKD | CHAR | 4 | Customer Account Group | 0001 |
| BRSCH | CHAR | 4 | Industry Sector | 1200 |
| ERDAT | DATS | 8 | Date Created | 20240115 |
| LOEVM | CHAR | 1 | Deletion Flag | (blank=active) |

**Business Rules:**
- KUNNR is unique across all customers
- KTOKD determines customer type: 0001=Standard, 0002=Key Account, 0003=Export
- BRSCH codes: 1200=Manufacturing, 2900=Retail, 5100=Distribution, 7100=Technology

#### KNVV - Customer Sales Data

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| KUNNR | CHAR | 10 | Customer Number (FK → KNA1) | 0000100234 |
| VKORG | CHAR | 4 | Sales Organization (FK → TVKO) | 1000 |
| VTWEG | CHAR | 2 | Distribution Channel (FK → TVTW) | 10 |
| SPART | CHAR | 2 | Division (FK → TSPA) | 00 |
| KDGRP | CHAR | 2 | Customer Group | 01 |
| WAERS | CUKY | 5 | Currency | USD |
| KALKS | CHAR | 1 | Pricing Procedure | 1 |
| VSBED | CHAR | 2 | Shipping Conditions | 01 |
| LPRIO | CHAR | 2 | Delivery Priority | 01 |

**Primary Key:** KUNNR + VKORG + VTWEG + SPART

**Business Rules:**
- One customer can have multiple sales org combinations
- Currency should align with sales org country
- Shipping conditions determine delivery SLA

#### KNB1 - Customer Company Code Data

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| KUNNR | CHAR | 10 | Customer Number (FK → KNA1) | 0000100234 |
| BUKRS | CHAR | 4 | Company Code (FK → T001) | 1000 |
| AKONT | CHAR | 10 | Reconciliation Account | 140000 |
| ZTERM | CHAR | 4 | Payment Terms | Z030 |
| FDGRV | CHAR | 10 | Planning Group | |

**Primary Key:** KUNNR + BUKRS

**Business Rules:**
- AKONT is the GL account for customer receivables
- ZTERM defines payment due date (e.g., Z030 = Net 30 days)

#### KNVP - Customer Partner Functions

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| KUNNR | CHAR | 10 | Customer Number | 0000100234 |
| VKORG | CHAR | 4 | Sales Organization | 1000 |
| VTWEG | CHAR | 2 | Distribution Channel | 10 |
| SPART | CHAR | 2 | Division | 00 |
| PARVW | CHAR | 2 | Partner Function | AG |
| KUNN2 | CHAR | 10 | Customer Number of Partner | 0000100234 |

**Primary Key:** KUNNR + VKORG + VTWEG + SPART + PARVW

**Partner Functions:**
- AG = Sold-to Party
- WE = Ship-to Party
- RE = Bill-to Party
- RG = Payer

---

### Material Master

#### MARA - Material General Data

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| MATNR | CHAR | 18 | Material Number (Primary Key) | 000000000000012345 |
| MTART | CHAR | 4 | Material Type | FERT |
| MATKL | CHAR | 9 | Material Group (FK → T023) | ELEC |
| MEINS | UNIT | 3 | Base Unit of Measure | EA |
| MTPOS_MARA | CHAR | 4 | Item Category Group | NORM |
| PRDHA | CHAR | 18 | Product Hierarchy | 000000000000000001 |
| ERNAM | CHAR | 12 | Created By | SYSUSER |
| ERSDA | DATS | 8 | Creation Date | 20230515 |
| LAEDA | DATS | 8 | Last Change Date | 20240915 |

**Material Types:**
- FERT = Finished Product
- HAWA = Trading Goods
- ROH = Raw Material

#### MARC - Material Plant Data

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| MATNR | CHAR | 18 | Material Number (FK → MARA) | 000000000000012345 |
| WERKS | CHAR | 4 | Plant | 1000 |
| PSTAT | CHAR | 15 | Maintenance Status | KE |
| LVORM | CHAR | 1 | Deletion Flag | |
| DISMM | CHAR | 2 | MRP Type | PD |
| DISPO | CHAR | 3 | MRP Controller | 001 |
| EKGRP | CHAR | 3 | Purchasing Group | 001 |

**Primary Key:** MATNR + WERKS

#### MAKT - Material Descriptions

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| MATNR | CHAR | 18 | Material Number (FK → MARA) | 000000000000012345 |
| SPRAS | LANG | 1 | Language Key | E |
| MAKTX | CHAR | 40 | Material Description | Widget Pro Standard 1234 |

**Primary Key:** MATNR + SPRAS

**Language Codes:**
- E = English
- D = German
- F = French

#### MVKE - Material Sales Data

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| MATNR | CHAR | 18 | Material Number | 000000000000012345 |
| VKORG | CHAR | 4 | Sales Organization | 1000 |
| VTWEG | CHAR | 2 | Distribution Channel | 10 |
| MVGR1 | CHAR | 3 | Material Group 1 | 01 |
| KONDM | CHAR | 2 | Material Pricing Group | 01 |
| KTGRM | CHAR | 2 | Account Assignment Group | 01 |

**Primary Key:** MATNR + VKORG + VTWEG

---

### Organizational Structures

#### T001 - Company Codes

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| BUKRS | CHAR | 4 | Company Code (Primary Key) | 1000 |
| BUTXT | CHAR | 25 | Company Name | US Company Inc. |
| WAERS | CUKY | 5 | Currency | USD |
| LAND1 | CHAR | 3 | Country | US |

#### TVKO - Sales Organizations

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VKORG | CHAR | 4 | Sales Organization (Primary Key) | 1000 |
| VTEXT | CHAR | 20 | Description | US Sales Org |
| BUKRS | CHAR | 4 | Company Code (FK → T001) | 1000 |

#### TVTW - Distribution Channels

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VTWEG | CHAR | 2 | Distribution Channel (Primary Key) | 10 |
| VTEXT | CHAR | 20 | Description | Direct Sales |

**Common Values:**
- 10 = Direct Sales
- 20 = Wholesale
- 30 = E-Commerce

#### TSPA - Divisions

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| SPART | CHAR | 2 | Division (Primary Key) | 00 |
| VTEXT | CHAR | 20 | Description | Cross-Division |

---

## Transaction Data Tables

### Sales Orders

#### VBAK - Sales Document Header

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number (Primary Key) | 0000001234 |
| ERDAT | DATS | 8 | Date Created | 20240115 |
| ERZET | TIMS | 6 | Time Created | 143000 |
| ERNAM | CHAR | 12 | Created By | SALESUSER |
| AEDAT | DATS | 8 | Date Changed | 20240115 |
| AUDAT | DATS | 8 | Document Date | 20240115 |
| VBTYP | CHAR | 1 | Document Category | C |
| AUART | CHAR | 4 | Order Type | OR |
| VKORG | CHAR | 4 | Sales Organization | 1000 |
| VTWEG | CHAR | 2 | Distribution Channel | 10 |
| SPART | CHAR | 2 | Division | 00 |
| KUNNR | CHAR | 10 | Sold-to Party (FK → KNA1) | 0000100234 |
| VKBUR | CHAR | 4 | Sales Office | 10001 |
| VKGRP | CHAR | 3 | Sales Group | 001 |
| NETWR | CURR | 15,2 | Net Value | 12450.00 |
| WAERK | CUKY | 5 | Currency | USD |
| GBSTK | CHAR | 1 | Overall Processing Status | B |
| ABSTK | CHAR | 1 | Rejection Status | |
| LIFSK | CHAR | 2 | Delivery Block | |
| FAKSK | CHAR | 2 | Billing Block | |

**Order Types:**
- OR = Standard Order
- ZOR = Rush Order
- QT = Quotation

**Status Values (GBSTK):**
- A = Fully Processed
- B = Partially Processed
- C = Not Processed

#### VBAP - Sales Document Item

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number (FK → VBAK) | 0000001234 |
| POSNR | NUMC | 6 | Item Number | 000010 |
| MATNR | CHAR | 18 | Material Number (FK → MARA) | 000000000000012345 |
| ARKTX | CHAR | 40 | Item Description | Widget A Standard |
| KWMENG | QUAN | 15,3 | Order Quantity | 100.000 |
| VRKME | UNIT | 3 | Sales Unit | EA |
| UMVKZ | DEC | 5 | Numerator for Conversion | 1 |
| UMVKN | DEC | 5 | Denominator for Conversion | 1 |
| NETPR | CURR | 11,2 | Net Price | 50.00 |
| NETWR | CURR | 15,2 | Net Value | 5000.00 |
| WAERK | CUKY | 5 | Currency | USD |
| WERKS | CHAR | 4 | Plant | 1000 |
| LGORT | CHAR | 4 | Storage Location | 0001 |
| PSTYV | CHAR | 4 | Item Category | TAN |
| ERDAT | DATS | 8 | Creation Date | 20240115 |
| ABGRU | CHAR | 2 | Rejection Reason | |

**Primary Key:** VBELN + POSNR

**Business Rules:**
- NETWR = KWMENG × NETPR
- Order total in VBAK.NETWR = SUM(VBAP.NETWR)

#### VBUK - Sales Document Header Status

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number (Primary Key) | 0000001234 |
| LFSTK | CHAR | 1 | Delivery Status | B |
| FKSTK | CHAR | 1 | Billing Status | B |
| GBSTK | CHAR | 1 | Overall Status | B |
| ABSTK | CHAR | 1 | Rejection Status | |
| LFGSK | CHAR | 1 | Delivery Status Overall | B |
| CMGST | CHAR | 1 | Credit Check Status | A |

**Status Codes:**
- A = Fully Processed
- B = Partially Processed
- C = Not Yet Processed

#### VBUP - Sales Item Status

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number | 0000001234 |
| POSNR | NUMC | 6 | Item Number | 000010 |
| LFSTA | CHAR | 1 | Delivery Status | B |
| FKSTA | CHAR | 1 | Billing Status | B |
| GBSTA | CHAR | 1 | Overall Processing Status | B |
| ABSTA | CHAR | 1 | Rejection Status | |
| LFGSA | CHAR | 1 | Total Delivery Status | B |
| WBSTA | CHAR | 1 | Goods Movement Status | B |

**Primary Key:** VBELN + POSNR

#### VBEP - Sales Schedule Lines

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number | 0000001234 |
| POSNR | NUMC | 6 | Item Number | 000010 |
| ETENR | NUMC | 4 | Schedule Line Number | 0001 |
| EDATU | DATS | 8 | Requested Delivery Date | 20240120 |
| BMENG | QUAN | 15,3 | Confirmed Quantity | 100.000 |
| VRKME | UNIT | 3 | Sales Unit | EA |
| ERDAT | DATS | 8 | Creation Date | 20240115 |

**Primary Key:** VBELN + POSNR + ETENR

---

### Deliveries

#### LIKP - Delivery Header

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Delivery Number (Primary Key) | 8000001234 |
| ERNAM | CHAR | 12 | Created By | WHSUSER |
| ERDAT | DATS | 8 | Creation Date | 20240118 |
| ERZET | TIMS | 6 | Creation Time | 100000 |
| WADAT_IST | DATS | 8 | Actual Goods Issue Date | 20240118 |
| WADAT | DATS | 8 | Planned Goods Issue Date | 20240119 |
| LFART | CHAR | 4 | Delivery Type | LF |
| VKORG | CHAR | 4 | Sales Organization | 1000 |
| VSTEL | CHAR | 4 | Shipping Point | 10001 |
| KUNNR | CHAR | 10 | Ship-to Party | 0000100234 |
| INCO1 | CHAR | 3 | Incoterms | EXW |
| LIFSK | CHAR | 2 | Delivery Block | |
| KODAT | DATS | 8 | Picking Date | 20240118 |

**Incoterms:**
- EXW = Ex Works
- FOB = Free on Board
- CIF = Cost, Insurance, Freight

#### LIPS - Delivery Item

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Delivery Number (FK → LIKP) | 8000001234 |
| POSNR | NUMC | 6 | Item Number | 000010 |
| MATNR | CHAR | 18 | Material Number | 000000000000012345 |
| LFIMG | QUAN | 15,3 | Actual Quantity Delivered | 100.000 |
| VRKME | UNIT | 3 | Sales Unit | EA |
| LGMNG | QUAN | 15,3 | Quantity in Stock Unit | 100.000 |
| MEINS | UNIT | 3 | Base Unit of Measure | EA |
| WERKS | CHAR | 4 | Plant | 1000 |
| LGORT | CHAR | 4 | Storage Location | 0001 |
| VGBEL | CHAR | 10 | Preceding Document (Sales Order) | 0000001234 |
| VGPOS | NUMC | 6 | Preceding Item | 000010 |
| ERDAT | DATS | 8 | Creation Date | 20240118 |

**Primary Key:** VBELN + POSNR

---

### Billing

#### VBRK - Billing Document Header

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Billing Document Number (Primary Key) | 9000001234 |
| FKART | CHAR | 4 | Billing Type | F2 |
| FKDAT | DATS | 8 | Billing Date | 20240119 |
| ERDAT | DATS | 8 | Creation Date | 20240119 |
| ERZET | TIMS | 6 | Creation Time | 110000 |
| ERNAM | CHAR | 12 | Created By | BILLUSER |
| KUNAG | CHAR | 10 | Sold-to Party | 0000100234 |
| KUNRG | CHAR | 10 | Payer | 0000100234 |
| VKORG | CHAR | 4 | Sales Organization | 1000 |
| NETWR | CURR | 15,2 | Net Value | 5000.00 |
| WAERK | CUKY | 5 | Currency | USD |
| FKSTO | CHAR | 1 | Cancellation Flag | |
| RFBSK | CHAR | 1 | Accounting Status | A |

**Billing Types:**
- F2 = Customer Invoice
- F8 = Pro Forma Invoice
- G2 = Credit Memo

**Accounting Status:**
- A = Posted
- B = Partially Posted
- C = Not Posted

#### VBRP - Billing Document Item

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Billing Document Number (FK → VBRK) | 9000001234 |
| POSNR | NUMC | 6 | Item Number | 000010 |
| MATNR | CHAR | 18 | Material Number | 000000000000012345 |
| ARKTX | CHAR | 40 | Item Description | Widget A Standard |
| FKIMG | QUAN | 15,3 | Billed Quantity | 100.000 |
| VRKME | UNIT | 3 | Sales Unit | EA |
| NETWR | CURR | 15,2 | Net Value | 5000.00 |
| WAERK | CUKY | 5 | Currency | USD |
| WERKS | CHAR | 4 | Plant | 1000 |
| VGBEL | CHAR | 10 | Reference Document (Delivery) | 8000001234 |
| VGPOS | NUMC | 6 | Reference Item | 000010 |
| ERDAT | DATS | 8 | Creation Date | 20240119 |
| AUBEL | CHAR | 10 | Sales Order Number | 0000001234 |
| AUPOS | NUMC | 6 | Sales Order Item | 000010 |

**Primary Key:** VBELN + POSNR

---

### Support Tables

#### VBFA - Sales Document Flow

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELV | CHAR | 10 | Preceding Sales Document | 0000001234 |
| POSNV | NUMC | 6 | Preceding Item | 000010 |
| VBELN | CHAR | 10 | Subsequent Sales Document | 8000001234 |
| POSNN | NUMC | 6 | Subsequent Item | 000010 |
| VBTYP_N | CHAR | 1 | Subsequent Doc Category | J |
| VBTYP_V | CHAR | 1 | Preceding Doc Category | C |
| RFMNG | QUAN | 15,3 | Quantity | 100.000 |
| MEINS | UNIT | 3 | Unit of Measure | EA |
| ERDAT | DATS | 8 | Creation Date | 20240118 |

**Document Categories:**
- C = Order
- J = Delivery
- M = Invoice
- H = Returns

**Primary Key:** VBELV + POSNV + VBELN + POSNN

#### KONV - Pricing Conditions

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| KNUMV | CHAR | 10 | Document Condition Number | 0000001234 |
| KPOSN | NUMC | 6 | Item Number | 000010 |
| STUNR | NUMC | 3 | Step Number | 001 |
| ZAEHK | NUMC | 3 | Counter | 01 |
| KSCHL | CHAR | 4 | Condition Type | PR00 |
| KWERT | CURR | 15,2 | Condition Value | 50.00 |
| KBETR | DEC | 11,2 | Condition Rate | 50.00 |
| WAERS | CUKY | 5 | Currency | USD |

**Condition Types:**
- PR00 = Base Price
- K004 = Discount
- MWST = Tax

**Primary Key:** KNUMV + KPOSN + STUNR + ZAEHK

#### VBPA - Sales Document Partners

| Field | Data Type | Length | Description | Example |
|-------|-----------|--------|-------------|---------|
| VBELN | CHAR | 10 | Sales Document Number | 0000001234 |
| POSNR | NUMC | 6 | Item Number (000000=Header) | 000000 |
| PARVW | CHAR | 2 | Partner Function | AG |
| KUNNR | CHAR | 10 | Customer Number | 0000100234 |
| PERNR | NUMC | 8 | Personnel Number | 10000 |

**Primary Key:** VBELN + POSNR + PARVW

---

## Data Relationships

### Entity Relationship Diagram (Key Flows)

```
KNA1 (Customer)
  └─→ KNVV (Customer Sales)
  └─→ KNB1 (Customer Company)
  └─→ VBAK.KUNNR (Order Sold-to)

MARA (Material)
  └─→ MARC (Material Plant)
  └─→ MAKT (Material Desc)
  └─→ VBAP.MATNR (Order Item)

VBAK (Order Header)
  └─→ VBAP (Order Items)
  └─→ VBUK (Order Status)
      └─→ VBUP (Item Status)
  └─→ VBEP (Schedule Lines)
  └─→ VBFA → LIKP (Delivery)

LIKP (Delivery Header)
  └─→ LIPS (Delivery Items)
  └─→ VBFA → VBRK (Billing)

VBRK (Billing Header)
  └─→ VBRP (Billing Items)

VBAK/VBAP
  └─→ KONV (Pricing)
  └─→ VBPA (Partners)
```

### Referential Integrity Rules

1. **Customer Foreign Keys:**
   - VBAK.KUNNR → KNA1.KUNNR
   - KNVV.KUNNR → KNA1.KUNNR
   - KNB1.KUNNR → KNA1.KUNNR

2. **Material Foreign Keys:**
   - VBAP.MATNR → MARA.MATNR
   - MARC.MATNR → MARA.MATNR
   - LIPS.MATNR → MARA.MATNR

3. **Document Flow:**
   - VBAP.VBELN → VBAK.VBELN (Order Item → Order Header)
   - LIPS.VGBEL → VBAK.VBELN (Delivery → Order)
   - VBRP.VGBEL → LIKP.VBELN (Billing → Delivery)
   - VBRP.AUBEL → VBAK.VBELN (Billing → Original Order)

4. **Organizational:**
   - VBAK.VKORG → TVKO.VKORG
   - TVKO.BUKRS → T001.BUKRS
   - VBAK.VTWEG → TVTW.VTWEG
   - VBAK.SPART → TSPA.SPART

---

## Data Quality Rules

### Completeness Checks

| Table | Field | Rule | Severity |
|-------|-------|------|----------|
| VBAK | KUNNR | Must not be null | Error |
| VBAK | VKORG | Must not be null | Error |
| VBAP | MATNR | Must not be null | Error |
| VBAP | KWMENG | Must be > 0 | Error |
| LIKP | WADAT_IST | Must not be null for completed deliveries | Warning |

### Consistency Checks

| Check | Rule | Severity |
|-------|------|----------|
| Order Dates | VBAK.ERDAT <= LIKP.ERDAT <= VBRK.FKDAT | Error |
| Order Value | VBAK.NETWR = SUM(VBAP.NETWR) | Error |
| Currency Match | VBAK.WAERK = VBAP.WAERK | Error |
| Status Logic | If VBUK.LFSTK = 'A' then all VBUP.LFSTA = 'A' | Warning |

### Referential Integrity Checks

All foreign key relationships listed above should be validated in the Silver layer transformations.

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-25 | System | Initial data dictionary creation |

