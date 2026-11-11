/**
 * PFPJ ry Contact & Volunteer Modal Helper
 * Dynamically injects modal CSS, HTML markup, and handles submissions to Telegram.
 */

(function() {
    // 1. Inject CSS Styles
    const css = `
        /* Modal Backdrop */
        .contact-modal {
            display: none;
            position: fixed;
            z-index: 100000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.85);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            align-items: center;
            justify-content: center;
        }
        .contact-modal.active {
            display: flex;
        }
        /* Modal Box */
        .contact-modal-content {
            background-color: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 32px;
            width: 90%;
            max-width: 500px;
            position: relative;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
            text-align: left;
            direction: ltr;
        }
        body[dir="rtl"] .contact-modal-content {
            text-align: right;
            direction: rtl;
        }
        .contact-modal-content h3 {
            font-family: var(--font-display), 'Inter', 'Vazirmatn', sans-serif;
        }
        @keyframes contact-modal-fade {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .contact-modal-content {
            animation: contact-modal-fade 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        /* Close Button */
        .contact-modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 1.5rem;
            font-weight: bold;
            color: #94a3b8;
            cursor: pointer;
            transition: color 0.2s;
            line-height: 1;
        }
        body[dir="rtl"] .contact-modal-close {
            right: auto;
            left: 20px;
        }
        .contact-modal-close:hover {
            color: #ffffff;
        }
        /* Form fields */
        .contact-form-group {
            margin-top: 14px;
        }
        .contact-form-group label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 6px;
            color: #e2e8f0;
            text-align: left;
        }
        body[dir="rtl"] .contact-form-group label {
            text-align: right;
        }
        .contact-form-group input,
        .contact-form-group select,
        .contact-form-group textarea {
            width: 100%;
            padding: 10px 12px;
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px;
            color: #ffffff;
            font-size: 0.9rem;
            font-family: inherit;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }
        .contact-form-group input:focus,
        .contact-form-group select:focus,
        .contact-form-group textarea:focus {
            border-color: #d4a853;
            outline: none;
        }
        /* Submit button */
        .contact-submit-btn {
            width: 100%;
            margin-top: 24px;
            padding: 12px;
            background: #d4a853;
            border: none;
            border-radius: 6px;
            color: #0f172a;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .contact-submit-btn:hover {
            background: #f1c463;
            transform: translateY(-1px);
        }
        /* Status Div */
        .contact-status {
            margin-top: 14px;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
            display: none;
            font-size: 0.88rem;
        }
    `;

    const styleEl = document.createElement('style');
    styleEl.innerHTML = css;
    document.head.appendChild(styleEl);

    // 2. Localization Map
    const modalI18n = {
        en: {
            title: "Contact & Support PFPJ ry",
            subtitle: "Reach out to support our legal advocacy, contribute evidence, or join our team. Submissions are saved directly and routed to our coordination team on Telegram.",
            label_name: "Name",
            label_email: "Email Address",
            label_handle: "Telegram @username or Signal / Phone (Optional)",
            placeholder_handle: "@username or +358...",
            label_role: "Area of Interest / Role",
            label_msg: "Message / Experience Summary",
            opt_volunteer: "Volunteer / OSINT Researcher",
            opt_scholar: "Legal Scholar / Advisor",
            opt_witness: "Witness / Evidence Contributor",
            opt_funder: "Litigation Fund Contributor",
            opt_general: "General Inquiry",
            submit_btn: "Submit Request",
            submitting: "Submitting...",
            success: "Thank you! Your message has been received by our team.",
            error: "Error sending request. Please try again.",
            tg_channel_note: "Official Telegram Channel:"
        },
        fa: {
            title: "ارتباط و پشتیبانی از PFPJ ry",
            subtitle: "جهت ارتباط، ارسال مستندات، همکاری علمی یا حمایت از صندوق حقوقی فرم زیر را تکمیل نمایید. پیام شما مستقیماً ثبت و به تیم هماهنگی در تلگرام ارسال می‌شود.",
            label_name: "نام و نام خانوادگی",
            label_email: "آدرس ایمیل",
            label_handle: "شناسه تلگرام (@username) یا شماره تماس / سیگنال (اختیاری)",
            placeholder_handle: "@username یا شماره تماس...",
            label_role: "زمینه همکاری / موضوع پیام",
            label_msg: "پیام / خلاصه دیدگاه یا مستندات",
            opt_volunteer: "داوطلب / پژوهشگر اطلاعات متن‌باز (OSINT)",
            opt_scholar: "حقوق‌دان / مشاور علمی",
            opt_witness: "شاهد / ارائه‌دهنده مدرک و مستندات",
            opt_funder: "حمایت از صندوق حقوقی پرونده",
            opt_general: "سایر موضوعات / ارتباط عمومی",
            submit_btn: "ارسال پیام",
            submitting: "در حال ارسال...",
            success: "سپاسگزاریم! پیام شما با موفقیت ثبت و دریافت شد.",
            error: "خطا در ارسال درخواست. لطفا مجدداً تلاش کنید.",
            tg_channel_note: "کانال رسمی تلگرام:"
        },
        fi: {
            title: "Ota yhteyttä & Tue — PFPJ ry",
            subtitle: "Täytä alla oleva lomake tukeaksesi oikeudenkäyntiämme, toimittaaksesi todisteita tai liittyäksesi tiimiin. Viestit ohjataan suoraan tiimillemme.",
            label_name: "Nimi",
            label_email: "Sähköpostiosoite",
            label_handle: "Telegram @käyttäjänimi tai Signal / Puhelin (Valinnainen)",
            placeholder_handle: "@username tai +358...",
            label_role: "Kiinnostuksen kohde / Rooli",
            label_msg: "Viesti / Kokemuksen tiivistelmä",
            opt_volunteer: "Vapaaehtoinen / OSINT-tutkija",
            opt_scholar: "Kansainvälisen oikeuden asiantuntija / Neuvonantaja",
            opt_witness: "Todistaja / Todisteiden toimittaja",
            opt_funder: "Oikeudenkäyntirahaston lahjoittaja",
            opt_general: "Yhteydenotto",
            submit_btn: "Lähetä viesti",
            submitting: "Lähetetään...",
            success: "Kiitos! Viestisi on vastaanotettu.",
            error: "Virhe lähetyksessä. Yritä uudelleen.",
            tg_channel_note: "Virallinen Telegram-kanava:"
        }
    };

    // Get current language from document element or globally set variable
    function getLang() {
        if (typeof currentLang !== 'undefined' && ['en', 'fa', 'fi'].includes(currentLang)) return currentLang;
        try {
            const saved = localStorage.getItem('pfp-lang') || localStorage.getItem('pfp_lang');
            if (saved && ['en', 'fa', 'fi'].includes(saved)) return saved;
        } catch (_) {}
        const htmlLang = document.documentElement.lang || 'en';
        return ['en', 'fa', 'fi'].includes(htmlLang) ? htmlLang : 'en';
    }

    function normalizeRoleOption(roleHint) {
        if (!roleHint) return null;
        const r = String(roleHint).toLowerCase();
        if (r.includes('fund') || r.includes('donat') || r.includes('capital')) {
            return 'Litigation Fund Contributor';
        }
        if (r.includes('scholar') || r.includes('advis') || r.includes('review') || r.includes('draft') || r.includes('legal')) {
            return 'Legal Scholar / Advisory';
        }
        if (r.includes('witness') || r.includes('evidence') || r.includes('fact')) {
            return 'Witness / Evidence Contributor';
        }
        if (r.includes('volunteer') || r.includes('research') || r.includes('osint')) {
            return 'Volunteer / Researcher';
        }
        if (r.includes('general') || r.includes('contact') || r.includes('inquir')) {
            return 'General Inquiry';
        }
        return null;
    }

    // 3. Inject HTML markup
    const lang = getLang();
    const t = modalI18n[lang];

    const modalHtml = `
        <div class="contact-modal-content">
            <span class="contact-modal-close" onclick="closeContactModal()">&times;</span>
            <h3 style="margin-top:0; margin-bottom:8px; color:#d4a853; font-size: 1.35rem;" id="modal_title">${t.title}</h3>
            <p style="font-size:0.88rem; color:#94a3b8; margin-bottom:16px; line-height: 1.5;" id="modal_subtitle">${t.subtitle}</p>
            
            <form id="contactForm" onsubmit="submitContactForm(event)">
                <div class="contact-form-group">
                    <label id="modal_label_name" for="contactName">${t.label_name}</label>
                    <input type="text" id="contactName" required>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_email" for="contactEmail">${t.label_email}</label>
                    <input type="email" id="contactEmail" required>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_handle" for="contactHandle">${t.label_handle}</label>
                    <input type="text" id="contactHandle" placeholder="${t.placeholder_handle}" dir="ltr">
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_role" for="contactRole">${t.label_role}</label>
                    <select id="contactRole">
                        <option value="Volunteer / Researcher" id="modal_opt_volunteer">${t.opt_volunteer}</option>
                        <option value="Legal Scholar / Advisory" id="modal_opt_scholar">${t.opt_scholar}</option>
                        <option value="Witness / Evidence Contributor" id="modal_opt_witness">${t.opt_witness}</option>
                        <option value="Litigation Fund Contributor" id="modal_opt_funder">${t.opt_funder}</option>
                        <option value="General Inquiry" id="modal_opt_general">${t.opt_general}</option>
                    </select>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_msg" for="contactMessage">${t.label_msg}</label>
                    <textarea id="contactMessage" required rows="4"></textarea>
                </div>
                
                <button type="submit" class="contact-submit-btn" id="modal_submit_btn">${t.submit_btn}</button>
            </form>
            
            <div id="contactFormStatus" class="contact-status"></div>

            <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08); display:flex; align-items:center; justify-content:space-between; font-size:0.8rem; color:#94a3b8;">
                <span id="modal_tg_note">${t.tg_channel_note}</span>
                <a href="https://t.me/people4peace" target="_blank" rel="noopener" style="color:#d4a853; text-decoration:none; font-weight:600;">✈ @people4peace</a>
            </div>
        </div>
    `;

    const modalDiv = document.createElement('div');
    modalDiv.id = 'contactModal';
    modalDiv.className = 'contact-modal';
    modalDiv.innerHTML = modalHtml;
    document.body.appendChild(modalDiv);

    // 4. Expose Global functions
    window.openContactModal = function(roleHint) {
        // Refresh localization strings in case language changed
        const currentL = getLang();
        const curT = modalI18n[currentL] || modalI18n.en;
        
        document.getElementById('modal_title').textContent = curT.title;
        document.getElementById('modal_subtitle').textContent = curT.subtitle;
        document.getElementById('modal_label_name').textContent = curT.label_name;
        document.getElementById('modal_label_email').textContent = curT.label_email;
        document.getElementById('modal_label_handle').textContent = curT.label_handle;
        document.getElementById('contactHandle').placeholder = curT.placeholder_handle;
        document.getElementById('modal_label_role').textContent = curT.label_role;
        document.getElementById('modal_label_msg').textContent = curT.label_msg;
        document.getElementById('modal_opt_volunteer').textContent = curT.opt_volunteer;
        document.getElementById('modal_opt_scholar').textContent = curT.opt_scholar;
        document.getElementById('modal_opt_witness').textContent = curT.opt_witness;
        document.getElementById('modal_opt_funder').textContent = curT.opt_funder;
        document.getElementById('modal_opt_general').textContent = curT.opt_general;
        document.getElementById('modal_submit_btn').textContent = curT.submit_btn;
        document.getElementById('modal_tg_note').textContent = curT.tg_channel_note;

        const statusDiv = document.getElementById('contactFormStatus');
        if (statusDiv) statusDiv.style.display = 'none';

        const matchedRole = normalizeRoleOption(roleHint);
        if (matchedRole) {
            const roleSelect = document.getElementById('contactRole');
            if (roleSelect) roleSelect.value = matchedRole;
        }

        document.getElementById('contactModal').classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeContactModal = function() {
        document.getElementById('contactModal').classList.remove('active');
        document.body.style.overflow = '';
    };

    window.submitContactForm = async function(event) {
        event.preventDefault();
        const currentL = getLang();
        const curT = modalI18n[currentL] || modalI18n.en;
        const statusDiv = document.getElementById('contactFormStatus');
        
        statusDiv.style.display = 'block';
        statusDiv.style.background = 'rgba(255, 255, 255, 0.05)';
        statusDiv.style.color = '#ffffff';
        statusDiv.textContent = curT.submitting;

        const payload = {
            name: document.getElementById('contactName').value,
            email: document.getElementById('contactEmail').value,
            contact_handle: document.getElementById('contactHandle').value,
            role: document.getElementById('contactRole').value,
            message: document.getElementById('contactMessage').value
        };

        try {
            let apiUrl = '/api/telegram/submit-contact/';
            if (window.location.protocol === 'file:') {
                apiUrl = 'http://localhost:8000/api/telegram/submit-contact/';
            }

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (response.ok) {
                statusDiv.style.background = 'rgba(16, 185, 129, 0.15)';
                statusDiv.style.color = '#10b981';
                statusDiv.textContent = curT.success;
                document.getElementById('contactForm').reset();
                setTimeout(window.closeContactModal, 2000);
            } else {
                throw new Error(data.message || data.error || 'Server error');
            }
        } catch (err) {
            statusDiv.style.background = 'rgba(239, 68, 68, 0.15)';
            statusDiv.style.color = '#ef4444';
            statusDiv.textContent = `${curT.error} (${err.message || 'Submission failed'})`;
        }
    };

    // Close on backdrop click
    modalDiv.addEventListener('click', function(e) {
        if (e.target === modalDiv) {
            window.closeContactModal();
        }
    });

    // 5. Global event delegation for all contact triggers (works with dynamic DOM)
    document.addEventListener('click', function(e) {
        const trigger = e.target.closest('a[href^="mailto:info@peopleforpeace.live"], a[href="#contact"], [data-open-contact], [data-contact-role]');
        if (!trigger) return;
        e.preventDefault();
        if (typeof window.closeMobileNav === 'function') {
            window.closeMobileNav();
        }
        const roleAttr = trigger.getAttribute('data-contact-role') || trigger.getAttribute('href') || '';
        window.openContactModal(roleAttr);
    });

    // 6. Global Accountability Vow Modal (Site-Wide Main CTA)
    const VOW_BADGE_THRESHOLD = 100;
    window.vowSignatoryCount = typeof window.vowSignatoryCount === 'number' ? window.vowSignatoryCount : 0;
    try { localStorage.removeItem('pfp_vow_count'); } catch (_) {}

    const vowCss = `
        #vowModal.vow-global-modal {
            display: none;
            position: fixed;
            z-index: 100050;
            inset: 0;
            background: rgba(5, 8, 15, 0.86);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-y: auto;
        }
        #vowModal.vow-global-modal.visible,
        #vowModal.modal-backdrop.visible {
            display: flex;
        }
        #vowModal .vow-modal-box {
            background: #0f1626;
            border: 1px solid rgba(229, 185, 95, 0.32);
            border-radius: 16px;
            padding: 24px 28px;
            width: 100%;
            max-width: 720px;
            color: #f5f3ef;
            color-scheme: dark;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.72);
            position: relative;
            text-align: left;
            direction: ltr;
            font-family: 'Source Sans 3', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            max-height: 92vh;
            overflow-y: auto;
        }
        body[dir="rtl"] #vowModal .vow-modal-box,
        html[dir="rtl"] #vowModal .vow-modal-box {
            text-align: right;
            direction: rtl;
            font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        #vowModal .vow-top-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }
        #vowModal .vow-badge-tag {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 4px 10px;
            border-radius: 6px;
            background: rgba(229, 185, 95, 0.14);
            border: 1px solid rgba(229, 185, 95, 0.35);
            color: #e5b95f;
        }
        #vowModal .vow-close-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 1.5rem;
            cursor: pointer;
            line-height: 1;
            padding: 4px 8px;
        }
        #vowModal .vow-close-btn:hover {
            color: #ffffff;
        }
        #vowModal .vow-title-h2 {
            font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
            font-size: 1.55rem;
            font-weight: 700;
            color: #f8fafc;
            margin: 0 0 4px 0;
        }
        body[dir="rtl"] #vowModal .vow-title-h2,
        html[dir="rtl"] #vowModal .vow-title-h2 {
            font-family: 'Vazirmatn', sans-serif;
        }
        #vowModal .vow-sub-cat {
            font-size: 0.84rem;
            font-weight: 600;
            color: #e5b95f;
            margin-bottom: 14px;
        }
        #vowModal .vow-pledge-box {
            background: rgba(229, 185, 95, 0.07);
            border: 1px solid rgba(229, 185, 95, 0.25);
            border-radius: 10px;
            padding: 14px 16px;
            font-size: 0.9rem;
            line-height: 1.62;
            color: #e2e8f0;
            font-style: italic;
            margin-bottom: 16px;
        }
        #vowModal .vow-form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 12px;
        }
        @media (max-width: 640px) {
            #vowModal .vow-form-grid {
                grid-template-columns: 1fr;
            }
        }
        #vowModal .vow-field {
            display: flex;
            flex-direction: column;
            gap: 5px;
            margin-bottom: 10px;
        }
        #vowModal .vow-form-grid .vow-field {
            margin-bottom: 0;
        }
        #vowModal .vow-field label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #cbd5e1;
        }
        #vowModal .vow-field input,
        #vowModal .vow-field select,
        #vowModal .vow-field textarea {
            width: 100%;
            box-sizing: border-box;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 8px;
            padding: 9px 12px;
            color: #f8fafc;
            font-size: 0.88rem;
            font-family: inherit;
        }
        #vowModal .vow-field input:focus-visible,
        #vowModal .vow-field select:focus-visible,
        #vowModal .vow-field textarea:focus-visible {
            border-color: #e5b95f;
            outline: 2px solid #e5b95f;
            outline-offset: 1px;
        }
        #vowModal .vow-roles-fieldset {
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 10px;
            padding: 10px 12px 12px;
            margin: 2px 0 12px;
            background: rgba(15, 23, 42, 0.55);
            min-inline-size: 0;
        }
        #vowModal .vow-roles-fieldset[aria-invalid="true"] {
            border-color: #f87171;
        }
        #vowModal .vow-roles-legend {
            font-size: 0.82rem;
            font-weight: 700;
            color: #e2e8f0;
            padding-inline: 6px;
        }
        #vowModal .vow-roles-hint {
            font-size: 0.76rem;
            color: #94a3b8;
            margin: 0 0 8px;
        }
        #vowModal .vow-roles-grid {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        #vowModal .vow-role-option {
            display: flex;
            align-items: center;
            gap: 10px;
            min-block-size: 44px;
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(15, 23, 42, 0.85);
            color: #e2e8f0;
            font-size: 0.84rem;
            line-height: 1.4;
            cursor: pointer;
            transition: border-color 0.16s ease, background-color 0.16s ease;
            text-align: start;
        }
        #vowModal .vow-role-option:hover {
            border-color: rgba(229, 185, 95, 0.45);
            background: rgba(229, 185, 95, 0.06);
        }
        #vowModal .vow-role-option.is-checked,
        #vowModal .vow-role-option:has(input[type="checkbox"]:checked) {
            border-color: rgba(229, 185, 95, 0.65);
            background: rgba(229, 185, 95, 0.12);
            color: #f8fafc;
        }
        #vowModal .vow-role-option input[type="checkbox"] {
            accent-color: #e5b95f;
            inline-size: 1.15rem;
            block-size: 1.15rem;
            margin: 0;
            flex-shrink: 0;
            cursor: pointer;
        }
        #vowModal .vow-role-option input[type="checkbox"]:focus-visible,
        #vowModal .vow-checkbox-row input[type="checkbox"]:focus-visible,
        #vowModal .vow-submit-btn:focus-visible,
        #vowModal .vow-close-btn:focus-visible {
            outline: 2px solid #e5b95f;
            outline-offset: 2px;
        }
        @supports not (accent-color: #e5b95f) {
            #vowModal .vow-role-option input[type="checkbox"] {
                position: absolute !important;
                clip-path: inset(50%) !important;
                overflow: hidden !important;
                width: 1px !important;
                height: 1px !important;
                margin: -1px !important;
                padding: 0 !important;
                border: 0 !important;
                white-space: nowrap !important;
            }
            #vowModal .vow-role-option {
                position: relative;
                padding-inline-start: 2.2rem;
            }
            #vowModal .vow-role-option input[type="checkbox"] + span::before {
                content: "";
                position: absolute;
                inset-inline-start: 0.75rem;
                top: 50%;
                transform: translateY(-50%);
                width: 1.1rem;
                height: 1.1rem;
                border: 2px solid #94a3b8;
                border-radius: 4px;
                background: #0f172a;
                box-sizing: border-box;
            }
            #vowModal .vow-role-option input[type="checkbox"]:checked + span::before {
                background: #e5b95f;
                border-color: #e5b95f;
            }
            #vowModal .vow-role-option input[type="checkbox"]:checked + span::after {
                content: "✓";
                position: absolute;
                inset-inline-start: 0.92rem;
                top: 50%;
                transform: translateY(-50%);
                color: #080b11;
                font-weight: 800;
                font-size: 0.82rem;
            }
            #vowModal .vow-role-option input[type="checkbox"]:focus-visible + span::before {
                outline: 2px solid #e5b95f;
                outline-offset: 2px;
            }
        }
        #vowModal .vow-checkbox-row {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 0.82rem;
            color: #cbd5e1;
            line-height: 1.45;
            margin: 12px 0 16px;
            cursor: pointer;
        }
        #vowModal .vow-checkbox-row input[type="checkbox"] {
            margin-top: 3px;
            accent-color: #e5b95f;
            width: 16px;
            height: 16px;
            flex-shrink: 0;
        }
        #vowModal .vow-submit-btn {
            width: 100%;
            padding: 13px 18px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg, #e5b95f 0%, #c89632 100%);
            color: #080b11;
            font-weight: 800;
            font-size: 0.95rem;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 6px 20px rgba(229, 185, 95, 0.3);
        }
        #vowModal .vow-submit-btn:hover {
            background: linear-gradient(135deg, #f0c975 0%, #d4a853 100%);
            transform: translateY(-1px);
        }
        #vowModal .vow-status-msg {
            display: none;
            margin-top: 12px;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 0.86rem;
            text-align: center;
        }
    `;
    const vowStyleEl = document.createElement('style');
    vowStyleEl.innerHTML = vowCss;
    document.head.appendChild(vowStyleEl);

    const vowI18n = {
        en: {
            badge: "Global Accountability Petition & Civic Vow",
            title: "The Minab Accountability Vow",
            subtitle: "November 20 World Children's Day · People for Peace & Justice ry",
            pledge: "\"Bearing witness to the verified forensic record of Shajareh Tayyebeh Primary School and the lives of the 120+ schoolchildren and 26 educators taken on February 28, 2026, I solemnly vow to stand ready and participate in every lawful civic, investigative, financial, and judicial endeavor to hold every person in the chain of command accountable for this atrocity.\"",
            nameLabel: "Full Name *",
            namePlaceholder: "Your full name",
            emailLabel: "Email Address *",
            emailPlaceholder: "you@example.com",
            tgLabel: "Telegram Username (Optional — for Action Mobilization)",
            tgPlaceholder: "@username",
            phoneLabel: "Phone / Signal / WhatsApp (Optional — for Action Mobilization)",
            phonePlaceholder: "+358 40 123 4567",
            cityLabel: "City & Country *",
            cityPlaceholder: "Helsinki, Finland",
            howLabel: "How I Will Take Action for Accountability *",
            howHint: "Select one or more ways you wish to contribute",
            optPetitioner: "Public Petitioner & Global Campaigner — Amplify the case & join collective actions",
            optFinancial: "Financial Support for the Legal Prosecution Campaign — Fund court filings & forensic experts",
            optLegal: "Legal, Human Rights & Judicial Action — Pro bono counsel & universal jurisdiction",
            optMedia: "Media, Journalism & Public Amplification — Investigative reporting & translations",
            optEvent: "Host or Join a Nov 20 World Children's Day Action — Vigil, university panel, or exhibition",
            optResearch: "Forensic, OSINT & Archival Research — Evidence verification & witness documentation",
            msgLabel: "Personal Message of Remembrance or Commitment (Optional)",
            msgPlaceholder: "In memory of the children of Minab...",
            consent: "I affirm this vow and consent to be contacted by People for Peace & Justice ry when collective legal, parliamentary, financial, or civic actions are mobilized.",
            submitBtn: "✍️ Sign the Vow & Join the Accountability Registry",
            submitting: "Recording your Accountability Vow...",
            selectError: "Please select at least one way to take action.",
            submitError: "Could not save your Accountability Vow right now. Please check your connection and try again.",
            successMsg: "✓ Thank you, {name}. Your Accountability Vow{count} has been recorded."
        },
        fa: {
            badge: "پتیشن جهانی و میثاق دادخواهی میناب",
            title: "میثاق دادخواهی کودکان میناب",
            subtitle: "۲۰ نوامبر (روز جهانی کودک) · انجمن صلح و عدالت فنلاند (PFPJ ry)",
            pledge: "«با گواهی بر مستندات راستی‌آزمایی‌شده دبستان شجره طیبه میناب و به یاد بیش از ۱۲۰ کودک دانش‌آموز و ۲۶ آموزگار که در ۹ اسفند ۱۴۰۴ جان باختند، صمیمانه پیمان می‌بندم که در هر تلاش قانونی، مدنی، تحقیقاتی، مالی و قضایی برای پاسخگو کردن تمامی آمران و عاملان این جنایت در سلسله‌مراتب فرماندهی مشارکت و همراهی کنم.»",
            nameLabel: "نام و نام خانوادگی *",
            namePlaceholder: "نام کامل شما",
            emailLabel: "آدرس ایمیل *",
            emailPlaceholder: "you@example.com",
            tgLabel: "شناسه تلگرام (اختیاری — جهت هماهنگی اقدامات دادخواهی)",
            tgPlaceholder: "@username",
            phoneLabel: "شماره تماس / سیگنال / واتس‌اپ (اختیاری — جهت هماهنگی اقدامات)",
            phonePlaceholder: "+358 40 123 4567",
            cityLabel: "شهر و کشور محل سکونت *",
            cityPlaceholder: "هلسینکی، فنلاند",
            howLabel: "نحوه همراهی و اقدام من در کارزار دادخواهی *",
            howHint: "می‌توانید یک یا چند مورد را هم‌زمان انتخاب کنید",
            optPetitioner: "امضاکننده عمومی و کنشگر کارزار جهانی — بازنشر مستندات و همراهی در اقدامات جمعی",
            optFinancial: "حمایت مالی از کارزار پیگرد قضایی بین‌المللی — تأمین هزینه‌های ثبت دادخواست و کارشناسان رسمی",
            optLegal: "همکاری حقوقی، قضایی و حقوق بشری — وکالت، صلاحیت قضایی جهانی و رایزنی پارلمانی",
            optMedia: "رسانه، روزنامه‌نگاری و روایت‌گری عمومی — پوشش خبری، مستندسازی و ترجمه",
            optEvent: "برگزاری یا مشارکت در رویداد ۲۰ نوامبر (روز جهانی کودک) — تجمع، پنل دانشگاهی یا نمایشگاه",
            optResearch: "پژوهش فنی، اطلاعات متن‌باز (OSINT) و مستندسازی — راستی‌آزمایی شواهد و ثبت شهادت‌ها",
            msgLabel: "پیام یادبود یا تعهد شخصی (اختیاری)",
            msgPlaceholder: "به یاد کودکان دبستان شجره طیبه میناب...",
            consent: "این میثاق را تأیید می‌کنم و موافقم در زمان آغاز اقدامات جمعی حقوقی، پارلمانی، مالی و مدنی با من تماس گرفته شود.",
            submitBtn: "✍️ ثبت امضا و پیوستن به کارزار جهانی دادخواهی",
            submitting: "در حال ثبت امضای شما در میثاق دادخواهی...",
            selectError: "لطفاً دست‌کم یک مورد از روش‌های همراهی را انتخاب کنید.",
            submitError: "ثبت امضا با خطا روبه‌رو شد. لطفاً اتصال اینترنت را بررسی کرده و دوباره تلاش کنید.",
            successMsg: "✓ سپاسگزاریم {name}؛ امضای شما در میثاق دادخواهی{count} با موفقیت ثبت شد."
        },
        fi: {
            badge: "Kansainvälinen vetoomus & vastuulupaus",
            title: "Minabin vastuulupaus",
            subtitle: "20. marraskuuta — Lapsen oikeuksien päivä · People for Peace & Justice ry",
            pledge: "\"Todistaen Shajareh Tayyebehin peruskoulun vahvistetun forensisen aineiston ja 28.2.2026 surmattujen yli 120 koululaisen ja 26 opettajan kohtalon, lupaan olla valmis osallistumaan kaikkiin laillisiin kansalais-, tutkinta-, rahoitus- ja oikeustoimiin, jotta jokainen komentoketjussa vastuussa oleva saatetaan oikeudenkäyntiin.\"",
            nameLabel: "Koko nimi *",
            namePlaceholder: "Koko nimesi",
            emailLabel: "Sähköpostiosoite *",
            emailPlaceholder: "you@example.com",
            tgLabel: "Telegram-käyttäjänimi (Valinnainen — toiminnan koordinointiin)",
            tgPlaceholder: "@username",
            phoneLabel: "Puhelin / Signal / WhatsApp (Valinnainen — toiminnan koordinointiin)",
            phonePlaceholder: "+358 40 123 4567",
            cityLabel: "Kaupunki & Maa *",
            cityPlaceholder: "Helsinki, Suomi",
            howLabel: "Miten osallistun oikeudelliseen vastuuseen saattamiseen *",
            howHint: "Voit valita yhden tai useamman osallistumistavan",
            optPetitioner: "Julkinen vetoomuksen allekirjoittaja & kampanjoija — Jaa tietoa ja osallistu yhteisiin toimiin",
            optFinancial: "Taloudellinen tuki oikeudenkäyntikampanjalle — Tue kansainvälisiä tuomioistuinmaksuja ja asiantuntijoita",
            optLegal: "Oikeudellinen & ihmisoikeustyö — Juridinen asiantuntijuus, yleinen toimivalta ja päättäjävaikuttaminen",
            optMedia: "Media, journalismi & viestintä — Tutkiva journalismi, dokumentointi ja käännökset",
            optEvent: "Järjestä tai liity 20.11. Lapsen oikeuksien päivän tapahtumaan — Muistotilaisuus tai paneeli",
            optResearch: "Forensinen & OSINT-tutkimus — Todisteiden verifiointi ja arkistointi",
            msgLabel: "Henkilökohtainen muistoviesti tai sitoumus (Valinnainen)",
            msgPlaceholder: "Minabin lasten muistolle...",
            consent: "Vahvistan tämän lupauksen ja suostun siihen, että People for Peace & Justice ry ottaa minuun yhteyttä oikeudellisten, taloudellisten tai kansalaistoimien käynnistyessä.",
            submitBtn: "✍️ Allekirjoita lupaus & liity rekisteriin",
            submitting: "Tallennetaan vastuulupaustasi...",
            selectError: "Valitse vähintään yksi osallistumistapa.",
            submitError: "Tallennus epäonnistui. Tarkista verkkoyhteys ja yritä uudelleen.",
            successMsg: "✓ Kiitos, {name}. Vastuulupauksesi{count} on tallennettu."
        }
    };

    function syncVowRoleCheckedStyles() {
        document.querySelectorAll('#vowContributionGroup .vow-role-option').forEach(function(lbl) {
            const cb = lbl.querySelector('input[type="checkbox"]');
            lbl.classList.toggle('is-checked', Boolean(cb && cb.checked));
        });
    }

    function getSelectedVowRoles() {
        const groupEl = document.getElementById('vowContributionGroup');
        if (groupEl) {
            return Array.from(groupEl.querySelectorAll('input[name="vowContribution"]:checked'))
                .map(function(cb) { return cb.value; })
                .filter(Boolean);
        }
        const legacySelect = document.getElementById('vowContribution');
        if (legacySelect && legacySelect.value) {
            return [legacySelect.value];
        }
        return [];
    }

    function formatVowRolesSummary(rolesList) {
        if (!rolesList || rolesList.length === 0) {
            return 'Accountability Vow — Public Petitioner & Campaigner';
        }
        if (rolesList.length === 1) {
            return rolesList[0];
        }
        const shortLabels = rolesList.map(function(r) {
            return String(r).replace(/^Accountability Vow\s*[—-]\s*/, '').trim();
        });
        return ('Accountability Vow — ' + shortLabels.join(' | ')).slice(0, 500);
    }

    function buildVowModalInnerHTML(vt) {
        return `
            <div class="vow-modal-box" role="dialog" aria-modal="true" aria-labelledby="vowTitleEl">
                <div class="vow-top-row">
                    <span class="vow-badge-tag" id="vowBadgeTag" data-i18n="vowBadge">${vt.badge}</span>
                    <button type="button" class="vow-close-btn" id="vowCloseBtn" aria-label="Close vow modal">&times;</button>
                </div>
                <h2 class="vow-title-h2" id="vowTitleEl" data-i18n="vowTitle">${vt.title}</h2>
                <div class="vow-sub-cat" id="vowSubEl" data-i18n="vowSubtitle">${vt.subtitle}</div>
                <div class="vow-pledge-box" id="vowPledgeText" data-i18n="vowPledgeText">${vt.pledge}</div>
                <form id="vowForm" method="post" action="/api/telegram/submit-contact/">
                    <div class="vow-form-grid">
                        <div class="vow-field">
                            <label id="vowNameLabelEl" for="vowName" data-i18n="vowNameLabel">${vt.nameLabel}</label>
                            <input type="text" id="vowName" name="name" autocomplete="name" required placeholder="${vt.namePlaceholder}" />
                        </div>
                        <div class="vow-field">
                            <label id="vowEmailLabelEl" for="vowEmail" data-i18n="vowEmailLabel">${vt.emailLabel}</label>
                            <input type="email" id="vowEmail" name="email" autocomplete="email" autocorrect="off" autocapitalize="none" spellcheck="false" required placeholder="${vt.emailPlaceholder}" dir="ltr" />
                        </div>
                    </div>
                    <div class="vow-form-grid">
                        <div class="vow-field">
                            <label id="vowTgLabelEl" for="vowTelegram" data-i18n="vowTgLabel">${vt.tgLabel}</label>
                            <input type="text" id="vowTelegram" name="telegram_username" autocorrect="off" autocapitalize="none" spellcheck="false" placeholder="${vt.tgPlaceholder}" dir="ltr" />
                        </div>
                        <div class="vow-field">
                            <label id="vowPhoneLabelEl" for="vowPhone" data-i18n="vowPhoneLabel">${vt.phoneLabel}</label>
                            <input type="tel" id="vowPhone" name="phone_number" autocomplete="tel" placeholder="${vt.phonePlaceholder}" dir="ltr" />
                        </div>
                    </div>
                    <div class="vow-field">
                        <label id="vowCityLabelEl" for="vowCity" data-i18n="vowCityLabel">${vt.cityLabel}</label>
                        <input type="text" id="vowCity" name="city_country" autocomplete="address-level2" required placeholder="${vt.cityPlaceholder}" />
                    </div>
                    <fieldset class="vow-roles-fieldset" id="vowContributionGroup" aria-describedby="vowHowHintEl">
                        <legend class="vow-roles-legend" id="vowHowLabelEl" data-i18n="vowHowLabel">${vt.howLabel}</legend>
                        <p class="vow-roles-hint" id="vowHowHintEl" data-i18n="vowHowHint">${vt.howHint}</p>
                        <div class="vow-roles-grid">
                            <label class="vow-role-option is-checked" for="vowCheckPetitioner">
                                <input type="checkbox" id="vowCheckPetitioner" name="vowContribution" value="Accountability Vow — Public Petitioner & Campaigner" checked />
                                <span id="vowOptPetitioner" data-i18n="vowOptPetitioner">${vt.optPetitioner}</span>
                            </label>
                            <label class="vow-role-option" for="vowCheckFinancial">
                                <input type="checkbox" id="vowCheckFinancial" name="vowContribution" value="Accountability Vow — Financial Support (Legal Prosecution)" />
                                <span id="vowOptFinancial" data-i18n="vowOptFinancial">${vt.optFinancial}</span>
                            </label>
                            <label class="vow-role-option" for="vowCheckLegal">
                                <input type="checkbox" id="vowCheckLegal" name="vowContribution" value="Accountability Vow — Legal & Judicial Counsel" />
                                <span id="vowOptLegal" data-i18n="vowOptLegal">${vt.optLegal}</span>
                            </label>
                            <label class="vow-role-option" for="vowCheckMedia">
                                <input type="checkbox" id="vowCheckMedia" name="vowContribution" value="Accountability Vow — Media, Documentary & XR" />
                                <span id="vowOptMedia" data-i18n="vowOptMedia">${vt.optMedia}</span>
                            </label>
                            <label class="vow-role-option" for="vowCheckEvent">
                                <input type="checkbox" id="vowCheckEvent" name="vowContribution" value="Accountability Vow — Event Organizer (Nov 20 Hub)" />
                                <span id="vowOptEvent" data-i18n="vowOptEvent">${vt.optEvent}</span>
                            </label>
                            <label class="vow-role-option" for="vowCheckResearch">
                                <input type="checkbox" id="vowCheckResearch" name="vowContribution" value="Accountability Vow — Forensic & OSINT Research" />
                                <span id="vowOptResearch" data-i18n="vowOptResearch">${vt.optResearch}</span>
                            </label>
                        </div>
                    </fieldset>
                    <div class="vow-field">
                        <label id="vowMsgLabelEl" for="vowMessage" data-i18n="vowMessageLabel">${vt.msgLabel}</label>
                        <textarea id="vowMessage" name="message" rows="2" placeholder="${vt.msgPlaceholder}"></textarea>
                    </div>
                    <label class="vow-checkbox-row" for="vowCheckbox">
                        <input type="checkbox" id="vowCheckbox" name="consent" required checked />
                        <span id="vowConsentTextEl" data-i18n="vowConsentText">${vt.consent}</span>
                    </label>
                    <button type="submit" class="vow-submit-btn" id="vowSubmitBtn" data-i18n="vowSubmitBtn">${vt.submitBtn}</button>
                    <div class="vow-status-msg" id="vowStatusMsg" role="status" aria-live="polite"></div>
                </form>
            </div>
        `;
    }

    function ensureVowModal() {
        const vt = vowI18n[getLang()] || vowI18n.en;
        let vowModalEl = document.getElementById('vowModal');
        if (!vowModalEl) {
            vowModalEl = document.createElement('div');
            vowModalEl.id = 'vowModal';
            vowModalEl.className = 'vow-global-modal';
            vowModalEl.innerHTML = buildVowModalInnerHTML(vt);
            document.body.appendChild(vowModalEl);
        } else if (!document.getElementById('vowContributionGroup')) {
            vowModalEl.classList.add('vow-global-modal');
            vowModalEl.innerHTML = buildVowModalInnerHTML(vt);
        }

        const closeBtn = document.getElementById('vowCloseBtn');
        if (closeBtn && !closeBtn.__pfpBound) {
            closeBtn.__pfpBound = true;
            closeBtn.addEventListener('click', function() {
                window.closeVowModal();
            });
        }
        if (!vowModalEl.__pfpBackdropBound) {
            vowModalEl.__pfpBackdropBound = true;
            vowModalEl.addEventListener('click', function(e) {
                if (e.target === vowModalEl) {
                    window.closeVowModal();
                }
            });
        }
        const formEl = document.getElementById('vowForm');
        if (formEl && !formEl.__pfpBound) {
            formEl.__pfpBound = true;
            formEl.addEventListener('submit', window.submitVowForm);
        }
        const groupEl = document.getElementById('vowContributionGroup');
        if (groupEl && !groupEl.__pfpChangeBound) {
            groupEl.__pfpChangeBound = true;
            groupEl.addEventListener('change', function() {
                syncVowRoleCheckedStyles();
                if (getSelectedVowRoles().length > 0 && groupEl.getAttribute('aria-invalid') === 'true') {
                    groupEl.removeAttribute('aria-invalid');
                    const statusEl = document.getElementById('vowStatusMsg');
                    if (statusEl) statusEl.style.display = 'none';
                }
            });
        }
        syncVowRoleCheckedStyles();
        return vowModalEl;
    }

    function refreshVowModalLanguage() {
        const vt = vowI18n[getLang()] || vowI18n.en;
        const setTxt = function(id, text) {
            const el = document.getElementById(id);
            if (el) el.textContent = text;
        };
        setTxt('vowBadgeTag', vt.badge);
        setTxt('vowTitleEl', vt.title);
        setTxt('vowSubEl', vt.subtitle);
        setTxt('vowPledgeText', vt.pledge);
        setTxt('vowNameLabelEl', vt.nameLabel);
        setTxt('vowEmailLabelEl', vt.emailLabel);
        setTxt('vowTgLabelEl', vt.tgLabel);
        setTxt('vowPhoneLabelEl', vt.phoneLabel);
        setTxt('vowCityLabelEl', vt.cityLabel);
        setTxt('vowHowLabelEl', vt.howLabel);
        setTxt('vowHowHintEl', vt.howHint);
        setTxt('vowOptPetitioner', vt.optPetitioner);
        setTxt('vowOptFinancial', vt.optFinancial);
        setTxt('vowOptLegal', vt.optLegal);
        setTxt('vowOptMedia', vt.optMedia);
        setTxt('vowOptEvent', vt.optEvent);
        setTxt('vowOptResearch', vt.optResearch);
        setTxt('vowMsgLabelEl', vt.msgLabel);
        setTxt('vowConsentTextEl', vt.consent);
        setTxt('vowSubmitBtn', vt.submitBtn);

        const nameIn = document.getElementById('vowName');
        if (nameIn) nameIn.placeholder = vt.namePlaceholder;
        const emailIn = document.getElementById('vowEmail');
        if (emailIn) emailIn.placeholder = vt.emailPlaceholder;
        const tgIn = document.getElementById('vowTelegram');
        if (tgIn) tgIn.placeholder = vt.tgPlaceholder;
        const phoneIn = document.getElementById('vowPhone');
        if (phoneIn) phoneIn.placeholder = vt.phonePlaceholder;
        const cityIn = document.getElementById('vowCity');
        if (cityIn) cityIn.placeholder = vt.cityPlaceholder;
        const msgIn = document.getElementById('vowMessage');
        if (msgIn) msgIn.placeholder = vt.msgPlaceholder;
    }

    window.updateVowBadge = function() {
        const count = typeof window.vowSignatoryCount === 'number' ? window.vowSignatoryCount : 0;
        document.querySelectorAll('#vowCountBadge, .vow-counter-pill').forEach(function(badge) {
            if (count >= VOW_BADGE_THRESHOLD) {
                badge.textContent = count.toLocaleString();
                badge.style.display = 'inline-block';
            } else {
                badge.textContent = '';
                badge.style.display = 'none';
            }
        });
    };

    window.openVowModal = function(roleHint) {
        const modalEl = ensureVowModal();
        refreshVowModalLanguage();
        const statusEl = document.getElementById('vowStatusMsg');
        if (statusEl) statusEl.style.display = 'none';
        const groupEl = document.getElementById('vowContributionGroup');
        if (groupEl) groupEl.removeAttribute('aria-invalid');
        const submitBtn = document.getElementById('vowSubmitBtn');
        if (submitBtn) submitBtn.disabled = false;

        if (roleHint) {
            const r = String(roleHint).toLowerCase();
            let targetCheckboxId = '';
            if (r.includes('finan') || r.includes('fund') || r.includes('donat') || r.includes('prosecut')) {
                targetCheckboxId = 'vowCheckFinancial';
            } else if (r.includes('legal') || r.includes('judic')) {
                targetCheckboxId = 'vowCheckLegal';
            } else if (r.includes('media') || r.includes('journal')) {
                targetCheckboxId = 'vowCheckMedia';
            } else if (r.includes('event') || r.includes('nov')) {
                targetCheckboxId = 'vowCheckEvent';
            } else if (r.includes('osint') || r.includes('research') || r.includes('forensic')) {
                targetCheckboxId = 'vowCheckResearch';
            } else if (r.includes('petition') || r.includes('campaign')) {
                targetCheckboxId = 'vowCheckPetitioner';
            }
            if (targetCheckboxId) {
                const cb = document.getElementById(targetCheckboxId);
                if (cb) cb.checked = true;
            }
        }
        syncVowRoleCheckedStyles();

        modalEl.classList.add('visible');
        if (typeof window.__pfpTrackEvent === 'function') {
            window.__pfpTrackEvent('vow_open');
        }
    };

    window.closeVowModal = function() {
        const modalEl = document.getElementById('vowModal');
        if (modalEl) modalEl.classList.remove('visible');
    };

    window.submitVowForm = async function(e) {
        if (e && e.preventDefault) e.preventDefault();
        const vt = vowI18n[getLang()] || vowI18n.en;
        const name = (document.getElementById('vowName')?.value || '').trim();
        const email = (document.getElementById('vowEmail')?.value || '').trim();
        const telegram_username = (document.getElementById('vowTelegram')?.value || '').trim();
        const phone_number = (document.getElementById('vowPhone')?.value || '').trim();
        const city = (document.getElementById('vowCity')?.value || '').trim();
        const selectedRoles = getSelectedVowRoles();
        const personalMsg = (document.getElementById('vowMessage')?.value || '').trim();
        const statusEl = document.getElementById('vowStatusMsg');
        const submitBtn = document.getElementById('vowSubmitBtn');
        const groupEl = document.getElementById('vowContributionGroup');

        if (selectedRoles.length === 0) {
            if (groupEl) groupEl.setAttribute('aria-invalid', 'true');
            if (statusEl) {
                statusEl.style.display = 'block';
                statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
                statusEl.style.color = '#fca5a5';
                statusEl.textContent = vt.selectError;
            }
            const firstCb = groupEl ? groupEl.querySelector('input[type="checkbox"]') : null;
            if (firstCb) firstCb.focus();
            return;
        }
        if (groupEl) groupEl.removeAttribute('aria-invalid');

        const roleSummary = formatVowRolesSummary(selectedRoles);

        if (statusEl) {
            statusEl.style.display = 'block';
            statusEl.style.background = 'rgba(255,255,255,0.06)';
            statusEl.style.color = '#f0ebe3';
            statusEl.textContent = vt.submitting;
        }
        if (submitBtn) submitBtn.disabled = true;

        const contact_handle = [telegram_username, phone_number].filter(Boolean).join(' | ');
        const rolesBulletText = selectedRoles.map(function(item) { return '  - ' + item; }).join('\n');
        const fullMessage = [
            '[MINAB ACCOUNTABILITY VOW — NOV 20 HYBRID EVENT]',
            `City/Country: ${city}`,
            telegram_username ? `Telegram: ${telegram_username}` : null,
            phone_number ? `Phone/Signal: ${phone_number}` : null,
            selectedRoles.length > 1
                ? `Action Roles (${selectedRoles.length}):\n${rolesBulletText}`
                : `Action Role: ${roleSummary}`,
            'Pledge: Affirmed solemn vow to participate in holding every person in the chain of command accountable.',
            `Note: ${personalMsg || 'Signed via peopleforpeace.live Accountability Vow.'}`
        ].filter(Boolean).join('\n');

        let apiUrl = '/api/telegram/submit-contact/';
        if (window.location.protocol === 'file:' || window.location.port === '8090') {
            apiUrl = 'http://localhost:8000/api/telegram/submit-contact/';
        }

        try {
            const resp = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    telegram_username: telegram_username,
                    phone_number: phone_number,
                    city_country: city,
                    contact_handle: contact_handle,
                    role: roleSummary,
                    roles: selectedRoles,
                    message: fullMessage
                })
            });
            let data = {};
            try {
                data = await resp.json();
            } catch (_) {}

            if (!resp.ok) {
                throw new Error(data.error || data.message || `HTTP ${resp.status}`);
            }

            if (typeof data.vow_count === 'number') {
                window.vowSignatoryCount = data.vow_count;
            } else {
                window.vowSignatoryCount += 1;
            }
        } catch (err) {
            if (submitBtn) submitBtn.disabled = false;
            if (statusEl) {
                statusEl.style.display = 'block';
                statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
                statusEl.style.color = '#fca5a5';
                statusEl.textContent = vt.submitError;
            }
            return;
        }

        window.updateVowBadge();
        if (typeof window.__pfpTrackEvent === 'function') {
            window.__pfpTrackEvent('vow_signed');
        }

        if (statusEl) {
            statusEl.style.background = 'rgba(16, 185, 129, 0.18)';
            statusEl.style.color = '#6ee7b7';
            const countSuffix = window.vowSignatoryCount >= VOW_BADGE_THRESHOLD ? ` (#${window.vowSignatoryCount.toLocaleString()})` : '';
            statusEl.textContent = vt.successMsg
                .replace('{name}', name)
                .replace('{count}', countSuffix);
        }
        const formEl = document.getElementById('vowForm');
        if (formEl) {
            formEl.reset();
            const defaultCb = document.getElementById('vowCheckPetitioner');
            if (defaultCb) defaultCb.checked = true;
            const consentCb = document.getElementById('vowCheckbox');
            if (consentCb) consentCb.checked = true;
            syncVowRoleCheckedStyles();
        }
        setTimeout(function() {
            if (submitBtn) submitBtn.disabled = false;
            window.closeVowModal();
            if (statusEl) statusEl.style.display = 'none';
        }, 2800);
    };

    ensureVowModal();

    // Sync real Vow signatory count on startup (kept hidden until >= 100)
    (async function fetchGlobalVowStats() {
        try {
            if (window.location.protocol === 'file:') return;
            const resp = await fetch('/api/telegram/vow-stats/');
            if (resp.ok) {
                const data = await resp.json();
                if (typeof data.count === 'number') {
                    window.vowSignatoryCount = data.count;
                }
            }
        } catch (_) {}
        window.updateVowBadge();
    })();

    // Global click delegation for all Accountability Vow triggers across all pages
    document.addEventListener('click', function(e) {
        const vowTrigger = e.target.closest('[data-open-vow], [data-vow-role], a[href="#vow"], #openVowBtn');
        if (!vowTrigger) return;
        e.preventDefault();
        if (typeof window.closeMobileNav === 'function') {
            window.closeMobileNav();
        }
        const roleHint = vowTrigger.getAttribute('data-vow-role') || '';
        window.openVowModal(roleHint);
    });

    // 7. Lightweight First-Party Web Analytics Beacon (Zero cookies, GDPR-compliant)
    window.__pfpTrackEvent = function(eventType, customPath) {
        try {
            if (window.location.protocol === 'file:') return;
            const payload = JSON.stringify({
                path: customPath || window.location.pathname || '/',
                event_type: eventType || 'pageview',
                referrer: document.referrer || '',
                lang: getLang(),
                screen_width: window.innerWidth || null
            });
            const url = '/api/analytics/pageview/';
            if (navigator.sendBeacon) {
                const blob = new Blob([payload], { type: 'application/json' });
                navigator.sendBeacon(url, blob);
            } else {
                fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: payload,
                    keepalive: true
                }).catch(function() {});
            }
        } catch (_) {}
    };

    if (!window.__pfpPageviewSent) {
        window.__pfpPageviewSent = true;
        window.__pfpTrackEvent('pageview');

        document.addEventListener('click', function(e) {
            const pdfLink = e.target.closest('a[href$=".pdf"], a[href*=".pdf?"]');
            if (pdfLink) {
                const href = pdfLink.getAttribute('href') || '';
                window.__pfpTrackEvent('pdf_download', href);
            }
        });
    }
})();
