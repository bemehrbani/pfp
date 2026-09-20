#!/usr/bin/env python3
"""
scripts/build_draft_package.py
-------------------------------------------------------------------------------
Automated report package compiler for People for Peace & Justice ry (PFPJ ry).
Generates date-versioned draft packages containing Word (.docx) and PDF (.pdf)
versions of:
  1. Main Report: Expert Judicial Determination & Comprehensive Legal Assessment
  2. Annex Document: Master Exhibit Dossier & Evidentiary Compendium

Applies clear "WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK" indicators:
  - Top callout banner on opening pages
  - Running headers on every page
  - Confidentiality footers with page counts
  - Diagonal semi-transparent background watermark (in PDFs)
-------------------------------------------------------------------------------
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime

# Microsoft Word generation
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# PDF generation via Playwright (System Chrome) - imported lazily in compile_html_to_pdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "Campaigns", "minab", "justiceForMinab", "docs")
DEFAULT_DRAFTS_ROOT = os.path.join(BASE_DIR, "Draft_Versions")

MAIN_REPORT_SRC = os.path.join(DOCS_DIR, "FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md")
ANNEX_DOC_SRC = os.path.join(DOCS_DIR, "MASTER_EXHIBIT_DOSSIER.md")


# -----------------------------------------------------------------------------
# XML Formatting Helpers for python-docx
# -----------------------------------------------------------------------------
def set_cell_background(cell, fill_hex):
    """Set the background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex.replace("#", ""))
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Set cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none",
                     color="CBD5E1", sz="4"):
    """Set custom borders on a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for border_name, border_style in borders.items():
        if border_style != "none":
            b_el = OxmlElement(f'w:{border_name}')
            b_el.set(qn('w:val'), border_style)
            b_el.set(qn('w:sz'), sz)
            b_el.set(qn('w:space'), '0')
            b_el.set(qn('w:color'), color.replace("#", ""))
            tcBorders.append(b_el)
        else:
            b_el = OxmlElement(f'w:{border_name}')
            b_el.set(qn('w:val'), 'nil')
            tcBorders.append(b_el)
    tcPr.append(tcBorders)

def add_callout_banner(doc, production_date, docket_no, doc_title):
    """Creates a prominent 'WORKING DRAFT' banner at the top of the Word doc."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "FEF2F2")
    set_cell_margins(cell, top=180, bottom=180, left=240, right=240)
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single",
                     color="B91C1C", sz="16")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_badge = p.add_run("WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK")
    run_badge.font.size = Pt(12)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)  # Crimson
    
    p_sub = cell.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(6)
    run_sub = p_sub.add_run("CONFIDENTIAL & PRIVILEGED · FOR PRE-FILING REVIEW & EDITORIAL CONSULTATION ONLY")
    run_sub.font.size = Pt(9)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
    
    p_desc = cell.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(0)
    p_desc.paragraph_format.space_after = Pt(6)
    run_desc = p_desc.add_run(
        f"This document constitutes an official preliminary working draft prepared by People for Peace & Justice ry (PFPJ ry) "
        f"in relation to {docket_no}. It is circulated on a strictly confidential basis to designated legal counsel, "
        f"forensic specialists, and reviewers for feedback. It must not be cited, copied, or circulated in public without prior written authorization."
    )
    run_desc.font.size = Pt(9)
    run_desc.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    p_meta = cell.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(0)
    run_meta = p_meta.add_run(
        f"Production Date: {production_date} · Status: Working Draft (Pre-Filing Review Edition) · Helsinki, Finland"
    )
    run_meta.font.size = Pt(8)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Spacer after banner
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(12)


# -----------------------------------------------------------------------------
# Inline Text Formatter for python-docx
# -----------------------------------------------------------------------------
def tokenize_inline(text):
    """Tokenize markdown inline formatting."""
    pattern = re.compile(
        r'(\*\*\*(.*?)\*\*\*|'
        r'\*\*(.*?)\*\*|'
        r'\*(.*?)\*|'
        r'`(.*?)`|'
        r'\[(.*?)\]\((.*?)\))'
    )
    tokens = []
    last_end = 0
    for m in pattern.finditer(text):
        start, end = m.span()
        if start > last_end:
            tokens.append(('plain', text[last_end:start]))
        if m.group(2) is not None:
            tokens.append(('bold_italic', m.group(2)))
        elif m.group(3) is not None:
            tokens.append(('bold', m.group(3)))
        elif m.group(4) is not None:
            tokens.append(('italic', m.group(4)))
        elif m.group(5) is not None:
            tokens.append(('code', m.group(5)))
        elif m.group(6) is not None:
            tokens.append(('link', m.group(6), m.group(7)))
        last_end = end
    if last_end < len(text):
        tokens.append(('plain', text[last_end:]))
    return tokens

def add_formatted_text_to_paragraph(p, text, base_font_size=10, base_color=None,
                                   is_quote=False):
    """Applies tokens to a Word paragraph with styling."""
    tokens = tokenize_inline(text)
    for tok in tokens:
        kind = tok[0]
        content = tok[1]
        run = p.add_run(content)
        run.font.size = Pt(base_font_size)
        run.font.name = 'Calibri'
        
        if base_color:
            run.font.color.rgb = base_color
        else:
            run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
            
        if kind == 'bold':
            run.font.bold = True
        elif kind == 'italic':
            run.font.italic = True
        elif kind == 'bold_italic':
            run.font.bold = True
            run.font.italic = True
        elif kind == 'code':
            run.font.name = 'Consolas'
            run.font.size = Pt(base_font_size - 0.5)
            run.font.color.rgb = RGBColor(0x83, 0x18, 0x43)  # Dark pink/magenta
        elif kind == 'link':
            run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)  # Blue
            run.font.underline = True
            
        if is_quote:
            run.font.italic = True


# -----------------------------------------------------------------------------
# Markdown to DOCX Compiler
# -----------------------------------------------------------------------------
def compile_markdown_to_docx(md_path, docx_path, production_date, doc_type="main"):
    """Reads Markdown and compiles into a fully styled Microsoft Word document."""
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = docx.Document()
    
    # Page Margins (0.75 in = 54 pt = 1080 dxa)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
        # Header setup
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK · NOT FOR PUBLIC CITATION")
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(8.5)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)  # Crimson
        
        # Footer setup
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        docket_tag = "PFPJ-2026-IR-001" if doc_type == "main" else "PFPJ-2026-IR-001 / EXHIBIT COMPENDIUM"
        frun = fp.add_run(f"CONFIDENTIAL · PEOPLE FOR PEACE & JUSTICE RY · DOCKET {docket_tag} · DRAFT DATE: {production_date}")
        frun.font.name = 'Calibri'
        frun.font.size = Pt(8)
        frun.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Set base font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    docket_num = "DOCKET NO.: PFPJ-2026-IR-001" if doc_type == "main" else "DOCKET NO.: PFPJ-2026-IR-001 / EXHIBIT COMPENDIUM"
    doc_title = "Minab Factual Determination & Legal Assessment" if doc_type == "main" else "Master Exhibit Dossier & Evidentiary Compendium"

    # Add Prominent Top Callout Banner
    add_callout_banner(doc, production_date, docket_num, doc_title)

    # Parsing state
    i = 0
    n = len(lines)
    table_lines = []

    def flush_table(lines_to_parse):
        if not lines_to_parse:
            return
        parsed_rows = []
        for line in lines_to_parse:
            stripped = line.strip()
            if stripped.startswith("|"):
                stripped = stripped[1:]
            if stripped.endswith("|"):
                stripped = stripped[:-1]
            cols = [c.strip() for c in stripped.split("|")]
            if all(re.match(r'^:?-+:?$', c) for c in cols):
                continue
            parsed_rows.append(cols)

        if not parsed_rows:
            return

        num_cols = max(len(r) for r in parsed_rows)
        for r in parsed_rows:
            while len(r) < num_cols:
                r.append("")

        tbl = doc.add_table(rows=len(parsed_rows), cols=num_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        for row_idx, row_data in enumerate(parsed_rows):
            is_header = (row_idx == 0)
            for col_idx, cell_value in enumerate(row_data):
                cell = tbl.cell(row_idx, col_idx)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                
                if is_header:
                    set_cell_background(cell, "E2E8F0")
                    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                    set_cell_borders(cell, top="single", bottom="single", left="none", right="none", color="94A3B8", sz="8")
                    add_formatted_text_to_paragraph(p, f"**{cell_value}**", base_font_size=9, base_color=RGBColor(0x0F, 0x17, 0x2A))
                else:
                    bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                    set_cell_background(cell, bg)
                    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                    set_cell_borders(cell, top="none", bottom="single", left="none", right="none", color="E2E8F0", sz="4")
                    add_formatted_text_to_paragraph(p, cell_value, base_font_size=8.5)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(6)

    while i < n:
        raw_line = lines[i]
        line = raw_line.rstrip('\r\n')
        stripped = line.strip()

        # Handle Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(stripped)
            i += 1
            continue
        elif table_lines:
            flush_table(table_lines)
            table_lines = []

        # Skip anchor tags
        if stripped.startswith("<a id=") or stripped.startswith("</a>"):
            i += 1
            continue

        # Blank lines
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("—" * 32)
            run.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            i += 1
            continue

        # Headings
        if stripped.startswith("# "):
            title_text = stripped[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(title_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)  # Navy
            i += 1
            continue
        elif stripped.startswith("## "):
            h2_text = stripped[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(h2_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
            i += 1
            continue
        elif stripped.startswith("### "):
            h3_text = stripped[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(h3_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            i += 1
            continue
        elif stripped.startswith("#### "):
            h4_text = stripped[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(h4_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.italic = True
            run.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
            i += 1
            continue

        # Blockquotes
        if stripped.startswith("> "):
            quote_text = stripped[2:].strip()
            while i + 1 < n and lines[i + 1].strip().startswith("> "):
                i += 1
                quote_text += " " + lines[i].strip()[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            add_formatted_text_to_paragraph(p, quote_text, base_font_size=9.5,
                                           base_color=RGBColor(0x33, 0x41, 0x55), is_quote=True)
            i += 1
            continue

        # Bullet lists (* or -)
        bullet_match = re.match(r'^(\s*)[*\-]\s+(.*)$', line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            bullet_text = bullet_match.group(2)
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            if indent >= 2:
                p.paragraph_format.left_indent = Inches(0.4)
            add_formatted_text_to_paragraph(p, bullet_text, base_font_size=9.5)
            i += 1
            continue

        # Numbered lists (e.g. "1. ")
        num_match = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if num_match:
            num_str = num_match.group(2)
            num_text = num_match.group(3)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            run_num = p.add_run(f"{num_str}. ")
            run_num.font.bold = True
            run_num.font.size = Pt(9.5)
            add_formatted_text_to_paragraph(p, num_text, base_font_size=9.5)
            i += 1
            continue

        # Regular Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        add_formatted_text_to_paragraph(p, stripped, base_font_size=10)
        i += 1

    if table_lines:
        flush_table(table_lines)

    doc.save(docx_path)
    print(f"  [DOCX OK] Generated {os.path.basename(docx_path)} ({os.path.getsize(docx_path):,} bytes)")


# -----------------------------------------------------------------------------
# Markdown to HTML Converter (for PDF Rendering)
# -----------------------------------------------------------------------------
def markdown_to_html(md_path, production_date, doc_type="main"):
    """Converts Markdown to clean, print-optimized HTML with working draft badges."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    docket_tag = "DOCKET NO.: PFPJ-2026-IR-001" if doc_type == "main" else "DOCKET NO.: PFPJ-2026-IR-001 / EXHIBIT COMPENDIUM"
    doc_title = "EXPERT JUDICIAL DETERMINATION & COMPREHENSIVE LEGAL ASSESSMENT" if doc_type == "main" else "MASTER EXHIBIT DOSSIER & EVIDENTIARY COMPENDIUM"

    lines = text.splitlines()
    html_parts = []
    in_table = False
    table_rows = []

    def flush_html_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return ""
        out = ['<table class="report-table">']
        for r_idx, r in enumerate(table_rows):
            stripped = r.strip()
            if stripped.startswith("|"):
                stripped = stripped[1:]
            if stripped.endswith("|"):
                stripped = stripped[:-1]
            cols = [c.strip() for c in stripped.split("|")]
            if all(re.match(r'^:?-+:?$', c) for c in cols):
                continue
            tag = "th" if r_idx == 0 else "td"
            out.append("  <tr>")
            for c in cols:
                c_formatted = format_inline_html(c)
                out.append(f"    <{tag}>{c_formatted}</{tag}>")
            out.append("  </tr>")
        out.append("</table>")
        table_rows = []
        in_table = False
        return "\n".join(out)

    def format_inline_html(s):
        s = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', s)
        s = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\*(.*?)\*', r'<em>\1</em>', s)
        s = re.sub(r'`(.*?)`', r'<code>\1</code>', s)
        return s

    for line in lines:
        stripped = line.strip()

        # Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            html_parts.append(flush_html_table())

        if not stripped:
            continue

        if stripped.startswith("<a id=") or stripped.startswith("</a>"):
            continue

        if stripped in ("---", "***", "___"):
            html_parts.append('<hr class="divider" />')
            continue

        if stripped.startswith("# "):
            html_parts.append(f'<h1 class="h1-title">{format_inline_html(stripped[2:])}</h1>')
            continue
        elif stripped.startswith("## "):
            html_parts.append(f'<h2 class="h2-heading">{format_inline_html(stripped[3:])}</h2>')
            continue
        elif stripped.startswith("### "):
            html_parts.append(f'<h3 class="h3-heading">{format_inline_html(stripped[4:])}</h3>')
            continue
        elif stripped.startswith("#### "):
            html_parts.append(f'<h4 class="h4-heading">{format_inline_html(stripped[5:])}</h4>')
            continue

        if stripped.startswith("> "):
            html_parts.append(f'<blockquote class="legal-quote">{format_inline_html(stripped[2:])}</blockquote>')
            continue

        bullet_match = re.match(r'^(\s*)[*\-]\s+(.*)$', line)
        if bullet_match:
            html_parts.append(f'<li class="bullet-item">{format_inline_html(bullet_match.group(2))}</li>')
            continue

        num_match = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if num_match:
            html_parts.append(f'<div class="numbered-item"><strong>{num_match.group(2)}.</strong> {format_inline_html(num_match.group(3))}</div>')
            continue

        html_parts.append(f'<p class="body-p">{format_inline_html(stripped)}</p>')

    if in_table:
        html_parts.append(flush_html_table())

    content_html = "\n".join(html_parts)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{doc_title} — Working Draft ({production_date})</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 22mm 16mm 22mm 16mm;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a;
      line-height: 1.55;
      font-size: 10pt;
      margin: 0;
      padding: 0;
      background: #ffffff;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    /* Diagonal Watermark for Working Draft */
    .watermark-overlay {{
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-35deg);
      font-size: 32pt;
      font-weight: 900;
      color: rgba(185, 28, 28, 0.08);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      white-space: nowrap;
      pointer-events: none;
      z-index: 9999;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Prominent Callout Banner */
    .draft-banner {{
      background: #fef2f2;
      border: 1.5px solid #b91c1c;
      border-left: 6px solid #b91c1c;
      padding: 14px 18px;
      border-radius: 6px;
      margin-bottom: 22px;
      page-break-inside: avoid;
    }}
    .draft-banner-title {{
      color: #991b1b;
      font-size: 11pt;
      font-weight: 800;
      letter-spacing: 0.5px;
      margin: 0 0 4px 0;
      text-transform: uppercase;
    }}
    .draft-banner-sub {{
      color: #b91c1c;
      font-size: 8pt;
      font-weight: 700;
      margin: 0 0 6px 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .draft-banner-text {{
      color: #334155;
      font-size: 8.5pt;
      line-height: 1.45;
      margin: 0 0 8px 0;
    }}
    .draft-banner-meta {{
      color: #64748b;
      font-size: 7.5pt;
      font-family: "Courier New", Courier, monospace;
      border-top: 1px dashed #fca5a5;
      padding-top: 6px;
      margin: 0;
    }}

    /* Headings */
    .h1-title {{
      font-size: 14pt;
      font-weight: 800;
      color: #0f172a;
      margin: 18px 0 6px 0;
      line-height: 1.25;
      page-break-after: avoid;
    }}
    .h2-heading {{
      font-size: 12pt;
      font-weight: 700;
      color: #1e293b;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 4px;
      margin: 16px 0 6px 0;
      page-break-after: avoid;
    }}
    .h3-heading {{
      font-size: 10.5pt;
      font-weight: 700;
      color: #334155;
      margin: 12px 0 4px 0;
      page-break-after: avoid;
    }}
    .h4-heading {{
      font-size: 9.5pt;
      font-weight: 600;
      color: #475569;
      margin: 10px 0 3px 0;
      page-break-after: avoid;
    }}

    .divider {{
      border: 0;
      border-top: 1px solid #cbd5e1;
      margin: 12px 0;
    }}

    .body-p {{
      margin: 0 0 8px 0;
      font-size: 9.5pt;
      color: #1e293b;
      text-align: justify;
    }}

    .legal-quote {{
      background: #f8fafc;
      border-left: 3px solid #94a3b8;
      padding: 6px 14px;
      margin: 6px 0 10px 0;
      font-style: italic;
      color: #334155;
      font-size: 9pt;
      page-break-inside: avoid;
    }}

    .bullet-item {{
      margin: 0 0 4px 18px;
      font-size: 9.5pt;
      color: #1e293b;
    }}

    .numbered-item {{
      margin: 0 0 6px 6px;
      font-size: 9.5pt;
      color: #1e293b;
    }}

    /* Data Tables */
    .report-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0 16px 0;
      font-size: 8.5pt;
      page-break-inside: avoid;
    }}
    .report-table th {{
      background: #e2e8f0;
      color: #0f172a;
      font-weight: 700;
      text-align: left;
      padding: 6px 8px;
      border: 1px solid #cbd5e1;
    }}
    .report-table td {{
      padding: 6px 8px;
      border: 1px solid #e2e8f0;
      color: #334155;
      vertical-align: top;
    }}
    .report-table tr:nth-child(even) td {{
      background: #f8fafc;
    }}

    code {{
      font-family: "Courier New", Courier, monospace;
      font-size: 8.5pt;
      background: #f1f5f9;
      color: #831843;
      padding: 1px 4px;
      border-radius: 3px;
    }}
    a {{
      color: #2563eb;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="watermark-overlay">WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK</div>

  <div class="draft-banner">
    <div class="draft-banner-title">⚠️  WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK</div>
    <div class="draft-banner-sub">CONFIDENTIAL & PRIVILEGED · FOR PRE-FILING REVIEW & EDITORIAL CONSULTATION ONLY</div>
    <p class="draft-banner-text">
      This document constitutes an official preliminary working draft prepared by <strong>People for Peace & Justice ry (PFPJ ry)</strong>
      in relation to <strong>{docket_tag}</strong>. It is circulated on a strictly confidential basis to designated legal counsel,
      forensic specialists, and reviewers for feedback. It must not be cited, copied, or circulated in public without prior written authorization.
    </p>
    <div class="draft-banner-meta">
      Production Date: {production_date} · Status: Working Draft (Pre-Filing Review Edition) · Helsinki, Finland
    </div>
  </div>

  {content_html}
</body>
</html>
"""
    return full_html


# -----------------------------------------------------------------------------
# PDF Compiler using Chromium via Playwright
# -----------------------------------------------------------------------------
def compile_html_to_pdf(html_content, pdf_path, production_date, doc_type="main"):
    """Compiles HTML into an A4 PDF with running headers, footers, and draft tags."""
    docket_tag = "DOCKET PFPJ-2026-IR-001" if doc_type == "main" else "DOCKET PFPJ-2026-IR-001 / EXHIBIT COMPENDIUM"
    
    header_template = """
    <div style="font-size: 7.5pt; font-family: -apple-system, BlinkMacSystemFont, sans-serif; color: #b91c1c; font-weight: 700; width: 100%; text-align: center; border-bottom: 1px solid #fecaca; padding-bottom: 3px; margin: 0 16mm;">
      WORKING DRAFT — PRIVATELY SHARED FOR FEEDBACK · STRICTLY CONFIDENTIAL
    </div>
    """
    
    footer_template = f"""
    <div style="font-size: 7.5pt; font-family: -apple-system, BlinkMacSystemFont, sans-serif; color: #64748b; width: 100%; display: flex; justify-content: space-between; padding: 3px 16mm 0 16mm; border-top: 1px solid #e2e8f0;">
      <span>CONFIDENTIAL · PEOPLE FOR PEACE & JUSTICE RY · {docket_tag} · {production_date}</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    """

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="load")
        page.pdf(
            path=pdf_path,
            format="A4",
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={"top": "22mm", "bottom": "22mm", "left": "16mm", "right": "16mm"},
            print_background=True
        )
        browser.close()

    print(f"  [PDF OK] Generated {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path):,} bytes)")


# -----------------------------------------------------------------------------
# SHA-256 Hash Helper
# -----------------------------------------------------------------------------
def calculate_sha256(filepath):
    """Computes the SHA-256 cryptographic checksum of a file."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


# -----------------------------------------------------------------------------
# Package Manifest & README Generator
# -----------------------------------------------------------------------------
def generate_manifest(version_dir, production_date, doc_records):
    """Generates a PACKAGE_MANIFEST.md file within the version directory."""
    manifest_path = os.path.join(version_dir, "PACKAGE_MANIFEST.md")
    
    lines = [
        f"# REPORT DRAFT PACKAGE MANIFEST: {production_date}",
        f"> **Issuing Authority:** People for Peace & Justice ry (PFPJ ry) — Helsinki, Finland (Business ID: `3616815-5`)  ",
        f"> **Production Date:** `{production_date}`  ",
        f"> **Classification:** **CONFIDENTIAL WORKING DRAFT / PRIVATELY SHARED FOR FEEDBACK**  ",
        f"> **Governing Dockets:** `PFPJ-2026-IR-001` (Main Report) & `PFPJ-2026-IR-001 / EXHIBIT COMPENDIUM` (Annex Dossier)  ",
        "",
        "---",
        "",
        "## 1. Document Inventory & Cryptographic Checksums",
        "",
        "| Document Role | Format | File Name | Size (KB) | SHA-256 Checksum |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for role, fmt, filename, size_bytes, sha_hash in doc_records:
        size_kb = f"{size_bytes / 1024:.1f}"
        lines.append(f"| **{role}** | `{fmt}` | `{filename}` | {size_kb} KB | `{sha_hash}` |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Working Draft & Confidentiality Directive",
        "",
        "All documents in this package have been compiled as **preliminary working drafts** intended exclusively for:",
        "1. **Expert Peer Review:** Review by international humanitarian law (IHL) scholars, human rights practitioners, and forensic analysts.",
        "2. **Evidence Cross-Checking:** Verification of coordinates, munitions serial numbers, casualty identities, and jurisdictional precedents.",
        "3. **Editorial & Translation Feedback:** Pre-submission proofing and editorial refinement.",
        "",
        "> [!WARNING]",
        "> **RESTRICTION ON CITATION AND DISSEMINATION:**  ",
        "> This package is **privately shared for feedback only**. It is not an official public release. None of the included materials may be publicly distributed, leaked, quoted, or cited in legal submissions or media publications without explicit prior written consent from People for Peace & Justice ry.",
        "",
        "---",
        "",
        "## 3. Contact & Submission of Feedback",
        "",
        "* **Submitting Body:** People for Peace & Justice ry (PFPJ ry)",
        "* **Helsinki Headquarters:** `legal@peopleforpeace.live` / `contact@peopleforpeace.live`",
        f"* **Package Generation Timestamp:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        ""
    ])

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [MANIFEST OK] Generated {os.path.basename(manifest_path)}")


def generate_drafts_readme(drafts_root):
    """Generates or updates the root README.md for the Draft_Versions folder."""
    readme_path = os.path.join(drafts_root, "README.md")
    content = """# Draft Versions Directory & Production Archive
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
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [README OK] Generated {os.path.basename(readme_path)}")


# -----------------------------------------------------------------------------
# Main Execution Pipeline
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Compile report package draft versions.")
    parser.add_argument("--date", default=None, help="Production date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--version-tag", default=None, help="Version tag (e.g. v2). Default: None.")
    parser.add_argument("--output-dir", default=None, help="Root drafts folder. Default: Draft_Versions.")
    parser.add_argument("--docx-only", action="store_true", help="Compile Word DOCX documents only (skip PDF).")
    args = parser.parse_args()

    production_date = args.date or datetime.now().strftime("%Y-%m-%d")
    drafts_root = args.output_dir or DEFAULT_DRAFTS_ROOT
    version_folder = f"{production_date}_{args.version_tag}" if args.version_tag else production_date
    version_dir = os.path.join(drafts_root, version_folder)

    os.makedirs(version_dir, exist_ok=True)

    tag_str = f" ({args.version_tag})" if args.version_tag else ""
    tag_file = f"_{args.version_tag}" if args.version_tag else ""

    print("=" * 70)
    print(f"PFPJ ry Report Package Compiler: Draft Version {production_date}{tag_str}")
    print(f"Target Version Directory: {version_dir}")
    print("=" * 70)

    for src in (MAIN_REPORT_SRC, ANNEX_DOC_SRC):
        if not os.path.exists(src):
            print(f"Error: Source document not found at {src}", file=sys.stderr)
            sys.exit(1)

    # 1. Main Report Filenames
    main_docx = os.path.join(version_dir, f"PFPJ_Minab_Factual_Determination_Main_Report_{production_date}{tag_file}_Draft.docx")
    main_pdf = os.path.join(version_dir, f"PFPJ_Minab_Factual_Determination_Main_Report_{production_date}{tag_file}_Draft.pdf")

    # 2. Annex Document Filenames
    annex_docx = os.path.join(version_dir, f"PFPJ_Minab_Master_Exhibit_Dossier_Annex_{production_date}{tag_file}_Draft.docx")
    annex_pdf = os.path.join(version_dir, f"PFPJ_Minab_Master_Exhibit_Dossier_Annex_{production_date}{tag_file}_Draft.pdf")

    if args.docx_only:
        # Step 1: Compile Main Report DOCX
        print("\n[1/2] Compiling Main Report (Word Document)...")
        compile_markdown_to_docx(MAIN_REPORT_SRC, main_docx, production_date, doc_type="main")

        # Step 2: Compile Annex Document DOCX
        print("\n[2/2] Compiling Annex Document (Word Document)...")
        compile_markdown_to_docx(ANNEX_DOC_SRC, annex_docx, production_date, doc_type="annex")

        # Step 3: Compute Hashes and Generate Manifest
        print("\n[3/3] Generating Package Manifest & Verification Hashes...")
        doc_records = [
            ("Main Report", "DOCX", os.path.basename(main_docx), os.path.getsize(main_docx), calculate_sha256(main_docx)),
            ("Annex Document", "DOCX", os.path.basename(annex_docx), os.path.getsize(annex_docx), calculate_sha256(annex_docx)),
        ]
        generate_manifest(version_dir, production_date, doc_records)
        generate_drafts_readme(drafts_root)
    else:
        # Step 1: Compile Main Report DOCX
        print("\n[1/4] Compiling Main Report (Word Document)...")
        compile_markdown_to_docx(MAIN_REPORT_SRC, main_docx, production_date, doc_type="main")

        # Step 2: Compile Main Report PDF
        print("\n[2/4] Compiling Main Report (PDF Document)...")
        main_html = markdown_to_html(MAIN_REPORT_SRC, production_date, doc_type="main")
        compile_html_to_pdf(main_html, main_pdf, production_date, doc_type="main")

        # Step 3: Compile Annex Document DOCX
        print("\n[3/4] Compiling Annex Document (Word Document)...")
        compile_markdown_to_docx(ANNEX_DOC_SRC, annex_docx, production_date, doc_type="annex")

        # Step 4: Compile Annex Document PDF
        print("\n[4/4] Compiling Annex Document (PDF Document)...")
        annex_html = markdown_to_html(ANNEX_DOC_SRC, production_date, doc_type="annex")
        compile_html_to_pdf(annex_html, annex_pdf, production_date, doc_type="annex")

        # Step 5: Compute Hashes and Generate Manifest
        print("\n[5/5] Generating Package Manifest & Verification Hashes...")
        doc_records = [
            ("Main Report", "DOCX", os.path.basename(main_docx), os.path.getsize(main_docx), calculate_sha256(main_docx)),
            ("Main Report", "PDF", os.path.basename(main_pdf), os.path.getsize(main_pdf), calculate_sha256(main_pdf)),
            ("Annex Document", "DOCX", os.path.basename(annex_docx), os.path.getsize(annex_docx), calculate_sha256(annex_docx)),
            ("Annex Document", "PDF", os.path.basename(annex_pdf), os.path.getsize(annex_pdf), calculate_sha256(annex_pdf)),
        ]
        generate_manifest(version_dir, production_date, doc_records)
        generate_drafts_readme(drafts_root)

    # Also place a convenient copy in the root workspace
    root_copy = os.path.join(BASE_DIR, f"PFPJ_Minab_Factual_Determination_Main_Report_Updated_{production_date}.docx")
    import shutil
    shutil.copy2(main_docx, root_copy)
    print(f"\n  [ROOT COPY OK] Placed convenient copy at: {root_copy}")

    print("\n" + "=" * 70)
    print(f"SUCCESS: Report package successfully created in {version_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
