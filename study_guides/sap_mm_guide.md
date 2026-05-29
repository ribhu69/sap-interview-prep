# SAP MM (Materials Management) — Comprehensive Interview Prep Guide
## For Experienced Professionals (5+ Years) | ECC & S/4HANA

---

## 1. ORGANIZATIONAL STRUCTURE

### Client
The highest organizational unit. All company codes, plants, and settings reside under a client. Master data and configuration are client-dependent.

### Company Code
Represents an independent legal entity with its own balance sheet and P&L. Assigned to a controlling area. Key for FI integration.

### Plant
A place where value-added activities occur — production, storage, or both. Assigned to a company code. Each plant has its own:
- Storage locations
- MRP area (optional)
- Purchasing organization assignment

### Storage Location
Differentiates stock within a plant. Stock is managed at storage location level. Not relevant for valuation (valuation is at plant level unless split valuation is active).

### Purchasing Organization
Responsible for negotiating purchase terms. Types:
- **Cross-company**: Serves multiple company codes
- **Company-specific**: Serves one company code
- **Plant-specific**: Serves one plant

### Purchasing Group
A buyer or group of buyers responsible for procurement activities. Used in reporting and workflows.

### MRP Area
Allows separate MRP planning within a plant. Can be defined for storage locations or subcontractors.

### Key Interview Question
> **Q: What is the difference between a Purchasing Organization and a Purchasing Group?**
> A: Purchasing Organization is an organizational unit legally responsible for procurement and negotiates prices/terms. Purchasing Group is a key that represents a buyer or buyer group — it is not an organizational unit but a master data field used for responsibility assignment and reporting.

---

## 2. MATERIAL MASTER

### Views and Relevant Organizational Levels
| View | Org Level |
|------|-----------|
| Basic Data 1 & 2 | Client |
| Classification | Client |
| Purchasing | Client / Plant |
| MRP 1-4 | Plant |
| Accounting 1 & 2 | Plant (Valuation Area) |
| Costing 1 & 2 | Plant |
| Storage | Plant / Storage Location |
| Warehouse Management | Warehouse / Storage Type |
| Quality Management | Plant |
| Plant Data / Storage | Plant |

### Material Types (Key)
| Type | Description |
|------|-------------|
| ROH | Raw Material |
| HALB | Semi-finished |
| FERT | Finished Product |
| HAWA | Trading Goods |
| DIEN | Services |
| NLAG | Non-stock material |
| VERP | Packaging material |
| LEIH | Returnable Transport Packaging |

### Material Type Controls
- Which views are available
- Account category reference (for automatic account determination)
- Quantity/value update in stock management
- Whether price control is V (MAP) or S (Standard)

### Key Interview Questions
> **Q: What is the difference between Material Type and Material Group?**
> A: Material Type (e.g., ROH, FERT) is a system classification that controls account determination, views, and price control. Material Group is a user-defined classification for grouping materials for reporting and output — it does not drive system behavior the way Material Type does.

> **Q: Can you change a material's Material Type after creation?**
> A: Yes, using transaction MMAM (Material Type Change), but with restrictions — the new type must use the same account category reference, and no open documents must exist.

> **Q: What is the significance of the Valuation Class in the material master?**
> A: The Valuation Class links the material to G/L accounts via the account category reference. It determines which G/L accounts are posted to during goods movements (via OBYC configuration).

---

## 3. VENDOR MASTER (SUPPLIER MASTER IN S/4HANA)

### Structure
1. **General Data** (Client level) — Name, address, language, tax info
2. **Company Code Data** — Payment terms, reconciliation account, payment methods, tolerance group
3. **Purchasing Organization Data** — Order currency, Incoterms, minimum order value, GR-based IV indicator

### Account Groups
Control:
- Number range (internal or external)
- Screen layout (mandatory/optional/suppressed fields)
- One-time vendor capability
- Partner functions allowed

### Key Partner Functions in Purchasing
| Function | Description |
|----------|-------------|
| LF | Vendor (Ordering Address) |
| RE | Invoice Presented By |
| RS | Invoicing Party (Different Payee) |
| WL | Goods Supplier |
| LS | Forwarding Agent |

### Key Interview Questions
> **Q: What is the difference between Ordering Address and Invoicing Party partner functions?**
> A: Ordering Address (LF) is where the PO is sent. Invoicing Party (RS) is who submits the invoice — relevant when a parent company invoices on behalf of a subsidiary.

> **Q: What is a one-time vendor and when is it used?**
> A: A one-time vendor (CPD account group) uses a single master record for multiple vendors. Address details are captured at document entry. Used for infrequent vendors where maintaining separate masters is not cost-effective.

> **Q: In S/4HANA, how does the vendor master change?**
> A: In S/4HANA, vendors and customers are replaced by the Business Partner (BP) concept using transaction BP. The vendor-specific data is maintained under BP role "FI Vendor" (FLVN01) and purchasing data under "Vendor" (FLVN00). The old XK01/MK01 transactions still work via compatibility mode.

---

## 4. PURCHASING INFO RECORDS (PIR)

### Purpose
Stores purchasing conditions (price, discounts, delivery time) for a material-vendor combination.

### Types
| Type | Description |
|------|-------------|
| Standard | Normal stock materials |
| Consignment | Vendor-owned stock in your premises |
| Subcontracting | Vendor performs work on your components |
| Pipeline | Continuous supply (utilities) |

### Key Fields
- Last Purchase Order (reference)
- Planned Delivery Time
- Purchasing Organization
- Plant (optional — plant-level PIR is more specific)
- Valid from/to dates
- Conditions (Pb00 for gross price)

### Transaction Codes
- ME11 — Create PIR
- ME12 — Change PIR
- ME13 — Display PIR
- ME1M — PIR per Material
- ME1L — PIR per Vendor

### Key Interview Questions
> **Q: How does SAP determine which PIR to use when creating a PO?**
> A: SAP uses the most specific PIR: Plant-level PIR overrides Purchasing-Org-level PIR. Within same level, the one with the latest valid-from date is used. PIR conditions are copied to PO conditions.

---

## 5. SOURCE LISTS

### Purpose
Defines allowed (or preferred) vendors for a material at plant level. Controls from which vendor and for which period procurement is allowed.

### Key Fields
- Validity period
- Vendor + Purchasing Organization
- Fixed source indicator (blocks other vendors)
- MRP relevance (1 = MRP will create PO/Schedule Agreement, 2 = blocked for MRP)

### Transaction Codes: ME01 (Create), ME03 (Display), ME04 (Changes)

### Key Interview Questions
> **Q: What is the Source List Check in the PO and how do you activate it?**
> A: In Purchasing Organization settings or Plant parameters, you can activate "Source List Required" — then a PO can only be created for vendors listed in the source list for that material/plant. Activated via SPRO > MM > Purchasing > Source List.

---

## 6. PROCUREMENT CYCLE — END TO END

### Step 1: Purchase Requisition (PR)
- Transactions: ME51N (Create), ME52N (Change), ME53N (Display)
- Can be created manually or automatically by MRP
- Item categories: Standard (blank), Subcontracting (L), Consignment (K), Stock Transfer (U), Third-party (S)
- Assigned to cost center, WBS element, asset, or order

### Step 2: Request for Quotation (RFQ) — Optional
- ME41 (Create), ME42 (Change), ME43 (Display)
- ME47 (Maintain Quotation — vendor prices entered)
- ME48 (Display Quotation)
- ME49 (Price Comparison — finds best vendor)

### Step 3: Purchase Order (PO)
- ME21N (Create), ME22N (Change), ME23N (Display)
- Document types: NB (Standard), FO (Framework Order/Blanket), UB (Stock Transfer)
- Can reference PR, RFQ, or contract
- Key fields: Delivery date, quantity, price, plant, storage location, account assignment

### Step 4: Goods Receipt (GR)
- MIGO (transaction for all MM movements) or MB01 (classic)
- Movement Type 101 — GR against PO (stock material)
- Stock updated, G/L accounts posted (GR/IR clearing account debited, inventory account credited)
- 3-way match begins: PO ↔ GR ↔ Invoice

### Step 5: Invoice Verification (LIV — Logistics Invoice Verification)
- MIRO (Enter Incoming Invoice)
- MIR4 (Display Invoice Document)
- MIR6 (Invoice Overview)
- MIR7 (Park Invoice)
- System checks: quantity, price, and delivery cost tolerances
- Posts debit to GR/IR and credit to vendor account

### Key Interview Questions
> **Q: Explain the 3-way match in SAP MM.**
> A: The 3-way match compares the Purchase Order (committed price & quantity), Goods Receipt (actual quantity received), and Vendor Invoice (billed amount). MIRO uses this to verify the invoice against both PO and GR. Variances within tolerance are accepted; outside tolerance block the invoice for payment.

> **Q: What happens to the GR/IR account?**
> A: At GR posting (MT 101): Debit Inventory Account, Credit GR/IR Clearing. At Invoice posting (MIRO): Debit GR/IR Clearing, Credit Vendor. The GR/IR account acts as a bridge. If goods are received but no invoice, GR/IR has a credit balance. MR11 (GR/IR Maintenance) is used to clear this account at period end.

> **Q: What is Evaluated Receipt Settlement (ERS)?**
> A: ERS is an automatic invoicing process where SAP creates an invoice automatically based on GR quantities and PO prices — no vendor invoice needed. Must be enabled in vendor master (ERS flag) and PIR. Runs via MRRL transaction.

---

## 7. OUTLINE AGREEMENTS

### Scheduling Agreement
- Long-term agreement with delivery schedule lines
- Document type LP (standard) or LPA (with release documentation)
- Transaction: ME31L (Create), ME32L (Change)
- Delivery schedule created in ME38
- GR references the scheduling agreement

### Contract (Value/Quantity)
- Value Contract (WK): Total value not to exceed agreed amount
- Quantity Contract (MK): Total quantity not to exceed agreed amount
- Transaction: ME31K (Create), ME32K (Change)
- Release orders created against the contract (ME21N referencing contract)

### Key Interview Questions
> **Q: What is the difference between a Contract and a Scheduling Agreement?**
> A: A Contract is a longer-term agreement stating total quantity or value to be procured — individual release POs are raised against it. A Scheduling Agreement contains time-phased delivery schedule lines (dates and quantities) built into the agreement itself — no separate PO is needed, GR is made directly against it.

---

## 8. SPECIAL PROCUREMENT TYPES

### Consignment
- Vendor stores goods in your plant at their risk and ownership
- MT 101K — GR (vendor owns stock)
- MT 201K — Goods Issue (trigger payment obligation to vendor)
- MT 122K — Return to vendor
- Consignment liabilities settled via MRKO transaction
- No payment until goods are consumed

### Subcontracting
- You send components (MT 541) to vendor
- Vendor processes and returns finished product (MT 101 with item category L)
- BOM defines which components are sent
- MT 543 — Vendor consumption of components
- Open subcontracting stocks monitored via ME2O

### Third-Party
- You create PO to vendor, vendor ships directly to customer
- PR → PO (item category S) → vendor invoice
- Shipping notification or confirmation required
- No GR in your plant (statistical GR possible)

### Stock Transfer Order (STO)
- Movement of goods between plants
- One-step: MT 351/352 (with SD delivery) or MT 301 (without delivery)
- Two-step: MT 303 (issue from supplying plant), MT 305 (receive at receiving plant)
- Requires Delivery (SD) for cross-company STOs

### Pipeline Materials
- Continuous consumption from pipelines (water, gas, electricity)
- MT 201P (consumption posting)
- No GR, no PO — just consumption posting
- Vendor settled via MRKO

### Key Interview Questions
> **Q: In consignment procurement, when does the payment obligation arise?**
> A: Payment obligation arises when goods are consumed (MT 201K — Goods Issue from consignment stock). Until consumption, no liability exists. MRKO settles the outstanding consignment liabilities with the vendor.

> **Q: What is the difference between one-step and two-step stock transfer?**
> A: One-step (MT 301): Stock is immediately transferred from issuing to receiving plant — suitable for same company code. Two-step (MT 303 + 305): Stock goes into "Stock in Transfer" interim state, visible to both plants — used when physical transit time is significant or when an SD delivery is required (cross-company).

---

## 9. INVENTORY MANAGEMENT — MOVEMENT TYPES

### Critical Movement Types
| MT | Description |
|----|-------------|
| 101 | GR for PO |
| 102 | Reversal of GR for PO |
| 103 | GR into Blocked Stock |
| 105 | Release from Blocked Stock |
| 122 | Return to vendor (from unrestricted) |
| 123 | Return to vendor (from blocked) |
| 201 | Goods Issue to Cost Center |
| 261 | Goods Issue for Production Order |
| 262 | Reversal of GI for Production Order |
| 301 | Plant-to-Plant Transfer (one step) |
| 303 | Issue from Supplying Plant (STO two-step) |
| 305 | Receive at Receiving Plant (STO two-step) |
| 311 | Transfer between Storage Locations (one step) |
| 313 | SL-to-SL (first step) — stock in transfer |
| 315 | SL-to-SL (second step) — clear in-transfer |
| 351 | GI for STO (with Delivery) |
| 501 | GR without PO (receipt into unrestricted) |
| 541 | Send components to subcontractor |
| 543 | Consume components at subcontractor |
| 551 | Scrapping |
| 561 | Initial Stock Entry |
| 601 | Goods Issue for Sales Order Delivery |
| 641 | GI for STO with delivery (supplying plant) |

### Stock Types
| Type | Description |
|------|-------------|
| Unrestricted | Available for planning and use |
| Quality Inspection | Under QM hold |
| Blocked | Rejected goods |
| Restricted | For batch-managed materials with restricted shelf life |
| In Transit | Being transferred between plants/SLs |
| Consignment | Vendor-owned goods in your premises |

### Physical Inventory
- MI01 — Create Physical Inventory Document
- MI04 — Enter Count
- MI07 — Post Differences
- MIDO — Physical Inventory Overview
- Annual inventory (all stock counted on one day)
- Cycle counting (based on ABC classification, periodic counting)

### Key Interview Questions
> **Q: What is the purpose of Movement Type 501 and when would you use it?**
> A: MT 501 posts a GR without a Purchase Order reference. Used for initial stock uploads, returns from customers not via SD, or emergency situations. It does not create a GR/IR entry, so there is no invoice matching — the debit goes directly to an inventory account with an offsetting entry.

> **Q: How do you reverse a GR in SAP?**
> A: Use MT 102 in MIGO to reverse an MT 101 GR. The system requires the original material document number. Alternatively, select "Cancel" in MIGO referencing the original document. Partial reversals are possible by specifying quantity. The reverse posting backs out all G/L entries and restores vendor/PO open quantities.

---

## 10. VALUATION AND ACCOUNT DETERMINATION

### Price Controls
| Control | Description | Used For |
|---------|-------------|----------|
| V (MAP) | Moving Average Price | Raw materials, trading goods |
| S (Standard Price) | Fixed standard cost | Finished/semi-finished products |

### Moving Average Price Mechanics
- MAP = Total Stock Value / Total Quantity
- GR at invoice price updates MAP if price differs from PO price
- Price differences go to inventory account (not to price difference account) when stock covers the quantity
- If stock = 0 and price differs, difference goes to price difference account

### Standard Price Mechanics
- Price is fixed regardless of actual purchase price
- Variances between PO price and standard are posted to price difference accounts
- Standard price is set via costing run (CK11N, CK24)

### Account Determination — OBYC
Key Transaction/Event Keys:
| Key | Description |
|-----|-------------|
| BSX | Inventory posting |
| WRX | GR/IR Clearing Account |
| PRD | Price Differences |
| KON | Consignment Liabilities |
| KDM | Exchange Rate Differences (MIRO) |
| GBB | Offsetting account for inventory posting |

Configuration path: SPRO → MM → Valuation → Account Determination → Configure Automatic Postings

### Valuation Class
- Links material to account determination
- Determined by: Material Type → Account Category Reference → Valuation Class
- Allows different G/L accounts for different material types

### Split Valuation
- Allows different prices for the same material based on a characteristic (batch, plant, origin)
- Requires Valuation Type and Valuation Category
- Use cases: imported vs domestic materials, new vs refurbished parts

### Key Interview Questions
> **Q: Why is Standard Price preferred for finished goods and MAP for raw materials?**
> A: Standard Price provides stable costs for production planning and variance analysis — it isolates actual vs planned cost variances in a separate account. MAP is preferred for raw materials since purchase prices fluctuate and the average price accurately reflects current inventory value without creating separate variance accounts.

> **Q: What is the GR/IR account and why does it exist?**
> A: The GR/IR (Goods Receipt/Invoice Receipt) is a clearing account. At GR, inventory is debited and GR/IR is credited (liability to vendor). At MIRO, GR/IR is debited and vendor account is credited. This balances the books even when GR and invoice arrive at different times. Open items at period end indicate either uninvoiced deliveries or invoices not yet matched to GR.

---

## 11. MRP — MATERIALS REQUIREMENTS PLANNING

### MRP Types
| Type | Description |
|------|-------------|
| PD | MRP (demand-driven, dependent requirements) |
| VB | Manual Reorder Point |
| VM | Automatic Reorder Point |
| VV | Forecast-based planning |
| ND | No planning |

### Lot Sizing Procedures
| Procedure | Description |
|-----------|-------------|
| EX | Exact lot size (lot = net requirement) |
| FX | Fixed lot size |
| HB | Replenish to maximum stock level |
| MB | Monthly lot size |
| WB | Weekly lot size |
| TB | Day lot size |
| ZB | Periodic lot size (configurable) |
| GR | Groff reorder procedure |

### MRP Relevant Fields in Material Master (MRP 1-4 Views)
- MRP Type
- MRP Controller
- Lot Size / Rounding Profile
- Minimum and Maximum lot sizes
- Safety Stock / Safety Time
- Planned Delivery Time
- In-house Production Time (for semi-finished)
- Scheduling Margin Key (floats)
- Backflush indicator

### MRP Planning Run
| Transaction | Description |
|-------------|-------------|
| MD01 | Total Planning — all materials in plant |
| MDBT | Total Planning in background |
| MD02 | Single Item Multi-level |
| MD03 | Single Item Single-level |
| MD04 | Stock/Requirements List (MRP result) |
| MD05 | MRP List |
| MD06 | Collective MRP List |
| MD07 | Collective Access to MRP Lists |

### Planning Run Modes
1. **Regenerative Planning (NETCH)**: Replanning all materials
2. **Net Change Planning (NETCH)**: Only materials with changes since last run
3. **Net Change in Planning Horizon (NETPL)**: Changes within planning horizon

### Exception Messages (MD04)
- 01: Reschedule In — existing planned order should be pulled earlier
- 02: Reschedule Out — existing planned order should be pushed later
- 10: Firming date — planned order near firming zone
- 07: Maintain firm receipt — fixed receipt due soon with unconfirmed quantity
- 20: New firm receipt — no receipt exists to cover requirement
- 30: Delayed requirements — requirement cannot be fully covered in time

### Key Interview Questions
> **Q: What is the difference between Planned Orders and Purchase Requisitions in MRP?**
> A: Planned Orders are internal planning elements created by MRP for in-house production. They can be converted to Production Orders. Purchase Requisitions are requests to procurement — MRP creates them for external procurement materials. PRs can then be converted to POs. The procurement type in the material master (E = in-house, F = external, X = both) determines what MRP creates.

> **Q: What is Safety Stock and how does it work in MRP?**
> A: Safety Stock is a fixed quantity maintained in the material master as a buffer against demand/supply uncertainties. MRP treats it as an additional requirement — it ensures the available stock never falls below the safety stock level. Unlike dynamic safety time (coverage profile), static safety stock does not adjust to demand variations.

> **Q: What is the Firming Zone in MRP?**
> A: The firming zone (defined by Planning Time Fence) protects planned orders from automatic rescheduling by MRP. Within this zone, planned orders are "firmed" and MRP will not automatically change them — preventing system-generated disruptions to confirmed production plans.

---

## 12. RELEASE STRATEGY (APPROVAL WORKFLOW)

### Components
1. **Release Group**: Groups together document types subject to release (e.g., PO, PR)
2. **Release Codes**: Individual approver identifiers (e.g., A1, B1, M1)
3. **Release Strategy**: Combination of release codes that defines the approval workflow
4. **Release Characteristic**: Classification characteristic that determines which strategy applies (e.g., total value, document type, plant)
5. **Release Class**: Class that groups the characteristics

### Configuration Path
SPRO → MM → Purchasing → Purchase Order → Release Procedure for Purchase Orders

### How It Works
1. When PO is saved, system evaluates classification of the PO against defined strategies
2. Matching strategy is assigned — release codes are activated in sequence
3. Approver with the release code logs in and releases via ME28 (collective release) or ME29N (individual)
4. After all codes are released, PO is released for further processing (GR, etc.)

### Key Interview Questions
> **Q: What is the difference between Release Strategy and Workflow for PO approval?**
> A: Release Strategy is a standard SAP classification-based approach — simpler, configurable without ABAP, and works within MM transaction codes. Workflow (SAP Business Workflow or BRF+) is more flexible — supports complex routing, notifications, delegation, and integration with other systems. Release Strategy is common for straightforward value-based approvals; Workflow is used for complex, dynamic approval scenarios.

> **Q: Can a released PO be changed and what happens?**
> A: If a field relevant to the release strategy (e.g., total value) changes after release, the system may reset the release status — forcing re-approval. This behavior is controlled by the "Change after Release" indicator in the release strategy configuration.

---

## 13. OUTPUT / MESSAGE DETERMINATION

### Condition Technique for Output
- **Application**: ME (Purchasing)
- **Condition Types**: NEU (New PO), AUFB (PO acknowledgement), MAHNA (Reminder)
- **Access Sequence**: Determines search order for condition records
- **Condition Records**: Stored in NACH table (Nachtichten = Messages)

### Communication Methods
| Medium | Code |
|--------|------|
| Print | 1 |
| Fax | 2 |
| Telex | 3 |
| EDI | 6 |
| Email | 5 |

### Output Types in Purchasing
- NEU — New Purchase Order
- MAHN — Reminder (Dunning)
- AUFB — Order Acknowledgement
- LPET — Scheduling Agreement Deadline Monitoring

### Transaction: MN04 (Create Message Condition Record), MN05 (Change), MN06 (Display)

### Key Interview Questions
> **Q: How does message determination work in purchasing?**
> A: When a PO is saved, SAP triggers message determination using the condition technique. The system evaluates the access sequence of the output type to find a matching condition record (by vendor, purchasing org, document type). The condition record specifies medium (print/email/EDI), timing (immediately/at batch run), and partner function. The output is then queued and processed.

---

## 14. INVOICE VERIFICATION (LOGISTICS INVOICE VERIFICATION — LIV)

### Tolerance Keys (Configuration)
| Key | Description |
|-----|-------------|
| AN | Amount for item without order reference |
| AP | Amount for item with order reference |
| BD | Form small differences automatically |
| BW | Percentage variance (quantity) |
| DQ | Quantity variance |
| KW | Price variance |
| PP | Price variance — moving average |
| PS | Price variance — standard price |
| ST | Date variance |
| VP | Moving average price variance |

### MIRO Transaction Key Tabs
- **Basic Data**: Invoice date, posting date, reference
- **PO Reference**: Reference to PO, GR, or scheduling agreement
- **Payment**: Payment method, payment terms
- **Tax**: Tax code and amount
- **Vendor**: Vendor bank details
- **Details**: Business area, document type

### GR-Based Invoice Verification
When the "GR-Based Invoice Verification" flag is set in vendor master/PIR:
- Invoice can only be posted for quantities already received
- Prevents payment before physical delivery
- Each GR line item must be individually referenced in MIRO

### Blocking Reasons
| Reason | Description |
|--------|-------------|
| M | Manually blocked |
| P | Price tolerance exceeded |
| Q | Quantity tolerance exceeded |
| D | Vendor default (payment block) |
| R | Stochastic block (random sample) |

### Key Transactions
- MIR6 — Invoice overview (see blocked invoices)
- MRBR — Release blocked invoices
- MR8M — Cancel invoice document
- MR11 — Maintain GR/IR account
- MRRL — Evaluate and settle ERS

### Subsequent Debit/Credit
- Used after invoice is already posted
- Subsequent Debit: Vendor charges additional amount (freight, duty)
- Subsequent Credit: Vendor issues credit note
- In MIRO: Select "Subsequent Debit" or "Credit Memo" from dropdown

### Key Interview Questions
> **Q: What is the difference between a Credit Memo and a Subsequent Credit?**
> A: A Credit Memo reverses a previous invoice (reduces the amount already invoiced and payable). A Subsequent Credit reduces the value of a specific delivery/GR without reversing the original invoice — used when a price reduction is agreed after invoicing.

> **Q: What is stochastic blocking and when is it used?**
> A: Stochastic blocking randomly selects invoices for manual verification regardless of tolerance variances. Configured with a probability percentage and minimum invoice amount. Used as a compliance/audit control measure.

---

## 15. INTEGRATION WITH OTHER SAP MODULES

### MM ↔ FI (Financial Accounting)
- Every goods movement generates an accounting document
- Material document (MIGO) = Accounting document (FI)
- Configured via OBYC (automatic account determination)
- Vendor liability posted in FI at MIRO
- Payment cleared in FI by AP team

### MM ↔ SD (Sales & Distribution)
- Stock Transfer Orders use SD delivery process
- Third-party procurement: SD creates PR automatically from sales order
- Returns: SD return sales order triggers MM movement
- Availability check (ATP) reads MM stock

### MM ↔ PP (Production Planning)
- Production orders consume materials via MT 261
- BOM (Bill of Materials) managed in MM/PP
- MRP planned orders converted to production orders
- Backflushing: automatic GI at production order confirmation

### MM ↔ WM (Warehouse Management) / EWM
- MM manages storage location level, WM manages bins within warehouse
- Transfer Order created in WM to fulfill MM transfer requirements
- EWM is the advanced warehouse system (successor to WM) in S/4HANA

### MM ↔ QM (Quality Management)
- Quality inspection lot created at GR
- Material goes to QI stock (MT 103 or inspection setup)
- Usage decision moves material to unrestricted (MT 321) or blocked (MT 344)
- Quality notifications linked to vendor for complaints

### Key Interview Questions
> **Q: How does MM integration with FI work during goods movements?**
> A: When a goods movement is posted in MM (MIGO), the system simultaneously creates an accounting document in FI. The G/L accounts are determined automatically via OBYC (Account Determination) based on movement type, valuation class, and chart of accounts. This ensures real-time inventory accounting without manual journal entries.

---

## 16. KEY CONFIGURATION ACTIVITIES (SPRO)

### Critical Config Nodes
| Config Area | SPRO Path |
|-------------|-----------|
| Purchasing Groups | MM → Purchasing → Create Purchasing Groups |
| Document Types for PO | MM → Purchasing → PO → Define Document Types |
| Number Ranges | MM → Purchasing → PO → Define Number Ranges |
| Release Procedure | MM → Purchasing → PO → Release Procedure |
| Message Determination | MM → Purchasing → Messages |
| Tolerance Keys | MM → LIV → Invoice Block → Set Tolerance Limits |
| Account Determination | MM → Valuation → Account Determination → OBYC |
| Movement Types | MM → Inventory Mgmt → Movement Types |
| Valuation Class | MM → Valuation → Material Valuation → Setup Material Accounts |
| MRP Parameters | MM → Consumption-Based Planning → Master Data |

### Transport Requests in Configuration
- Configuration changes go in Customizing Requests (task type = Customizing)
- Testing in Development → Quality → Production (3-system landscape typical)

---

## 17. KEY TRANSACTION CODES REFERENCE

### Master Data
| TCode | Description |
|-------|-------------|
| MM01/MM02/MM03 | Create/Change/Display Material |
| MMAM | Change Material Type |
| XK01/XK02/XK03 | Create/Change/Display Vendor (Company Code & Purch Org) |
| MK01/MK02/MK03 | Create/Change/Display Vendor (Purch Org only) |
| XK99 | Mass Change Vendor |
| ME11/ME12/ME13 | Create/Change/Display PIR |
| ME01/ME03 | Maintain/Display Source List |

### Procurement
| TCode | Description |
|-------|-------------|
| ME51N/ME52N/ME53N | Create/Change/Display PR |
| ME54N/ME55 | Release PR (individual/collective) |
| ME41/ME42/ME43 | Create/Change/Display RFQ |
| ME47/ME48/ME49 | Quotation/Price Comparison |
| ME21N/ME22N/ME23N | Create/Change/Display PO |
| ME28/ME29N | Release PO (collective/individual) |
| ME31K/ME32K/ME33K | Create/Change/Display Contract |
| ME31L/ME32L/ME33L | Create/Change/Display Scheduling Agreement |
| ME38 | Maintain Delivery Schedule (SA) |
| ME2L/ME2M/ME2N | PO by Vendor/Material/Document |
| ME80FN | General Purchasing Analysis |

### Inventory Management
| TCode | Description |
|-------|-------------|
| MIGO | All Goods Movements |
| MB01/MB0A | Post Goods Receipt (classic) |
| MB51 | Material Document List |
| MB52 | Warehouse Stock Display |
| MB53 | Plant Stock Availability |
| MMBE | Stock Overview |
| MI01/MI04/MI07 | Physical Inventory |
| MIDO | Physical Inventory Overview |

### Invoice Verification
| TCode | Description |
|-------|-------------|
| MIRO | Enter Incoming Invoice |
| MIR4 | Display Invoice Document |
| MIR6 | Invoice Overview |
| MIR7 | Park Invoice |
| MRBR | Release Blocked Invoices |
| MR8M | Cancel Invoice Document |
| MR11 | GR/IR Account Maintenance |
| MRRL | ERS Settlement Run |
| MRKO | Settle Consignment/Pipeline Liabilities |

### MRP
| TCode | Description |
|-------|-------------|
| MD01/MDBT | MRP Total Planning |
| MD02/MD03 | Single Item MRP |
| MD04 | Stock/Requirements List |
| MD06/MD07 | MRP List (collective) |
| MD16 | Collective Conversion of Planned Orders |
| ME57 | Assign and Process PRs |

---

## 18. ADVANCED TOPICS FOR SENIOR ROLES

### Batch Management
- Batch = sub-lot of a material with unique characteristics
- Batch classification: characteristics stored in batch master
- Batch determination in PO, GR, GI using search strategies
- FEFO (First Expired First Out) for shelf-life materials
- Transaction: MSC1N (Create), MSC2N (Change), MSC3N (Display)

### Consignment Settlement (MRKO)
- Settles all consumed consignment/pipeline quantities
- Creates vendor invoices automatically
- Can be run periodically (month-end)

### Schedule Line Categories in STO
- For cross-company STO with SD delivery, schedule line category controls delivery relevance and movement type assignment

### Vendor Evaluation (ME61-ME65)
- Criteria: Price, Quality, Delivery, Service
- Automatic and manual scores
- Used in source determination

### Quota Arrangement
- ME61 (Create Quota Arrangement)
- Splits procurement quantities between multiple vendors by percentage
- MRP respects quota arrangement in vendor selection

### Key Interview Questions for Senior Roles
> **Q: How would you troubleshoot a GR/IR account mismatch at month end?**
> A: Run MR11 (GR/IR Account Maintenance) to identify open items — GRs without invoices (credit balance) and invoices without GR (debit balance). For items older than the tolerance period, either post a clearing entry or investigate with the vendor. Also check FBL3N on the GR/IR account for individual open items and their document references.

> **Q: How do you handle price differences in material ledger?**
> A: In Material Ledger (mandatory in S/4HANA), all price differences from procurement, production, and exchange rates are captured throughout the period. At period end, CKMLCP (Actual Costing Run) distributes these differences to consuming cost objects. This provides actual cost of goods vs standard cost — essential for accurate profitability analysis.

> **Q: Describe your experience with output-related configuration issues in purchasing.**
> A: Common issues include missing condition records (check MN05/MEQ1), incorrect partner functions in vendor master, output types not configured for the document type, and printer/email server setup issues. Debug with ME22N → Messages tab → check processing log. For EDI, check NACE → Application ME → Output Types.

---

## 19. COMMON INTERVIEW SCENARIOS

### Scenario 1: Vendor sends invoice but no GR done
**Answer**: With GR-based IV active, MIRO will not allow posting beyond received quantity. The invoice will be parked (MIR7) and blocked until GR is posted. With GR-based IV inactive, invoice can be posted and a quantity variance block (if configured) will hold it for approval.

### Scenario 2: Material price is MAP, new GR at significantly different price
**Answer**: New MAP = (Old Value + GR Value) / (Old Qty + GR Qty). The debit goes to inventory account at the new MAP. If there is insufficient stock to absorb the difference, the remainder goes to a price difference account. After the GR, the MAP is updated in the material master for future transactions.

### Scenario 3: Purchase Order issued to wrong vendor
**Answer**: If no GR or invoice exists, the PO can be cancelled (set deletion flag, close items). If GR exists, the GR must be reversed (MT 102) before the PO can be changed. If invoice is posted, the invoice must first be cancelled (MR8M), then GR reversed, then PO corrected.

### Scenario 4: MRP is generating too many planned orders
**Answer**: Check planning horizon settings, safety stock levels, lot sizing procedure, scheduling agreement/contract validity. Also check for incorrect open POs or schedule lines inflating supply. Review net requirements calculation in MD04. Consider adjusting the planning time fence to protect the near-term horizon.

---

*End of SAP MM Study Guide — Version 2025 | Covers ECC 6.0 and S/4HANA 2023*
