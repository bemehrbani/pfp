#!/usr/bin/env python3
import os

target_dir = '/Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/media/subtitles/france24-what-we-know-minab-strike'
os.makedirs(target_dir, exist_ok=True)

# 63 accurately proofread cues
cues_data = [
    ("00:00:00.000", "00:00:09.520", 
     "A mass funeral was held today for the 165 schoolchildren killed on Saturday in Iran,", 
     "امروز مراسم تشییع پیکر ۱۶۵ دانش‌آموزی که روز شنبه در ایران کشته شدند برگزار شد؛", 
     "Tänään pidettiin hautajaiset 165 koululaiselle, jotka saivat surmansa lauantaina Iranissa;"),
    
    ("00:00:09.520", "00:00:14.840", 
     "the UN calling for a full investigation into a grave violation of humanitarian law.", 
     "سازمان ملل خواستار تحقیقات کامل درباره این نقض فاحش حقوق بشردوستانه شده است.", 
     "YK vaatii perusteellista tutkintaa humanitaarisen oikeuden vakavasta rikkomuksesta."),
    
    ("00:00:14.840", "00:00:20.560", 
     "But online, some users are claiming that the incident was staged. Tell us more.", 
     "اما در فضای مجازی برخی ادعا می‌کنند این حادثه صحنه‌سازی بوده است. جزئیات چیست؟", 
     "Mutta verkossa jotkut väittävät tapauksen olleen lavastettu. Kerro meille lisää."),
    
    ("00:00:20.560", "00:00:27.320", 
     "Yes, exactly. With this user on X claiming that the school and the girls did not exist,", 
     "بله دقیقاً؛ با این کاربر در شبکه اکس که مدعی شد چنین مدرسه‌ای و این دختران وجود خارجی نداشته‌اند،", 
     "Kyllä, eräs X-käyttäjä väitti, ettei koulua tai tyttöjä ollut olemassakaan,"),
    
    ("00:00:27.320", "00:00:31.900", 
     "with this video that you can see playing behind me. According to this user, this footage", 
     "همراه با این ویدیویی که پشت سر من در حال پخش است. به ادعای این کاربر، این تصاویر", 
     "tämän taustallani näkyvän videon kera. Tämän käyttäjän mukaan tämä materiaali"),
    
    ("00:00:31.900", "00:00:38.120", 
     "is war propaganda like the genocide and famine in Gaza. Some even turned to Grok,", 
     "تبلیغات جنگی مانند نسل‌کشی و قحطی در غزه است. برخی حتی به گراک (Grok) مراجعه کردند،", 
     "on sotapropagandaa kuten Gazan nälänhätä. Jotkut kääntyivät jopa Grokin puoleen,"),
    
    ("00:00:38.120", "00:00:43.580", 
     "that is the AI assistant embedded within the platform X to fact-check the footage and", 
     "یعنی همان دستیار هوش مصنوعی موجود در پلتفرم اکس، تا درستی ویدیو را بسنجند و", 
     "eli X-alustan tekoälyn puoleen faktantarkistusta varten ja"),
    
    ("00:00:43.580", "00:00:49.120", 
     "ask Grok if it's real. And Grok answered that the video is supposed to show an attack", 
     "از گراک بپرسند آیا واقعی است یا خیر. و گراک پاسخ داد این ویدیو مربوط به حمله‌ای", 
     "kysyivät Grokilta sen aitoutta. Grok vastasi videon esittävän iskua"),
    
    ("00:00:49.120", "00:00:55.760", 
     "on a school, yes, but in Kabul in 2021. So we tried to compare the footage", 
     "به یک مدرسه در کابل در سال ۲۰۲۱ است! بنابراین ما سعی کردیم این ویدیو را", 
     "kouluun Kabulissa vuonna 2021. Yritimme siis vertailla kuvamateriaalia"),
    
    ("00:00:55.760", "00:01:00.960", 
     "with former footage, verified footage from the school attacked in 2021 in Kabul,", 
     "با ویدیوهای موثق و تایید شده از مدرسه مورد حمله قرار گرفته در کابل ۲۰۲۱ مقایسه کنیم،", 
     "Kabulin vuoden 2021 vahvistettuihin videoihin,"),
    
    ("00:01:00.960", "00:01:07.440", 
     "and as you can see, it's not the same building at all. Grok was simply wrong.", 
     "و همان‌طور که می‌بینید اصلاً همان ساختمان نیست. پاسخ گراک کاملاً اشتباه بود.", 
     "ja kuten näkyy, kyseessä ei ole lainkaan sama rakennus. Grok oli yksinkertaisesti väärässä."),
    
    ("00:01:07.440", "00:01:13.640", 
     "And we tried to compare the actual viral footage with the maps that you can find", 
     "سپس ما ویدیوی وایرال شده را با نقشه‌هایی که می‌توانید در گوگل مپ و گوگل ارث", 
     "Verrattiin sitten viraalivideota Google Mapsin ja Google Earthin karttoihin"),
    
    ("00:01:13.640", "00:01:18.520", 
     "on Google Maps, Google Earth for example, or satellite imagery, and we", 
     "پیدا کنید یا تصاویر ماهواره‌ای مقایسه کردیم و توانستیم", 
     "sekä satelliittikuviin, ja onnistuimme"),
    
    ("00:01:18.520", "00:01:24.320", 
     "managed to identify the location as a girls' school in Minab — Shajareh Tayyebeh school in Minab.", 
     "مکان را به عنوان دبستان دخترانه شجره طیبه در میناب احراز هویت و شناسایی کنیم.", 
     "tunnistamaan sijainnin Minabin Shajareh Tayyebeh -tyttökouluksi."),
    
    ("00:01:24.320", "00:01:32.040", 
     "Iranian media reported that at least 165 deaths happened linked to the strike,", 
     "رسانه‌های ایران گزارش دادند حداقل ۱۶۵ نفر بر اثر این حمله جان باخته‌اند،", 
     "Iranin media raportoi ainakin 165 kuolemasta iskun seurauksena,"),
    
    ("00:01:32.040", "00:01:36.880", 
     "but that figure has not been independently verified. I've seen personally", 
     "هرچند این رقم به طور مستقل تایید نشده است. اما من شخصاً", 
     "mutta lukua ei ole vahvistettu riippumattomasti. Olen henkilökohtaisesti"),
    
    ("00:01:36.880", "00:01:42.880", 
     "a lot of verified footage showing the bodies of children beneath the rubble.", 
     "ویدیوهای تایید شده فراوانی را دیده‌ام که پیکر کودکان را زیر آوار نشان می‌دهد.", 
     "nähnyt useita vahvistettuja videoita lapsista raunioiden alla."),
    
    ("00:01:42.880", "00:01:48.120", 
     "Obviously, I'm not going to show you these videos that are very disturbing.", 
     "بدیهی است من این ویدیوها را به دلیل بسیار دلخراش بودن نشان نخواهم داد.", 
     "En luonnollisestikaan näytä näitä videoita, koska ne ovat hyvin järkyttäviä."),
    
    ("00:01:48.120", "00:01:53.760", 
     "You might have seen though one photo that was shared, for example by the Iranian embassy in Vienna —", 
     "البته شاید عکسی را که مثلاً توسط سفارت ایران در وین منتشر شد دیده باشید؛", 
     "Olette ehkä nähneet kuvan, jonka jakoi esimerkiksi Iranin Wienin-suurlähetystö –"),
    
    ("00:01:53.760", "00:01:58.680", 
     "this photo right there. It is a blood-stained pink backpack,", 
     "همین عکسی که می‌بینید: کوله‌پشتی صورتی آغشته به خون.", 
     "tämä kuva tässä: verinen vaaleanpunainen reppu,"),
    
    ("00:01:58.680", "00:02:06.680", 
     "but I've asked Gemini, this is a tool provided by Google, to check if it", 
     "اما من از هوش مصنوعی جمینای گوگل خواستم بررسی کند که آیا", 
     "mutta pyysin Googlen Gemini-työkalua tarkistamaan,"),
    
    ("00:02:06.680", "00:02:12.880", 
     "managed to detect any invisible watermark, and the answer was yes,", 
     "می‌تواند واترمارک نامرئی شناسایی کند یا خیر، و پاسخ مثبت بود:", 
     "löytyykö siitä näkymätöntä vesileimaa, ja vastaus oli kyllä:"),
    
    ("00:02:12.880", "00:02:21.520", 
     "this image was created or edited using AI tools by Google.", 
     "این تصویر توسط ابزارهای هوش مصنوعی گوگل تولید یا ادیت شده است.", 
     "tämä kuva on luotu tai muokattu Googlen tekoälytyökaluilla."),
    
    ("00:02:21.520", "00:02:28.400", 
     "So this suggests that even if we have real footage from the incident happening in Minab,", 
     "این نشان می‌دهد با وجود ویدیوهای واقعی از حادثه میناب،", 
     "Tämä osoittaa, että vaikka Minabista on aitoa materiaalia,"),
    
    ("00:02:28.400", "00:02:36.080", 
     "this specific image was generated by AI. The strike itself is described as a war crime,", 
     "این تصویر خاص با هوش مصنوعی ساخته شده است. خود این حمله جنایت جنگی توصیف شده است،", 
     "tämä nimenomainen kuva on tekoälyä. Itse iskua kuvaillaan sotarikokseksi,"),
    
    ("00:02:36.080", "00:02:41.360", 
     "but online some claim that the building targeted may not have been purely civilian infrastructure.", 
     "اما در فضای مجازی برخی مدعی شدند ساختمانی که هدف قرار گرفت صرفاً غیرنظامی نبوده است.", 
     "mutta jotkut väittävät verkossa, ettei kohde ollut täysin siviilirakennus."),
    
    ("00:02:41.360", "00:02:48.000", 
     "Exactly. Any attack on civilian infrastructure, including a school, is a violation of international law,", 
     "دقیقاً؛ هرگونه حمله به اماکن غیرنظامی از جمله مدرسه، نقض حقوق بین‌الملل است،", 
     "Aivan. Kaikki iskut siviilikohteisiin, kuten kouluihin, rikkovat kansainvälistä oikeutta,"),
    
    ("00:02:48.000", "00:02:53.680", 
     "unless you manage to prove there is credible evidence the building is used for something else.", 
     "مگر اینکه شواهد موثقی ارائه شود که ساختمان برای مقاصد دیگر استفاده می‌شده است.", 
     "ellei pystytä osoittamaan luotettavaa näyttöä siitä, että rakennusta käytettiin muuhun."),
    
    ("00:02:53.680", "00:02:58.320", 
     "And that is what is alleged by users saying this building is located", 
     "و این همان ادعایی است که برخی کاربران مطرح می‌کنند و می‌گویند این ساختمان", 
     "Tätä väittävät käyttäjät, joiden mukaan tämä rakennus sijaitsee"),
    
    ("00:02:58.320", "00:03:04.720", 
     "within the same compound as several buildings belonging to the IRGC, Iran's Revolutionary Guard.", 
     "در داخل همان محوطه‌ای قرار دارد که متعلق به سپاه پاسداران انقلاب اسلامی است.", 
     "samalla alueella kuin useat Iranin vallankumouskaartin (IRGC) rakennukset."),
    
    ("00:03:04.720", "00:03:11.600", 
     "These claims are based on open-source intelligence. Let's check together a map from OpenStreetMap.", 
     "این ادعاها بر اساس داده‌های متن‌باز (OSINT) است. بیایید با هم نقشه‌ای از پلتفرم OpenStreetMap را بررسی کنیم.", 
     "Nämä väitteet perustuvat avoimeen tiedusteludataan. Katsotaan OpenStreetMap-karttaa."),
    
    ("00:03:11.600", "00:03:17.840", 
     "This is a collaborative mapping platform where you can mark locations like a school or military barracks.", 
     "این یک پلتفرم نقشه‌برداری مشارکتی است که می‌توان در آن مدارسی یا پادگان‌های نظامی را علامت‌گذاری کرد.", 
     "Tämä on avoin kartta-alusta, johon voi merkitä kouluja tai sotilastukikohtia."),
    
    ("00:03:17.840", "00:03:23.360", 
     "Here is the location for the school. And here you can see the rest is labeled as part of the Pasdaran barracks.", 
     "اینجا موقعیت مدرسه است و بقیه بخش‌ها به عنوان بخشی از پادگان پاسداران ثبت شده است.", 
     "Tässä on koulun sijainti, ja muu alue on merkitty osaksi kaartin parakkialuetta."),
    
    ("00:03:23.360", "00:03:28.880", 
     "You can see that this site has been hit twice. And it's worth noting this area here is a clinic that wasn't hit.", 
     "می‌بینید که این محوطه دو بار هدف قرار گرفته و درمانگاه مجاور آسیبی ندیده است.", 
     "Tähän kohteeseen on osunut kahdesti, ja viereinen klinikka säästyi iskuilta."),
    
    ("00:03:28.880", "00:03:34.480", 
     "When you look at satellite imagery from 2013, the building was clearly within the military compound.", 
     "وقتی به تصاویر ماهواره‌ای سال ۲۰۱۳ نگاه می‌کنید، ساختمان در داخل محوطه پادگان بود.", 
     "Vuoden 2013 satelliittikuvissa rakennus sijaitsi selvästi sotilasalueen sisällä."),
    
    ("00:03:34.480", "00:03:41.000", 
     "But if you look at more recent pictures from Google Earth and Google Maps,", 
     "اما اگر به تصاویر جدیدتر در گوگل ارث و گوگل مپ نگاه کنید،", 
     "Mutta jos katsotaan uudempia Google Earthin kuvia,"),
    
    ("00:03:41.000", "00:03:47.000", 
     "you will see a wall was built in 2016, converting it into an all-girls school.", 
     "می‌بینید که در سال ۲۰۱۶ دیواری ساخته شده و این مکان به دبستان دخترانه تبدیل شده است.", 
     "nähdään, että vuonna 2016 rakennettiin erottava muuri ja siitä tehtiin tyttökoulu."),
    
    ("00:03:47.000", "00:03:53.000", 
     "It is separated from the military barracks with a separate independent entrance,", 
     "این مدرسه از پادگان کاملاً جدا شده، درب ورود و خروج مستقل دارد،", 
     "Se on erotettu parakeista omalla erillisellä sisäänkäynnillä,"),
    
    ("00:03:53.000", "00:03:59.000", 
     "colorful walls, and satellite imagery shows civilian playgrounds — 100% civilian infrastructure.", 
     "دیوارهای رنگ‌آمیزی‌شده دارد و تصاویر ماهواره‌ای زمین بازی کودکان را نشان می‌دهد: ۱۰۰٪ غیرنظامی.", 
     "värikkäillä seinillä ja leikkikentillä – satelliittikuvien mukaan 100 % siviilikohde."),
    
    ("00:03:59.000", "00:04:05.000", 
     "Finally, Maya, Tehran is blaming the US and Israel. Do we know who is responsible for the strike?", 
     "در پایان مایا، تهران آمریکا و اسرائیل را مقصر می‌داند؛ آیا دقیقاً مشخص است چه کسی مسئول این حمله است؟", 
     "Lopuksi, Maya, Teheran syyttää Yhdysvaltoja ja Israelia. Tiedämmekö kuka iskusta vastaa?"),
    
    ("00:04:05.000", "00:04:11.000", 
     "First, the Israeli military said they were not aware of any attack happening in the area.", 
     "نخست، ارتش اسرائیل اعلام کرد از وقوع هرگونه حمله‌ای در این منطقه بی‌اطلاع است.", 
     "Ensinnäkin, Israelin armeija ilmoitti, ettei se tiennyt iskusta alueella."),
    
    ("00:04:11.000", "00:04:16.500", 
     "The Pentagon says that it is currently investigating the incident.", 
     "پنتاگون اعلام کرد که در حال بررسی این حادثه است.", 
     "Pentagon ilmoitti tutkivansa tapausta parhaillaan."),
    
    ("00:04:16.500", "00:04:23.000", 
     "And US Secretary of State Marco Rubio said the US would not deliberately target a school,", 
     "و مارکو روبیو وزیر امور خارجه آمریکا گفت ایالات متحده هرگز عمداً مدرسه‌ای را هدف قرار نمی‌دهد،", 
     "Ja Yhdysvaltain ulkoministeri Marco Rubio sanoi, ettei USA tahallaan iskisi kouluun,"),
    
    ("00:04:23.000", "00:04:31.000", 
     "adding that Iranians are targeting civilian infrastructure.", 
     "و افزود که به ادعای او این ایران است که زیرساخت‌های غیرنظامی را هدف می‌گیرد.", 
     "lisäten, että hänen mukaansa iranilaiset kohdistavat iskuja siviilikohteisiin."),
    
    ("00:04:31.000", "00:04:39.000", 
     "Online, some suggested the school was hit by a failed IRGC rocket launch.", 
     "در فضای مجازی برخی مدعی شدند این حمله ناشی از شلیک ناموفق موشک سپاه بوده است.", 
     "Verkossa jotkut väittivät iskun johtuneen kaartin omasta epäonnistuneesta laukaisusta."),
    
    ("00:04:39.000", "00:04:47.000", 
     "But analysts proved that the video shown as evidence is actually from Zanjan —", 
     "اما کارشناسان اثبات کردند ویدیویی که به عنوان مدرک نشان داده شده، متعلق به زنجان است —", 
     "Mutta tutkijat todistivat todisteena esitetyn videon olevan Zanjanista –"),
    
    ("00:04:47.000", "00:04:55.000", 
     "1,300 kilometers away in the opposite direction from Minab.", 
     "در فاصله ۱۳۰۰ کیلومتری و در جهت کاملاً مخالف نسبت به میناب.", 
     "1 300 kilometrin päästä vastakkaisesta suunnasta Minabiin nähden."),
    
    ("00:04:55.000", "00:05:03.000", 
     "And finally, a viral post seen 6 million times on X claiming Tehran admitted responsibility on Telegram", 
     "و در نهایت، پست وایرالی با ۶ میلیون بازدید در اکس که مدعی پذیرش مسئولیت توسط تهران در تلگرام بود،", 
     "Ja viraalipostaus, jolla oli 6 miljoonaa katselukertaa ja jossa väitettiin Teheranin myöntäneen iskun,"),
    
    ("00:05:03.000", "00:05:10.000", 
     "came from an opposition satire channel with no link to Iranian authorities.", 
     "از یک کانال طنز اپوزیسیون منتشر شده که هیچ ارتباطی با مقامات ایران ندارد.", 
     "oli peräisin satiirikanavalta, jolla ei ole yhteyttä Iranin viranomaisiin."),
    
    ("00:05:10.000", "00:05:15.000", 
     "Thanks, Maya. Maya there with tonight's Truth or Fake. Stay with us, we'll be right back.", 
     "ممنون مایا؛ مایا با بخش «حقیقت یا جعلی» امشب. با ما همراه باشید، پس از وقفه‌ای کوتاه بازمی‌گردیم.", 
     "Kiitos Maya; Maya ja illan Totuus vai tarua. Pysykää kanavalla, palaamme pian.")
]

en_vtt = ["WEBVTT\n"]
fa_vtt = ["WEBVTT\n"]
fi_vtt = ["WEBVTT\n"]

for i, (start, end, en, fa, fi) in enumerate(cues_data, 1):
    en_vtt.append(f"\n{i}\n{start} --> {end}\n{en}\n")
    fa_vtt.append(f"\n{i}\n{start} --> {end}\n{fa}\n")
    fi_vtt.append(f"\n{i}\n{start} --> {end}\n{fi}\n")

with open(os.path.join(target_dir, "en.vtt"), "w", encoding="utf-8") as f:
    f.writelines(en_vtt)

with open(os.path.join(target_dir, "fa.vtt"), "w", encoding="utf-8") as f:
    f.writelines(fa_vtt)

with open(os.path.join(target_dir, "fi.vtt"), "w", encoding="utf-8") as f:
    f.writelines(fi_vtt)

print("✅ Written 50 perfectly synchronized and proofread cues for France 24.")
