# SAP SD Sales Analytics - Complete Data Inventory

## Overview

This document provides a complete inventory of all synthetic data generated for the SAP SD Sales Analytics platform, organized by source system.

**Generated Date**: October 25, 2025
**Total Data Sources**: 2 (SAP ECC/S4HANA, Salesforce CRM)
**Total Tables**: 38
**Total Records**: 790,727

---

## Data Structure

```
data/raw/
├── sap/              # SAP ECC/S4HANA SD Module Data
│   ├── master/       # Master Data (Dimensions)
│   └── transactional/ # Transaction Data (Facts)
└── crm/              # Salesforce CRM Data
    └── *.csv         # CRM Objects
```

---

## 1. SAP ECC/S4HANA SD MODULE DATA

### 1.1 Master Data Tables

#### Customer Master (4 tables, 45,065 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **KNA1** | Customer Master General | 5,000 | data/raw/sap/master/customer/KNA1.csv |
| **KNVV** | Customer Sales Data | 7,013 | data/raw/sap/master/customer/KNVV.csv |
| **KNB1** | Customer Company Code Data | 5,000 | data/raw/sap/master/customer/KNB1.csv |
| **KNVP** | Customer Partner Functions | 28,052 | data/raw/sap/master/customer/KNVP.csv |

**Key Fields:**
- KUNNR: Customer Number (Primary Key in KNA1)
- VKORG: Sales Organization
- VTWEG: Distribution Channel
- SPART: Division

#### Material Master (4 tables, 10,014 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **MARA** | Material General Data | 2,000 | data/raw/sap/master/material/MARA.csv |
| **MARC** | Material Plant Data | 3,410 | data/raw/sap/master/material/MARC.csv |
| **MAKT** | Material Descriptions | 2,000 | data/raw/sap/master/material/MAKT.csv |
| **MVKE** | Material Sales Data | 2,604 | data/raw/sap/master/material/MVKE.csv |

**Key Fields:**
- MATNR: Material Number (Primary Key in MARA)
- WERKS: Plant
- SPRAS: Language

#### Organizational Structures (7 tables, 39 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **T001** | Company Codes | 3 | data/raw/sap/master/organizational/T001.csv |
| **TVKO** | Sales Organizations | 3 | data/raw/sap/master/organizational/TVKO.csv |
| **TVTW** | Distribution Channels | 3 | data/raw/sap/master/organizational/TVTW.csv |
| **TSPA** | Divisions | 3 | data/raw/sap/master/organizational/TSPA.csv |
| **T023** | Material Groups | 5 | data/raw/sap/master/organizational/T023.csv |
| **T005** | Countries | 5 | data/raw/sap/master/organizational/T005.csv |
| **T171T** | Product Hierarchy Text | 20 | data/raw/sap/master/product_hierarchy/T171T.csv |

**Organizational Codes:**
- **Company Codes**: 1000 (US), 2000 (Germany), 3000 (UK)
- **Sales Orgs**: 1000, 2000, 3000
- **Distribution Channels**: 10 (Direct), 20 (Wholesale), 30 (E-Commerce)
- **Divisions**: 00 (Cross), 01 (Electronics), 02 (Machinery)

### 1.2 Transaction Data Tables

#### Sales Orders (5 tables, 253,719 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **VBAK** | Sales Document Header | 14,310 | data/raw/sap/transactional/sales_orders/VBAK.csv |
| **VBAP** | Sales Document Items | 71,435 | data/raw/sap/transactional/sales_orders/VBAP.csv |
| **VBUK** | Sales Document Header Status | 14,310 | data/raw/sap/transactional/sales_orders/VBUK.csv |
| **VBUP** | Sales Item Status | 71,435 | data/raw/sap/transactional/sales_orders/VBUP.csv |
| **VBEP** | Sales Schedule Lines | 82,229 | data/raw/sap/transactional/sales_orders/VBEP.csv |

**Key Metrics:**
- Total Orders: 14,310
- Total Order Items: 71,435
- Average Items per Order: 4.99
- Date Range: September 25, 2025 - October 24, 2025 (30 days)
- Daily Order Volume: ~500 orders/day

**Order Types:**
- OR (Standard Order): 70.3%
- ZOR (Rush Order): 20.3%
- QT (Quotation): 9.4%

**Order Status Distribution:**
- A (Complete): 39.6%
- B (In Process): 35.6%
- C (Not Processed): 24.8%

#### Deliveries (2 tables, 51,516 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **LIKP** | Delivery Header | 8,586 | data/raw/sap/transactional/deliveries/LIKP.csv |
| **LIPS** | Delivery Items | 42,930 | data/raw/sap/transactional/deliveries/LIPS.csv |

**Key Metrics:**
- Total Deliveries: 8,586
- Total Delivery Items: 42,930
- Delivery Rate: 60% of orders

#### Billing (2 tables, 41,214 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **VBRK** | Billing Document Header | 6,869 | data/raw/sap/transactional/billing/VBRK.csv |
| **VBRP** | Billing Document Items | 34,345 | data/raw/sap/transactional/billing/VBRP.csv |

**Key Metrics:**
- Total Billing Documents: 6,869
- Total Billing Items: 34,345
- Billing Rate: 80% of deliveries

**Billing Types:**
- F2 (Customer Invoice): 94.9%
- F8 (Credit Memo): 5.1%

#### Support Tables (5 tables, 371,738 records)

| Table | Description | Records | File Location |
|-------|-------------|---------|---------------|
| **VBFA** | Sales Document Flow | 77,275 | data/raw/sap/transactional/document_flow/VBFA.csv |
| **KONV** | Pricing Conditions | 214,305 | data/raw/sap/transactional/pricing/KONV.csv |
| **VBPA** | Sales Partners | 71,550 | data/raw/sap/transactional/partners/VBPA.csv |
| **VTTK** | Shipment Header | 3,434 | data/raw/sap/transactional/shipment/VTTK.csv |
| **VTTP** | Shipment Items | 5,191 | data/raw/sap/transactional/shipment/VTTP.csv |

**Total SAP Records**: 773,305

---

## 2. SALESFORCE CRM DATA

### 2.1 CRM Core Objects (9 tables, 17,422 records)

| Object | Description | Records | File Location | Key Use Case |
|--------|-------------|---------|---------------|--------------|
| **Account** | Company Master | 1,000 | data/raw/crm/Account.csv | Customer 360, Account hierarchy |
| **Contact** | Decision Makers | 2,735 | data/raw/crm/Contact.csv | Stakeholder management |
| **Lead** | Prospects | 2,000 | data/raw/crm/Lead.csv | Lead qualification, conversion |
| **Campaign** | Marketing Campaigns | 20 | data/raw/crm/Campaign.csv | Marketing ROI, attribution |
| **Opportunity** | Sales Pipeline | 1,115 | data/raw/crm/Opportunity.csv | Forecast, pipeline analysis |
| **OpportunityLineItem** | Products in Deals | 2,544 | data/raw/crm/OpportunityLineItem.csv | Product mix, pricing |
| **Case** | Support Tickets | 1,074 | data/raw/crm/Case.csv | Service quality, CSAT |
| **Activity** | Engagement Tracking | 5,913 | data/raw/crm/Activity.csv | Sales activity metrics |
| **Quote** | CPQ Quotes | 1,021 | data/raw/crm/Quote.csv | Quote-to-cash, win rates |

### 2.2 Account (Company Master) - 1,000 records

**Key Fields:**
- Id: Salesforce Account ID (e.g., 001000010000)
- Name: Company Name
- AccountNumber: External Account Number (ACC-xxxxxx)
- Type: Customer - Direct, Customer - Channel, Prospect, Partner, Competitor
- Industry: Technology, Manufacturing, Financial Services, Healthcare, Retail, etc.
- AnnualRevenue: $1M - $100M range
- NumberOfEmployees: 10 - 10,000

**Distribution:**
- Customer - Direct: 40%
- Prospect: 20%
- Customer - Channel: 15%
- Partner: 15%
- Competitor: 10%

**Rating:**
- Hot: 20%
- Warm: 50%
- Cold: 30%

### 2.3 Contact (Decision Makers) - 2,735 records

**Key Fields:**
- Id: Salesforce Contact ID
- AccountId: Related Account (FK)
- FirstName, LastName: Contact name
- Email: Contact email
- Title: CEO, CFO, CTO, VP Sales, Director IT, etc.
- Department: Executive, Finance, IT, Sales, Marketing, Operations

**Distribution:**
- Average 2.7 contacts per account
- Titles: Executive (C-level), VP-level, Director, Manager
- Lead Sources: Web, Phone Inquiry, Partner Referral, Trade Show, Event

### 2.4 Lead (Prospects) - 2,000 records

**Key Fields:**
- Id: Lead ID (00Qxxxxxxxxx)
- FirstName, LastName, Company: Lead information
- Email, Phone: Contact info
- LeadSource: Web, Phone Inquiry, Partner Referral, etc.
- Status: Open, Working, Closed - Converted, Closed - Not Converted
- Rating: Hot, Warm, Cold
- IsConverted: Boolean
- ConvertedAccountId, ConvertedContactId, ConvertedOpportunityId: Conversion linkage

**Conversion Stats:**
- Converted Leads: 25%
- Working Leads: 40%
- Open Leads: 20%
- Not Converted: 15%

### 2.5 Campaign (Marketing) - 20 records

**Key Fields:**
- Id: Campaign ID
- Name: Campaign name (e.g., "Q1 2024 - Product Launch")
- Type: Email, Webinar, Conference, Trade Show, Direct Mail, Social Media
- Status: Planned, In Progress, Completed, Aborted
- BudgetedCost, ActualCost: Financial metrics
- NumberSent, NumberOfResponses, NumberOfLeads: Performance metrics
- ExpectedRevenue: Revenue target

**Campaign Performance:**
- Average Budget: $50K - $150K
- Response Rate: 2% - 15%
- Lead Conversion: 30% - 70%

### 2.6 Opportunity (Pipeline) - 1,115 records

**Key Fields:**
- Id: Opportunity ID (006xxxxxxxxx)
- AccountId: Related Account
- Name: Opportunity name
- StageName: Prospecting → Closed Won/Lost
- Probability: 0% - 100%
- Amount: Deal size ($10K - $1M)
- CloseDate: Expected close date
- Type: New Business, Upgrade, Replacement, Downgrade
- IsClosed, IsWon: Status flags
- ForecastCategory: Pipeline, Best Case, Commit, Closed

**Pipeline Distribution:**
- Closed Won: 15%
- Closed Lost: 5%
- Negotiation/Review: 10%
- Proposal/Price Quote: 15%
- Value Proposition: 15%
- Needs Analysis: 15%
- Qualification: 15%
- Prospecting: 10%

**Deal Size:**
- Average: ~$100K
- Range: $10K - $1M (log-normal distribution)

### 2.7 OpportunityLineItem (Products) - 2,544 records

**Product Catalog:**
1. Enterprise Software License - $50,000
2. Professional Services - Implementation - $25,000
3. Annual Support & Maintenance - $10,000
4. Training Package - 10 Users - $5,000
5. Hardware Appliance - Standard - $15,000
6. Cloud Subscription - Monthly - $2,000
7. Consulting Services - Daily Rate - $2,500
8. Data Migration Services - $30,000

**Key Fields:**
- OpportunityId: Related Opportunity
- Product2Id, ProductCode: Product reference
- Quantity: Units (1-100)
- ListPrice, UnitPrice: Pricing
- Discount: 0% - 25%
- TotalPrice: Extended amount

**Distribution:**
- Average 2.3 products per opportunity
- Discount applied: 50% of line items
- Average discount: 10%

### 2.8 Case (Support Tickets) - 1,074 records

**Key Fields:**
- Id: Case ID
- CaseNumber: Case number (CS-xxxxxx)
- AccountId, ContactId: Related records
- Status: New, Working, Escalated, Closed
- Priority: Low, Medium, High, Critical
- Type: Problem, Question, Feature Request, Bug Report, Configuration
- Origin: Web, Phone, Email, Chat, Portal
- Subject, Description: Case details
- IsClosed, IsEscalated: Status flags

**Support Metrics:**
- Only customer accounts have cases
- Average 1.5 cases per customer account
- Closed rate: 50%
- Escalation rate: 10%

**Priority Distribution:**
- Low: 40%
- Medium: 35%
- High: 20%
- Critical: 5%

### 2.9 Activity (Engagement) - 5,913 records

**Key Fields:**
- Id: Activity/Task ID
- WhatId: Related to (Opportunity, Account, etc.)
- Subject: Call, Email, Meeting, Demo, Follow-up, Send Quote
- ActivityDate: Scheduled/completed date
- Status: Not Started, In Progress, Completed, Deferred
- Priority: Low, Normal, High
- IsClosed: Completion flag

**Activity Metrics:**
- Average 5-7 activities per opportunity
- Completion rate: 70%
- Activity types aligned with sales process

### 2.10 Quote (CPQ Quotes) - 1,021 records

**Key Fields:**
- Id: Quote ID
- QuoteNumber: Quote number (QT-xxxxxx)
- OpportunityId, AccountId: Related records
- Status: Draft, In Review, Approved, Rejected, Presented, Accepted, Denied
- ExpirationDate: Validity period (30 days)
- Subtotal, Discount, Tax, TotalPrice: Pricing breakdown
- GrandTotal: Final amount

**Quote Metrics:**
- Opportunities with probability >= 20% get quotes
- Average 1 quote per qualified opportunity
- Quote values align with opportunity amounts (±10%)
- Acceptance rate: Varies by opportunity stage

---

## 3. DATA RELATIONSHIPS

### 3.1 SAP Data Flow

```
Order-to-Cash Process:
VBAK (Order) → VBAP (Order Items)
       ↓
LIKP (Delivery) → LIPS (Delivery Items)
       ↓
VBRK (Billing) → VBRP (Billing Items)

Document Flow tracked in: VBFA

Supporting Data:
- KONV: Pricing conditions for each line item
- VBPA: Partners (sold-to, ship-to, bill-to, payer)
- VTTK/VTTP: Shipments consolidating multiple deliveries
```

### 3.2 CRM Data Flow

```
Lead-to-Cash Process:
Lead (Prospect)
  ↓ [Conversion]
Account (Company) ← Contact (Decision Maker)
  ↓
Opportunity (Deal) ← Campaign (Attribution)
  ↓
OpportunityLineItem (Products)
  ↓
Quote (Pricing)
  ↓
[Closed Won] → Account becomes Customer
  ↓
Case (Support) ← Activity (Engagement)
```

### 3.3 Cross-System Integration Points

**Customer Master Matching:**
- SAP KNA1.KUNNR ↔ CRM Account.AccountNumber
- Matching logic: Account number prefix "ACC-" + KUNNR

**Order-to-Opportunity Linkage:**
- SAP VBAK (Sales Order) ↔ CRM Opportunity
- Closed Won opportunities generate SAP orders
- Link via external reference fields

**Contact Synchronization:**
- SAP KNVP (Partner Functions) ↔ CRM Contact
- Decision makers in CRM map to SAP partners

---

## 4. USE CASES & ANALYTICS

### 4.1 SAP SD Analytics

1. **Sales Performance Dashboard**
   - Daily/Weekly/Monthly sales trends
   - Revenue by product, customer, region
   - Order fulfillment metrics

2. **Order-to-Cash Cycle Analysis**
   - Days from order to delivery
   - Days from delivery to invoice
   - Cash collection cycle time
   - Bottleneck identification

3. **Customer Analytics**
   - Top customers by revenue
   - Customer segmentation (RFM)
   - Order frequency patterns

4. **Product Performance**
   - Best-selling products
   - Product mix analysis
   - Pricing variance analysis

### 4.2 CRM Analytics

1. **Sales Pipeline Management**
   - Pipeline value by stage
   - Forecast accuracy
   - Win/loss analysis
   - Sales velocity

2. **Marketing ROI**
   - Campaign performance
   - Cost per lead
   - Lead conversion rates
   - Attribution modeling

3. **Customer 360 View**
   - Account hierarchy
   - Relationship mapping
   - Engagement history
   - Support ticket trends

4. **Sales Activity Metrics**
   - Activity-to-conversion correlation
   - Sales rep productivity
   - Follow-up effectiveness

### 4.3 Integrated Analytics

1. **Quote-to-Order Conversion**
   - CRM Quote → SAP Order linkage
   - Quote acceptance rate
   - Time from quote to order

2. **Customer Lifetime Value**
   - CRM opportunity value + SAP historical orders
   - Customer profitability analysis
   - Churn prediction

3. **Sales Forecasting**
   - CRM pipeline + SAP historical trends
   - ML-based demand prediction
   - Inventory planning

4. **Service Impact on Sales**
   - CRM cases vs renewal opportunities
   - CSAT correlation with upsell
   - Support SLA impact on retention

---

## 5. FILE SIZES & TECHNICAL DETAILS

### 5.1 SAP Data Files

| Category | File Count | Approx Size | Compression Recommended |
|----------|------------|-------------|-------------------------|
| Customer Master | 4 | ~5 MB | Parquet with Snappy |
| Material Master | 4 | ~2 MB | Parquet with Snappy |
| Organizational | 7 | ~50 KB | CSV acceptable |
| Sales Orders | 5 | ~30 MB | Parquet with Snappy |
| Deliveries | 2 | ~15 MB | Parquet with Snappy |
| Billing | 2 | ~12 MB | Parquet with Snappy |
| Support Tables | 5 | ~80 MB | Parquet with Snappy |

**Total SAP Data**: ~144 MB (CSV), ~40 MB (Parquet compressed)

### 5.2 CRM Data Files

| Object | Records | Approx Size | Fields |
|--------|---------|-------------|--------|
| Account | 1,000 | ~500 KB | 19 |
| Contact | 2,735 | ~1.5 MB | 19 |
| Lead | 2,000 | ~1.2 MB | 21 |
| Campaign | 20 | ~10 KB | 19 |
| Opportunity | 1,115 | ~600 KB | 20 |
| OpportunityLineItem | 2,544 | ~1 MB | 14 |
| Case | 1,074 | ~550 KB | 16 |
| Activity | 5,913 | ~2.5 MB | 12 |
| Quote | 1,021 | ~550 KB | 17 |

**Total CRM Data**: ~8.4 MB (CSV)

---

## 6. DATA QUALITY SUMMARY

### 6.1 Completeness
✅ All 38 tables generated successfully
✅ All required fields populated
✅ No orphan records (all FKs valid)

### 6.2 Referential Integrity
✅ VBAK.KUNNR → KNA1.KUNNR (100% valid)
✅ VBAP.MATNR → MARA.MATNR (100% valid)
✅ VBAP.VBELN → VBAK.VBELN (100% valid)
✅ LIPS.VBELN → LIKP.VBELN (100% valid)
✅ VBRP.VBELN → VBRK.VBELN (100% valid)
✅ CRM Contact.AccountId → Account.Id (100% valid)
✅ CRM Opportunity.AccountId → Account.Id (100% valid)

### 6.3 Data Realism
✅ Temporal consistency (Order Date ≤ Delivery Date ≤ Invoice Date)
✅ Realistic distributions (80/20 rule for customers/products)
✅ Proper status progressions
✅ Currency consistency within documents
✅ Quantity values > 0
✅ No null values in required fields

---

## 7. NEXT STEPS

### 7.1 Data Conversion
```bash
# Convert CSV to Parquet for better performance
# Reduces file size by ~70% and improves query performance

# For SAP data
python scripts/convert_to_parquet.py --source sap

# For CRM data
python scripts/convert_to_parquet.py --source crm
```

### 7.2 Upload to Azure Data Lake
```bash
# Upload to ADLS Gen2
az storage blob upload-batch \
  --account-name <storage-account> \
  --destination raw/sap \
  --source data/raw/sap \
  --pattern "*.parquet"

az storage blob upload-batch \
  --account-name <storage-account> \
  --destination raw/crm \
  --source data/raw/crm \
  --pattern "*.csv"
```

### 7.3 Databricks Processing
1. Mount ADLS to Databricks
2. Create Bronze tables (raw data)
3. Apply transformations for Silver layer (cleansed)
4. Build Gold layer (business metrics)

---

## 8. APPENDIX

### 8.1 Generation Parameters

**SAP Data:**
- Customers: 5,000
- Materials: 2,000
- Orders per day: 500
- Simulation period: 30 days
- Average items per order: 5
- Delivery rate: 60%
- Billing rate: 80%

**CRM Data:**
- Accounts: 1,000
- Contacts per account: ~2.7
- Leads: 2,000
- Campaigns: 20
- Opportunities per account: ~1.1
- Activities per opportunity: ~5.3
- Quote rate: ~92% (for qualified opps)

### 8.2 Random Seed
All generators use seed=42 for reproducibility

### 8.3 Date Ranges
- **SAP Orders**: September 25, 2025 - October 24, 2025
- **CRM Accounts**: Created over past 5 years
- **CRM Opportunities**: Created 30-365 days after account creation
- **CRM Cases**: Past 2 years of support history

---

**Document Version**: 1.0
**Last Updated**: October 25, 2025
**Total Tables**: 38
**Total Records**: 790,727
**Total Size (CSV)**: ~152 MB
