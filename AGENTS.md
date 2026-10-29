# PFPJ ry Repository Guardrails (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`)

Mandatory rules for all AI coding agents and contributors working in `bemehrbani/pfp` (People for Peace & Justice ry, Helsinki, Finland — Business ID: `3616815-5`).

## 1. Strict UTF-8 Without BOM (Zero Mojibake Policy)
- All `.md`, `.html`, `.py`, and `.ps1` files **must** be read and saved as **UTF-8 without BOM** (`\xef\xbb\xbf` is strictly forbidden).
- **Windows PowerShell 5.1 Warning:** Never use default `Get-Content` or `Set-Content` on `.md` or `.html` files without explicit UTF-8 no-BOM encoding, as Windows PowerShell defaults to Windows-1252 and corrupts legal symbols (`—` → `â€”`, `–` → `â€“`, `¶` → `Â¶`, `§` → `Â§`, `’` → `â€™`, `Chorzów` → `ChorzÃ³w`, `Koriša` → `KoriÅ¡a`, `↑` → `â†‘`).
- In PowerShell scripts, always use `.NET` UTF-8 without BOM:
  ```powershell
  $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
  $text = [System.IO.File]::ReadAllText($Path, $utf8NoBom)
  [System.IO.File]::WriteAllText($Path, $text, $utf8NoBom)
  ```
- In Python scripts, always specify `encoding="utf-8"` (never `utf-8-sig` when writing).
- Before staging any change to `.md` or `.html` files, verify zero UTF-8 BOM and zero mojibake sequences remain.

## 2. Pre-Edit Branch Synchronization
- Before editing `Campaigns/minab/justiceForMinab/docs/FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` or `MASTER_EXHIBIT_DOSSIER.md`, always synchronize with the latest canonical `main` branch:
  ```bash
  git checkout main && git pull origin main
  ```
- Never branch off stale local commits or overwrite upstream edits with one-off patch scripts.

## 3. Repository-Relative Paths Only
- Never hardcode machine-specific absolute paths (such as `E:\Papers\PFPJ` or `/Users/...`) inside any script or document.
- Always resolve paths relative to the repository root:
  - **Python:** `BASE_DIR = Path(__file__).resolve().parent.parent`
  - **PowerShell:** `$RepoRoot = Split-Path -Parent $PSScriptRoot`
- Never commit temporary one-off patch scripts (`apply_*.ps1`, `fix_*.ps1`, `verify_*.ps1`) to `scripts/`.

## 4. Source vs. Compiled Binary Separation
- Keep `Campaigns/minab/justiceForMinab/docs/` strictly for Markdown (`.md`) and source text files.
- **Never** commit compiled `.docx` or `.pdf` binaries inside `Campaigns/minab/justiceForMinab/docs/`.
- Compiled publication packages belong exclusively in:
  - `Draft_Versions/<YYYY-MM-DD>/` (date-stamped archive packages + `PACKAGE_MANIFEST.md`)
  - `PFP_Platform/web/public/docs/minab-report/` (canonical web download mirrors)

## 5. Strict Legal Citation & Evidentiary Verification
- Never fabricate, guess, or extrapolate legal citations, UN document numbers, tribunal case names, paragraph numbers (`¶` / `§`), or forensic identifiers (e.g., CAGE codes, munitions serials, coordinates).
- Every benchmark precedent cited in `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` must match the verified primary source dossiers in `Campaigns/minab/legal_benchmarks/` (`case_01` through `case_19`, `benchmarked_facts_cases_01_to_19.md`, and `COMPREHENSIVE_BENCHMARKING_REMAINING_15_CASES.md`).
