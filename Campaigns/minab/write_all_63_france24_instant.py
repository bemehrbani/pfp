#!/usr/bin/env python3
import os

target_dir = '/Users/mahdifarimani/Documents/PFP/PFP_Platform/web/public/media/subtitles/france24-what-we-know-minab-strike'
os.makedirs(target_dir, exist_ok=True)

# 63 fine-grained segments spanning the ENTIRE 6m 28s video (00:00.000 to 06:28.480)
cues = [
    ("00:00:00.000", "00:00:09.520", 
     "A mass funeral was held today for the 165 school children killed on Saturday in Iran,", 
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
     "تبلیغات جنگی مانند نسل‌کشی و قحطی در غزه است. برخی حتی به گراک مراجعه کردند،", 
     "on sotapropagandaa kuten Gazan nälänhätä. Jotkut kääntyivät jopa Grokin puoleen,"),
    
    ("00:00:38.120", "00:00:43.580", 
     "that is the AI assistant embedded within the platform X, to fact-check the footage and", 
     "یعنی همان دستیار هوش مصنوعی پلتفرم اکس، تا درستی ویدیو را ارزیابی کنند و", 
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
     "with former verified footage from the school attacked in 2021 in Kabul,", 
     "با ویدیوهای موثق و تایید شده از مدرسه مورد حمله قرار گرفته در کابل ۲۰۲۱ مقایسه کنیم،", 
     "Kabulin vuoden 2021 vahvistettuihin videoihin,"),
    
    ("00:01:00.960", "00:01:07.440", 
     "and as you can see, it's not the same building at all. Grok was simply wrong.", 
     "و همان‌طور که می‌بینید اصلاً همان ساختمان نیست. پاسخ گراک کاملاً اشتباه بود.", 
     "ja kuten näkyy, kyseessä ei ole lainkaan sama rakennus. Grok oli yksinkertaisesti väärässä."),
    
    ("00:01:07.440", "00:01:13.640", 
     "And we tried to compare the actual viral footage with the maps that you can find", 
     "سپس ما ویدیوی وایرال شده را با نقشه‌هایی که می‌توانید پیدا کنید مقایسه کردیم؛", 
     "Verrattiin sitten viraalivideota saatavilla oleviin karttoihin,"),
    
    ("00:01:13.640", "00:01:18.520", 
     "on Google Maps and Google Earth for example, or satellite imagery, and we", 
     "مثلاً در گوگل مپ و گوگل ارث یا تصاویر ماهواره‌ای، و ما", 
     "kuten Google Mapsiin, Google Earthiin tai satelliittikuviin, ja"),
    
    ("00:01:18.520", "00:01:24.320", 
     "managed to identify the location as a girls' school in Minab — Shajareh Tayyebeh school in Minab.", 
     "موفق شدیم مکان را به عنوان دبستان دخترانه شجره طیبه در میناب شناسایی کنیم.", 
     "onnistuimme tunnistamaan sijainnin Minabin Shajareh Tayyebeh -tyttökouluksi."),
    
    ("00:01:24.320", "00:01:32.040", 
     "Iranian media reported that at least 165 deaths happened linked to the strike,", 
     "رسانه‌های ایران گزارش دادند حداقل ۱۶۵ نفر در پی این حمله جان باخته‌اند،", 
     "Iranin media raportoi ainakin 165 kuolemasta iskun seurauksena,"),
    
    ("00:01:32.040", "00:01:36.880", 
     "but that figure has not been independently verified. I have personally seen", 
     "هرچند این آمار مستقلاً تایید نشده است. اما من شخصاً", 
     "mutta lukua ei ole vahvistettu riippumattomasti. Olen henkilökohtaisesti"),
    
    ("00:01:36.880", "00:01:42.880", 
     "a lot of verified footage showing the bodies of children beneath the rubble.", 
     "ویدیوهای تایید شده بسیاری را دیده‌ام که پیکر کودکان را در زیر آوار نشان می‌دهد.", 
     "nähnyt useita vahvistettuja videoita lapsista raunioiden alla."),
    
    ("00:01:42.880", "00:01:48.120", 
     "Obviously, I'm not going to show you these videos that are very disturbing.", 
     "بدیهی است که من این ویدیوها را به دلیل تکان‌دهنده بودن نشان نخواهم داد.", 
     "En luonnollisestikaan näytä näitä videoita, koska ne ovat hyvin järkyttäviä."),
    
    ("00:01:48.120", "00:01:53.760", 
     "You might have seen though one photo that was shared for example by the Iranian embassy in Vienna —", 
     "شاید عکسی را که مثلاً توسط سفارت ایران در وین به اشتراک گذاشته شد دیده باشید —", 
     "Olette ehkä nähneet kuvan, jonka jakoi esimerkiksi Iranin Wienin-suurlähetystö –"),
    
    ("00:01:53.760", "00:01:58.680", 
     "this photo right there. It is a blood-stained pink backpack,", 
     "همین عکسی که می‌بینید: کوله‌پشتی صورتی آغشته به خون،", 
     "tämä kuva tässä: verinen vaaleanpunainen reppu,"),
    
    ("00:01:58.680", "00:02:06.680", 
     "but I've asked Gemini, this is an AI tool provided by Google, to check if it", 
     "اما من از هوش مصنوعی جمینای گوگل خواستم بررسی کند که آیا", 
     "mutta pyysin Googlen Gemini-tekoälyä tarkistamaan,"),
    
    ("00:02:06.680", "00:02:12.880", 
     "managed to detect any invisible watermark, and the answer was yes:", 
     "می‌تواند واترمارک نامرئی را شناسایی کند یا خیر، و پاسخ مثبت بود:", 
     "löytyykö siitä näkymätöntä vesileimaa, ja vastaus oli kyllä:"),
    
    ("00:02:12.880", "00:02:21.520", 
     "this image was created or edited using AI tools by Google.", 
     "این تصویر با استفاده از ابزارهای هوش مصنوعی گوگل خلق یا ویرایش شده است.", 
     "tämä kuva on luotu tai muokattu Googlen tekoälytyökaluilla."),
    
    ("00:02:21.520", "00:02:28.400", 
     "So this suggests that even if we have real footage from the incident happening in Minab,", 
     "بنابراین این نشان می‌دهد با وجود ویدیوهای واقعی از حادثه میناب،", 
     "Tämä osoittaa, että vaikka Minabista on aitoa kuvamateriaalia,"),
    
    ("00:02:28.400", "00:02:36.080", 
     "this specific photo was generated by AI. The strike itself is described as a war crime,", 
     "این تصویر ویژه با هوش مصنوعی ساخته شده است. این حمله خود به عنوان جنایت جنگی توصیف شده،", 
     "tämä tietty kuva on tekoälyä. Itse iskua kuvaillaan sotarikokseksi,"),
    
    ("00:02:36.080", "00:02:41.360", 
     "but online you found some people claiming that the building that was targeted may", 
     "اما در اینترنت کسانی مدعی شدند ساختمانی که هدف قرار گرفت شاید", 
     "mutta verkossa jotkut väittävät, ettei kohteena ollut rakennus ollut"),
    
    ("00:02:41.360", "00:02:48.000", 
     "not have been a purely civilian infrastructure. Exactly — any attack on anything civilian,", 
     "صرفاً یک زیرساخت غیرنظامی نبوده است. دقیقاً؛ هرگونه حمله به اهداف غیرنظامی،", 
     "täysin siviilikohde. Aivan – mikä tahansa isku siviilikohteeseen,"),
    
    ("00:02:48.000", "00:02:53.680", 
     "including a school for example, is generally a violation of international law,", 
     "از جمله یک مدرسه، به طور کلی نقض حقوق بین‌الملل محسوب می‌شود،", 
     "mukaan lukien kouluun, on yleensä kansainvälisen oikeuden rikkomus,"),
    
    ("00:02:53.680", "00:02:58.320", 
     "unless you manage to prove there is credible evidence the building is used for something else.", 
     "مگر اینکه اثبات شود شواهد معتبری وجود دارد که ساختمان برای اهداف دیگری استفاده می‌شده است.", 
     "ellei pystytä osoittamaan luotettavia todisteita sen käytöstä muuhun tarkoitukseen."),
    
    ("00:02:58.320", "00:03:04.720", 
     "And that is what is alleged by this user who is saying that this building is located", 
     "و این همان ادعایی است که این کاربر مطرح می‌کند و می‌گوید این ساختمان", 
     "Ja tätä väittää tämä käyttäjä, jonka mukaan tämä rakennus sijaitsee"),
    
    ("00:03:04.720", "00:03:11.600", 
     "within the same compound as several buildings belonging to the IRGC, Iran's Revolutionary Guard.", 
     "در همان محوطه‌ای قرار دارد که متعلق به ساختمان‌های سپاه پاسداران انقلاب اسلامی است.", 
     "samalla alueella useiden Iranin vallankumouskaartille kuuluvien rakennusten kanssa."),
    
    ("00:03:11.600", "00:03:17.840", 
     "These claims are based actually on open-source intelligence. Let's check together a map", 
     "این ادعاها در واقع بر اساس داده‌های متن‌باز (OSINT) است. بیایید با هم نقشه‌ای را بررسی کنیم", 
     "Nämä väitteet perustuvat avoimeen tiedusteludataan. Tarkastellaan yhdessä karttaa"),
    
    ("00:03:17.840", "00:03:23.360", 
     "from this platform, OpenStreetMap. This is a collaborative mapping platform where you can", 
     "از پلتفرم OpenStreetMap. این یک پلتفرم نقشه‌برداری مشارکتی است که در آن می‌توانید", 
     "OpenStreetMap-alustalta. Tämä on yhteisöllinen karttapalvelu, johon voi"),
    
    ("00:03:23.360", "00:03:28.880", 
     "mark many places, such as a school for example or military barracks, and that's", 
     "مکان‌های مختلفی مانند مدرسه یا پادگان‌های نظامی را ثبت کنید، و این همان چیزی است", 
     "merkitä kohteita, kuten koulun tai sotilastukikohdan, ja näin"),
    
    ("00:03:28.880", "00:03:34.480", 
     "what happened here. Here is the location for the school, right here, and here you can see that", 
     "که در اینجا رخ داده است. این موقعیت مدرسه است، درست در اینجا، و می‌بینید که", 
     "tässä on tapahtunut. Tässä on koulun sijainti, ja tässä näkyy,"),
    
    ("00:03:34.480", "00:03:40.720", 
     "the rest is labeled as part of the Pasdaran barracks held by the Revolutionary Guards in Iran.", 
     "بقیه بخش‌ها به عنوان پادگان پاسداران متعلق به سپاه در ایران نام‌گذاری شده است.", 
     "että muu alue on merkitty osaksi kaartin sotilasparakkeja."),
    
    ("00:03:40.800", "00:03:46.080", 
     "And you can see that this site has been hit twice, and it's worth noting", 
     "می‌بینید که این محل دو بار هدف اصابت قرار گرفته، و شایان ذکر است", 
     "Näette, että tähän kohteeseen on osunut kahdesti, ja on huomionarvoista,"),
    
    ("00:03:46.080", "00:03:52.160", 
     "that this area here is a clinic that was not hit.", 
     "که این بخش در اینجا یک درمانگاه است که مورد اصابت قرار نگرفته است.", 
     "että tämä alue tässä on klinikka, johon ei osunut."),
    
    ("00:03:52.160", "00:03:59.440", 
     "But the building that is currently a school has been hit. When you look at satellite imagery from 2013,", 
     "اما ساختمانی که اکنون مدرسه است اصابت کرده است. وقتی به تصاویر ماهواره‌ای سال ۲۰۱۳ نگاه می‌کنید،", 
     "Mutta rakennus, joka nykyään toimii kouluna, kärsi osuman. Vuoden 2013 satelliittikuvissa"),
    
    ("00:03:59.440", "00:04:05.120", 
     "that would be the building here, you can see that it is clearly within the military compound.", 
     "یعنی همین ساختمان، می‌بینید که کاملاً در داخل محوطه نظامی قرار داشته است.", 
     "rakennus sijaitsi selvästi sotilasalueen sisäpuolella."),
    
    ("00:04:05.200", "00:04:10.400", 
     "But if you look at more recent pictures from Google Earth and Google Maps,", 
     "اما اگر به تصاویر تازه‌تر در گوگل ارث و گوگل مپ نگاه کنید،", 
     "Mutta jos katsotte uudempia kuvia Google Earthista ja Google Mapsista,"),
    
    ("00:04:10.400", "00:04:15.920", 
     "you're going to see that there is now a wall, and this wall was built in 2016,", 
     "مشاهده خواهید کرد که اکنون دیواری وجود دارد که این دیوار در سال ۲۰۱۶ ساخته شده است،", 
     "näette, että siellä on nykyään muuri, joka rakennettiin vuonna 2016,"),
    
    ("00:04:15.920", "00:04:23.280", 
     "and this building was turned into an all-girls school in 2016. So it is separated from the military barracks,", 
     "و این ساختمان در سال ۲۰۱۶ به یک دبستان دخترانه تبدیل شد. بنابراین از پادگان نظامی جدا شده است،", 
     "ja rakennus muutettiin tyttökouluksi vuonna 2016. Se on siis erotettu sotilasalueesta,"),
    
    ("00:04:23.280", "00:04:28.720", 
     "and there is a separate independent entrance, and you also see these colorful walls,", 
     "دارای درب ورودی کاملاً مجزا و مستقل است، و این دیوارهای رنگارنگ نقاشی‌شده را می‌بینید،", 
     "sillä on erillinen sisäänkäynti ja värikkäät seinämaalaukset,"),
    
    ("00:04:29.520", "00:04:35.360", 
     "and satellite imagery shows civilian infrastructure, such as playgrounds.", 
     "و تصاویر ماهواره‌ای زیرساخت‌های غیرنظامی مانند حیاط بازی کودکان را نشان می‌دهد.", 
     "ja satelliittikuvissa näkyy siviilirakenteita, kuten leikkikenttiä."),
    
    ("00:04:35.360", "00:04:41.040", 
     "So this is 100% civilian infrastructure according to satellite imagery.", 
     "بنابراین طبق تصاویر ماهواره‌ای، این مکان ۱۰۰٪ زیرساخت غیرنظامی است.", 
     "Tämä on siis satelliittikuvien perusteella 100-prosenttisesti siviilikohde."),
    
    ("00:04:41.040", "00:04:46.400", 
     "And finally, Maya, Tehran is blaming the US and Israel for this attack. Do we actually know who is responsible?", 
     "و در پایان مایا، تهران آمریکا و اسرائیل را مقصر این حمله می‌داند؛ آیا دقیقاً می‌دانیم چه کسی مسئول است؟", 
     "Ja lopuksi, Maya, Teheran syyttää Yhdysvaltoja ja Israelia. Tiedetäänkö todella kuka on vastuussa?"),
    
    ("00:04:46.400", "00:04:52.000", 
     "First, we have the Israeli military: They say they were not aware of any attack happening in the area.", 
     "نخست، ارتش اسرائیل می‌گوید از وقوع هرگونه حمله‌ای در این منطقه بی‌اطلاع بوده است.", 
     "Ensinnäkin Israelin armeija: He sanovat, etteivät tienneet mistään iskusta alueella."),
    
    ("00:04:52.000", "00:04:57.280", 
     "We have the Pentagon: The Pentagon says that it is currently investigating the incident.", 
     "پنتاگون نیز اعلام کرده که در حال حاضر مشغول بررسی این حادثه است.", 
     "Pentagon: Pentagon ilmoittaa tutkivansa tapausta parhaillaan."),
    
    ("00:04:57.280", "00:05:03.040", 
     "And we have US Secretary of State Marco Rubio, who was asked about it yesterday, and he said", 
     "و مارکو روبیو وزیر امور خارجه آمریکا، دیروز در این باره مورد سوال قرار گرفت و گفت", 
     "Ja Yhdysvaltain ulkoministeri Marco Rubio sanoi eilen kysyttäessä,"),
    
    ("00:05:03.040", "00:05:09.040", 
     "that the US would not deliberately target a school, before adding that the Iranians, on the other hand,", 
     "ایالات متحده هرگز عمداً مدرسه‌ای را هدف قرار نمی‌دهد، و افزود که از سوی دیگر ایرانی‌ها", 
     "ettei USA tahallaan iskisi kouluun, lisäten että iranilaiset toisaalta"),
    
    ("00:05:09.040", "00:05:15.200", 
     "according to him, are targeting civilian infrastructure, without adding any link to this school strike.", 
     "به ادعای او زیرساخت‌های غیرنظامی را هدف می‌گیرند، بدون اینکه ارتباطی با این حمله به مدرسه ذکر کند.", 
     "hänen mukaansa kohdistavat iskuja siviilikohteisiin, liittämättä sitä suoraan tähän kouluiskuun."),
    
    ("00:05:15.200", "00:05:22.640", 
     "Online, some users suggested that the school was targeted not by the US or Israel, but rather by Iran,", 
     "در فضای مجازی برخی کاربران ادعا کردند مدرسه نه توسط آمریکا یا اسرائیل، بلکه توسط خود ایران هدف قرار گرفته،", 
     "Verkossa jotkut väittivät, ettei iskua tehnyt USA tai Israel, vaan pikemminkin Iran itse,"),
    
    ("00:05:22.640", "00:05:31.200", 
     "explaining that this was a failed rocket launch from the IRGC.", 
     "و گفتند این حادثه ناشی از شلیک ناموفق راکت سپاه بوده است.", 
     "väittäen kyseessä olleen kaartin epäonnistunut ohjuslaukaisu."),
    
    ("00:05:31.200", "00:05:39.360", 
     "But researchers managed to prove that the video shown as evidence to explain it was Iran", 
     "اما محققان موفق شدند اثبات کنند ویدیویی که به عنوان مدرک برای متهم کردن ایران نشان داده شده،", 
     "Mutta tutkijat todistivat, että todisteena näytetty video"),
    
    ("00:05:39.360", "00:05:45.040", 
     "is actually showing another region in Iran: Zanjan —", 
     "در واقع مربوط به منطقه‌ای دیگر در ایران یعنی زنجان است —", 
     "esittää itse asiassa toista aluetta Iranissa: Zanjania –"),
    
    ("00:05:45.040", "00:05:52.960", 
     "that is 1,300 kilometers in the opposite direction from where the strike took place.", 
     "که ۱۳۰۰ کیلومتر در جهت کاملاً مخالف مکانی است که این حمله رخ داد.", 
     "joka on 1 300 kilometriä vastakkaiseen suuntaan iskun tapahtumapaikasta."),
    
    ("00:05:52.960", "00:05:59.440", 
     "So these are unrelated pictures showing a misfire elsewhere, not in Minab.", 
     "بنابراین این‌ها تصاویری بی‌ربط از شلیکی ناموفق در جایی دیگر است، نه در میناب.", 
     "Nämä ovat siis täysin erillisiä kuvia laukaisuvirheestä muualla, eivät Minabista."),
    
    ("00:05:59.440", "00:06:07.680", 
     "And finally, there is another viral post seen 6 million times on X claiming Tehran admitted responsibility on Telegram.", 
     "و در پایان، پست وایرال دیگری با ۶ میلیون بازدید در اکس مدعی شد تهران در تلگرام مسئولیت را پذیرفته است.", 
     "Ja lopuksi, toinen 6 miljoonaa kertaa katsottu viraalipostaus väitti Teheranin myöntäneen vastuun Telegramissa."),
    
    ("00:06:07.680", "00:06:14.080", 
     "But if you look into this account, you will see very clearly that this Telegram account has no link to Iranian authorities.", 
     "اما اگر این حساب را بررسی کنید، کاملاً روشن است که این کانال تلگرامی هیچ پیوندی با مقامات ایرانی ندارد.", 
     "Mutta jos tutkitaan tätä tiliä, näkyy selvästi, ettei Telegram-kanavalla ole yhteyttä viranomaisiin."),
    
    ("00:06:14.080", "00:06:19.680", 
     "It is an opposition outlet well known for mixing information and satire.", 
     "این یک رسانه اپوزیسیون است که به ترکیب اخبار و مطالب طنز شهرت دارد.", 
     "Se on oppositiomedia, joka tunnetaan uutisten ja satiirin sekoittamisesta."),
    
    ("00:06:19.680", "00:06:25.120", 
     "Thanks, Maya. Maya there with tonight's Truth or Fake.", 
     "ممنون مایا؛ مایا با بخش «حقیقت یا ساختگی» امشب.", 
     "Kiitos Maya; Maya ja illan Totuus vai tarua -katsaus."),
    
    ("00:06:25.120", "00:06:28.480", 
     "Do stay with us, we will be right back after this short break.", 
     "با ما بمانید، پس از وقفه‌ای کوتاه بازخواهیم گشت.", 
     "Pysykää seurassamme, palaamme heti lyhyen tauon jälkeen.")
]

en_lines = ["WEBVTT\n"]
fa_lines = ["WEBVTT\n"]
fi_lines = ["WEBVTT\n"]

for i, (start, end, en, fa, fi) in enumerate(cues, 1):
    en_lines.append(f"\n{i}\n{start} --> {end}\n{en}\n")
    fa_lines.append(f"\n{i}\n{start} --> {end}\n{fa}\n")
    fi_lines.append(f"\n{i}\n{start} --> {end}\n{fi}\n")

with open(os.path.join(target_dir, "en.vtt"), "w", encoding="utf-8") as f:
    f.writelines(en_lines)

with open(os.path.join(target_dir, "fa.vtt"), "w", encoding="utf-8") as f:
    f.writelines(fa_lines)

with open(os.path.join(target_dir, "fi.vtt"), "w", encoding="utf-8") as f:
    f.writelines(fi_lines)

print(f"✅ Generated all {len(cues)} cues perfectly matching 00:00.000 to 06:28.480.")
