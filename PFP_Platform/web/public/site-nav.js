/**
 * PFPJ ry Unified Site Navigation Bar (Matches landing.html across all pages)
 * Renders the canonical .site-header + .mobile-drawer with dropdown menus,
 * active-page highlighting, and synchronized EN / FA / FI language switching.
 */
(function () {
  const NAV_TRANSLATIONS = {
    en: {
      logo_sub: "Legal Accountability",
      nav_home: "Home",
      nav_case_file: "Case File",
      nav_memorial: "Memorial",
      nav_multimedia: "Multimedia",
      nav_about: "About",
      nav_contact: "✉ Contact",
      dropdown_report_title: "Case Determination",
      dropdown_report_desc: "Full 10-chapter factual finding & IAC analysis",
      dropdown_recon_title: "3D Strike Reconstruction",
      dropdown_recon_desc: "Interactive school rooms, footage & impact physics",
      dropdown_evidence_title: "Forensic Evidence",
      dropdown_evidence_desc: "OSINT, satellite imagery & weapon shells",
      dropdown_annex_title: "Technical Annex",
      dropdown_annex_desc: "10 similarity factors & 18 legal precedents",
      dropdown_sources_title: "Primary Sources",
      dropdown_sources_desc: "Declassified records, UN docs & testimonies",
      dropdown_memorial_title: "Minab Victims Register",
      dropdown_memorial_desc: "Biographies and memorial wall for 156 victims",
      dropdown_mothers_title: "Mothers & Families",
      dropdown_mothers_desc: "Survivor accounts and family cluster testimonies",
      dropdown_about_title: "PFPJ ry Association",
      dropdown_about_desc: "Finnish registry, governance & legal mandate",
      dropdown_initiatives_title: "Global Initiatives",
      dropdown_initiatives_desc: "International coalitions & ICC communications",
      signVowBtn: "Sign Accountability Vow"
    },
    fa: {
      logo_sub: "دادخواهی حقوقی بین‌المللی",
      nav_home: "خانه",
      nav_case_file: "پرونده حقوقی",
      nav_memorial: "یادبود شهیدان",
      nav_multimedia: "چندرسانه‌ای",
      nav_about: "درباره انجمن",
      nav_contact: "✉ تماس با ما",
      dropdown_report_title: "گزارش نهایی سانحه",
      dropdown_report_desc: "بررسی حقوقی و شواهد در ۱۰ فصل",
      dropdown_recon_title: "بازسازی سه‌بعدی سانحه",
      dropdown_recon_desc: "بازدید تعاملی از کلاس‌های مدرسه و مستندات",
      dropdown_evidence_title: "مستندات فنی و شواهد",
      dropdown_evidence_desc: "داده‌های OSINT، تصاویر ماهواره‌ای و ترکش‌ها",
      dropdown_annex_title: "پیوست فنی و سوابق",
      dropdown_annex_desc: "۱۰ فاکتور شباهت و ۱۸ پرونده تطبیقی بین‌المللی",
      dropdown_sources_title: "منابع دست اول",
      dropdown_sources_desc: "اسناد از طبقه‌بندی خارج‌شده و اظهارات شاهدان",
      dropdown_memorial_title: "دفتر یادبود ۱۵۶ شهید",
      dropdown_memorial_desc: "زندگینامه و یادبود ۱۲۰ کودک و ۲۶ معلم",
      dropdown_mothers_title: "مادران و خانواده‌ها",
      dropdown_mothers_desc: "شهادت‌ها و روایت‌های دست اول خانواده‌های داغدار",
      dropdown_about_title: "انجمن حقوقی PFPJ ry",
      dropdown_about_desc: "ثبت رسمی در فنلاند و اهداف دادخواهی",
      dropdown_initiatives_title: "ابتکارات جهانی",
      dropdown_initiatives_desc: "ائتلاف‌های بین‌المللی و مکاتبات دیوان لاهه",
      signVowBtn: "امضای میثاق دادخواهی"
    },
    fi: {
      logo_sub: "Oikeudellinen vastuu",
      nav_home: "Koti",
      nav_case_file: "Oikeustapaus",
      nav_memorial: "Muistomerkki",
      nav_multimedia: "Multimedia",
      nav_about: "Tietoa",
      nav_contact: "✉ Ota yhteyttä",
      dropdown_report_title: "Tapausseloste",
      dropdown_report_desc: "10-osainen tosiseikkojen selvitys & IAC-analyysi",
      dropdown_recon_title: "3D-rekonstruktio",
      dropdown_recon_desc: "Vuorovaikutteinen koulun 3D-malli ja todisteet",
      dropdown_evidence_title: "Forensinen aineisto",
      dropdown_evidence_desc: "OSINT-tiedot, satelliittikuvat ja asetyyppien sirpaleet",
      dropdown_annex_title: "Tekninen liite",
      dropdown_annex_desc: "10 kohdistusvirhetekijää & 18 ennakkotapausta",
      dropdown_sources_title: "Alkuperäislähteet",
      dropdown_sources_desc: "Julkistetut asiakirjat, YK-raportit ja todistukset",
      dropdown_memorial_title: "Minabin uhrien rekisteri",
      dropdown_memorial_desc: "156 uhrin elämäkerrat ja digitaalinen muistoseinä",
      dropdown_mothers_title: "Äidit & perheet",
      dropdown_mothers_desc: "Eloonjääneiden perheiden ja äitien todistajanlausunnot",
      dropdown_about_title: "PFPJ ry -yhdistys",
      dropdown_about_desc: "Suomen yhdistysrekisteri, hallinto ja oikeudellinen mandaatti",
      dropdown_initiatives_title: "Globaalit aloitteet",
      dropdown_initiatives_desc: "Kansainväliset koalitiot ja ICC-viestintä",
      signVowBtn: "Allekirjoita vastuulupaus"
    }
  };

  const NAV_CSS = `
    :root {
      --pfp-nav-height: 72px;
      --pfp-bg-glass: rgba(13, 18, 29, 0.90);
      --pfp-bg-dropdown: rgba(15, 20, 32, 0.97);
      --pfp-text-primary: #f5f3ef;
      --pfp-text-secondary: #a3adc2;
      --pfp-text-muted: #626d84;
      --pfp-gold: #e5b95f;
      --pfp-gold-dim: rgba(229, 185, 95, 0.12);
      --pfp-gold-border: rgba(229, 185, 95, 0.3);
      --pfp-border-subtle: rgba(255, 255, 255, 0.08);
      --pfp-border-medium: rgba(255, 255, 255, 0.14);
      --pfp-font-display: 'Cinzel', 'Playfair Display', Georgia, serif;
      --pfp-font-body: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
      --pfp-font-rtl: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif;
      --pfp-transition: 0.25s cubic-bezier(0.2, 0, 0, 1);
    }

    .site-header {
      position: sticky;
      top: 0;
      left: 0;
      right: 0;
      height: var(--pfp-nav-height);
      z-index: 1000;
      background: var(--pfp-bg-glass);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--pfp-border-subtle);
      font-family: var(--pfp-font-body);
    }

    body[dir="rtl"] .site-header,
    body.rtl .site-header {
      font-family: var(--pfp-font-rtl);
      direction: rtl;
    }

    .site-header .nav-container {
      max-width: 1400px;
      margin: 0 auto;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      gap: 24px;
    }

    .site-header .brand-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      flex-shrink: 0;
      white-space: nowrap;
    }

    .site-header .brand-emblem {
      width: 38px;
      height: 38px;
      border-radius: 6px;
      background: linear-gradient(135deg, rgba(229, 185, 95, 0.2), rgba(229, 185, 95, 0.05));
      border: 1px solid var(--pfp-gold-border);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--pfp-gold);
      font-size: 1.25rem;
      transition: all var(--pfp-transition);
    }

    .site-header .brand-logo:hover .brand-emblem {
      transform: scale(1.04);
      border-color: var(--pfp-gold);
      box-shadow: 0 0 16px rgba(229, 185, 95, 0.25);
    }

    .site-header .brand-text {
      display: flex;
      flex-direction: column;
      line-height: 1.15;
    }

    .site-header .brand-title {
      font-family: var(--pfp-font-display);
      font-size: 1.08rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      color: var(--pfp-text-primary);
    }

    .site-header .brand-subtitle {
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--pfp-gold);
      font-weight: 600;
      margin-top: 2px;
    }

    body[dir="rtl"] .site-header .brand-subtitle,
    body.rtl .site-header .brand-subtitle {
      letter-spacing: 0;
    }

    .site-header .nav-menu {
      display: flex;
      align-items: center;
      gap: 6px;
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .site-header .nav-item {
      position: relative;
    }

    .site-header .nav-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      font-size: 0.92rem;
      font-weight: 500;
      color: var(--pfp-text-secondary);
      border-radius: 6px;
      transition: all var(--pfp-transition);
      white-space: nowrap;
      text-decoration: none;
    }

    .site-header .nav-link:hover,
    .site-header .nav-link.active,
    .site-header .nav-item:hover > .nav-link {
      color: var(--pfp-text-primary);
      background: rgba(255, 255, 255, 0.04);
    }

    .site-header .nav-link.active {
      color: var(--pfp-gold);
    }

    .site-header .nav-link .caret {
      font-size: 0.65rem;
      opacity: 0.6;
      transition: transform var(--pfp-transition);
    }

    .site-header .nav-item:hover .nav-link .caret,
    .site-header .nav-item.is-open .nav-link .caret {
      transform: rotate(180deg);
      opacity: 1;
    }

    .site-header .dropdown-menu {
      position: absolute;
      top: 100%;
      left: 0;
      margin-top: 8px;
      min-width: 280px;
      background: var(--pfp-bg-dropdown);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
      border: 1px solid var(--pfp-border-medium);
      border-radius: 12px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.55);
      padding: 8px;
      opacity: 0;
      visibility: hidden;
      transform: translateY(8px);
      transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                  visibility 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      transition-delay: 150ms;
      pointer-events: none;
      z-index: 1001;
    }

    .site-header .dropdown-menu::before {
      content: '';
      position: absolute;
      top: -16px;
      left: 0;
      right: 0;
      height: 16px;
      background: transparent;
    }

    body[dir="rtl"] .site-header .dropdown-menu,
    body.rtl .site-header .dropdown-menu {
      left: auto;
      right: 0;
    }

    .site-header .nav-item:hover .dropdown-menu,
    .site-header .nav-item.is-open .dropdown-menu,
    .site-header .nav-item:focus-within .dropdown-menu {
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
      pointer-events: auto;
      transition-delay: 0s;
    }

    .site-header .dropdown-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 6px;
      color: var(--pfp-text-secondary);
      text-decoration: none;
      transition: all var(--pfp-transition);
    }

    .site-header .dropdown-item:hover,
    .site-header .dropdown-item.active {
      background: rgba(229, 185, 95, 0.10);
      color: var(--pfp-text-primary);
    }

    .site-header .dropdown-icon {
      font-size: 1.1rem;
      color: var(--pfp-gold);
      margin-top: 2px;
      flex-shrink: 0;
    }

    .site-header .dropdown-text {
      display: flex;
      flex-direction: column;
    }

    .site-header .dropdown-title {
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--pfp-text-primary);
    }

    .site-header .dropdown-desc {
      font-size: 0.75rem;
      color: var(--pfp-text-muted);
      margin-top: 2px;
      line-height: 1.35;
    }

    .site-header .dropdown-item:hover .dropdown-title,
    .site-header .dropdown-item.active .dropdown-title {
      color: var(--pfp-gold);
    }

    .site-header .dropdown-badge {
      margin-left: auto;
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 7px;
      border-radius: 4px;
      background: var(--pfp-gold-dim);
      color: var(--pfp-gold);
      border: 1px solid var(--pfp-gold-border);
    }

    body[dir="rtl"] .site-header .dropdown-badge,
    body.rtl .site-header .dropdown-badge {
      margin-left: 0;
      margin-right: auto;
    }

    .site-header .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    .site-header .lang-switch {
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--pfp-border-subtle);
      border-radius: 9999px;
      padding: 3px;
    }

    .site-header .lang-btn {
      background: transparent;
      border: none;
      color: var(--pfp-text-muted);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all var(--pfp-transition);
    }

    .site-header .lang-btn:hover {
      color: var(--pfp-text-primary);
    }

    .site-header .lang-btn.active {
      background: var(--pfp-gold);
      color: #080b11;
      box-shadow: 0 2px 8px rgba(229, 185, 95, 0.35);
    }

    .site-header .btn-nav-cta {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--pfp-gold);
      background: var(--pfp-gold-dim);
      border: 1px solid var(--pfp-gold-border);
      padding: 7px 16px;
      border-radius: 9999px;
      transition: all var(--pfp-transition);
      text-decoration: none;
      white-space: nowrap;
    }

    .site-header .btn-nav-cta:hover {
      background: var(--pfp-gold);
      color: #080b11;
      box-shadow: 0 4px 14px rgba(229, 185, 95, 0.3);
    }

    .site-header .hamburger-btn {
      display: none;
      width: 40px;
      height: 40px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--pfp-border-subtle);
      border-radius: 6px;
      color: var(--pfp-text-primary);
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.25rem;
    }

    .mobile-drawer {
      position: fixed;
      top: var(--pfp-nav-height);
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(8, 11, 17, 0.98);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      z-index: 999;
      padding: 24px;
      overflow-y: auto;
      transform: translateX(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      gap: 20px;
      font-family: var(--pfp-font-body);
    }

    body[dir="rtl"] .mobile-drawer,
    body.rtl .mobile-drawer {
      transform: translateX(-100%);
      font-family: var(--pfp-font-rtl);
    }

    .mobile-drawer.open {
      transform: translateX(0);
    }

    .mobile-group {
      border-bottom: 1px solid var(--pfp-border-subtle);
      padding-bottom: 16px;
    }

    .mobile-group-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--pfp-gold);
      font-weight: 700;
      margin-bottom: 10px;
    }

    .mobile-links {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .mobile-link {
      padding: 8px 12px;
      border-radius: 6px;
      color: var(--pfp-text-secondary);
      font-size: 0.95rem;
      font-weight: 500;
      text-decoration: none;
    }

    .mobile-link:hover,
    .mobile-link.active {
      background: rgba(229, 185, 95, 0.1);
      color: var(--pfp-gold);
    }

    @media (max-width: 1080px) {
      .site-header .nav-menu {
        display: none;
      }
      .site-header .hamburger-btn {
        display: inline-flex;
      }
      .site-header .nav-container {
        padding: 0 18px;
      }
    }

    @media print {
      .site-header, .mobile-drawer {
        display: none !important;
      }
    }
  `;

  function getActivePageInfo() {
    const path = (window.location.pathname || '').split('/').pop() || 'landing.html';
    const casePages = ['draft.html', 'report.html', 'reconstruction.html', 'evidence.html', 'similarity_annex.html', 'similarity_factors.html', 'sources.html'];
    const memorialPages = ['memorial.html', 'child.html', 'mothers.html'];
    const aboutPages = ['about.html', 'initiatives.html', 'association_index.html'];
    const multiPages = ['multimedia.html', 'media-item.html'];

    return {
      page: path,
      isHome: path === 'landing.html' || path === 'index.html' || path === '',
      isCase: casePages.includes(path),
      isMemorial: memorialPages.includes(path),
      isMultimedia: multiPages.includes(path),
      isAbout: aboutPages.includes(path)
    };
  }

  function buildNavHTML(extraRightHTML) {
    const info = getActivePageInfo();
    const p = info.page;

    return `
      <div class="nav-container">
        <a href="landing.html" class="brand-logo">
          <div class="brand-emblem">☮</div>
          <div class="brand-text">
            <span class="brand-title">PFPJ ry</span>
            <span class="brand-subtitle" data-nav-i18n="logo_sub">Legal Accountability</span>
          </div>
        </a>

        <ul class="nav-menu">
          <li class="nav-item">
            <a href="landing.html" class="nav-link ${info.isHome ? 'active' : ''}" data-nav-i18n="nav_home">Home</a>
          </li>

          <li class="nav-item has-dropdown">
            <a href="draft.html" class="nav-link ${info.isCase ? 'active' : ''}">
              <span data-nav-i18n="nav_case_file">Case File</span>
              <span class="caret">▼</span>
            </a>
            <div class="dropdown-menu">
              <a href="draft.html" class="dropdown-item ${p === 'draft.html' || p === 'report.html' ? 'active' : ''}">
                <span class="dropdown-icon">⚖️</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_report_title">Case Determination</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_report_desc">Full 10-chapter factual finding &amp; IAC analysis</span>
                </div>
                <span class="dropdown-badge">ICC</span>
              </a>
              <a href="reconstruction.html" class="dropdown-item ${p === 'reconstruction.html' ? 'active' : ''}">
                <span class="dropdown-icon">✦</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_recon_title">3D Strike Reconstruction</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_recon_desc">Interactive school rooms, footage &amp; impact physics</span>
                </div>
              </a>
              <a href="evidence.html" class="dropdown-item ${p === 'evidence.html' ? 'active' : ''}">
                <span class="dropdown-icon">📁</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_evidence_title">Forensic Evidence</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_evidence_desc">OSINT, satellite imagery &amp; weapon shells</span>
                </div>
              </a>
              <a href="similarity_annex.html" class="dropdown-item ${p === 'similarity_annex.html' || p === 'similarity_factors.html' ? 'active' : ''}">
                <span class="dropdown-icon">📄</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_annex_title">Technical Annex</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_annex_desc">10 similarity factors &amp; 18 legal precedents</span>
                </div>
              </a>
              <a href="sources.html" class="dropdown-item ${p === 'sources.html' ? 'active' : ''}">
                <span class="dropdown-icon">📑</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_sources_title">Primary Sources</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_sources_desc">Declassified records, UN docs &amp; testimonies</span>
                </div>
              </a>
            </div>
          </li>

          <li class="nav-item has-dropdown">
            <a href="memorial.html" class="nav-link ${info.isMemorial ? 'active' : ''}">
              <span data-nav-i18n="nav_memorial">Memorial</span>
              <span class="caret">▼</span>
            </a>
            <div class="dropdown-menu">
              <a href="memorial.html" class="dropdown-item ${p === 'memorial.html' || p === 'child.html' ? 'active' : ''}">
                <span class="dropdown-icon">🕊️</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_memorial_title">Minab Victims Register</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_memorial_desc">Biographies and memorial wall for 156 victims</span>
                </div>
                <span class="dropdown-badge">156</span>
              </a>
              <a href="mothers.html" class="dropdown-item ${p === 'mothers.html' ? 'active' : ''}">
                <span class="dropdown-icon">🥀</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_mothers_title">Mothers &amp; Families</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_mothers_desc">Survivor accounts and family cluster testimonies</span>
                </div>
              </a>
            </div>
          </li>

          <li class="nav-item">
            <a href="multimedia.html" class="nav-link ${info.isMultimedia ? 'active' : ''}" data-nav-i18n="nav_multimedia">Multimedia</a>
          </li>

          <li class="nav-item has-dropdown">
            <a href="about.html" class="nav-link ${info.isAbout ? 'active' : ''}">
              <span data-nav-i18n="nav_about">About</span>
              <span class="caret">▼</span>
            </a>
            <div class="dropdown-menu">
              <a href="about.html" class="dropdown-item ${p === 'about.html' ? 'active' : ''}">
                <span class="dropdown-icon">🏛️</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_about_title">PFPJ ry Association</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_about_desc">Finnish registry, governance &amp; legal mandate</span>
                </div>
              </a>
              <a href="initiatives.html" class="dropdown-item ${p === 'initiatives.html' ? 'active' : ''}">
                <span class="dropdown-icon">🌐</span>
                <div class="dropdown-text">
                  <span class="dropdown-title" data-nav-i18n="dropdown_initiatives_title">Global Initiatives</span>
                  <span class="dropdown-desc" data-nav-i18n="dropdown_initiatives_desc">International coalitions &amp; ICC communications</span>
                </div>
              </a>
            </div>
          </li>
        </ul>

        <div class="nav-actions">
          ${extraRightHTML || ''}
          <div class="lang-switch">
            <button type="button" class="lang-btn active" data-pfp-lang="en" onclick="window.__pfpSwitchLang('en')">EN</button>
            <button type="button" class="lang-btn" data-pfp-lang="fa" onclick="window.__pfpSwitchLang('fa')">فارسی</button>
            <button type="button" class="lang-btn" data-pfp-lang="fi" onclick="window.__pfpSwitchLang('fi')">FI</button>
          </div>

          <a href="#contact" data-open-contact="true" onclick="if(window.openContactModal){event.preventDefault();window.openContactModal();}" class="btn-nav-cta" data-nav-i18n="nav_contact">✉ Contact</a>

          <button type="button" class="hamburger-btn" id="mobileToggle" aria-label="Toggle navigation" onclick="window.toggleMobileNav()">☰</button>
        </div>
      </div>
    `;
  }

  function buildMobileDrawerHTML() {
    const info = getActivePageInfo();
    const p = info.page;
    return `
      <div class="mobile-group">
        <div class="mobile-group-title">Navigation</div>
        <div class="mobile-links">
          <a href="landing.html" class="mobile-link ${info.isHome ? 'active' : ''}" data-nav-i18n="nav_home">Home</a>
          <a href="multimedia.html" class="mobile-link ${info.isMultimedia ? 'active' : ''}" data-nav-i18n="nav_multimedia">Multimedia</a>
        </div>
      </div>

      <div class="mobile-group">
        <div class="mobile-group-title" data-nav-i18n="nav_case_file">Case File</div>
        <div class="mobile-links">
          <a href="draft.html" class="mobile-link ${p === 'draft.html' || p === 'report.html' ? 'active' : ''}" data-nav-i18n="dropdown_report_title">Case Determination (Report)</a>
          <a href="reconstruction.html" class="mobile-link ${p === 'reconstruction.html' ? 'active' : ''}" data-nav-i18n="dropdown_recon_title">3D Strike Reconstruction</a>
          <a href="evidence.html" class="mobile-link ${p === 'evidence.html' ? 'active' : ''}" data-nav-i18n="dropdown_evidence_title">Forensic Evidence</a>
          <a href="similarity_annex.html" class="mobile-link ${p === 'similarity_annex.html' || p === 'similarity_factors.html' ? 'active' : ''}" data-nav-i18n="dropdown_annex_title">Technical Annex &amp; Precedents</a>
          <a href="sources.html" class="mobile-link ${p === 'sources.html' ? 'active' : ''}" data-nav-i18n="dropdown_sources_title">Primary Sources</a>
        </div>
      </div>

      <div class="mobile-group">
        <div class="mobile-group-title" data-nav-i18n="nav_memorial">Memorial</div>
        <div class="mobile-links">
          <a href="memorial.html" class="mobile-link ${p === 'memorial.html' || p === 'child.html' ? 'active' : ''}" data-nav-i18n="dropdown_memorial_title">Minab Victims Register</a>
          <a href="mothers.html" class="mobile-link ${p === 'mothers.html' ? 'active' : ''}" data-nav-i18n="dropdown_mothers_title">Mothers &amp; Families</a>
        </div>
      </div>

      <div class="mobile-group">
        <div class="mobile-group-title" data-nav-i18n="nav_about">About</div>
        <div class="mobile-links">
          <a href="about.html" class="mobile-link ${p === 'about.html' ? 'active' : ''}" data-nav-i18n="dropdown_about_title">PFPJ ry Association</a>
          <a href="initiatives.html" class="mobile-link ${p === 'initiatives.html' ? 'active' : ''}" data-nav-i18n="dropdown_initiatives_title">Global Initiatives</a>
        </div>
      </div>

      <div>
        <a href="#contact" data-open-contact="true" onclick="if(window.openContactModal){event.preventDefault();if(window.closeMobileNav)window.closeMobileNav();window.openContactModal();}" class="btn-nav-cta" data-nav-i18n="nav_contact" style="width: 100%; justify-content: center;">✉ Contact Association</a>
      </div>
    `;
  }

  function applyNavTranslations(lang) {
    const dict = NAV_TRANSLATIONS[lang] || NAV_TRANSLATIONS.en;
    document.querySelectorAll('[data-nav-i18n]').forEach((el) => {
      const key = el.getAttribute('data-nav-i18n');
      if (dict[key]) el.textContent = dict[key];
    });
    document.querySelectorAll('.site-header .lang-btn').forEach((btn) => {
      const btnLang = btn.getAttribute('data-pfp-lang');
      btn.classList.toggle('active', btnLang === lang);
    });
  }

  window.__pfpSwitchLang = function (lang) {
    try {
      localStorage.setItem('pfp-lang', lang);
      localStorage.setItem('pfp_lang', lang);
    } catch (_) {}

    applyNavTranslations(lang);

    if (typeof window.setLang === 'function') {
      window.setLang(lang);
    } else if (typeof window.setLanguage === 'function') {
      window.setLanguage(lang);
    } else if (typeof window.toggleLang === 'function') {
      window.toggleLang(lang === 'fa' ? 'fa' : 'en');
    } else if (typeof window.setMode === 'function') {
      window.setMode(lang === 'fa' ? 'fa' : 'en');
    } else {
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'fa' ? 'rtl' : 'ltr';
      document.body.dir = lang === 'fa' ? 'rtl' : 'ltr';
    }
    document.querySelectorAll('.site-header .lang-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-pfp-lang') === lang);
    });
  };

  window.toggleMobileNav = function () {
    const drawer = document.getElementById('mobileDrawer');
    const btn = document.getElementById('mobileToggle');
    if (!drawer) return;
    const isOpen = drawer.classList.toggle('open');
    if (btn) btn.textContent = isOpen ? '✕' : '☰';
  };

  function bindDropdownInteractions(headerEl) {
    const dropdownItems = headerEl.querySelectorAll('.nav-item.has-dropdown');
    dropdownItems.forEach((item) => {
      const link = item.querySelector(':scope > .nav-link');
      const menu = item.querySelector('.dropdown-menu');
      if (!link || !menu) return;

      link.setAttribute('aria-haspopup', 'true');
      link.setAttribute('aria-expanded', 'false');

      link.addEventListener('click', (e) => {
        e.preventDefault();
        const wasOpen = item.classList.contains('is-open');
        dropdownItems.forEach((other) => {
          other.classList.remove('is-open');
          const otherLink = other.querySelector(':scope > .nav-link');
          if (otherLink) otherLink.setAttribute('aria-expanded', 'false');
        });
        if (!wasOpen) {
          item.classList.add('is-open');
          link.setAttribute('aria-expanded', 'true');
        }
      });
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-item.has-dropdown')) {
        dropdownItems.forEach((item) => {
          item.classList.remove('is-open');
          const link = item.querySelector(':scope > .nav-link');
          if (link) link.setAttribute('aria-expanded', 'false');
        });
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        dropdownItems.forEach((item) => {
          item.classList.remove('is-open');
          const link = item.querySelector(':scope > .nav-link');
          if (link) link.setAttribute('aria-expanded', 'false');
        });
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 1080) {
        const drawer = document.getElementById('mobileDrawer');
        const btn = document.getElementById('mobileToggle');
        if (drawer && drawer.classList.contains('open')) {
          drawer.classList.remove('open');
          if (btn) btn.textContent = '☰';
        }
      }
    });
  }

  function mountUnifiedNavbar() {
    if (!document.getElementById('pfp-unified-nav-styles')) {
      const styleEl = document.createElement('style');
      styleEl.id = 'pfp-unified-nav-styles';
      styleEl.textContent = NAV_CSS;
      document.head.appendChild(styleEl);
    }

    const existingSiteHeader = document.querySelector('header.site-header');
    if (existingSiteHeader && existingSiteHeader.querySelector('.nav-menu')) {
      return;
    }

    let extraRightHTML = '';
    const info = getActivePageInfo();

    // Preserve Sign Accountability Vow button on reconstruction.html
    if (info.page === 'reconstruction.html') {
      const countText = document.getElementById('vowCountBadge')?.textContent || '1,428';
      extraRightHTML = `
        <button class="vow-cta-btn" id="openVowBtn" type="button">
          <span>✍️</span>
          <span data-nav-i18n="signVowBtn">Sign Accountability Vow</span>
          <span class="vow-counter-pill" id="vowCountBadge">${countText}</span>
        </button>
      `;
    } else if (info.page === 'draft.html') {
      extraRightHTML = `
        <div class="view-mode-selector" title="Switch Reading Mode" style="display:inline-flex; gap:4px;">
          <button type="button" class="mode-btn active" id="btnModeBoth" onclick="setMode('both')" style="font-size:0.75rem; padding:4px 8px;">⚖️ Side-by-Side</button>
          <button type="button" class="btn-nav-action" onclick="window.print()" style="font-size:0.75rem; padding:4px 8px;">🖨️ PDF</button>
        </div>
      `;
    }

    const headerEl = existingSiteHeader || document.createElement('header');
    headerEl.className = 'site-header';
    headerEl.id = 'pfpSiteHeader';
    headerEl.innerHTML = buildNavHTML(extraRightHTML);

    const legacyNavs = document.querySelectorAll('nav.nav, nav.lang-bar, div.lang-bar, header.hud-header');
    if (!existingSiteHeader) {
      if (legacyNavs.length > 0 && info.page !== 'reconstruction.html') {
        legacyNavs[0].replaceWith(headerEl);
        for (let i = 1; i < legacyNavs.length; i++) {
          legacyNavs[i].remove();
        }
      } else {
        document.body.insertBefore(headerEl, document.body.firstChild);
        legacyNavs.forEach((n) => n.remove());
      }
    } else {
      legacyNavs.forEach((n) => n.remove());
    }

    // Remove duplicate inline language selectors on similarity_annex / similarity_factors
    document.querySelectorAll('.control-container .lang-selector, .container header .lang-toggle').forEach((el) => el.remove());

    if (!document.getElementById('mobileDrawer')) {
      const drawerEl = document.createElement('div');
      drawerEl.className = 'mobile-drawer';
      drawerEl.id = 'mobileDrawer';
      drawerEl.innerHTML = buildMobileDrawerHTML();
      headerEl.insertAdjacentElement('afterend', drawerEl);
    }

    bindDropdownInteractions(headerEl);

    const savedLang = localStorage.getItem('pfp-lang') || localStorage.getItem('pfp_lang') || 'en';
    applyNavTranslations(['en', 'fa', 'fi'].includes(savedLang) ? savedLang : 'en');
  }

  if (document.body) {
    mountUnifiedNavbar();
  }
  document.addEventListener('DOMContentLoaded', mountUnifiedNavbar);
})();
