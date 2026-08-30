#!/usr/bin/env python3
"""
Update public HTML pages with full relational linkages:
- child.html (Mothers, family clusters, identification methods, forensic audit links)
- memorial.html, evidence.html, landing.html, about.html (Nav links to Mothers & Forensic Report)
- Synchronize public/ and build/ directories
"""

import os
import re

WEB_PUBLIC = "PFP_Platform/web/public"
WEB_BUILD = "PFP_Platform/web/build"

# 1. Update child.html
for target_dir in [WEB_PUBLIC, WEB_BUILD]:
    child_html_path = os.path.join(target_dir, "child.html")
    if not os.path.exists(child_html_path):
        continue
    with open(child_html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Bio rows replacement
    old_snippet = """            if (child.notes) {
                bioRows.push(`<div class="bio-row"><span class="bio-label">Notes</span><span class="bio-value">${child.notes}</span></div>`);
            }"""

    new_snippet = """            if (child.notes) {
                bioRows.push(`<div class="bio-row"><span class="bio-label">Notes</span><span class="bio-value">${child.notes}</span></div>`);
            }
            if (child.motherName || child.motherNameFa) {
                const mName = (currentLang === 'fa' && child.motherNameFa) ? child.motherNameFa : (child.motherName || child.motherNameFa);
                const mLabel = currentLang === 'fa' ? 'مادر' : (currentLang === 'ar' ? 'الأم' : 'Mother');
                bioRows.push(`<div class="bio-row"><span class="bio-label">${mLabel}</span><span class="bio-value"><a href="mothers.html" style="color:var(--rose);">${mName} ↗</a></span></div>`);
            }
            if (child.familyClusterName) {
                const fLabel = currentLang === 'fa' ? 'تبار خانوادگی' : (currentLang === 'ar' ? 'العائلة' : 'Family Cluster');
                bioRows.push(`<div class="bio-row"><span class="bio-label">${fLabel}</span><span class="bio-value"><a href="mothers.html" style="color:var(--gold);">${child.familyClusterName} ↗</a></span></div>`);
            }
            if (child.identificationMethod) {
                const idLabel = currentLang === 'fa' ? 'روش احراز هویت' : (currentLang === 'ar' ? 'طريقة التعرف' : 'Identification');
                const idVal = child.identificationMethod === 'unrecovered' ? (currentLang === 'fa' ? 'جاویدالاثر (بدون مزار)' : 'Unrecovered / Epicenter') : child.identificationMethod.toUpperCase();
                bioRows.push(`<div class="bio-row"><span class="bio-label">${idLabel}</span><span class="bio-value">${idVal}</span></div>`);
            }
            const srcLabel = currentLang === 'fa' ? 'گزارش مراجع' : (currentLang === 'ar' ? 'التقرير الجنائي' : 'Forensic Audit');
            const srcVal = currentLang === 'fa' ? 'پزشکی قانونی و دادستانی میناب ↗' : 'Forensic DNA & Judicial Indictment ↗';
            bioRows.push(`<div class="bio-row"><span class="bio-label">${srcLabel}</span><span class="bio-value"><a href="sources.html" style="color:var(--blue);">${srcVal}</a></span></div>`);"""

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet)

    # Footer links
    old_footer_links = """                    <div class="footer-links" style="display:flex; justify-content:center; gap:20px; margin-bottom:16px; font-size:0.9rem;">
                        <a href="landing.html">Home</a>
                        <a href="about.html">About Us</a>
                        <a href="memorial.html">Memorial</a>
                        <a href="evidence.html">Evidence</a>
                        <a href="mailto:info@peopleforpeace.live">${t.footer_contact}</a>
                    </div>"""

    new_footer_links = """                    <div class="footer-links" style="display:flex; justify-content:center; flex-wrap:wrap; gap:20px; margin-bottom:16px; font-size:0.9rem;">
                        <a href="landing.html">Home</a>
                        <a href="memorial.html">Memorial</a>
                        <a href="mothers.html">Mothers</a>
                        <a href="evidence.html">Evidence</a>
                        <a href="sources.html">Forensic Report</a>
                        <a href="data.html">Open Data</a>
                    </div>"""

    if old_footer_links in content:
        content = content.replace(old_footer_links, new_footer_links)

    with open(child_html_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ child.html updated in public/ and build/")

# 2. Update Navbars across all HTML pages
PAGES_TO_UPDATE_NAV = [
    "memorial.html", "evidence.html", "landing.html", "report.html", "about.html", "amplify.html", "initiatives.html"
]

for p in PAGES_TO_UPDATE_NAV:
    for target_dir in [WEB_PUBLIC, WEB_BUILD]:
        page_path = os.path.join(target_dir, p)
        if not os.path.exists(page_path):
            continue
        with open(page_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check for nav links patterns
        # 1. Standard pattern with Memorial & Evidence
        if '<a href="memorial.html"' in html and '<a href="mothers.html"' not in html and '<a href="/mothers.html"' not in html:
            # Add Mothers and Forensic Sources
            html = re.sub(
                r'(<a\s+href=[\'"]\/?memorial\.html[\'"][^>]*>.*?<\/a>)',
                r'\1\n            <a href="mothers.html">Mothers & Families</a>',
                html
            )
            html = re.sub(
                r'(<a\s+href=[\'"]\/?evidence\.html[\'"][^>]*>.*?<\/a>)',
                r'\1\n            <a href="sources.html">Forensic Report</a>',
                html
            )

        with open(page_path, "w", encoding="utf-8") as f:
            f.write(html)

print("✅ Navbars updated across public pages")
