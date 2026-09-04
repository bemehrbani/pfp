# People for Peace & Justice ry (PFPJ ry) — Local RAG & Project Knowledge Base

> **Entity:** People for Peace & Justice ry (Registered Association / Rekisteröity Yhdistys)  
> **Domicile:** Helsinki, Finland 🇫🇮  
> **Business ID (Y-tunnus):** 3616815-5  
> **Live Domain:** [https://peopleforpeace.live](https://peopleforpeace.live)  
> **Primary Campaign:** Justice for Minab Children & Mothers (*Shajareh Tayyebeh Elementary Airstrike*)  
> **Last Synchronized:** September 2026

---

## 1. Executive Summary & Governance Structure

**People for Peace & Justice ry (PFPJ ry)** is an independent international human rights, legal advocacy, and forensic documentation association registered under the Finnish Associations Act (Yhdistyslaki 503/1989) with the Finnish Patent and Registration Office (PRH).

### Board of Directors & Founding Team
| Name | Role | Location | Focus Area |
| :--- | :--- | :--- | :--- |
| **Mahdi Farimani** | Chairperson / Campaign Lead | Helsinki, Finland | Association management, PRH compliance, full-stack tech, campaign strategy |
| **Zahra Azhar** | Legal Lead / Board Member | The Hague, Netherlands | International criminal law (ICC/universal jurisdiction), European liaison |
| **Ali Akbar SiahPoush** | Founding Member / Board Member | The Hague / Europe | Governance, legal filings, international stakeholder engagement |

### Legal Advisory Council
- **Dr. Seyyed Mohammad Garih Seyed-Fatemi:** Professor of International Law & Human Rights (Shahid Beheshti University).
- **Dr. Mohammad Jalali:** Associate Professor of Public Law (Shahid Beheshti University) — State vetting & command negligence.
- **Dr. Tahmoures Bashirieh:** Assistant Professor of Criminal Law & Criminology (Allameh Tabataba'i University) — International Criminal Law.

---

## 2. Technical Stack & System Architecture

```
+----------------------------------------------------------------------------------------------------+
|                                    PFP PRODUCTION ARCHITECTURE                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   [ Public Visitors / Victims' Families / Legal Researchers ]                                       |
|                               │                                                                    |
|                               ▼                                                                    |
|                 [ Cloudflare DNS / Let's Encrypt SSL ]                                             |
|                               │                                                                    |
|                               ▼                                                                    |
|          [ Nginx Web Server (Alpine) on Hetzner Host (65.109.198.200) ]                            |
|                 ├── /               --> Static Web & React Portal (web/public)                     |
|                 ├── /api/           --> Django REST Framework API (:8000)                          |
|                 └── /media/, /static/                                                              |
|                               │                                                                    |
|                               ▼                                                                    |
|          [ Django REST API (Python 3.11 / Gunicorn) ]                                              |
|                 ├── PostgreSQL 15    --> Primary relational database                               |
|                 ├── Redis 7          --> Message broker & caching                                  |
|                 ├── Celery Workers   --> Asynchronous task processing                              |
|                 └── Telegram Bot     --> python-telegram-bot v20+ (async_to_sync)                  |
|                               │                                                                    |
|                               ▼                                                                    |
|          [ PFPJ Ry Board Telegram Group (Chat ID: -5259699687) ]                                   |
|                 └── Instant real-time contact modal alerts & form submissions                      |
+----------------------------------------------------------------------------------------------------+
```

- **Backend:** Django 4.2+ / Django REST Framework (DRF), Celery 5.3+, PostgreSQL 15, Redis 7.
- **Frontend:** Vanilla HTML5/CSS3/ES6 + React components, Tailwind CSS, Vite.
- **Infrastructure:** Docker Compose (production, staging, stealth), Systemd, Nginx reverse proxy.
- **Telegram Bot:** Real-time volunteer management, campaign broadcasts, and contact form webhook delivery.

---

## 3. Project Directory Map & Core Inventories

### Root Directory
- [ASSOCIATION_INDEX.md](file:///Users/mahdifarimani/Documents/PFP/ASSOCIATION_INDEX.md): Master file index with web URLs and document explanations.
- [association_index.html](file:///Users/mahdifarimani/Documents/PFP/association_index.html): Password-protected board registry portal (`pfpj2026`).
- [LOCAL_RAG.md](file:///Users/mahdifarimani/Documents/PFP/LOCAL_RAG.md): Authoritative local RAG knowledge base.
- [docker-compose.production.yml](file:///Users/mahdifarimani/Documents/PFP/docker-compose.production.yml): Production container configuration.
- [deploy.sh](file:///Users/mahdifarimani/Documents/PFP/deploy.sh): Automated production deployment script.

### A. Campaigns & Forensic Investigation (`Campaigns/minab/`)
- **Unified Data Pipeline (`Campaigns/minab/data/`):**
  - [`minab_incident_dataset.json`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/minab_incident_dataset.json): Canonical JSON dataset of all casualties, mothers, family clusters, and evidentiary sources.
  - [`minab_data_model.json`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/minab_data_model.json): Formal JSON Schema (Draft-07) defining incident data models.
  - [`minab_types.ts`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/minab_types.ts): TypeScript interface mirror for frontend integration.
  - [`validate_minab_data.py`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/validate_minab_data.py): Integrity validator verifying foreign keys, bidirectional relations, and casualty counts.
  - [`IRANIAN_SOURCES_RELIABILITY_REPORT.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/IRANIAN_SOURCES_RELIABILITY_REPORT.md): 4-tier OSINT & primary source evaluation (156 confirmed martyrs, 120 children, 26 female educators).
  - [`MINAB_CASUALTIES_MASTER_REGISTRY.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/MINAB_CASUALTIES_MASTER_REGISTRY.md): Comprehensive victim directory and casualty reconciliation.
  - [`MINAB_MOTHERS_AND_FAMILIES_DIRECTORY.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/MINAB_MOTHERS_AND_FAMILIES_DIRECTORY.md): Documentation of bereaved mothers and affected family clusters.
  - [`exports/`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/data/exports): Flatted CSV exports (`minab_victims.csv`, `minab_mothers.csv`, `minab_family_clusters.csv`, `minab_sources.csv`).
- **Legal Campaign & Evidence (`Campaigns/minab/justiceForMinab/`):**
  - [`docs/fact_retrieval_handover_fa.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/docs/fact_retrieval_handover_fa.md): Official handover document outlining verified facts, pending investigations, and evidentiary requirements for international court filings.
  - [`evidence/satellite_evidence.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/evidence/satellite_evidence.md): Planet Labs/Google Earth temporal imagery proving physical separation of school since 2016.
  - [`evidence/munitions_evidence.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/evidence/munitions_evidence.md): Technical analysis of BGM-109 Tomahawk cruise missile wreckage.
  - [`evidence/launch_attribution.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/evidence/launch_attribution.md): USS Abraham Lincoln carrier strike group flight trajectories.
  - [`evidence/centcom_preliminary_report.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/evidence/centcom_preliminary_report.md): Analysis of US military 15-6 investigation admission regarding outdated pre-2016 DIA intelligence data.
  - [`evidence/victim_memorial_list.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/justiceForMinab/evidence/victim_memorial_list.md): Detailed profiles of the initial 100 verified victims.
- **Legal Precedents & Benchmarking Pipeline (`Campaigns/minab/legal_benchmarks/`):**
  - [`index.md`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/index.md): Master index of 18 international benchmarks and 10 similarity factors.
  - [`query_similar_cases.py`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/query_similar_cases.py): Live CLI query tool connecting to ECtHR HUDOC API and CourtListener US Case Law API.
  - [`fetch_all_full_reports.py`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/fetch_all_full_reports.py): Automated pipeline for downloading and assembling full-text reports, UN inquiry findings, and court decisions.
  - [`full_reports/`](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/full_reports/): Complete full-text case reports, official UN CoI/UNAMA/UN GEE reports, and unabridged ECtHR/ICTY judgments for all 18 benchmark cases.
  - Individual case studies: [Belgrade Embassy](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_01_belgrade_embassy.md), [Kunduz Tankers (Hanan v. Germany)](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_02_kunduz_tankers.md), [Katyr-Yurt (Isayeva v. Russia)](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_03_katyr_yurt.md), [Al-Jina Mosque](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_04_al_jina_mosque.md), [Kabul Drone](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_05_kabul_drone.md), [Dora Farms](file:///Users/mahdifarimani/Documents/PFP/Campaigns/minab/legal_benchmarks/case_06_dora_farms.md).

### B. Association Governance & Legal Filings (`PFPJ_Ry/` & `web/public/legal/jfmc-2026/`)
- [`saannot.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/saannot.html): Bilingual (Finnish/English) Association Rules (§1–9 Säännöt) registered with PRH.
- [`perustamiskirja.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/perustamiskirja.html): Bilingual Founding Charter signed by Mahdi Farimani, Zahra Azhar, and Ali Akbar SiahPoush.
- [`poytakirja.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/poytakirja.html): Founding Meeting Minutes (Perustavan kokouksen pöytäkirja).
- [`finland-process.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/finland-process.html): 7-phase registration roadmap, tax-exemption (Vero), and banking setup.
- [`tasks.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/tasks.html): OKR tracking board and NGO establishment Kanban.
- [`benchmarks.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/benchmarks.html): Benchmarking of 8 international human rights NGOs (TRIAL, CIJA, etc.).
- [`asp-guide.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/legal/jfmc-2026/asp-guide.html): Roadmap for ICC Assembly of States Parties (ASP) NGO observer status.

### C. Web Frontend (`PFP_Platform/web/public/`)
- [`landing.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/landing.html): Public homepage.
- [`about.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/about.html): Organization overview, Board, and Legal Advisory Council.
- [`memorial.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/memorial.html): Interactive digital memorial grid honoring victims.
- [`child.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/child.html): Individual victim profile & virtual memorial candle.
- [`mothers.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/mothers.html): Dedicated showcase for bereaved mothers & families.
- [`evidence.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/evidence.html): Forensic evidence, missile analysis, and timeline.
- [`sources.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/sources.html): Open-source reliability registry & media cross-verification.
- [`data.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/data.html): Open data download portal for researchers & journalists.
- [`similarity_factors.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/similarity_factors.html): Technical analysis of accident similarity factors.
- [`initiatives.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/initiatives.html): Global civil society & legal initiatives directory.
- [`report.html`](file:///Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/report.html): **Restricted Board Dossier** (Password: `pfpj2026`).

---

## 4. Security & Access Credentials

| Portal / Resource | URL Path | Password / Credential | Scope & Intended Audience |
| :--- | :--- | :--- | :--- |
| **Board Report Portal** | `/report.html` | `pfpj2026` | Board of Trustees & Legal Counsel |
| **Legal Index Portal** | `/legal/jfmc-2026/index.html` | `pfpj2026` | Board Members, Legal Team & Advisors |
| **Master Association Index**| `/association_index.html` | `pfpj2026` | Board Members (Confidential internal overview) |
| **Onboarding Guide** | `/onboarding.html` | `PFP2026!` | Core Team & Technical Volunteers |
| **Board Telegram Notifications**| Telegram API | Group ID: `-5259699687` | PFPJ Ry Board real-time contact alerts |

---

## 5. Deployment & CI/CD Pipelines

- **Production Host:** `65.109.198.200` (Hetzner, Finland)
- **Git Deployment Remote:** `deploy` (`65.109.198.200:/opt/pfp.git`)
- **SSH Key:** `/Users/mahdifarimani/Documents/PFP/PFP_Platform/infra/deploy_key`
- **Deploy Guardrail Bypass:** `BYPASS_DEPLOY_GUARDRAIL=1`
- **Standard Deployment Command:**
  ```bash
  BYPASS_DEPLOY_GUARDRAIL=1 git push origin main && \
  BYPASS_DEPLOY_GUARDRAIL=1 GIT_SSH_COMMAND="ssh -i /Users/mahdifarimani/Documents/PFP/PFP_Platform/infra/deploy_key -o StrictHostKeyChecking=no" git push deploy main
  ```
- **Post-Receive Hook Operations:**
  1. Creates compressed database backup (`/opt/backups/pfp_pre_deploy_*.sql.gz`).
  2. Pulls new code into `/opt/pfp`.
  3. Rebuilds Docker containers (`backend`, `celery`, `frontend`, `telegram-bot`, `postgres`, `redis`).
  4. Runs Django migrations.
  5. Executes health check endpoint validation.
