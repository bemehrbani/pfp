# Draft Versions Directory & Production Archive
> **Managed by:** People for Peace & Justice ry (PFPJ ry)  
> **Repository Location:** `Draft_Versions/`

This directory houses official, date-stamped working draft packages of the Minab Airstrike Factual Determination and Legal Dossier.

---

## Directory Structure Protocol

Each version is preserved in an immutable subfolder named strictly according to its **Date of Production** (`YYYY-MM-DD`):

```
Draft_Versions/
├── README.md                                  # This protocol guide
└── <YYYY-MM-DD>/                              # Production Date folder (e.g. 2026-09-13/)
    ├── PACKAGE_MANIFEST.md                    # File inventory, sizes, and SHA-256 hashes
    ├── PFPJ_Minab_Factual_Determination_Main_Report_<DATE>_Draft.docx
    ├── PFPJ_Minab_Factual_Determination_Main_Report_<DATE>_Draft.pdf
    ├── PFPJ_Minab_Master_Exhibit_Dossier_Annex_<DATE>_Draft.docx
    └── PFPJ_Minab_Master_Exhibit_Dossier_Annex_<DATE>_Draft.pdf
```

---

## Standard Package Contents

Each draft version package comprises **four companion files**:
1. **Main Report Word Document (`.docx`):** The 10-chapter judicial determination and legal assessment dossier.
2. **Main Report PDF Document (`.pdf`):** High-resolution, print-formatted PDF with embedded draft watermarks, running headers, and footers.
3. **Annex Document Word Document (`.docx`):** The Master Exhibit Dossier, including SAT, MUN, LAUNCH, CENTCOM, and VIC exhibit series.
4. **Annex Document PDF Document (`.pdf`):** Formal evidentiary compendium with embedded draft watermarks and exhibit inventories.

---

## How to Build or Update Draft Packages

To generate a new draft package based on the current state of canonical source dossiers:

```bash
# Generate package for today's production date
python3 scripts/build_draft_package.py

# Or specify an explicit production date
python3 scripts/build_draft_package.py --date 2026-09-13
```

The build engine automatically:
* Ingests `Campaigns/minab/justiceForMinab/docs/FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` and `MASTER_EXHIBIT_DOSSIER.md`.
* Injects prominent `WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK` banners, running headers, and watermarks.
* Compiles both Word and PDF formats.
* Generates SHA-256 checksums in `PACKAGE_MANIFEST.md`.
