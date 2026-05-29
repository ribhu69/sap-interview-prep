# SAP ECC (ERP Central Component) — Comprehensive Interview Prep Guide
## For Experienced Professionals (5+ Years) | Architecture, Configuration & Technical Concepts

---

## 1. SAP ECC ARCHITECTURE

### What is SAP ECC?
SAP ECC (ERP Central Component) is SAP's on-premise ERP suite, with the latest release being ECC 6.0 (also called SAP ERP 6.0). It includes core business modules: FI, CO, MM, SD, PP, HR, PM, QM, WM, and others.

### Three-Tier Architecture
```
Presentation Layer  →  SAP GUI / Web Dynpro / Fiori (via Gateway)
Application Layer   →  Work Processes (DIA, BGD, UPD, ENQ, MSG, SPO)
Database Layer      →  Any supported RDBMS (Oracle, DB2, MaxDB, HANA)
```

### Work Process Types
| Type | Code | Description |
|------|------|-------------|
| Dialog | DIA | Handles user interactions (online transactions) |
| Background | BGD | Batch jobs (MRP runs, reports) |
| Update | UPD/UP2 | Asynchronous database updates |
| Enqueue | ENQ | Manages locks |
| Message | MSG | Routes RFC calls between instances |
| Spool | SPO | Manages print output |

### SAP Client
A client is a self-contained unit within an SAP system. Configuration, master data, and transaction data are client-dependent. Standard clients:
- **000**: Reference client (do not modify)
- **001**: Customizing template (copy of 000)
- **066**: EarlyWatch client (SAP support)
- Customer clients: e.g., 100 (DEV), 200 (QAS), 300 (PRD)

### System Landscape
Typical 3-system landscape:
```
DEV (Development) → QAS (Quality/Test) → PRD (Production)
```
Changes flow from DEV to QAS (via transport) to PRD after testing.

---

## 2. CUSTOMIZING AND CONFIGURATION

### Implementation Guide (IMG) — Transaction SPRO
The IMG (Implementation Guide) is the central tool for SAP configuration. It provides a tree structure of all configuration activities.

### Types of Customizing
| Type | Description | Transport |
|------|-------------|-----------|
| Client-independent | Applies across all clients (number ranges for transport, etc.) | System change request |
| Client-dependent | Applies within one client | Customizing request |

### Customizing vs Development
| Aspect | Customizing | Development |
|--------|-------------|-------------|
| Tool | SPRO (IMG) | ABAP Workbench (SE80) |
| Skill needed | Functional | Technical (ABAP) |
| Risk | Lower | Higher |
| Transport type | Customizing request | Workbench request |
| Examples | Tolerance keys, document types | User exits, BADIs, reports |

### Key Interview Questions
> **Q: What is the difference between a Customizing request and a Workbench request?**
> A: A Customizing request (task type = Customizing) carries configuration table entries (from SPRO). A Workbench request (task type = Workbench) carries ABAP objects — programs, function modules, classes, data dictionary objects. Both are transport requests but serve different purposes and go through the same transport path.

> **Q: Can you explain the "Spanner" icon in SPRO?**
> A: The spanner icon indicates an activity is critical and cannot be undone easily. It's a warning to proceed with care. Other icons indicate: clock (time-critical), checkbox (one-time activity), info (documentation only), arrow (go to a transaction).

---

## 3. TRANSPORT MANAGEMENT SYSTEM (TMS)

### Transport Request Lifecycle
1. Developer creates/modifies objects → captured in a Task (sub-unit of request)
2. Task released → object locked in request
3. Request released → becomes a transportable cofile (.cofiles) and data file (.data)
4. Basis team imports via STMS to QAS, then PRD

### Transport Request Types
| Type | Description |
|------|-------------|
| Workbench | ABAP programs, function modules, dictionary objects |
| Customizing | IMG configuration table entries |
| Transport of Copies | Copy of objects, not tracked (for hotfixes/emergency) |
| Relocation | Move objects between systems without deletion |

### Key Transactions
| TCode | Description |
|-------|-------------|
| SE09/SE10 | Create/Display Transport Requests (organizer) |
| STMS | Transport Management System |
| SCC1 | Client Copy within system |
| SM35 | Batch Input Sessions |
| SM37 | Background Job Monitor |

### Transport Issues and Troubleshooting
- **Object locked**: Another request has the object → coordinate with team or reassign
- **Missing objects**: Check SLIN (ABAP extended check), SE80 for consistency
- **Import errors in QAS**: Check STMS import log → common causes: missing basis objects, syntax errors, missing table entries in target system
- **Retransport**: Use SE01 to create new request and add objects

### Key Interview Questions
> **Q: What happens when you release a transport request?**
> A: Releasing a request freezes its content — no more changes can be made. The system generates export files in the transport directory (/usr/sap/trans/): cofiles (contain object list) and data files (contain actual data). The request is then queued for import in the target system's TMS import queue.

> **Q: How do you handle an urgent fix that needs to go directly to Production?**
> A: For an emergency fix, a "rush transport" or "hotfix" approach is used: create a transport of copies in Development, test minimally in QAS or a sandbox, and import to Production with explicit approval from change management. This should be documented and a proper fix subsequently developed and transported through the standard path.

---

## 4. ABAP FUNDAMENTALS FOR FUNCTIONAL CONSULTANTS

### Understanding ABAP Programs
| Type | Description | Example |
|------|-------------|---------|
| Type 1 | Executable (reports) | Reports via SE38 |
| Type M | Module pool | Dialog transactions |
| Type F | Function group/module | Function modules |
| Type K | Class | OO ABAP classes |
| Type J | Interface | OO interfaces |
| Type X | Includes | Code includes |

### ABAP Data Dictionary (SE11)
- **Tables**: Transparent (1-to-1 with DB table), Pool, Cluster
- **Views**: Database view, Projection view, Maintenance view, Help view
- **Data Elements**: Define the semantic meaning and field labels
- **Domains**: Define technical attributes (data type, length, value range)
- **Structures**: Like tables but without DB storage (used in programs)
- **Type groups**: Shared type definitions

### Reading Data in ABAP (Relevant to Functional)
```abap
" Reading from a single table
SELECT * FROM ekko INTO TABLE lt_ekko
  WHERE bukrs = '1000'
  AND bstyp = 'F'.  " Purchase Orders

" Inner join example
SELECT a~ebeln, a~ebelp, b~matnr
  FROM ekko AS a
  INNER JOIN ekpo AS b ON a~ebeln = b~ebeln
  INTO TABLE lt_result
  WHERE a~lifnr = lv_vendor.
```

### Key Purchasing Tables
| Table | Description |
|-------|-------------|
| EKKO | Purchasing Document Header |
| EKPO | Purchasing Document Item |
| EKBE | Purchasing Document History |
| EKET | Scheduling Agreement Schedule Lines |
| EKES | Vendor Confirmations |
| EORD | Source List |
| EINA | Purchasing Info Record (General) |
| EINE | Purchasing Info Record (Org Level) |
| EKPV | Shipping-Specific Data for PO |
| MSEG | Material Document Segment |
| MKPF | Material Document Header |
| MARA | Material General Data |
| MARC | Plant-Level Material Data |
| MARD | Storage Location Data |
| MAKT | Material Descriptions |
| MARM | Material Units of Measure |
| LFA1 | Vendor Master (General) |
| LFB1 | Vendor Master (Company Code) |
| LFM1 | Vendor Master (Purchasing Org) |
| T001 | Company Codes |
| T001W | Plants |
| T024 | Purchasing Groups |

### Key Interview Questions
> **Q: What tables would you query to find all PO line items with GR documents for a specific material?**
> A: Join EKKO (PO header) + EKPO (PO item) on EBELN for PO details, then join EKBE (PO history — movement type 'E' for GR entries) to get GR documents. Filter by MATNR in EKPO. MSEG/MKPF can provide the full goods movement details.

> **Q: Where is the actual stock quantity stored in the database?**
> A: Unrestricted stock is stored in MARD (Storage Location Data) in the LABST field. Other stock types: EINME (quality inspection), SPEME (blocked), RETME (returns). Plant stock (without SL) is in MARC: LBKUM (total stock), INSME, SPEME. Note: In S/4HANA, the new unified journal removes some redundant tables.

---

## 5. USER EXITS, BADIs, AND ENHANCEMENT FRAMEWORK

### Enhancement Types (Evolution)
```
Classic User Exits (pre-4.6)
  → BADIs (Business Add-Ins, ~4.6+)
    → Enhancement Framework (EHP+ and later)
      → New Enhancement Framework (implicit / explicit enhancements)
```

### Classic User Exits
- Function module-based exits in SAP standard code
- Called via CALL CUSTOMER-FUNCTION
- Find exits: SMOD transaction
- Implement via CMOD (Project creation)
- Examples in MM:
  - **EXIT_SAPMM06E_001**: Exit for PO header data
  - **EXIT_SAPMM06E_006**: Exit for PO item data
  - **MBCF0002**: Goods Movement item check

### BADIs (Business Add-Ins)
- Object-oriented enhancement mechanism
- Classic BADIs (SE18/SE19) and New BADIs (AIF)
- Can have multiple active implementations
- Key MM BADIs:
  - **ME_PROCESS_PO_CUST**: Process purchase orders (most used)
  - **ME_PROCESS_REQ_CUST**: Process purchase requisitions
  - **MB_DOCUMENT_BADI**: Post goods movements
  - **ME_TAX_FROM_ADDRESS**: Determine tax from address

### Enhancement Framework (EHP)
| Type | Description |
|------|-------------|
| Implicit Enhancement | Add code at start/end of any form/function |
| Explicit Enhancement | Pre-defined enhancement points in SAP code |
| Enhancement Spot | Container for explicit enhancements |
| Enhancement Implementation | The customer's actual code |

### Finding User Exits/BADIs
1. Run transaction in debug mode (add `/h` before TCode)
2. Set breakpoint on CALL CUSTOMER-FUNCTION or GET BADI
3. Use SE84 (ABAP Workbench Repository Browser) to search
4. Use SPRO documentation
5. Consult OSS notes or SAP help

### Key Interview Questions
> **Q: What is the difference between a User Exit and a BADI?**
> A: User Exits are function module-based with a fixed interface — only one implementation is possible per exit. BADIs are object-oriented and support multiple implementations simultaneously. BADIs also support filters (to run implementation only for specific conditions). The enhancement framework (new BADIs) further improves on this by supporting implicit enhancements and better lifecycle management.

> **Q: How would you add a custom validation when saving a Purchase Order?**
> A: Use BADI ME_PROCESS_PO_CUST, method PROCESS_HEADER or PROCESS_ITEM. In the method, check your custom condition and raise a message (using method MESSAGES → ADD_MESSAGE) if validation fails — this will display the error and prevent saving. Implement via SE19 (Create BADI Implementation), assign to the BADI definition, activate.

> **Q: What is an implicit enhancement and how is it used?**
> A: Implicit enhancements are pre-defined hook points at the beginning and end of every ABAP program, form routine, and function module. They are activated in enhancement mode (Utilities → Enhancement Operations → Enter Enhancement Mode in SE38). You can add code that executes before/after the standard logic without modifying SAP objects.

---

## 6. AUTHORIZATION CONCEPT

### Authorization Objects
Authorization is controlled through Authorization Objects, each containing fields with allowed values.

Key Authorization Objects in MM:
| Object | Description |
|--------|-------------|
| M_BEST_BSA | Authorization for PO document types |
| M_BEST_EKG | Authorization for Purchasing Groups |
| M_BEST_EKO | Authorization for Purchasing Organizations |
| M_BEST_WRK | Authorization for Plants |
| M_MSEG_BWA | Authorization for Movement Types |
| M_MSEG_WMB | Authorization for Plants in IM |
| M_RQST_BSA | Authorization for PR document types |

### Roles and Profiles
- **Transaction Role (Single Role)**: Contains authorization objects for specific transactions
- **Composite Role**: Groups multiple single roles
- **Profile**: Generated from role (old mechanism, still used internally)
- Authorization managed in PFCG

### Authorization Check in ABAP
```abap
AUTHORITY-CHECK OBJECT 'M_BEST_BSA'
  ID 'BSART' FIELD ls_ekko-bsart
  ID 'ACTVT' FIELD '02'.  " 01=Create, 02=Change, 03=Display, 06=Delete

IF sy-subrc <> 0.
  MESSAGE e001(zz) "No authorization".
ENDIF.
```

### Key Interview Questions
> **Q: What is SU53 and when would you use it?**
> A: SU53 displays the last failed authorization check for the current user. When a user gets an "Authorization Failed" error, running SU53 immediately after shows which authorization object and field value was missing. This information is given to the Basis/Security team to add the authorization to the user's role.

> **Q: What is the difference between a Role and a Profile in SAP?**
> A: A Role (PFCG) is a container for authorization objects, organizational levels, and menu items — it represents a job function. The Profile is generated from the role and is what's actually assigned to the user. Profiles are the technical implementation of roles. The modern approach is to always work with roles, not manually created profiles.

---

## 7. SAP WORKFLOW (BASIC CONCEPTS)

### Workflow Components
| Component | Description |
|-----------|-------------|
| Task | Unit of work (can be a method call, dialog, or notification) |
| Standard Task | Reusable task based on object method |
| Agent | Who performs the task (user, role, org unit, expression) |
| Binding | Data mapping between workflow container and task container |
| Event | Trigger that starts a workflow (object event, timer, message) |
| Work Item | Instance of a task assigned to an agent |
| Workflow Template | Definition of the process flow (WS prefix, e.g., WS20000075) |

### Starting a Workflow
Workflows can be started by:
1. **Business Object Event**: e.g., PurchaseOrder.CREATED
2. **Direct call**: SWI5 (Workflow Outbox), SWI6 (Workflow display)
3. **Schedule**: Time-based event
4. **External system event**: RFC/BAPI trigger

### Workflow for PO Release (Example)
Standard workflow template WS20000075 handles PO release strategy notifications. When a PO requires approval:
1. Release strategy determines who must approve
2. Work item appears in approver's SAP Inbox (SBWP)
3. Approver releases via work item → ME29N automatically called
4. Next approver in chain is notified

### Key Interview Questions
> **Q: What is the difference between Release Strategy and Workflow in SAP?**
> A: Release Strategy uses the SAP classification system — it is deterministic, configuration-only (no ABAP), and controlled via SPRO. Workflow (SAP Business Workflow/BRF+) is flexible, supports dynamic routing, delegation, escalation, notifications via email, and integration with portals. Release Strategy is the standard approach for value-based PO approval; Workflow handles complex, multi-step, dynamic approvals.

> **Q: How do you find which workflow a user's work item belongs to?**
> A: Use SWI5 (Workflow Outbox) or SWIA (Workflow Item Administration). From a work item, you can navigate to the workflow definition, task, and object instance. SWDD (Workflow Builder) lets you view the definition, and SWEL/SWELS allows monitoring of active workflows.

---

## 8. OUTPUT AND FORMS

### SAP Script (Classic)
- Older print form technology
- Form definition in SE71
- Print program (driver program) calls the form
- Not recommended for new development

### Smart Forms
- Improved over SAP Script
- Function module-based
- Transaction: SMARTFORMS
- Better graphics support, multiple pages
- Driver program calls generated function module

### Adobe Forms (Interactive Forms)
- Based on Adobe LiveCycle Designer
- Transaction: SFP (Form Builder), SFPDF (Design Form in Adobe)
- Supports interactive (fillable) PDF forms
- Requires Adobe Document Services (ADS) installation

### BRF+ / Adobe Correspondence
- Business Rules Framework for form logic (S/4HANA direction)

### Key Interview Questions
> **Q: How is a Smart Form called from ABAP?**
> A: First determine the function module name using FM SSF_FUNCTION_MODULE_NAME (pass form name). Then call the returned FM with required parameters (control data, output options, and form-specific data in interface). The FM renders the form and sends to spool or printer based on output parameters.

---

## 9. BATCH JOBS AND BACKGROUND PROCESSING

### Creating a Background Job (SM36)
1. Define job (job name, class: A/B/C where A=highest priority)
2. Add steps (ABAP program or external program)
3. Set start condition (immediately, specific time, after job event)
4. Save and schedule

### Job Classes
| Class | Description | Processing |
|-------|-------------|------------|
| A | Highest priority | Gets dedicated WP |
| B | Normal | Queued normally |
| C | Lowest | Runs when resources available |

### Monitoring Background Jobs (SM37)
- Filter by job name, user, status, date/time
- Status: Scheduled, Released, Active, Finished, Cancelled
- View spool output (SP01)
- View job log for errors

### Periodic Jobs vs One-Time Jobs
- Periodic: Runs at fixed intervals (daily, weekly, hourly)
- One-time: Runs once at a specified time
- MRP runs (MDBT) typically scheduled as daily background jobs

### Key Interview Questions
> **Q: How do you schedule MRP to run automatically every night?**
> A: In SM36, create a job with step = ABAP program RPLANEW (or the variant-based MDBT transaction). Configure program variant with required plant/MRP controller settings. Set periodic scheduling (every 24 hours) with start time at off-peak hours. The job class should be A to ensure priority processing. Monitor results in SM37 and MD05/MD06.

---

## 10. DATA ARCHIVING

### Purpose
Move historical data from the active database to archive files to:
- Improve system performance
- Reduce database size
- Meet legal retention requirements

### Archiving Objects in MM
| Object | Description |
|--------|-------------|
| MM_MATBEL | Material Documents |
| MM_EKKO | Purchase Orders |
| MM_SPSTOCK | Special Stocks |
| MM_ACCTIT | Accounting Items |
| LO_STOCKS | Stock Data |
| FI_DOCUMNT | FI Documents |

### Transaction: SARA (Archive Management)

### Key Interview Questions
> **Q: When can a Purchase Order be archived?**
> A: A PO can be archived when: it has a deletion flag, all items are fully invoiced and goods received, all accounting documents are cleared, the retention period (configured in customizing) has elapsed, and no open commitments or follow-on documents exist. The archiving program checks these prerequisites.

---

## 11. PERFORMANCE AND TROUBLESHOOTING

### SQL Trace (ST05)
- Captures database queries
- Identifies missing indexes, full table scans
- Shows SQL statements and execution time

### ABAP Runtime Analysis (SE30/SAT)
- Profiles ABAP program execution
- Shows which code lines take most time
- Identifies N+1 query problems

### System Monitoring
| TCode | Description |
|-------|-------------|
| SM50 | Work Process Overview (current) |
| SM66 | Global Work Process Monitor (all instances) |
| SM04 | User Overview |
| AL08 | Users Logged On |
| SM21 | System Log |
| SM13 | Update Records Monitor |
| SM12 | Lock Entry List (Enqueue Table) |

### Lock Management (SM12)
- Locks prevent concurrent modification
- SAP uses Application-level locks (not DB locks)
- Lock entry stored in Enqueue server (not database)
- SM12 shows active locks — if user session dies, locks may need manual deletion

### Key Interview Questions
> **Q: A user reports that they cannot save a PO — it says "object locked by another user." How do you resolve?**
> A: Go to SM12, search for the PO number or the user's lock entries. If the user who holds the lock is no longer active (check SM04), the lock can be safely deleted in SM12. If the lock holder is active, coordinate with them. Investigate if a background job has the document locked (common cause: update task stuck in SM13).

> **Q: How do you find why a background job fails?**
> A: In SM37, select the failed job, click Job Log to see the error message. If the error is in an ABAP dump, check ST22 (ABAP Runtime Error) for the dump details. For database errors, check SM21 (System Log). For update errors, check SM13. The job spool (SP01) may also contain printed output before failure.

---

## 12. KEY ECC CONCEPTS FOR INTERVIEWS

### Enhancement Packages (EhPs)
- EhP1 through EhP8 added new features to ECC 6.0 without upgrading
- Features activated via Switch Framework (SFW5)
- EhP8 is the latest for ECC — no further functional releases planned

### Business Functions (SFW)
- Switchable enhancement packages features
- Activate in SFW5 (Switch Framework)
- Once activated in production, cannot be deactivated

### SAP Solution Manager
- Central platform for SAP landscape management
- Tools: Change Management, Technical Monitoring, Test Management, Service Desk
- Transport requests tracked via ChaRM (Change Request Management)

### Unicode Compliance
- SAP ECC is Unicode-compliant since 4.7
- Affects string handling in ABAP (CHAR vs STRING, type lengths)

### Key Interview Questions
> **Q: What is the difference between ECC and S/4HANA from an architecture perspective?**
> A: ECC runs on any supported database (Oracle, DB2, HANA, etc.) and uses a three-tier ABAP stack. S/4HANA runs exclusively on SAP HANA database, uses a simplified data model (fewer tables, aggregates eliminated), and includes Fiori as the primary UI. S/4HANA reduces data footprint significantly (e.g., aggregate tables FI replaced by ACDOCA universal journal). The ABAP application server still exists in S/4HANA but is enhanced.

> **Q: What are Enhancement Packages and why are they significant?**
> A: Enhancement Packages (EhPs) allow customers to adopt new SAP functionality without a full system upgrade. Features are delivered as switch-based add-ons — customers can selectively activate only what they need. This reduced the need for major upgrades and allowed incremental feature adoption. EhP8 for ECC 6.0 is the final major enhancement package.

---

## 13. ABAP DEBUGGING FOR FUNCTIONAL CONSULTANTS

### Starting Debug Mode
- Add `/h` to command field and press Enter (activates debugger mode for next transaction)
- Or set breakpoint in SE38 on a specific program/line
- External breakpoints: Set in ABAPDEBUGGER and debug RFC calls

### Debugger Tools
| Tool | Description |
|------|-------------|
| Classic Debugger | Transaction /H, shows field values |
| New Debugger (ABAP Debugger) | Available since 7.0, with watchpoints, watchpoints, breakpoints |
| Watchpoints | Stop execution when variable changes value |
| Breakpoints | Stop at specific line |
| Display variables | Check table/structure contents |

### Useful Debug Scenarios in MM
- Debug output determination to see condition evaluation
- Debug goods movement to see account determination logic
- Debug MRP planning to understand why specific orders are created
- Debug PO save to see BADI/exit execution sequence

### Key Interview Questions
> **Q: A goods movement is posting to the wrong G/L account. How would you debug?**
> A: Set breakpoint in function module OBYC_GET_ACCOUNT or in the MB_POST_DOCUMENT program. Check the movement type, valuation class, and transaction/event key being used. Compare against OBYC configuration. Alternatively, use FS10N to check the G/L account and trace back via MB51 (material docs) and FBL3N (G/L line items) to find the source of incorrect postings.

---

## 14. SAP NOTES AND SUPPORT

### OSS (Online Support System) / SAP Launchpad
- SAP Notes contain bug fixes, corrections, enhancements
- Types: Correction notes (code corrections), Note for information, SAP HOW-TO
- Applied via SNOTE transaction (Note Assistant)

### Applying SAP Notes (SNOTE)
1. Download note from SAP Launchpad (formerly SCN/Service Marketplace)
2. Import via SNOTE
3. System checks if note is already applied
4. Apply correction instructions
5. Create transport request for the changes

### Support Packages
- Larger collection of notes bundled together
- Applied via SPAM (Support Package Manager)
- Applied in sequence — cannot skip support packages

### Key Interview Questions
> **Q: How do you apply an OSS note and what precautions do you take?**
> A: Download the note XML file from SAP Launchpad and import via SNOTE. First apply to Development system, test thoroughly, then transport via standard TMS to QAS and PRD. For manual corrections (notes with "Instruction" type), carefully follow the modification steps and document changes in the transport request. Always take a backup of modified objects before applying.

---

## 15. COMMON ECC SCENARIO QUESTIONS

### Scenario 1: System is very slow during month-end
**Answer**: Check SM50/SM66 for work process utilization. Look for long-running background jobs (SM37) competing with dialog users. Check database locks (SM12). Review SM21 for database errors. Common causes: MRP run running during business hours, large batch jobs without off-peak scheduling, missing database indexes. Consider scheduling large batch jobs in low-usage windows.

### Scenario 2: Transport import fails in Quality system
**Answer**: Check STMS import log for error details. Common issues: missing basis-level objects (check with Basis team), syntax errors in transported code (check SE38 SLIN), table structure mismatch (check SE11), or missing customizing entries that the program depends on. For object conflicts, use STMS overwrite protection analysis. Fix the root cause in DEV, re-transport.

### Scenario 3: User cannot post a goods movement — authorization error
**Answer**: Ask user to run SU53 immediately after the error. SU53 shows the failed authorization check with the object name and field. Take screenshot and provide to Basis/Security team to add the required authorization to the user's role via PFCG. Ensure role changes are transported to production before assigning.

### Scenario 4: MRP run creates incorrect planned orders
**Answer**: Check MD04 (Stock/Requirements List) to see the complete demand/supply picture. Verify the material master MRP settings (MRP type, lot size, safety stock, planned delivery time). Check if the planning calendar or scheduling margin key settings are causing date issues. Check if there are any firm planned orders or open POs interfering. Use MD05 (MRP List) to see planning results and exception messages.

---

*End of SAP ECC Study Guide — Version 2025 | SAP ECC 6.0 EhP8*
