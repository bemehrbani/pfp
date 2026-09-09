import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_styled_doc(title):
    doc = docx.Document()
    
    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Style default
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Header
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_badge = p_header.add_run("MAKAN RY · REKISTERÖITY YHDISTYS · FINLAND")
    run_badge.font.size = Pt(9)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(0x94, 0x73, 0x1E)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(title)
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_line = p_line.add_run("―" * 40)
    run_line.font.color.rgb = RGBColor(0xC9, 0xA8, 0x4C)

    return doc

# 1. Perustamiskirja (Founding Charter)
def build_perustamiskirja():
    doc = create_styled_doc("YHDISTYKSEN PERUSTAMISKIRJA\nCHARTER OF FOUNDATION / منشور تأسیس انجمن ماکان")

    doc.add_paragraph("Tämä virallinen perustamisasiakirja laaditaan yhdistystä perustettaessa Suomen yhdistyslain (503/1989 5 §) mukaisesti. Asiakirjan allekirjoittaa vähintään kolme (3) perustajajäsentä.")
    
    p = doc.add_paragraph()
    run = p.add_run("PÄÄTÖS YHDISTYKSEN PERUSTAMISESTA / STATEMENT OF FOUNDATION:")
    run.bold = True
    p2 = doc.add_paragraph("Me allekirjoittaneet olemme perustaneet Makan ry -nimisen yhdistyksen, liittyneet siihen jäseniksi ja hyväksyneet sille liitteenä olevat säännöt.")
    p2.runs[0].italic = True

    p_fa = doc.add_paragraph("ما امضاکنندگان زیر، انجمنی با نام «انجمن ماکان» (Makan ry) را به عنوان نهادی غیرانتفاعی و مستقل در کشور فنلاند تأسیس نموده، به عضویت آن درآمده و اساسنامه ضمیمه را تصویب نمودیم.")
    p_fa.runs[0].font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # Board Section
    h_board = doc.add_heading("1. HALLITUS / BOARD OF DIRECTORS / هیئت مدیره", level=2)
    h_board.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)

    doc.add_paragraph("Yhdistyksen hallitukseen on valittu seuraavat henkilöt (huom. puheenjohtajan kotikunta on oltava Suomessa):")

    # Table for board members with address
    table = doc.add_table(rows=4, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Rooli / Role", "Koko nimi / Full Name", "Henkilötunnus / Synt.aika", "Kotiosoite ja postinumero (Full Address)", "Kotikunta (City)"]
    
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, 120, 120, 150, 150)

    rows_data = [
        ("Puheenjohtaja\n(Chairperson)", "[Täytä nimi]", "[Henkilötunnus]", "[Katuosoite, postinumero ja kaupunki]", "[Kotikunta Suomessa]"),
        ("Hallituksen jäsen\n(Board Member 1)", "[Täytä nimi]", "[Henkilötunnus / Synt.aika]", "[Katuosoite, postinumero ja kaupunki]", "[Kotikunta]"),
        ("Hallituksen jäsen\n(Board Member 2)", "[Täytä nimi]", "[Henkilötunnus / Synt.aika]", "[Katuosoite, postinumero ja kaupunki]", "[Kotikunta]")
    ]

    for row_idx, data in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_margins(cell, 100, 100, 120, 120)

    # Operations Inspectors
    h_insp = doc.add_heading("2. TOIMINNANTARKASTAJAT / OPERATIONS INSPECTORS / بازرسان مالی و عملکرد", level=2)
    h_insp.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)

    table_insp = doc.add_table(rows=3, cols=4)
    table_insp.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_insp = ["Tehtävä / Role", "Koko nimi / Full Name", "Yhteystiedot (Email / Puh)", "Kotiosoite ja kotikunta"]
    for i, h in enumerate(headers_insp):
        cell = table_insp.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, 120, 120, 150, 150)

    insp_data = [
        ("Toiminnantarkastaja\n(Operations Inspector)", "[Nimi / نام بازرس اصلی]", "[Sähköposti / Puhelin]", "[Osoite ja kotikunta]"),
        ("Varatoiminnantarkastaja\n(Deputy Inspector)", "[Nimi / نام بازرس علی‌البدل]", "[Sähköposti / Puhelin]", "[Osoite ja kotikunta]")
    ]
    for row_idx, data in enumerate(insp_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_insp.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_margins(cell, 100, 100, 120, 120)

    # Signatures
    h_sig = doc.add_heading("3. PÄIVÄYS JA ALLEKIRJOITUKSET / SIGNATURES / تاریخ و امضاها", level=2)
    h_sig.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)

    doc.add_paragraph("Aika ja paikka (Date and place / تاریخ و محل): Helsinki, _____ / _____ / 2026")
    doc.add_paragraph("Perustajajäsenten allekirjoitukset ja nimenselvennykset (vähintään 3 perustajaa):")

    sig_table = doc.add_table(rows=4, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_headers = ["Perustaja 1 (Chairperson)", "Perustaja 2 (Board Member)", "Perustaja 3 (Board Member)"]
    for i, h in enumerate(sig_headers):
        cell = sig_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "F3F4F6")

    for i in range(3):
        cell_sig = sig_table.cell(1, i)
        cell_sig.text = "\n\n_______________________\n(Allekirjoitus / Signature)"
        cell_sig.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        cell_name = sig_table.cell(2, i)
        cell_name.text = "Nimi: __________________\nHenkilötunnus: _________"
        
        cell_addr = sig_table.cell(3, i)
        cell_addr.text = "Osoite: ________________\nKotikunta: _____________"

    return doc

# 2. Perustavan kokouksen pöytäkirja (Minutes)
def build_poytakirja():
    doc = create_styled_doc("PERUSTAVAN KOKOUKSEN PÖYTÄKIRJA\nMINUTES OF THE CONSTITUTIVE MEETING / صورت‌جلسه مجمع عمومی مؤسس")

    doc.add_paragraph("Yhdistys: Makan ry\nKokous: Perustava kokous (Constitutive Meeting / مجمع عمومی مؤسس)\nAika: _____._____.2026 klo ____:____\nPaikka: Helsinki / Etäyhteys\nLäsnä: Perustajajäsenet (listattu alla)")

    sections = [
        ("1. Kokouksen avaus", "Kokous avattiin klo ____:____. Todettiin kokouksen tarkoitus: Makan ry -nimisen itsenäisen ja voittoa tavoittelemattoman rauhanjärjestön perustaminen."),
        ("2. Järjestäytyminen", "Kokouksen puheenjohtajaksi valittiin: ________________________\nSihteeriksi valittiin: ________________________\nPöytäkirjantarkastajiksi ja ääntenlaskijoiksi valittiin: ________________________ ja ________________________"),
        ("3. Laillisuus ja päätösvaltaisuus", "Todettiin kokous laillisesti koollekutsutuksi ja päätösvaltaiseksi."),
        ("4. Työjärjestyksen hyväksyminen", "Hyväksyttiin kokouksen esityslista työjärjestykseksi."),
        ("5. Yhdistyksen perustaminen ja nimen päättäminen", "Päätettiin perustaa yhdistys nimeltä Makan ry. Allekirjoitettiin perustamiskirja."),
        ("6. Sääntöjen hyväksyminen", "Käytiin läpi yhdistyksen sääntöluonnos (§ 1–10). Säännöt hyväksyttiin yksimielisesti liitteen mukaisina."),
        ("7. Jäsenmaksun suuruudesta päättäminen", "Päätettiin, että varsinaisen jäsenen jäsenmaksu on 5 euroa kuukaudessa (tai 60 euroa vuodessa). Kannatusjäsenmaksuksi vahvistettiin vähintään 20 euroa vuodessa yksityishenkilöille ja 100 euroa vuodessa oikeushenkilöille."),
        ("8. Hallituksen valinta", "Yhdistyksen hallitukseen valittiin:\n- Puheenjohtaja: ________________________ (kotikunta: ________________)\n- Varsinainen jäsen: ________________________ (kotikunta: ________________)\n- Varsinainen jäsen: ________________________ (kotikunta: ________________)"),
        ("9. Toiminnantarkastajien valinta", "Valittiin tilikaudelle 2026:\n- Toiminnantarkastaja: ________________________\n- Varatoiminnantarkastaja: ________________________"),
        ("10. Yhdistyksen rekisteröinti (PRH)", "Päätettiin rekisteröidä yhdistys Patentti- ja rekisterihallituksen yhdistysrekisteriin. Valtuutettiin hallituksen puheenjohtaja tekemään perusilmoitus."),
        ("11. Kokouksen päättäminen", "Puheenjohtaja päätti kokouksen klo ____:____.")
    ]

    for title, body in sections:
        h = doc.add_heading(title, level=2)
        h.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)
        doc.add_paragraph(body)

    doc.add_paragraph("\nPöytäkirjan vakuudeksi:")
    p_sig = doc.add_paragraph("_____________________________\t\t_____________________________\nPuheenjohtaja\t\t\t\tSihteeri")
    
    doc.add_paragraph("\nPöytäkirjan tarkastus:")
    doc.add_paragraph("Olemme tarkastaneet pöytäkirjan ja todenneet sen vastaavan kokouksen kulkua.")
    doc.add_paragraph("_____________________________\t\t_____________________________\nPöytäkirjantarkastaja 1\t\t\tPöytäkirjantarkastaja 2")

    return doc

# 3. Official PRH Rules
def build_saannot_prh():
    doc = create_styled_doc("MAKAN RY — SÄÄNNÖT\nOFFICIAL FINNISH ASSOCIATION RULES (PRH)")

    doc.add_paragraph("Hyväksytty perustavassa kokouksessa __.__.2026")

    rules = [
        ("§ 1 — Nimi ja kotipaikka", "Yhdistyksen nimi on Makan ry.\nYhdistyksen kotipaikka on Helsinki."),
        ("§ 2 — Tarkoitus ja toimintamuodot", """Yhdistys on itsenäinen, voittoa tavoittelematon, humanitaarinen ja yleishyödyllinen kansalaisjärjestö, joka on riippumaton puoluepolitiikasta, ideologioista ja uskonnoista.

Yhdistyksen tarkoituksena on:
1. Edistää rauhaa, kansojen itsemääräämisoikeutta, suvereniteettia ja kansainvälistä oikeudenmukaisuutta Yhdistyneiden kansakuntien (YK) peruskirjan periaatteiden mukaisesti.
2. Vastustaa sotia, aseellista väkivaltaa, sotilaallista aggressiota, miehitystä sekä ulkovaltojen kolonialistista ja uuskolonialistista sekaantumista kansojen ja valtioiden sisäisiin asioihin, erityisesti Länsi-Aasiassa ja Iranissa.
3. Vastustaa, tutkia ja tuoda julki yksipuolisia ja laittomia talouspakotteita, jotka vaarantavat siviiliväestön toimeentulon, terveydenhuollon, lääketurvan ja perusihmisoikeudet.
4. Lisätä yleistä ja yhteiskunnallista tietoisuutta sotien, ulkopuolisten interventioiden ja taloussaartojen inhimillisistä ja yhteiskunnallisista tuhoista.
5. Vahvistaa yhteisöllisyyttä, kulttuurienvälistä ymmärrystä, aktiivista kansalaisuutta ja vuoropuhelua suomalaisten, Suomessa asuvien iranilaisten sekä muiden maahanmuuttajaryhmien välillä.

Tarkoituksensa toteuttamiseksi yhdistys:
- Järjestää avoimia yleisötilaisuuksia, seminaareja, paneelikeskusteluja, työpajoja, luentosarjoja ja kulttuuri- sekä rauhantapahtumia.
- Tuottaa, kääntää ja jakaa tiedotteita, analyysejä, lausuntoja ja julkaisuja suomen, persian ja englannin kielillä.
- Harjoittaa asiantuntevaa ja rakentavaa tiedotus- ja valistustoimintaa kansalaisten, tiedotusvälineiden ja päättäjien keskuudessa.
- Tekee yhteistyötä muiden kotimaisten ja kansainvälisten rauhan-, ihmisoikeus- ja kansalaisjärjestöjen sekä tutkimuslaitosten kanssa, jotka jakavat yhdistyksen arvot.
- Käyttää muita vastaavia laillisia ja rauhanomaisia toimintamuotoja, jotka edistävät yhdistyksen tavoitteita.

Toimintansa tukemiseksi yhdistys voi kantaa jäsenmaksuja, ottaa vastaan lahjoituksia ja avustuksia, järjestää rahankeräyksiä asianmukaisella luvalla sekä omistaa tarpeellista omaisuutta. Yhdistys ei harjoita kaupallista elinkeinotoimintaa."""),
        ("§ 3 — Jäsenet", "Varsinaiseksi jäseneksi voi liittyä jokainen luonnollinen henkilö, joka hyväksyy yhdistyksen tarkoituksen ja tukee kansojen itsenäisyyttä. Kannatusjäseneksi voidaan hyväksyä henkilö tai oikeustoimikelpoinen yhteisö. Jäseneksi hyväksymisestä päättää yhdistyksen hallitus."),
        ("§ 4 — Jäsenmaksut", "Varsinaisilta jäseniltä ja kannatusjäseniltä perittävän jäsenmaksun suuruudesta päättää vuosikokous (esim. 5 euroa kuukaudessa / 60 euroa vuodessa)."),
        ("§ 5 — Hallitus", "Yhdistyksen asioita hoitaa hallitus, johon kuuluu vuosikokouksessa valittu puheenjohtaja sekä 2–6 varsinaista jäsentä. Hallituksen toimikausi on vuosikokousten välinen aika."),
        ("§ 6 — Yhdistyksen nimen kirjoittaminen", "Yhdistyksen nimen kirjoittaa hallituksen puheenjohtaja yksin tai kaksi hallituksen jäsentä yhdessä."),
        ("§ 7 — Tilikausi ja toiminnantarkastus", "Yhdistyksen tilikausi on kalenterivuosi (1.1.–31.12.). Tilinpäätös annetaan toiminnantarkastajalle 4 viikkoa ennen vuosikokousta. Vuosikokous valitsee yhden toiminnantarkastajan ja yhden varatoiminnantarkastajan."),
        ("§ 8 — Yhdistyksen kokoukset", "Vuosikokous pidetään maaliskuun loppuun mennessä. Kokouskutsu toimitetaan vähintään 7 päivää ennen kokousta sähköpostitse."),
        ("§ 9 — Vuosikokouksessa käsiteltävät asiat", "Käsitellään sääntömääräiset asiat: tilinpäätöksen vahvistaminen, vastuuvapauden myöntäminen, toimintasuunnitelma, talousarvio, jäsenmaksut sekä hallituksen ja toiminnantarkastajien vaalit."),
        ("§ 10 — Sääntöjen muuttaminen ja purkaminen", "Sääntöjen muuttamiseen tai purkamiseen vaaditaan 3/4 ääntenenemmistö. Purkautuessa yhdistyksen varat luovutetaan rekisteröidylle yleishyödylliselle rauhanjärjestölle.")
    ]

    for title, text in rules:
        h = doc.add_heading(title, level=2)
        h.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)
        doc.add_paragraph(text)

    return doc

# 4. Trilingual Rules
def build_saannot_trilingual():
    doc = create_styled_doc("MAKAN RY — ASASNAMEH / SÄÄNNÖT / BYLAWS\nTRILINGUAL MASTER EDITION (FA / FI / EN)")

    p = doc.add_paragraph()
    p.add_run("این اساسنامه نسخه رسمی و تطبیقی انجمن ماکان به سه زبان فارسی، فنلاندی و انگلیسی است.").italic = True

    sections = [
        ("ماده ۱: نام و اقامتگاه / § 1 Nimi ja kotipaikka / Name and Domicile",
         "FA: نام انجمن «انجمن ماکان» (Makan ry) است. اقامتگاه قانونی آن شهر هلسینکی فنلاند می‌باشد.\n"
         "FI: Yhdistyksen nimi on Makan ry. Yhdistyksen kotipaikka on Helsinki.\n"
         "EN: The name of the association is Makan ry. The domicile is Helsinki, Finland."),
        
        ("ماده ۲: اهداف و روش‌های فعالیت / § 2 Tarkoitus ja toimintamuodot / Purpose & Activities",
         "FA: انجمن نهادی مستقل، غیرانتفاعی و بشردوستانه است. اهداف: ترویج صلح، مخالفت با جنگ و تجاوز نظامی، افشای سیاست‌های استعماری، مخالفت با تحریم‌های ظالمانه علیه غیرنظامیان، و آموزش سه زبانه به فارسی، فنلاندی و انگلیسی.\n\n"
         "FI: Yhdistys on itsenäinen, voittoa tavoittelematon ja humanitaarinen järjestö. Tarkoitus: edistää rauhaa, vastustaa sotia ja talouspakotteita, lisätä tietoisuutta ja edistää vuoropuhelua suomalaisten ja maahanmuuttajien välillä.\n\n"
         "EN: The association is independent, non-profit, and humanitarian. Purposes: promote peace per UN Charter, oppose military aggression, expose colonial foreign intervention, condemn unilateral sanctions targeting civilians, and conduct trilingual education."),

        ("ماده ۳: شرایط عضویت / § 3 Jäsenyys / Membership",
         "FA: عضویت برای هواداران صلح و استقلال ملل آزاد است. اعضای حامی حقیقی و حقوقی نیز پذیرفته می‌شوند.\n"
         "FI: Varsinaiseksi jäseneksi voi liittyä jokainen, joka hyväksyy tarkoituksen. Kannatusjäsenet hyväksytään.\n"
         "EN: Open to individuals supporting peace and sovereignty. Supporting members accepted."),

        ("ماده ۴: حق عضویت / § 4 Jäsenmaksu / Dues",
         "FA: حق عضویت ماهانه ۵ یورو (۶۰ یورو سالانه) توسط مجمع عمومی تصویب می‌شود.\n"
         "FI: Jäsenmaksu on 5 € kuukaudessa / 60 € vuodessa.\n"
         "EN: Membership fee is €5 per month / €60 per year as approved by General Meeting."),

        ("ماده ۵ تا ۱۰: ارکان و نظارت / Governance & Auditing",
         "FA: ارکان شامل مجمع عمومی سالیانه، هیئت مدیره (رئیس و حداقل ۲ عضو)، بازرس قانونی مالی (Toiminnantarkastaja)، دوره مالی سال تقویمی، و واگذاری دارایی‌ها به سازمان‌های عام‌المنفعه صلح در صورت انحلال.\n\n"
         "FI: Hallinto: Vuosikokous, hallitus (puheenjohtaja + 2-6 jäsentä), toiminnantarkastaja, tilikausi kalenterivuosi, purkamisessa varat rauhanjärjestölle.\n\n"
         "EN: Supreme body is AGM, executive board of Chairperson + 2-6 members, operations inspector, calendar financial year, and transfer of net assets to peace NGOs on dissolution.")
    ]

    for title, text in sections:
        h = doc.add_heading(title, level=2)
        h.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)
        doc.add_paragraph(text)

    return doc

# 5. Membership & Dues Policy
def build_membership_policy():
    doc = create_styled_doc("MAKAN RY — JÄSENYYS- JA MAKSUSÄÄNTÖ\nMEMBERSHIP & DUES POLICY / دستورالعمل عضویت و دریافت حق عضویت")

    sections = [
        ("۱. دسته‌بندی اعضا (Membership Categories)",
         "• اعضای عادی (Varsinaiset jäsenet): اشخاص حقیقی بالای ۱۵ سال حامی صلح و استقلال ملت‌ها. دارای حق رأی کامل و حق نامزدی در هیئت مدیره.\n"
         "• اعضای حامی (Kannatusjäsenet): اشخاص حقیقی و حقوقی حامی مالی و معنوی (فاقد حق رأی در مجمع)."),
        ("۲. سازوکار دریافت ۵ یورو حق عضویت ماهانه (Dues Collection Methods)",
         "• واریز خودکار بانکی دوره‌ای (SEPA Recurring Payment / Toistuva tilisiirto): تنظیم انتقال خودکار ماهانه ۵ یورو به حساب بانکی انجمن.\n"
         "• پرداخت اینترنتی هولوی (Holvi Store Subscriptions): اتصال کارت‌های بانکی به اشتراک ماهانه ۵ یورویی.\n"
         "• سرویس MobilePay: امکان واریز فوری موبایلی ویژه اعضای مقیم فنلاند."),
        ("۳. دفتر ثبت اعضا و صدور رسید (Registry & Bookkeeping)",
         "هیئت مدیره طبق ماده ۱۱ قانون انجمن‌های فنلاند دفتری از اسامی کامل و شهر اقامت اعضا را تحت ضوابط محرمانگی (GDPR) نگهداری می‌نماید و رسیدهای مالی دوره‌ای صادر خواهد شد.")
    ]

    for title, text in sections:
        h = doc.add_heading(title, level=2)
        h.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)
        doc.add_paragraph(text)

    return doc

# 6. Founders Registration Kit
def build_registration_kit():
    doc = create_styled_doc("MAKAN RY — PERUSTAJAN OPAS JA ASIAKIRJAPAKETTI\nFOUNDERS' REGISTRATION GUIDE & CHECKLIST\nراهنمای جامع اعضای هیئت مؤسس انجمن ماکان")

    sections = [
        ("۱. اطلاعات فردی مورد نیاز از مؤسسین برای اداره ثبت فنلاند (PRH)",
         "طبق ماده ۳۵ قانون انجمن‌های فنلاند (Yhdistyslaki)، موارد زیر برای اعضای هیئت مدیره الزامی است:\n"
         "۱. نام و نام خانوادگی کامل مطابق پاسپورت (Koko nimi)\n"
         "۲. کد ملی فنلاند یا تاریخ تولد (Henkilötunnus / syntymäaika)\n"
         "۳. تابعیت (Kansalaisuus)\n"
         "۴. آدرس پستی کامل و کد پستی (Täydellinen katuosoite ja postinumero)\n"
         "۵. شهر محل سکونت (Kotikunta) - رئیس هیئت مدیره باید مقیم فنلاند باشد.\n"
         "۶. تصویر صفحه اول پاسپورت یا کارت شناسایی فنلاندی معتبر"),
        ("۲. روش امضا و ارسال اسناد (Signing Instructions)",
         "اعضای محترم هیئت مؤسس می‌توانند فایل‌های Word منشور تأسیس و صورت‌جلسه را باز کرده، مشخصات خود را تکمیل و به یکی از روش‌های زیر امضا نمایند:\n"
         "• روش اول (پرینت و امضای دستی): چاپ نسخه کاغذی، امضا با خودکار، و اسکن به فرمت PDF.\n"
         "• روش دوم (امضای دیجیتال رسمی): تبدیل به PDF و امضا از طریق سامانه‌های Visma Sign، Adobe Sign یا امضای الکترونیک امن بانکی فنلاند."),
        ("۳. مراحل اداری پس از امضا (PRH Roadmap)",
         "۱. بارگذاری فرم perusilmoitus در سامانه الکترونیکی prh.fi توسط رئیس هیئت مدیره.\n"
         "۲. پرداخت کارمزد ثبت آنلاین (۵۸ یورو).\n"
         "۳. دریافت شناسه ملی انجمن (Y-tunnus) ظرف ۲ تا ۵ روز کاری.\n"
         "۴. افتتاح حساب بانکی حقوقی در هولوی (Holvi) یا OP/Nordea و فعال‌سازی شماره حساب جهت واریز حق عضویت‌ها.")
    ]

    for title, text in sections:
        h = doc.add_heading(title, level=2)
        h.runs[0].font.color.rgb = RGBColor(0x94, 0x73, 0x1E)
        doc.add_paragraph(text)

    return doc

def main():
    generators = [
        ("01_Makan_ry_Perustamiskirja_Founding_Charter.docx", build_perustamiskirja),
        ("02_Makan_ry_Perustava_kokous_Poytakirja_Minutes.docx", build_poytakirja),
        ("03_Makan_ry_Saannot_Official_PRH.docx", build_saannot_prh),
        ("04_Makan_ry_Saannot_Trilingual_Bylaws.docx", build_saannot_trilingual),
        ("05_Makan_ry_Membership_and_Dues_Policy.docx", build_membership_policy),
        ("06_Makan_ry_Founders_Registration_Kit.docx", build_registration_kit)
    ]

    out_dirs = [
        "Makan_Ry/downloads",
        "PFP_Platform/web/public/legal/makan/downloads"
    ]

    for filename, func in generators:
        doc = func()
        for out_dir in out_dirs:
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, filename)
            doc.save(out_path)
            print(f"Generated: {out_path}")

if __name__ == "__main__":
    main()
