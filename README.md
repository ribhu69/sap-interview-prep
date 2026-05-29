# SAP Interview Prep Guide
### Comprehensive preparation material for SAP MM / ECC / S4HANA | 5+ Years Experience Track

---

## What's Inside

| Resource | Description |
|----------|-------------|
| `pdfs/SAP_MM_Study_Guide.pdf` | 19 chapters covering MM end-to-end (org structure, MRP, valuation, LIV, integration) |
| `pdfs/SAP_ECC_Study_Guide.pdf` | ECC architecture, ABAP, transport management, enhancements, authorizations |
| `pdfs/SAP_HANA_Study_Guide.pdf` | HANA concepts, S/4HANA migration, Business Partner, Fiori, EWM, Material Ledger |
| `interactive_tool/main.py` | Terminal-based study tool with Study Mode, Quiz Mode, Flashcards |

---

## Quick Start

### 1. Launch the Interactive Study Tool (macOS / Linux)

```bash
chmod +x launch.sh
./launch.sh
```

Or run directly:
```bash
python3 interactive_tool/main.py
```

**Requirements**: Python 3.8+ (no external libraries needed)

### 2. Regenerate PDFs

```bash
./launch.sh pdf
# Requires: pip3 install fpdf2
```

---

## Interactive Tool Features

```
┌─────────────────────────────────────────┐
│          SAP INTERVIEW PREP             │
├──────────────────────────────────────────┤
│  Topics:                                 │
│    [1] SAP MM  — Materials Management   │
│    [2] SAP ECC — Architecture & Config  │
│    [3] SAP HANA — S/4HANA & Migration  │
│                                          │
│    [p] Progress Dashboard               │
└──────────────────────────────────────────┘
```

Each topic has three modes:

| Mode | Description |
|------|-------------|
| **Study Guide** | Read through sections interactively with formatted display |
| **Quiz Mode** | 20 MCQ questions per topic — Full, Quick (10), or by Difficulty |
| **Flashcards** | Rapid-fire Q&A cards for key terms and concepts |

Progress (quiz scores, attempts) is saved locally in `.progress.json`.

---

## Study Guide Topics

### SAP MM (19 Sections)
1. Organizational Structure
2. Material Master
3. Vendor Master
4. Purchasing Info Records
5. Source Lists
6. Procurement Cycle (End-to-End)
7. Outline Agreements (Contracts & Scheduling Agreements)
8. Special Procurement (Consignment, Subcontracting, STO, Third-party)
9. Inventory Management & Movement Types
10. Valuation & Account Determination (OBYC)
11. MRP — Materials Requirements Planning
12. Release Strategy (Approval Workflow)
13. Output / Message Determination
14. Invoice Verification (LIV)
15. Integration (FI, SD, PP, QM, WM)
16. Key Configuration Activities (SPRO)
17. Transaction Code Reference
18. Advanced Topics (Batch Management, Vendor Evaluation, Quota Arrangement)
19. Common Interview Scenarios

### SAP ECC (15 Sections)
1. Architecture (3-tier, work processes, clients)
2. Customizing & Configuration (IMG/SPRO)
3. Transport Management System (TMS)
4. ABAP Fundamentals (tables, data dictionary, SQL)
5. User Exits, BADIs & Enhancement Framework
6. Authorization Concept (PFCG, SU53)
7. SAP Workflow basics
8. Output & Forms (Smart Forms, Adobe)
9. Background Jobs (SM36, SM37)
10. Data Archiving (SARA)
11. Performance & Troubleshooting (ST05, SM50, SM12)
12. Enhancement Packages (EhPs)
13. ABAP Debugging for Functional Consultants
14. SAP Notes & Support (SNOTE, SPAM)
15. Common ECC Scenarios

### SAP HANA & S/4HANA (16 Sections)
1. HANA Database Fundamentals (column store, in-memory, delta merge)
2. S/4HANA vs ECC Key Differences
3. Business Partner (BP)
4. Fiori Apps for MM
5. MRP Live
6. Material Ledger (mandatory in S/4HANA)
7. Central Purchasing
8. EWM — Extended Warehouse Management
9. Migration Approaches (Greenfield, Brownfield, Bluefield)
10. S/4HANA Embedded Analytics & CDS Views
11. Sourcing & Procurement in S/4HANA
12. S/4HANA Specific TCodes & Apps
13. HANA Studio & Administration basics
14. SAP BTP & Cloud Integration (Ariba, IBP)
15. Certification Guide
16. Key Interview Scenarios

---

## Interview Tips for 5+ Year Professionals

1. **Lead with architecture** — interviewers expect you to know the WHY, not just the HOW
2. **Quote transaction codes** — shows hands-on experience
3. **Mention table names** — demonstrates ABAP-awareness even as a functional consultant
4. **Cite configuration paths** (SPRO nodes) — shows you can implement, not just advise
5. **S/4HANA awareness** — even if your experience is ECC, show knowledge of the migration path
6. **Scenario-based answers** — always relate answers to real project experience

---

## Repository Structure

```
sap-interview-prep/
├── README.md
├── launch.sh                         ← Run this to start
├── generate_pdfs.py                  ← PDF generator script
├── study_guides/
│   ├── sap_mm_guide.md
│   ├── sap_ecc_guide.md
│   └── sap_hana_guide.md
├── pdfs/
│   ├── SAP_MM_Study_Guide.pdf
│   ├── SAP_ECC_Study_Guide.pdf
│   └── SAP_HANA_Study_Guide.pdf
└── interactive_tool/
    ├── main.py                       ← Interactive study tool
    ├── requirements.txt
    └── questions/
        ├── mm_questions.json         ← 20 MM MCQ questions
        ├── ecc_questions.json        ← 20 ECC MCQ questions
        └── hana_questions.json       ← 20 HANA MCQ questions
```

---

*Covers SAP ECC 6.0 EhP8 and S/4HANA 2023/2024 | Updated 2025*
