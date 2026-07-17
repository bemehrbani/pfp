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
            title: "Join & Support PFPJ ry",
            subtitle: "Fill out the form below to support our legal advocacy or join our team. Submissions are instantly routed to our Telegram group.",
            label_name: "Name",
            label_email: "Email Address",
            label_role: "Area of Interest / Role",
            label_msg: "Message / Experience Summary",
            opt_volunteer: "Volunteer / OSINT Researcher",
            opt_scholar: "Legal Scholar / Advisor",
            opt_witness: "Witness / Evidence Contributor",
            opt_funder: "Litigation Fund Contributor",
            opt_general: "General Inquiry",
            submit_btn: "Submit Request",
            submitting: "Submitting...",
            success: "Submission received successfully!",
            error: "Error sending request. Please try again."
        },
        fa: {
            title: "مشارکت و پشتیبانی از PFPJ ry",
            subtitle: "جهت عضویت، همکاری یا حمایت مالی فرم زیر را تکمیل نمایید. اطلاعات به گروه تلگرام هدایت می‌شوند.",
            label_name: "نام و نام خانوادگی",
            label_email: "آدرس ایمیل",
            label_role: "زمینه همکاری / نقش",
            label_msg: "پیام / خلاصه سوابق و تجربه",
            opt_volunteer: "داوطلب / پژوهشگر اطلاعات متن‌باز (OSINT)",
            opt_scholar: "حقوق‌دان / مشاور علمی",
            opt_witness: "شاهد / ارائه‌دهنده مدرک",
            opt_funder: "حمایت از صندوق حقوقی پرونده",
            opt_general: "سایر موضوعات",
            submit_btn: "ارسال درخواست",
            submitting: "در حال ارسال...",
            success: "درخواست شما با موفقیت ارسال شد.",
            error: "خطا در ارسال درخواست. لطفا مجدداً تلاش کنید."
        },
        fi: {
            title: "Liity & Tue — PFPJ ry",
            subtitle: "Täytä alla oleva lomake tukeaksesi oikeudenkäyntiämme tai liittyäksesi tiimiin. Tiedot lähetetään Telegram-ryhmäämme.",
            label_name: "Nimi",
            label_email: "Sähköpostiosoite",
            label_role: "Kiinnostuksen kohde / Rooli",
            label_msg: "Viesti / Kokemuksen tiivistelmä",
            opt_volunteer: "Vapaaehtoinen / OSINT-tutkija",
            opt_scholar: "Kansainvälisen oikeuden asiantuntija / Neuvonantaja",
            opt_witness: "Todistaja / Todisteiden toimittaja",
            opt_funder: "Oikeudenkäyntirahaston lahjoittaja",
            opt_general: "Yhteydenotto",
            submit_btn: "Lähetä pyyntö",
            submitting: "Lähetetään...",
            success: "Pyyntö lähetetty onnistuneesti!",
            error: "Virhe lähetyksessä. Yritä uudelleen."
        }
    };

    // Get current language from document element or globally set variable
    function getLang() {
        if (typeof currentLang !== 'undefined') return currentLang;
        const htmlLang = document.documentElement.lang || 'en';
        return ['en', 'fa', 'fi'].includes(htmlLang) ? htmlLang : 'en';
    }

    // 3. Inject HTML markup
    const lang = getLang();
    const t = modalI18n[lang];

    const modalHtml = `
        <div class="contact-modal-content">
            <span class="contact-modal-close" onclick="closeContactModal()">&times;</span>
            <h3 style="margin-top:0; margin-bottom:8px; color:#d4a853; font-size: 1.35rem;" id="modal_title">${t.title}</h3>
            <p style="font-size:0.88rem; color:#94a3b8; margin-bottom:20px; line-height: 1.5;" id="modal_subtitle">${t.subtitle}</p>
            
            <form id="contactForm" onsubmit="submitContactForm(event)">
                <div class="contact-form-group">
                    <label id="modal_label_name">${t.label_name}</label>
                    <input type="text" id="contactName" required>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_email">${t.label_email}</label>
                    <input type="email" id="contactEmail" required>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_role">${t.label_role}</label>
                    <select id="contactRole">
                        <option value="Volunteer / Researcher" id="modal_opt_volunteer">${t.opt_volunteer}</option>
                        <option value="Legal Scholar / Advisory" id="modal_opt_scholar">${t.opt_scholar}</option>
                        <option value="Witness / Evidence Contributor" id="modal_opt_witness">${t.opt_witness}</option>
                        <option value="Litigation Fund Contributor" id="modal_opt_funder">${t.opt_funder}</option>
                        <option value="General Inquiry" id="modal_opt_general">${t.opt_general}</option>
                    </select>
                </div>
                <div class="contact-form-group">
                    <label id="modal_label_msg">${t.label_msg}</label>
                    <textarea id="contactMessage" required rows="4"></textarea>
                </div>
                
                <button type="submit" class="contact-submit-btn" id="modal_submit_btn">${t.submit_btn}</button>
            </form>
            
            <div id="contactFormStatus" class="contact-status"></div>
        </div>
    `;

    const modalDiv = document.createElement('div');
    modalDiv.id = 'contactModal';
    modalDiv.className = 'contact-modal';
    modalDiv.innerHTML = modalHtml;
    document.body.appendChild(modalDiv);

    // 4. Expose Global functions
    window.openContactModal = function() {
        // Refresh localization strings in case language changed
        const currentL = getLang();
        const curT = modalI18n[currentL];
        
        document.getElementById('modal_title').textContent = curT.title;
        document.getElementById('modal_subtitle').textContent = curT.subtitle;
        document.getElementById('modal_label_name').textContent = curT.label_name;
        document.getElementById('modal_label_email').textContent = curT.label_email;
        document.getElementById('modal_label_role').textContent = curT.label_role;
        document.getElementById('modal_label_msg').textContent = curT.label_msg;
        document.getElementById('modal_opt_volunteer').textContent = curT.opt_volunteer;
        document.getElementById('modal_opt_scholar').textContent = curT.opt_scholar;
        document.getElementById('modal_opt_witness').textContent = curT.opt_witness;
        document.getElementById('modal_opt_funder').textContent = curT.opt_funder;
        document.getElementById('modal_opt_general').textContent = curT.opt_general;
        document.getElementById('modal_submit_btn').textContent = curT.submit_btn;

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
        const curT = modalI18n[currentL];
        const statusDiv = document.getElementById('contactFormStatus');
        
        statusDiv.style.display = 'block';
        statusDiv.style.background = 'rgba(255, 255, 255, 0.05)';
        statusDiv.style.color = '#ffffff';
        statusDiv.textContent = curT.submitting;

        const payload = {
            name: document.getElementById('contactName').value,
            email: document.getElementById('contactEmail').value,
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

    // 5. Automatically rewrite raw mailto links to trigger modal
    function bindMailtoLinks() {
        const links = document.querySelectorAll('a[href^="mailto:info@peopleforpeace.live"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                window.openContactModal();
            });
        });
    }

    // Run binding on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindMailtoLinks);
    } else {
        bindMailtoLinks();
    }
})();
