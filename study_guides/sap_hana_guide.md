# SAP HANA & S/4HANA — Comprehensive Interview Prep Guide
## For Experienced MM/ECC Professionals Transitioning to S/4HANA

---

## 1. SAP HANA DATABASE FUNDAMENTALS

### What is SAP HANA?
SAP HANA (High-performance ANalytic Appliance) is an in-memory, column-oriented, relational database management system. It serves as both a database and an application platform.

### Core HANA Concepts
| Concept | Description |
|---------|-------------|
| In-Memory | All active data stored in RAM — eliminates disk I/O for reads |
| Columnar Storage | Data stored by column (not row) — ideal for analytics/aggregations |
| Row Store | Certain operational tables stored row-wise for fast single-record access |
| Compression | Column store allows 5-10x data compression |
| MVCC | Multi-Version Concurrency Control — readers don't block writers |
| Delta Merge | Writes go to row-based delta store, then merged into column store |

### HANA Architecture Layers
```
Applications (ABAP, Java, HTML5)
         ↓
Index Server (SQL Engine, Calc Engine, Graph Engine)
         ↓
Persistence Layer (Log Volume + Data Volume)
         ↓
Physical Disks (for persistence/restart only)
```

### Column Store vs Row Store
| | Column Store | Row Store |
|-|-------------|-----------|
| Best for | Analytical queries, aggregations | Transactional, single-record updates |
| Compression | Very high | Low |
| Query speed | Fast for few columns, many rows | Fast for all columns of one row |
| Examples in HANA | Most HANA tables | Session management tables |

### Key Interview Questions
> **Q: Why is SAP HANA faster than traditional RDBMS for analytical queries?**
> A: Column storage means only the columns needed for a query are read from memory — not entire rows. This dramatically reduces data volume scanned. Combined with in-memory operation (no disk I/O), data compression (less memory bandwidth), and SIMD CPU instructions for column operations, HANA delivers orders-of-magnitude faster analytics. The elimination of aggregate tables (like totals tables in ECC) also simplifies the data model.

> **Q: What is the Delta Merge in HANA and why does it exist?**
> A: Write operations go to a row-based delta store for fast insert/update performance. Periodically, HANA merges the delta store into the main column store (delta merge). This allows both fast writes (row-optimized) and fast reads (column-optimized). The merge can be triggered manually or automatically based on size thresholds.

---

## 2. S/4HANA vs ECC — KEY DIFFERENCES

### Architecture Shift
| Aspect | ECC | S/4HANA |
|--------|-----|---------|
| Database | Any RDBMS | HANA only |
| Data Model | Complex (aggregate tables, totals tables) | Simplified (aggregate tables eliminated) |
| UI | SAP GUI / Web Dynpro | Fiori (primary) + SAP GUI (compatibility) |
| Vendor/Customer | Separate vendor master / customer master | Business Partner (unified) |
| Material Ledger | Optional | Mandatory |
| Currency | Up to 2 parallel currencies easily | Up to 10 parallel currencies |
| MRP | Classic MRP | MRP Live (embedded in HANA) |
| Reporting | BW aggregates / extractors | Embedded Analytics / CDS views |

### Simplified Data Model — Key Examples
| ECC Tables | S/4HANA Replacement |
|------------|---------------------|
| BKPF + BSEG + BSIS + BSAS + BSID... | ACDOCA (Universal Journal) |
| AUFK + COEP + COSP + COSS | ACDOCA |
| MARA + MARC + MARD + MBEW | Simplified, MATDOC replaces MSEG |
| Customer Master (KNA1+KNB1...) | BP (Business Partner) |
| Vendor Master (LFA1+LFB1...) | BP (Business Partner) |

### Deployment Options
| Type | Description |
|------|-------------|
| S/4HANA Cloud (Public) | Fully managed, standard processes only, quarterly updates |
| S/4HANA Cloud (Private) | Hosted by SAP, customer-specific config, less flexibility than on-prem |
| S/4HANA On-Premise | Customer-hosted, full flexibility, annual release cycle |
| S/4HANA Rise | Commercial offering bundling cloud infrastructure + S/4HANA |

### Key Interview Questions
> **Q: What is the biggest structural change in S/4HANA compared to ECC from an MM perspective?**
> A: Several fundamental changes: (1) Business Partner replaces separate vendor/customer masters — using BP transaction instead of XK01/MK01; (2) Material Ledger is mandatory — all materials must use actual costing; (3) MRP Live runs directly on HANA for near-real-time planning; (4) Inventory management uses MATDOC document table replacing the complex MSEG/MKPF structure; (5) GR/IR clearing is handled differently in the simplified accounting model.

> **Q: Can you still use SAP GUI transactions in S/4HANA?**
> A: Yes, SAP GUI (backend) transactions are largely still available for backward compatibility. However, SAP's strategic direction is Fiori. Some old transactions may be blocked or deprecated in newer S/4HANA releases. New functionality is typically Fiori-only. SAP recommends adopting Fiori for new user onboarding.

---

## 3. BUSINESS PARTNER (BP)

### Why Business Partner?
In ECC, customers (KNA1, KNB1) and vendors (LFA1, LFB1, LFM1) were completely separate master records — even for the same real-world entity. BP unifies them under a single master record.

### BP Roles in Purchasing Context
| BP Role | Description | TCode (old) |
|---------|-------------|-------------|
| BP (General) | Basic partner data | — |
| FLVN00 | Vendor (Purchasing Org data) | MK01 |
| FLVN01 | FI Vendor (Company Code data) | XK01 |
| FLCU00 | Customer (Sales Area data) | VD01 |
| FLCU01 | FI Customer (Company Code data) | XD01 |

### BP Categories
- **Person**: Individual person (HR-related)
- **Organization**: Legal entity (companies, organizations)
- **Group**: Group of persons

### Migration from Vendor to BP
During ECC → S/4HANA migration, the FSCM_BP (Business Partner Migration) program synchronizes existing vendors to Business Partners. Old vendor transactions (XK01, MK01) work via SAP-delivered compatibility mode during transition.

### Configuring BP for Procurement
1. Create Number Range for BP
2. Define BP Grouping (controls number range and screen layout)
3. Assign BP roles to grouping
4. Activate CVI (Customer-Vendor Integration) synchronization
5. Configure account groups to BP groupings mapping

### Key Interview Questions
> **Q: In S/4HANA, if a user tries to use MK01 to create a vendor, what happens?**
> A: In S/4HANA, MK01 routes to the BP transaction via compatibility coding. The user may see the old UI but a BP is created in the background. However, SAP strongly recommends using transaction BP directly. In some S/4HANA releases, MK01 may be fully deprecated. For Fiori, the "Create Supplier" (Manage Business Partner) app is used.

> **Q: What is CVI (Customer-Vendor Integration)?**
> A: CVI is a synchronization mechanism that keeps the BP data and legacy customer/vendor master data in sync. When a BP is created/changed, CVI automatically updates the corresponding vendor master (LFA1/LFB1) tables and vice versa. This allows compatibility with ABAP programs that still read LFA1/LFB1 while the master data is managed via BP.

---

## 4. FIORI APPS FOR MM

### Fiori App Types
| Type | Description | Examples |
|------|-------------|---------|
| Transactional | Replace single MM transactions | Create Purchase Order |
| Analytical | KPIs, charts, dashboards | Purchase Order Value per Vendor |
| Fact Sheet | Display object details (search-driven) | Material Details, Supplier Overview |

### Key Fiori Apps for MM

**Procurement:**
| App Name | Replaces | Description |
|----------|----------|-------------|
| Create Purchase Order | ME21N | Create PO with modern UX |
| Manage Purchase Orders | ME22N/ME23N | Change/display POs with filtering |
| My Purchase Requisitions | ME52N | PR management by requester |
| Approve Purchase Orders | ME28/ME29N | PO approval workflow |
| Manage Supplier Invoices | MIRO | Invoice entry and management |
| Release Supplier Invoices | MRBR | Release blocked invoices |

**Inventory:**
| App Name | Replaces | Description |
|----------|----------|-------------|
| Post Goods Receipt | MIGO | GR posting (simplified) |
| Stock Overview | MMBE | Real-time stock visibility |
| Monitor Inventory | — | Analytics for inventory levels |
| Create Physical Inventory Document | MI01 | Physical inventory creation |

**Master Data:**
| App Name | Replaces | Description |
|----------|----------|-------------|
| Manage Business Partner | XK01/MK01 | Vendor/customer creation in BP model |
| Maintain Material | MM01 | Material master management |
| Manage Purchasing Info Records | ME11 | PIR management |

### Fiori Launchpad
- Entry point for all Fiori apps
- Tiles organized in groups
- Personalization: Users can add/remove tiles, create their own groups
- Role-based: Tiles visible based on authorization role (business catalog)

### Fiori Architecture
```
Browser (HTML5)
    ↓
Fiori Frontend Server (Gateway + ABAP)
    ↓
OData Service (backend data provider)
    ↓
S/4HANA Backend (application logic)
```

### Key Interview Questions
> **Q: What is the difference between an OData service and a classic ABAP program?**
> A: An OData (Open Data Protocol) service exposes business data as RESTful web services (CRUD operations via HTTP). Fiori apps consume OData services — the Fiori frontend (HTML5/UI5) sends HTTP GET/POST/PATCH/DELETE requests to OData services, which then execute ABAP logic on the backend. Classic ABAP programs run entirely on the server and serve SAP GUI. OData enables the decoupling of UI from backend.

> **Q: How does the tile count (badge) on a Fiori tile work?**
> A: The badge/count on a Fiori tile is provided by an OData service returning an annotation called `UI.Badge`. The Launchpad calls the count endpoint periodically (or on page load) and displays the result on the tile. For example, "Purchase Orders to Approve" tile shows the number of POs pending the user's release.

---

## 5. MRP LIVE (S/4HANA)

### Classic MRP vs MRP Live
| Aspect | Classic MRP (ECC) | MRP Live (S/4HANA) |
|--------|-------------------|---------------------|
| Execution | Sequential, material-by-material | Parallel, multi-material |
| Location | ABAP layer | HANA procedures |
| Speed | Hours for large runs | Minutes (10-100x faster) |
| Lock behavior | Locks all planning records | Fine-grained locking |
| Transaction | MD01, MDBT | MD01N, MDBT (with HANA engine) |
| BOM explosion | In ABAP | In HANA |
| Availability | ECC 6.0 EhP7+ | S/4HANA |

### Enabling MRP Live
1. Activate switch PLMD_MRP in SFW5 (Business Function: Embedded MRP)
2. Ensure materials use MRP type compatible with HANA MRP
3. Run via MD01N or MDBT with "MRP Live" indicator

### Key Benefits of MRP Live
- Planning runs during business hours without major performance impact
- Real-time re-planning after demand changes
- Responsive planning horizon (shorter planning cycles possible)
- Detailed exception monitoring in Fiori

### Key Interview Questions
> **Q: How does MRP Live improve on Classic MRP?**
> A: MRP Live executes planning directly in HANA using native procedures (not ABAP). It processes materials in parallel rather than sequentially, reducing a 4-hour MRP run to under 15 minutes for large plants. It also allows finer-grained locking so other users can work during MRP. The planning logic is the same as classic MRP — results are identical, only the execution engine changes.

---

## 6. MATERIAL LEDGER IN S/4HANA

### Why Mandatory?
In ECC, Material Ledger (ML) was optional. In S/4HANA, it is mandatory because:
- The simplified accounting model (ACDOCA) requires ML for inventory valuation
- ML provides multi-currency inventory valuation
- Actual costing (optional within ML) allows product cost actuals

### Material Ledger Concepts
| Concept | Description |
|---------|-------------|
| ML Document | Records all value movements for a material in a period |
| Preliminary Valuation | Value at standard price during the period |
| Actual Price | Calculated at period close via actual costing run |
| Price Difference | Variance between standard and actual, allocated at period end |
| Alternative Valuation Run | CKMLCPAVR — calculate actual cost for parallel ledgers |

### Actual Costing Run (CKMLCP)
Steps in sequence:
1. **Opening of new period**: MMPV (open new posting period for MM)
2. **Single-level price determination**: Calculate actual cost from procurement
3. **Multi-level price determination**: Propagate cost differences up BOM
4. **Close**: Finalize and post differences

### Material Ledger Documents
- Created for every inventory movement
- Link accounting documents with material valuation
- Visible via MR51 (Material Ledger Documents per Material)

### Key Interview Questions
> **Q: What is the purpose of the Actual Costing Run in S/4HANA?**
> A: The Actual Costing Run (CKMLCP) calculates the actual cost of materials at period end. During the period, materials are valued at standard price. Differences (price variances from procurement, exchange rate differences) are collected in the ML. At period close, CKMLCP distributes these differences to all consuming cost objects, providing actual product cost — essential for accurate profitability analysis and inventory valuation.

> **Q: What happens if Material Ledger is not configured correctly during S/4HANA go-live?**
> A: Incorrect ML configuration can cause posting errors for all goods movements. Key requirements: ML must be activated in valuation area, all materials must be set up with the correct valuation variant, the ML document type must be defined. Missing or incorrect setup leads to posting failures (error M7 021 or similar). A cutover plan must include ML balance migration from ECC.

---

## 7. CENTRAL PURCHASING IN S/4HANA

### SAP Central Procurement
S/4HANA introduced Central Purchasing to manage procurement across multiple backend systems from a single hub:
- Central Purchase Contracts visible across all connected systems
- Central purchasing analytics
- Manage supplier catalog centrally

### Two-System Landscapes
- **Hub System**: S/4HANA acting as central procurement hub
- **Spoke Systems**: Backend ECC or S/4HANA systems where actual transactions run

### Key Interview Questions
> **Q: What is the difference between a Hub-Spoke procurement model and a standalone S/4HANA?**
> A: Standalone S/4HANA manages procurement within a single system. Hub-Spoke (Central Procurement) connects an S/4HANA hub to multiple backend systems (ECC or other S/4HANA instances). The hub provides a unified view of contracts and analytics across all spokes, even when physical transactions occur in the spoke systems. Useful for global companies with multiple SAP instances.

---

## 8. EWM (EXTENDED WAREHOUSE MANAGEMENT)

### EWM vs Classic WM
| Aspect | Classic WM (ECC) | EWM (S/4HANA) |
|--------|-----------------|----------------|
| Integration | Tightly coupled with MM | Decoupled (separate WM layer) |
| Location | Within ECC | Embedded in S/4HANA or stand-alone |
| Features | Basic bin management | Advanced: Slotting, labor mgmt, yard mgmt |
| Document | Transfer Order | Warehouse Task (WT) / Warehouse Order (WO) |
| User | SAP GUI/TCode | Fiori + RF Framework |
| Wave management | Not available | Available |
| Yard management | Not available | Available |

### EWM Architecture in S/4HANA
- **Embedded EWM**: EWM runs within S/4HANA system (recommended for new implementations)
- **Decentralized EWM**: Separate EWM system connected to S/4HANA via ALE/IDoc

### EWM Key Terms
| Term | Description |
|------|-------------|
| Warehouse Number | Unique identifier for a warehouse complex |
| Storage Type | Physical area within warehouse (e.g., Bulk, Rack, Floor) |
| Storage Section | Subdivision of storage type |
| Storage Bin | Smallest addressable unit (like a shelf slot) |
| HU (Handling Unit) | Packaged unit with barcode/label |
| Warehouse Task (WT) | Instruction to move goods between bins |
| Warehouse Order (WO) | Grouping of warehouse tasks for a worker |
| Physical Inventory (EWM) | Bin-level counting, distinct from MM inventory |

### GR Process in EWM
1. PO created in MM (S/4HANA core)
2. Inbound delivery created (via VL31N or automatically)
3. Inbound delivery transferred to EWM
4. EWM creates put-away warehouse task
5. RF/Fiori user confirms put-away to bin
6. Goods receipt confirmed in MM

### Key Interview Questions
> **Q: What is the difference between a Warehouse Task and a Transfer Order in classic WM?**
> A: A Transfer Order (classic WM) is a simple instruction to move goods from source to destination bin. A Warehouse Task (EWM) is more granular — it represents a single physical movement step. Multiple warehouse tasks can be grouped into a Warehouse Order for efficient worker routing. EWM also supports two-step picking (staging area) and complex putaway strategies.

> **Q: How does EWM integrate with MM in S/4HANA?**
> A: When a goods movement relevant to a WM warehouse occurs in MM (e.g., GR against PO), the integrated EWM is automatically notified and creates corresponding warehouse tasks. The goods receipt is only finalized in MM after the EWM put-away is confirmed. This ensures inventory consistency between MM (storage location level) and EWM (bin level).

---

## 9. MIGRATION FROM ECC TO S/4HANA

### Migration Approaches
| Approach | Description | Best For |
|----------|-------------|----------|
| Greenfield (New Implementation) | Fresh S/4HANA installation, migrate only master data + open items | Large transformation, process redesign |
| Brownfield (System Conversion) | Convert existing ECC to S/4HANA, all history preserved | Minimal disruption, speed |
| Bluefield (Selective Data Transition) | Mix: some processes migrated, some run in parallel | Complex multi-entity scenarios |
| Shell Conversion | Convert system structure without business data, then migrate data | Clean data fresh start |

### Key Migration Checks for MM
1. **Business Partner Migration**: All vendors migrated to BP model
2. **Material Ledger Activation**: ML must be activated for all valuation areas
3. **Custom Code Adaptation**: ABAP code reading obsolete tables must be updated (use Custom Code Migration Tool)
4. **S/4HANA Simplification List**: SAP publishes a list of all functional changes — must be reviewed
5. **Add-on compatibility**: All installed add-ons must be S/4HANA-compatible
6. **Fiori setup**: Frontend server configuration, business catalogs/roles

### SAP Readiness Check
Tool available on SAP Launchpad that analyzes existing ECC system:
- Identifies simplification items affecting the system
- Custom code that needs adaptation
- Add-on compatibility issues
- Provides effort estimates

### Simplification Items (Key MM Examples)
| Item | Change in S/4HANA |
|------|------------------|
| Material Number Length | Up to 40 characters (ECC: 18) — requires configuration |
| Aggregation Tables | Eliminated (e.g., MCHBH, MKOL) — custom code reading these must be rewritten |
| Purchase Info Record | New EINA/EINE structure in HANA — read via virtual data model |
| Goods Movement | MATDOC replaces MSEG/MKPF — new API for GR posting |
| Account Determination | KOBP/KOSP tables changed — custom account determination exits may need update |

### Key Interview Questions
> **Q: What is a Brownfield migration and what are its main risks?**
> A: Brownfield (system conversion) in-place converts an ECC system to S/4HANA, preserving all historical data and transactions. Risks include: data volume (HANA requires significant RAM), custom code requiring updates (checked via Custom Code Migration), business process disruptions if simplification items are not addressed, and the complexity of testing a live system conversion. Advantage: no data migration project, historical reporting continuity.

> **Q: What is the S/4HANA Simplification List?**
> A: SAP publishes a Simplification List for each S/4HANA release (available on SAP Help Portal). It documents every functional and technical change from ECC — what's removed, changed, or added. For MM, it details changes to tables, transaction codes, APIs, and business processes. It must be reviewed by both functional and technical teams before any migration project.

> **Q: How does custom code adaptation work for S/4HANA migration?**
> A: SAP provides the Custom Code Migration tool and ATC (ABAP Test Cockpit) with S/4HANA-specific checks. These tools scan customer ABAP code and flag: reading from obsolete tables, use of deprecated APIs, SQL statements on eliminated aggregate tables, and other incompatibilities. Flagged code must be rewritten to use the new APIs or virtual data models before migration.

---

## 10. S/4HANA EMBEDDED ANALYTICS

### CDS Views (Core Data Services)
- Virtual data models defined in ABAP
- Replace aggregate/totals tables for reporting
- Two types: **Basic CDS** (data foundation) and **Analytical CDS** (cube/dimension views)
- Consumed by Fiori analytical apps, Analysis for Office, SAP Analytics Cloud

### Key MM Analytical CDS Views
| CDS View | Description |
|----------|-------------|
| C_PurchaseOrderAnalysis | Purchase order analytics |
| C_PurchasingInfoRecordTP | PIR analytical view |
| I_MaterialStock | Real-time stock analytical view |
| C_GRIRAccountMaintenance | GR/IR analytics |
| C_SupplierInvoiceAnalysis | Invoice analytics |

### SAP Analytics Cloud (SAC) Integration
- SAC connects to S/4HANA live via OData or import mode
- Live connection: Real-time queries to HANA
- Provides ML-based planning, predictive analytics, collaborative finance planning

### Embedded BW (BW4HANA)
- HANA-optimized data warehouse
- Replaces standalone BW for most scenarios
- Data sources: CDS views, extractors (still available)

### Key Interview Questions
> **Q: What is the difference between a CDS view and an ABAP report for analytics?**
> A: A CDS view is a virtual data model defined in the database layer — it pushes computation down to HANA (code-to-data paradigm). Results are served directly from HANA memory without ABAP processing overhead. An ABAP report pulls data to the application server for processing. CDS views are dramatically faster for large datasets and are the S/4HANA recommended approach for analytical queries. They're also consumable by multiple frontend tools (Fiori, Analysis for Office, SAC).

---

## 11. SOURCING AND PROCUREMENT IN S/4HANA

### New Purchasing Features
1. **Central Contracts**: Company-wide contracts accessible across plants/org units
2. **Purchase Contract Cockpit**: Single view of all contracts with compliance monitoring
3. **Intelligent Sourcing**: ML-recommended suppliers based on history
4. **Procurement Analytics**: Real-time spending analytics via Fiori

### SRM (Supplier Relationship Management) Convergence
In S/4HANA, many SRM functions are embedded:
- Self-service procurement (shopping cart) via S/4HANA
- Central contracts
- Supplier qualification integrated with Ariba Network

### Ariba Integration
- SAP Ariba handles external procurement network
- Ariba Network connects buyers and suppliers globally
- Integration scenarios: Purchase Requisition to Ariba, Invoice from Ariba to S/4HANA (via Ariba Network)
- Transaction data flows via middleware (SAP Integration Suite)

### Key Interview Questions
> **Q: How does S/4HANA integrate with SAP Ariba?**
> A: S/4HANA connects to Ariba via SAP Integration Suite (formerly Cloud Platform Integration). Procurement scenarios: PRs created in S/4HANA are transferred to Ariba for sourcing/approval, POs flow back to S/4HANA after approval, invoices from suppliers via Ariba Network are transferred to S/4HANA for posting. The integration uses standard APIs and can be configured via SAP's pre-built integration flows.

---

## 12. S/4HANA SPECIFIC TCODES AND APPS

### Changed/New Transactions
| S/4HANA | ECC Equivalent | Description |
|---------|---------------|-------------|
| MD01N | MD01/MDBT | MRP Live planning run |
| F3000 (Fiori) | MIGO | Post Goods Receipt (Fiori) |
| BP | XK01/MK01 | Create Business Partner |
| CKMLCP | CKMLCP (similar) | Actual Costing Run (enhanced) |
| S_AL_87000027 | MMBE | Stock Overview (Fiori preferred) |
| FAGLL03H | FBL3N | G/L Line Items (HANA-optimized) |

### Deprecated/Changed in S/4HANA
| ECC TCode | Status in S/4HANA | Reason |
|-----------|------------------|--------|
| MB51 | Available but use Fiori | Replaced by analytical Fiori app |
| MK01/MK02 | Works via compatibility | Use BP instead |
| ME49 | Works | Still available |
| MRKO | Works | Consignment settlement still valid |
| MMPV | Works | Period closing still required |
| CKMVFM | Works | ML revaluation |

---

## 13. KEY S/4HANA INTERVIEW SCENARIOS

### Scenario 1: ECC vendor master has 10,000 vendors — how to migrate to BP?
**Answer**: Use the FSCM_BP migration program or the Vendor Integration Workbench (transaction MDMGX). The program reads existing LFA1/LFB1/LFM1 records and creates corresponding Business Partners with the correct roles (FLVN00 for purchasing, FLVN01 for FI data). Exceptions (duplicate data, missing mandatory fields) must be resolved before migration. The CVI cockpit tracks migration status.

### Scenario 2: MRP run produces different results in S/4HANA vs ECC
**Answer**: MRP Live uses the same core algorithm but differences can arise from: parallel processing sequence (results should be same mathematically but floating-point rounding may differ), firming zones calculated differently, planning horizon configuration, or HANA-side fixes for known ECC MRP issues (check simplification list). Run MD05N comparison reports and check MD04N for specific materials. Engage SAP if systematic differences found.

### Scenario 3: User reports that stock in MMBE doesn't match accounting value
**Answer**: In S/4HANA with Material Ledger, stock quantity is managed in MM (MARD/MARC) and value in ML (MLBESTAND, ACDOCA). If there is a discrepancy, run CKMVFM (Material Ledger: Revaluation) or check for update errors (SM13). Also check if the period is properly closed (MMPV) and if the costing run (CKMLCP) was completed. CKMI1 (Post Closing) ensures ML values align with FI.

### Scenario 4: Fiori app for GR posting shows different fields than MIGO
**Answer**: Fiori GR apps expose a simplified, role-based interface — they don't show all MIGO fields. For complex GR scenarios (split valuation, multiple account assignments, special stocks), MIGO via SAP GUI or SAP Business Client may still be needed. The Fiori app is designed for common 80% use cases. Custom Fiori extensions can add fields via app extensibility (key user tools in S/4HANA Cloud or AIF-based extensions in on-premise).

---

## 14. HANA STUDIO AND HANA ADMINISTRATION

### SAP HANA Studio
- Eclipse-based IDE for HANA development and administration
- Key perspectives: Administration, Modeler, Debugger

### Basic HANA SQL
```sql
-- Check column store table size
SELECT TABLE_NAME, MEMORY_SIZE_IN_TOTAL/1024/1024 AS SIZE_MB
FROM M_CS_TABLES
WHERE SCHEMA_NAME = 'SAPHANADB'
ORDER BY MEMORY_SIZE_IN_TOTAL DESC;

-- Check row count
SELECT COUNT(*) FROM "SAPHANADB"."EKKO";

-- Column store aggregation (fast)
SELECT LIFNR, SUM(NETWR) AS TOTAL
FROM "SAPHANADB"."EKKO"
GROUP BY LIFNR;
```

### Key HANA Monitoring Views (M_ prefix = System Views)
| View | Description |
|------|-------------|
| M_CS_TABLES | Column Store table info |
| M_RS_TABLES | Row Store table info |
| M_SERVICE_MEMORY | Memory usage by service |
| M_LOAD_HISTORY_SERVICE | CPU/memory trends |
| M_BACKUP_CATALOG | Backup history |
| M_CONNECTIONS | Active DB connections |

### Key Interview Questions
> **Q: What is the difference between Column Store and Row Store in HANA, and how does it affect MM queries?**
> A: Column store organizes data by column — when querying specific columns across many rows (like summing PO values by vendor), only those columns are read, making it very fast. Row store organizes data by row — for single-record reads/updates (like looking up one PO header), row store is faster. In HANA, most business tables are column-stored. MM analytics (MB52 stock report, purchasing analysis) benefit enormously from the column store since they aggregate across millions of rows but only need a few columns.

---

## 15. SAP SUCCESSFACTORS AND CONCUR RELEVANCE (CLOUD ECOSYSTEM)

### SAP Business Technology Platform (BTP)
- Platform for building extensions and integrations
- Key services: SAP Integration Suite, SAP Build (low-code), SAP Analytics Cloud, HANA Cloud
- Replaces SAP Cloud Platform (SCP)

### Integration with SAP Cloud Applications
| Cloud App | Integration with S/4HANA MM |
|-----------|---------------------------|
| SAP Ariba | Procurement, sourcing, supplier management |
| SAP FieldGlass | Contingent workforce, service procurement |
| SAP Concur | Travel & expense (indirect procurement) |
| SAP IBP | Integrated Business Planning (advanced supply chain) |
| SAP Asset Manager | Asset management (PM-linked procurement) |

### Key Interview Questions
> **Q: How does SAP IBP differ from MRP Live for supply chain planning?**
> A: MRP Live handles operational short-term planning within S/4HANA (days to weeks horizon, material requirements). SAP IBP (Integrated Business Planning) is a strategic and tactical planning solution on BTP — covers demand sensing, supply planning, S&OP, and inventory optimization over longer horizons (months to years). IBP and S/4HANA are integrated: IBP's constrained supply plans are pushed to S/4HANA as planned orders or purchase requisitions.

---

## 16. CERTIFICATION RELEVANCE

### SAP Certifications Relevant to MM/S4HANA
| Certification | Code | Description |
|--------------|------|-------------|
| SAP S/4HANA Sourcing and Procurement | C_TS450_2022 | MM in S/4HANA (primary) |
| SAP S/4HANA Supply Chain - Inventory Management | C_TSCM52_67 | Inventory focus |
| SAP ERP Materials Management (ECC) | C_TSCM52_67 | Legacy ECC cert |
| SAP Certified Associate – S/4HANA Cloud (MM) | Cloud-specific | For cloud implementations |

### Study Tips for S/4HANA MM Certification
1. Focus on Business Partner concept and setup
2. Understand Material Ledger mandatory activation
3. Know MRP Live configuration and differences
4. Practice Fiori app navigation and configuration
5. Know the Simplification List changes for MM
6. Understand the EWM vs WM differences
7. Practice HANA concepts (column store, in-memory)

---

*End of SAP HANA & S/4HANA Study Guide — Version 2025 | Covers S/4HANA 2023/2024*
