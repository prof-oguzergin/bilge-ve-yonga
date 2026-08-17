# -*- coding: utf-8 -*-
"""Bilge ve Yonga sitesini kurar: her kitap icin tarayici okuyucu (okuyucu/) +
ana sayfa (index.html). Gorseller depodaki gercek dosyalara baglanir; serit icin
kucuk jpg'ler uretilir. Yeni kitap eklerken BOOKS listesine bir satir ekleyip calistir."""
import hashlib, io, json, re, zipfile
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape
from PIL import Image

REPO = Path(__file__).resolve().parent
OKU = REPO / 'okuyucu'
THUMBS = OKU / 'thumbs'
OKU.mkdir(exist_ok=True)
THUMBS.mkdir(exist_ok=True)

# Okuyucudaki konusan kalibi ({B}"..." / {Y}"...") ilk kapanan tirnakta durur.
# Bir replik icinde ikinci bir cift tirnak acilirsa kalip repligi ortasindan
# keser; gerisi renksiz, simgesiz duz metin olarak kalir. Kirilmanin izi nettir:
# yakalanan replik boslukla biter ('"Buna "' gibi). Anlatiya dusen tirnaklar
# (... dedi. Bu "ANLA" adimiydi.) kalibi bozmaz, uyari uretmez. Terimi vurgulamak
# icin replik icinde tirnak degil **kalin** kullanilir.
UYARILAR = []


def replik_denetle(kitap, no, text):
    for m in re.finditer(r'\{[BYD]\}"([^"]*)"', text):
        if m.group(1) != m.group(1).strip():
            UYARILAR.append('%s S%s: replik icinde ikinci tirnak aciliyor -> %s'
                            % (kitap, no, m.group(0)[:46]))

# Seri kimlikleri: (baslik, aciklama, seri-rengi). Anahtar = kitap numarasinin
# noktadan onceki kismi ('1' -> Alt Seri 1). Yeni seri eklerken buraya bir satir ekle.
SERIES = {
    '1': ('Kumdan Bilgisayara',
          'Bir yonga nasıl doğar, bilgisayar nasıl çalışır ve nasıl düşünmeyi öğrenir.',
          '#2E8CC7'),
    '2': ('Hız ve Güç',
          'Bir bilgisayarı hızlı ve güvenilir yapan nedir? Başarımın sırları.',
          '#D97326'),
    '3': ('Buyrukların Dünyası',
          'Bir bilgisayara ne yapacağını nasıl söyleriz? Buyrukların dili.',
          '#2E9E5B'),
    # 4. seri MOR kimliktedir (eflatundan koyu mora). Kitaplari BOOKS listesine
    # eklenene kadar bu seri sayfada gorunmez, build_index bos seriyi atlar.
    # Kart sirasi (10 kitap): #9B5FD0 #8F57C2 #834EB4 #7746A7 #6B3E99
    #                        #5E358B #522D7D #462570 #3A1C62 #2E1454
    '4': ('İşlemcinin İçi',
          'İşlemcinin kapağını açıyoruz: toplayan, taşıyan ve herkese işaret veren parçalar.',
          '#8A4FC0'),
}

# (klasor, no, baslik, alt-baslik, vurgu-renk)
# Alt Seri 1 mavi kimliktedir: her kitap camgobeginden civit maviye uzanan bir mavi tonu.
# Alt Seri 2 turuncu kimliktedir: kehribardan kiremit turuncusuna uzanan tonlar.
# ─── Kahraman destesi ────────────────────────────────────────────────────────
# Ondeki kart hep ayni (ilk izlenim ve serinin girisi), arkadaki dort kart
# her sayfa yuklenisinde bu havuzdan rastgele cekilir. Havuz elle secildi:
# kucuk egik kartta guclu duran, birbirine benzemeyen, uc seriyi de temsil
# eden kapaklar. Kapaklar 900 piksele olceklenir; 480 piksellik kapaklar
# yogun ekranlarda bulanik kaliyordu.
DESTE_ON = 'kitap1.01a'
DESTE_HAVUZ = ['kitap1.02a', 'kitap1.09', 'kitap2.02', 'kitap2.04', 'kitap2.06',
               'kitap2.10', 'kitap3.01b', 'kitap3.07', 'kitap3.08', 'kitap3.11']
DESTE_ARKA = 4            # ondeki kartin arkasinda kac kart durur
DESTE_GENISLIK = 900      # piksel

BOOKS = [
    ('kitap1.01a-kumdan-bilgisayar', '1.1a', 'Kumdan Bilgisayar',
     'Bir avuç kumdan yongaya uzanan üretim yolculuğu', '#2B93D1'),
    ('kitap1.01b-bazen-gecer-bazen-gecmez', '1.1b', 'Bazen Geçer, Bazen Geçmez',
     'Silisyum neden seçildi: yarı iletken ve transistörün doğuşu', '#2889C6'),
    ('kitap1.01c-anahtarlardan-mantik-kapilarina', '1.1c',
     'Anahtarlardan Mantık Kapılarına',
     'VE, VEYA, DEĞİL: anahtarlardan kurulan üç mantık kapısı', '#2784C0'),
    ('kitap1.02a-milyarlarca-kucuk-anahtar', '1.2a', 'Milyarlarca Küçük Anahtar',
     'Transistörler, açık-kapalı anahtarlar ve ikili sayılar', '#267FBA'),
    ('kitap1.02b-ayni-rakam-baska-deger', '1.2b', 'Aynı Rakam, Başka Değer',
     'Basamak değeri: aynı rakam nerede durduğuna göre başka değer taşır',
     '#257AB5'),
    ('kitap1.02c-dunyanin-butun-harfleri', '1.2c', 'Dünyanın Bütün Harfleri',
     'Unicode ve UTF-8: her işarete bir numara, numaraya göre valiz',
     '#2477B2'),
    ('kitap1.03-bilgisayarin-bes-arkadasi', '1.3', 'Bilgisayarın Beş Arkadaşı',
     'İşlemci, bellek, depo, giriş ve çıkış', '#2375AF'),
    ('kitap1.04-al-anla-yap', '1.4', 'Al, Anla, Yap!',
     'Bir bilgisayar buyrukları nasıl adım adım işler', '#216BA3'),
    ('kitap1.05-soganin-katmanlari', '1.5', 'Soğanın Katmanları',
     'Donanımdan uygulamalara yazılımın katmanları', '#1E6298'),
    ('kitap1.06-moorenun-sihirli-takvimi', '1.6', 'Moore’un Sihirli Takvimi',
     'Moore Yasası ve transistörlerin çoğalışı', '#1B588D'),
    ('kitap1.07-iki-kardes-risc-ve-cisc', '1.7', 'İki Kardeş: RISC ve CISC',
     'İki buyruk kümesi ailesi: az ama hızlı, çok ama güçlü', '#194E81'),
    ('kitap1.08-acik-kapi', '1.8', 'Açık Kapı',
     'Açık kaynak donanım ve RISC-V: paylaşınca herkes büyür', '#164476'),
    ('kitap1.09-bilgisayarin-atesi', '1.9', 'Bilgisayarın Ateşi',
     'Güç, ısı ve güç duvarı: bilgisayar neden ısınır', '#143A6A'),
    ('kitap1.10-bilgisayar-dusunmeyi-ogreniyor', '1.10', 'Bilgisayar Düşünmeyi Öğreniyor',
     'Yapay zeka hızlandırıcıları: CPU, GPU, TPU, NPU', '#11305F'),
    ('kitap1.11-bilgisayardan-once', '1.11', 'Bilgisayardan Önce',
     'Abaküsten mikroişlemciye: makineler nasıl bilgisayara dönüştü',
     '#0E2A54'),
    ('kitap2.01-uzaydaki-bilgisayar', '2.1', 'Uzaydaki Bilgisayar',
     'Güvenilirlik, kozmik ışınlar ve Mars’taki Curiosity', '#E08A2E'),
    ('kitap2.02-davulcu-ve-kurekciler', '2.2', 'Davulcu ve Kürekçiler',
     'Saat vuruş sıklığı, buyruk sayısı ve BBÇ: başarım denklemi', '#D97326'),
    ('kitap2.03-dunyanin-en-hizli-mutfagi', '2.3', 'Dünyanın En Hızlı Mutfağı',
     'Gecikme, işlem hacmi ve koşutluk: aşçılar gibi çekirdekler', '#C85F1F'),
    ('kitap2.04-corumlu-orhan-ile-edirneli-orhan', '2.4', 'Çorumlu Orhan ile Edirneli Orhan',
     'Adım boyu × tempo: bir adımda yapılan iş ile saat hızı', '#C04F18'),
    ('kitap2.05-ayakkabi-bagini-hizli-baglasan', '2.5', 'Ayakkabı Bağını Hızlı Bağlasan Ne Olur?',
     'Amdahl Yasası: en büyük parçayı, darboğazı hızlandır', '#B84812'),
    ('kitap2.06-yaris-pisti', '2.6', 'Yarış Pisti',
     'Sınama programları ve SPEC: bilgisayarları adil karşılaştırmak', '#B0400E'),
    ('kitap2.07-altin-cag-ve-duvar', '2.7', 'Altın Çağ ve Duvar',
     'Altın çağ, güç duvarı ve çok çekirdeğe geçiş', '#A8380A'),
    ('kitap2.08-gustafsonun-bahcesi', '2.8', 'Gustafson\'un Bahçesi',
     'Gustafson Yasası: daha çok çekirdekle daha büyük iş', '#A0300B'),
    ('kitap2.09-dar-gecit', '2.9', 'Dar Geçit',
     'Bellek duvarı ve önbellek: hızlı işlemci, yavaş bellek', '#982A0B'),
    ('kitap2.10-kim-daha-hizli', '2.10', 'Kim Daha Hızlı?',
     'Her iş için doğru araç: telefondan süper bilgisayara', '#90240B'),
    ('kitap3.01a-dedigimi-yap', '3.1a', 'Dediğimi Yap',
     'Program nedir: bilgisayara iş adım adım ve kesin anlatılır',
     '#33A866'),
    ('kitap3.01b-iki-dunyanin-koprusu', '3.1b', 'İki Dünyanın Köprüsü',
     'Buyruk kümesi mimarisi: yazılım ile donanımın ortak dili', '#2E9E5B'),
    ('kitap3.02-siranin-ustundeki-kalemler', '3.2', 'Sıranın Üstündeki Kalemler',
     'Yazmaçlar, bellek düzeni ve bayt sırası', '#2C9553'),
    ('kitap3.03-zarfin-ustundeki-bolmeler', '3.3', 'Zarfın Üstündeki Bölmeler',
     'Buyruk biçimleri ve adresleme kipleri', '#2A8C4E'),
    ('kitap3.04-parkta-kavsak', '3.4', 'Parkta Kavşak',
     'Dallanma, döngüler ve altyordamlar', '#277F49'),
    ('kitap3.05-mektup-fabrikasi', '3.5', 'Mektup Fabrikası',
     'Derleme zinciri: derleyici, çevirici, bağlayıcı', '#24763F'),
    ('kitap3.06-toplama-makinesi', '3.6', 'Toplama Makinesi',
     'Aritmetik buyruklar: toplama, çıkarma, çarpma', '#216D3A'),
    ('kitap3.07-sihirli-maskeler', '3.7', 'Sihirli Maskeler',
     'Mantık buyrukları: VE, VEYA, DEĞİL ve bit maskeleri', '#1E6435'),
    ('kitap3.08-sifirin-gucu', '3.8', 'Sıfırın Gücü',
     'x0 yazmacı: hep sıfır kalan güvenilir arkadaş', '#1B5B30'),
    ('kitap3.09-kulelerin-oyunu', '3.9', 'Kulelerin Oyunu',
     'Yığıt ve altyordamlar: son giren ilk çıkar', '#195B2C'),
    ('kitap3.10a-tasiyicilar', '3.10a', 'Taşıyıcılar',
     'Yükle ve sakla: bellek ile yazmaç arasındaki yolculuk', '#175229'),
    ('kitap3.10b-programin-bellekteki-mahallesi', '3.10b', 'Programın Bellekteki Mahallesi',
     'Buyruk, veri, yığın ve yığıt: çalışan programın bellekteki yerleşimi', '#175229'),
    ('kitap3.11-dedektif-bilge-ve-kayip-sonuc', '3.11', 'Dedektif Bilge ve Kayıp Sonuç',
     'Hata ayıklama: ara nokta, adım adım yürütme, yazmaçlara bakmak', '#144822'),
    ('kitap4.01a-eldenin-yolculugu', '4.1a', 'Eldenin Yolculuğu',
     'Toplayıcılar ve eldenin basamaktan basamağa yolculuğu', '#9B5FD0'),
    ('kitap4.01b-yonganin-eksi-derdi', '4.1b', "Yonga'nın Eksi Derdi",
     'Eksi sayılar bitlerle nasıl yazılır: sıfırdan bir geri ve ikiye tümleyen',
     '#9559C9'),
    ('kitap4.02-cok-yonlu-alet-amb', '4.2', 'Çok Yönlü Alet: AMB',
     'Aritmetik Mantık Birimi: tek alette toplama, çıkarma, karşılaştırma', '#8F57C2'),
    ('kitap4.03-uzun-isler-carpma-bolme', '4.3', 'Uzun İşler: Çarpma ve Bölme',
     'Kaydır ve topla, kaydır ve çıkar: uzun işlemlerin donanımı', '#834EB4'),
    ('kitap4.04a-virgulun-dansi', '4.4a', 'Virgülün Dansı',
     'Kayan nokta: işaret, üs ve kesirle dev ve minik sayılar', '#7746A7'),
    ('kitap4.04b-bir-bit-nasil-hatirlar', '4.4b', 'Bir Bit Nasıl Hatırlar?',
     'Halka, mandal, saat ve yazmaç: bir bit nasıl saklanır', '#7746A7'),
    ('kitap4.05-veri-yolu-fabrikasi', '4.5', 'Veri Yolu Fabrikası',
     'İşlemcinin beş istasyonu ve onları bağlayan teller', '#6B3E99'),
    ('kitap4.06-bir-buyrugun-yolculugu', '4.6', 'Bir Buyruğun Yolculuğu',
     'Bir buyruğun yedi durağı: getir, çöz, yürüt, geri yaz', '#5E358B'),
    ('kitap4.07-orkestra-sefi-denetim-birimi', '4.7', 'Orkestra Şefi: Denetim Birimi',
     'Her parçaya doğru zamanda doğru işareti veren şef', '#522D7D'),
    ('kitap4.08-tek-vurusta', '4.8', 'Tek Vuruşta',
     'Tek vuruşluk işlemci: her buyruk tek saat vuruşunda biter, ama beklenir', '#462570'),
    ('kitap4.09-adim-adim', '4.9', 'Adım Adım',
     'Çok vuruşluk işlemci: buyruğu küçük adımlara bölmek, kısa buyruk çabuk biter', '#3A1C62'),
    ('kitap4.10-icindeki-minik-buyruklar', '4.10', 'İçindeki Minik Buyruklar',
     'Mikroprogram: şefin küçük bir bellekten okuduğu minik adımlar', '#2E1454'),
    ('kitap4.11-bir-seferde-kac-bit', '4.11', 'Bir Seferde Kaç Bit?',
     'Sözcük boyu ve adres yolu: bir seferde ne kadarı taşınır, kaç göze ulaşılır',
     '#241046'),
]


def make_thumb(src_png, out_jpg, w=240, q=72):
    im = Image.open(src_png).convert('RGB')
    h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(out_jpg, 'JPEG', quality=q)


def find_pdf(folder_dir):
    pdfs = sorted(folder_dir.glob('*.pdf'))
    return pdfs[0].name if pdfs else None


# Deneme Zamani sayfasinin afisi. Ilk afis ikilik sayilar kitabi icin
# cizilmisti, ortasinda dort basamak kutusu var; butun kitaplarda ayni afis
# cikinca o kutular anlamsiz kaliyordu. Dort kutulu afis kendi kitabinda,
# otekiler konudan bagimsiz afiste.
DENEME_AFIS = {
    'kitap1.02b-ayni-rakam-baska-deger': 'deneme-afisi.jpg',
}


# Okuyucuda beliren kucuk deneme alanlari. Kitap klasoru -> HTML.
# Dis kitaplik yok, ag istegi yok; cevrimdisi da calisir.
DENEME_WIDGET = {
    # Kitap klasoru -> okuyucuda beliren deneme alaninin turu.
    # Kap bos gelir, icini okuyucunun kendi betigi kurar; HTML'e
    # <script> gomulmez (gomulen betik calismaz ve sayfayi kirar).
    'kitap1.02b-ayni-rakam-baska-deger':
        '<div class="dene" data-dene="basamak"></div>',
    'kitap1.01c-anahtarlardan-mantik-kapilarina':
        '<div class="dene" data-dene="kapi"></div>',
    # 1.02a ikili sayilari anlattigi icin ayni denemede sayilar da gorunur.
    # 1.01c'de gorunmez: o kitap 1.02a'dan once geliyor ve sifir-bir dilini
    # bilerek kullanmiyor.
    'kitap1.02a-milyarlarca-kucuk-anahtar':
        '<div class="dene" data-dene="kapi" data-sayi="1"></div>',
}

def _damga(yol):
    """Görsel adresine dosyanın içeriğinden türeyen bir sürüm damgası ekler.

    Hizmet çalışanı görselleri adrese göre kalıcı önbelleğe alıyor. Bir kare
    düzeltilip aynı adla yayımlanınca okur eski kareyi görmeye devam
    ediyordu (9 Ağu 2026'da 1.02b'nin altı parmaklı elleri böyle yaşandı).
    İçerik değişince adres de değişsin ki önbellek kendiliğinden ıskalasın.
    """
    try:
        h = hashlib.md5(Path(yol).read_bytes()).hexdigest()[:8]
    except OSError:
        return ''
    return '?v=' + h


def parse_book(folder, no, title, subtitle):
    d = REPO / folder
    md = (d / (folder + '.md')).read_text(encoding='utf-8')
    res = d / 'resimler'
    key = 'k' + no.replace('.', '')  # 1.7 -> k17
    pages = []

    # kapak
    make_thumb(res / 'GPT_Kapak.jpg', THUMBS / f'{key}_K.jpg')
    pages.append({
        'type': 'cover',
        'eyebrow': f'Bilge ve Yonga · Kitap {no}',
        'title': title,
        'sub': subtitle,
        'img': f'../{folder}/resimler/GPT_Kapak.jpg' + _damga(res / 'GPT_Kapak.jpg'),
        'thumb': f'thumbs/{key}_K.jpg',
    })

    # sayfalar
    for b in re.split(r'\n## ', md):
        m = re.match(r'Sayfa (\d+)(?:\s*[—–-]\s*(.+))?', b)
        if not m:
            continue
        n = int(m.group(1))
        ttl = (m.group(2) or '').strip()
        # Metin ya alt satirda ya da **Metin:** ile ayni satirda baslar
        # (3.11 ayni satir bicimini kullaniyor). Her ikisini de kabul et.
        tm = re.search(r'\*\*Metin:\*\*[ \t]*\n?(.+?)\n\s*\n\*\*Resim', b, re.S)
        text = tm.group(1).strip() if tm else ''
        # Madde imleri: kaynak markdown '-' kullaniyor ama ne okuyucu ne PDF
        # markdown listesi cozuyor; ham '-' metne sizmasin diye gercek
        # madde isaretine cevriliyor.
        text = re.sub(r'(?m)^[-*+] ', '• ', text)
        replik_denetle(folder, n, text)
        png = res / f'GPT_Sayfa_{n}.jpg'
        if not png.exists():
            continue
        make_thumb(png, THUMBS / f'{key}_{n}.jpg')
        pages.append({'type': 'page', 'no': n, 'title': ttl, 'text': text,
                      'img': f'../{folder}/resimler/GPT_Sayfa_{n}.jpg' + _damga(png),
                      'thumb': f'thumbs/{key}_{n}.jpg'})

    # bugun ne ogrendik
    sm = re.search(r'## Bugün Ne Öğrendik\?\s*\n(.+?)(?:\n\s*---|\Z)', md, re.S)
    if sm:
        lines = [re.sub(r'^[-*+\u2022]\s+', '', ln.strip())
                 for ln in sm.group(1).strip().split('\n') if ln.strip()]
        pages.append({'type': 'summary', 'title': 'Bugün Ne Öğrendik?', 'lines': lines})

    # deneme zamani (bolum sonu sorulari)
    dm = re.search(r'## Deneme Zamanı\s*\n(.+?)(?:\n\s*---|\Z)', md, re.S)
    if dm:
        ham = dm.group(1).strip()
        sorular, yanitlar = [], []
        hedef = sorular
        for ln in ham.split('\n'):
            ln = ln.strip()
            if not ln:
                continue
            if ln.startswith('**Yanıtlar**'):
                hedef = yanitlar
                continue
            hedef.append(re.sub(r'^\d+\.\s*', '', ln))
        pages.append({'type': 'deneme', 'title': 'Deneme Zamanı',
                      'sorular': sorular, 'yanitlar': yanitlar,
                      'afis': DENEME_AFIS.get(folder, 'deneme-afisi-genel.jpg'),
                      'widget': DENEME_WIDGET.get(folder, '')})
    return pages


def _epub_bloklar(t):
    """Sayfa metnini <p>/<pre> bloklarina ayirir.

    (html, olculer) dondurur; olculer sabit duzende yazi boyu hesabi icin
    ('p', karakter) ya da ('kod', satir) ciftleridir. Bos satirla ayrilan
    paragraflar ayri <p> olur; eskiden hepsi tek <p> icinde birlesip
    paragraf araligi kayboluyordu.
    """
    # Konusan isaretleri yalnizca tarayici okuyucusunda gosteriliyor;
    # EPUB ve PDF'te temizleniyor.
    t = re.sub(r'\{[BYD]\}', '', t)
    kod = []

    def _sakla(m):
        kod.append(m.group(1).rstrip())
        return '\x00K%d\x00' % (len(kod) - 1)

    t = re.sub(r'```\n?([\s\S]*?)```', _sakla, t)

    html, olcu = [], []
    for par in re.split(r'\n\s*\n', t.strip()):
        par = par.strip()
        if not par:
            continue
        tek = re.fullmatch(r'\x00K(\d+)\x00', par)
        if tek:
            k = kod[int(tek.group(1))]
            html.append('<pre class="code">' + escape(k) + '</pre>')
            olcu.append(('kod', k.count('\n') + 1))
            continue
        s = escape(par)
        # paragrafin ortasina dusen kod parcasi <pre> olamaz, satir ici olur
        s = re.sub(r'\x00K(\d+)\x00',
                   lambda m: '<code class="cmd">' + escape(kod[int(m.group(1))]) + '</code>', s)
        s = re.sub(r'`([^`\n]+)`', r'<code class="cmd">\1</code>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<em class="term">\1</em>', s)
        html.append('<p>' + s.replace('\n', ' ') + '</p>')
        olcu.append(('p', len(par)))
    return ''.join(html), olcu


def _yazi_boyu(olcu, genislik, butce, boylar, satir=1.5, ara=0.5):
    """Bloklarin tahmini yuksekligi butceye sigan en buyuk yazi boyunu secer.

    Sabit duzende sayfa tasmasi metni kirpar, bu yuzden boy pesin hesaplanir.
    Karakter genisligi olcut olarak 0.52 em alinir (Georgia, Turkce metin).
    """
    for fs in boylar:
        kps = max(8, int(genislik / (fs * 0.52)))
        satirlar = 0
        for tur, deger in olcu:
            satirlar += deger if tur == 'kod' else max(1, -(-deger // kps))
        h = satirlar * fs * satir + max(0, len(olcu) - 1) * fs * ara
        if h <= butce:
            return fs
    return boylar[-1]


def _jpeg_bytes(path, w=1400, q=82):
    im = Image.open(path).convert('RGB')
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    bio = io.BytesIO(); im.save(bio, 'JPEG', quality=q)
    return bio.getvalue()


def _parse_pages_local(folder, no, title, subtitle):
    """EPUB icin: gorsel dosya yollari + metin dondurur."""
    d = REPO / folder
    md = (d / (folder + '.md')).read_text(encoding='utf-8')
    res = d / 'resimler'
    pages = [{'kind': 'cover', 'img': res / 'GPT_Kapak.jpg'}]
    for b in re.split(r'\n## ', md):
        m = re.match(r'Sayfa (\d+)(?:\s*[—–-]\s*(.+))?', b)
        if not m:
            continue
        n = int(m.group(1)); ttl = (m.group(2) or '').strip()
        # Metin ya alt satirda ya da **Metin:** ile ayni satirda baslar
        # (3.11 ayni satir bicimini kullaniyor). Her ikisini de kabul et.
        tm = re.search(r'\*\*Metin:\*\*[ \t]*\n?(.+?)\n\s*\n\*\*Resim', b, re.S)
        text = tm.group(1).strip() if tm else ''
        # Madde imleri: kaynak markdown '-' kullaniyor ama ne okuyucu ne PDF
        # markdown listesi cozuyor; ham '-' metne sizmasin diye gercek
        # madde isaretine cevriliyor.
        text = re.sub(r'(?m)^[-*+] ', '• ', text)
        png = res / f'GPT_Sayfa_{n}.jpg'
        if not png.exists():
            continue
        pages.append({'kind': 'page', 'no': n, 'title': ttl, 'text': text, 'img': png})
    sm = re.search(r'## Bugün Ne Öğrendik\?\s*\n(.+?)(?:\n\s*---|\Z)', md, re.S)
    if sm:
        lines = [re.sub(r'^[-*+\u2022]\s+', '', ln.strip())
                 for ln in sm.group(1).strip().split('\n') if ln.strip()]
        pages.append({'kind': 'summary', 'lines': lines})
    return pages


# ─── EPUB hak bildirimleri ───────────────────────────────────────────────────
# Metinler Av. Mehmet Arın Gülüm'ün uygulama şartnamesinin H.2 ve H.3
# bölümlerinden BİREBİR alınmıştır; sözcükleri değiştirilmez.
EPUB_HAKLAR = (
    '© 2026 Prof. Dr. Oğuz Ergin. Bu eser Creative Commons '
    'Atıf-GayriTicari-Türetilemez 4.0 Uluslararası (CC BY-NC-ND 4.0) lisansı '
    'ile açık erişime sunulmuştur '
    '(https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr). '
    'Lisansın kapsamadığı tüm haklar saklıdır: "Bilge ve Yonga" seri adı, '
    '"Bilge" ve "Yonga" karakter adları ile figürleri, marka hakları, eser '
    'sahibinin adı ve unvanı ve manevi haklar lisans kapsamı dışındadır. '
    'Metin ve veri madenciliği ile yapay zekâ modeli eğitimi bakımından '
    'haklar açıkça saklı tutulmuştur. Ticari kullanım izni: '
    'bilgi@oguzergin.net'
)
EPUB_KATKI = (
    'Prof. Dr. Oğuz Ergin (görsel yönetimi: karakter föyü, seçim ve '
    'düzenleme; görseller yapay zekâ araçlarıyla üretilmiştir)'
)
CC_URI = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'

# Sabit duzen (fixed-layout) sayfa olcusu. Resimler 16:9 oldugu icin sayfa da
# 16:9: boylece resim kenar bosluksuz oturur ve Apple Books sayfayi iki sutuna
# bolmez. Yeniden akan (reflowable) kipte iPad yatayken bir ekranda iki kitap
# sayfasi goruluyor, kapak da sutun genisligine kuculuyordu.
EP_W, EP_H = 1400, 788

EPUB_CSS = """@charset "utf-8";
html,body{margin:0;padding:0;width:1400px;height:788px;overflow:hidden}
body{background:#0a0e20;color:#2b2440;-webkit-text-size-adjust:none;
  font-family:"Andika",Georgia,"Times New Roman",serif}
.pg{position:absolute;top:0;left:0;width:1400px;height:788px;overflow:hidden}
.pg img{position:absolute;top:0;left:0;width:1400px;height:788px;margin:0;padding:0}
.band{position:absolute;left:0;bottom:0;width:1400px;box-sizing:border-box;
  padding:22px 44px 26px;color:#fff;
  background:-webkit-linear-gradient(top,rgba(23,32,110,.56),rgba(23,32,110,.86));
  background:linear-gradient(to bottom,rgba(23,32,110,.56),rgba(23,32,110,.86))}
.band p{margin:0;padding:0}
.band p+p{margin-top:.5em}
.band .term{font-style:normal;font-weight:700;color:#FFC978}
.band .cmd{font-family:"Courier New",monospace;color:#9FE8C4;
  background:rgba(255,255,255,.12);padding:0 .22em;border-radius:4px}
.band .code{display:block; font-family:"Courier New",monospace;color:#D6E9FF;white-space:pre;
  background:rgba(0,0,0,.34);padding:.5em .7em;border-radius:8px;margin:.5em 0 0}
.sum{position:absolute;top:0;left:0;width:1400px;height:788px;box-sizing:border-box;
  background:#FBF2E1;color:#33294A;padding:38px 68px}
.sum h2{font-family:"Helvetica Neue",Arial,sans-serif;color:#182253;
  font-size:34px;line-height:1.15;margin:0 0 22px}
.sum ul{list-style:none;padding:0;margin:0}
.sum li{border-left:3px solid #f3ac2e;padding:.1em 0 .1em .7em;margin:0 0 .5em}
.sum li:last-child{margin-bottom:0}
.sum .term{font-style:normal;font-weight:700;color:#C24A18}
.sum .telif{position:absolute;left:0;bottom:20px;width:1400px;margin:0;
  text-align:center;font-size:15px;opacity:.55}
"""


def _xhtml(title_text, body):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="tr" lang="tr">\n'
            '<head><meta charset="utf-8"/>'
            f'<meta name="viewport" content="width={EP_W}, height={EP_H}"/>'
            '<title>' + escape(title_text) + '</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            '<body>' + body + '</body>\n</html>\n')



# Sartname B.1 — her sayfada ayni telif blogu (D.3 tutarlilik kurali)
BVY_TELIF_META = '''<!-- BVY-TELIF-BASLANGIC -->
<meta name="author" content="Prof. Dr. Oğuz Ergin">
<meta name="copyright" content="© 2026 Prof. Dr. Oğuz Ergin. Tüm eserler CC BY-NC-ND 4.0 lisansı ile açık erişime sunulmuştur. Lisansın kapsamadığı tüm haklar saklıdır.">
<link rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/">
<meta name="license" content="https://creativecommons.org/licenses/by-nc-nd/4.0/">
<meta name="dcterms.rightsHolder" content="Prof. Dr. Oğuz Ergin">
<meta name="tdm-reservation" content="1">
<meta name="tdm-policy" content="https://bilgeveyonga.oguzergin.net/tdm-policy.json">
<meta name="robots" content="index, follow, noai, noimageai">
<meta name="ai-content-declaration" content="no-training, no-mining">
<!-- BVY-TELIF-BITIS -->
'''

# Sartname D.5 — kitap sayfasi yapisal verisi (Book)
BVY_KITAP_LD = '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "Book",\n  "@id": "https://bilgeveyonga.oguzergin.net/okuyucu/__SLUG__.html#kitap",\n  "name": "__AD__",\n  "alternateName": "Bilge ve Yonga · Kitap __NO__",\n  "description": "__ACIKLAMA__",\n  "url": "https://bilgeveyonga.oguzergin.net/okuyucu/__SLUG__.html",\n  "inLanguage": "tr",\n  "bookFormat": "https://schema.org/EBook",\n  "numberOfPages": __SAYFA__,\n  "datePublished": "2026",\n  "author": {\n    "@type": "Person",\n    "@id": "https://oguzergin.net/#kisi",\n    "name": "Prof. Dr. Oğuz Ergin",\n    "url": "https://oguzergin.net"\n  },\n  "copyrightHolder": { "@id": "https://oguzergin.net/#kisi" },\n  "copyrightYear": 2026,\n  "copyrightNotice": "© 2026 Prof. Dr. Oğuz Ergin. Lisansın kapsamadığı tüm haklar saklıdır.",\n  "publisher": {\n    "@type": "Organization",\n    "name": "Bilge ve Yonga — Bilgisayar Mimarisi Çocuk Kitapları",\n    "url": "https://bilgeveyonga.oguzergin.net/"\n  },\n  "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/",\n  "usageInfo": "https://bilgeveyonga.oguzergin.net/telif-ve-lisans.html",\n  "isAccessibleForFree": true,\n  "creditText": "Ergin, O. (2026). Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi. https://bilgeveyonga.oguzergin.net",\n  "isPartOf": {\n    "@type": "CreativeWorkSeries",\n    "@id": "https://bilgeveyonga.oguzergin.net/#seri",\n    "name": "Bilge ve Yonga",\n    "url": "https://bilgeveyonga.oguzergin.net/"\n  },\n  "audience": {\n    "@type": "PeopleAudience",\n    "suggestedMinAge": 7,\n    "suggestedMaxAge": 12\n  },\n  "learningResourceType": "Hikâye kitabı",\n  "educationalUse": "Ders dışı okuma, sınıf içi okuma",\n  "associatedMedia": [\n    {\n      "@type": "MediaObject",\n      "encodingFormat": "application/pdf",\n      "contentUrl": "https://bilgeveyonga.oguzergin.net/__MEDYA__.pdf",\n      "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/",\n      "copyrightHolder": { "@id": "https://oguzergin.net/#kisi" },\n      "isAccessibleForFree": true\n    },\n    {\n      "@type": "MediaObject",\n      "encodingFormat": "application/epub+zip",\n      "contentUrl": "https://bilgeveyonga.oguzergin.net/__MEDYA__.epub",\n      "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/",\n      "copyrightHolder": { "@id": "https://oguzergin.net/#kisi" },\n      "isAccessibleForFree": true\n    }\n  ]\n}\n</script>'

def build_epub(folder, no, title, subtitle):
    d = REPO / folder
    pdf = find_pdf(d)
    epub_name = (Path(pdf).stem if pdf else title) + '.epub'
    pages = _parse_pages_local(folder, no, title, subtitle)

    files = {}          # arcname -> bytes
    manifest = []       # (id, href, media-type, extra)
    spine = []          # idref
    nav_items = []      # (href, label)
    imgcount = 0

    ilk_sayfa = 'cover.xhtml'   # landmarks icin ilk icerik sayfasi

    # her sayfayi xhtml + jpeg olarak uret
    for idx, p in enumerate(pages):
        if p['kind'] == 'cover':
            files['OEBPS/img/cover.jpg'] = _jpeg_bytes(p['img'], EP_W, 86)
            manifest.append(('img-cover', 'img/cover.jpg', 'image/jpeg', ' properties="cover-image"'))
            body = ('<div class="pg" epub:type="cover"><img src="img/cover.jpg" alt="' +
                    escape(title) + ' kapağı"/></div>')
            files['OEBPS/cover.xhtml'] = _xhtml(title, body).encode('utf-8')
            manifest.append(('cover', 'cover.xhtml', 'application/xhtml+xml', ''))
            spine.append('cover'); nav_items.append(('cover.xhtml', 'Kapak'))
        elif p['kind'] == 'summary':
            lis, olcu = '', []
            for ln in p['lines']:
                olcu.append(('p', len(ln)))
                lis += '<li>' + re.sub(r'\*\*(.+?)\*\*', r'<em class="term">\1</em>',
                                       escape(ln)) + '</li>'
            fs = _yazi_boyu(olcu, EP_W - 150, EP_H - 190,
                            [27, 25, 23, 21, 19, 17, 15], ara=0.75)
            body = ('<div class="sum"><h2>🎓 Bugün Ne Öğrendik?</h2>'
                    '<ul style="font-size:%dpx;line-height:1.5">%s</ul>'
                    '<p class="telif">© Oğuz Ergin · Bilge ve Yonga · CC BY-NC-ND 4.0</p>'
                    '</div>' % (fs, lis))
            files['OEBPS/summary.xhtml'] = _xhtml('Bugün Ne Öğrendik?', body).encode('utf-8')
            manifest.append(('summary', 'summary.xhtml', 'application/xhtml+xml', ''))
            spine.append('summary'); nav_items.append(('summary.xhtml', 'Bugün Ne Öğrendik?'))
        else:
            n = p['no']; imgcount += 1
            iid = 'img%d' % n; ihref = 'img/p%d.jpg' % n
            files['OEBPS/' + ihref] = _jpeg_bytes(p['img'], EP_W, 82)
            manifest.append((iid, ihref, 'image/jpeg', ''))
            ic, olcu = _epub_bloklar(p['text'])
            bant = ''
            if ic:
                fs = _yazi_boyu(olcu, EP_W - 96, 400, [31, 29, 27, 25, 23, 21, 19])
                bant = ('<div class="band" style="font-size:%dpx;line-height:1.5">%s</div>'
                        % (fs, ic))
            alt = ('Sayfa %d — %s' % (n, p['title'])) if p['title'] else ('Sayfa %d' % n)
            body = ('<div class="pg"><img src="%s" alt="%s"/>%s</div>'
                    % (ihref, escape(alt), bant))
            pid = 'page%d' % n; phref = 'page%d.xhtml' % n
            files['OEBPS/' + phref] = _xhtml('Sayfa %d' % n, body).encode('utf-8')
            manifest.append((pid, phref, 'application/xhtml+xml', ''))
            spine.append(pid)
            if ilk_sayfa == 'cover.xhtml':
                ilk_sayfa = phref
            nav_items.append((phref, alt))

    # Kunye sayfasi (sartname H.4). Metin G.2'den birebir; ek olarak
    # gorsellerin uretim yontemine iliskin seffaflik paragrafi.
    kunye = ('<div class="sum" style="font-size:19px;line-height:1.5">'
             '<h2>Künye</h2>'
             '<p><strong>© 2026 Prof. Dr. Oğuz Ergin</strong><br/>'
             + escape(title) + '<br/>'
             'Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi<br/>'
             'Ankara, 2026</p>'
             '<p>Bu eser, Creative Commons Atıf-GayriTicari-Türetilemez 4.0 '
             'Uluslararası (CC BY-NC-ND 4.0) lisansı ile açık erişime '
             'sunulmuştur.<br/>Lisans metni: '
             'https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr</p>'
             '<p><strong>LİSANSIN KAPSAMADIĞI TÜM HAKLAR SAKLIDIR.</strong> '
             '“Bilge ve Yonga” seri adı, “Bilge” ve “Yonga” karakter adları '
             'ile figürleri, seri amblemi, marka hakları, eser sahibinin adı '
             've unvanı ile manevi haklar bu lisansın kapsamı dışındadır ve '
             'ayrı yazılı izne bağlıdır.</p>'
             '<p>Metin ve veri madenciliği ile yapay zekâ modeli eğitimi '
             'bakımından haklar açıkça saklı tutulmuştur.</p>'
             '<p>Görseller, tek bir karakter föyüne sadık kalınarak yapay '
             'zekâ araçlarıyla üretilmiş ve tek tek elden geçirilmiştir; '
             'seçim, düzenleme ve görsel yönetimi eser sahibine aittir.</p>'
             '<p>Ticari kullanım izni ve sorularınız için: '
             'bilgi@oguzergin.net<br/>Telif ve lisans politikası: '
             'bilgeveyonga.oguzergin.net/telif-ve-lisans.html</p>'
             '<p>Atıf: Ergin, O. (2026). Bilge ve Yonga: Bilgisayar Mimarisi '
             'Çocuk Kitapları Serisi. https://bilgeveyonga.oguzergin.net</p>'
             '</div>')
    files['OEBPS/colophon.xhtml'] = _xhtml('Künye', kunye).encode('utf-8')
    manifest.append(('kunye', 'colophon.xhtml', 'application/xhtml+xml', ''))
    spine.append('kunye')
    nav_items.append(('colophon.xhtml', 'Künye'))

    files['OEBPS/style.css'] = EPUB_CSS.encode('utf-8')

    # nav.xhtml
    nav_ol = ''.join('<li><a href="%s">%s</a></li>' % (h, escape(l)) for h, l in nav_items)
    nav = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
           '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
           'xml:lang="tr" lang="tr"><head><meta charset="utf-8"/><title>' + escape(title) +
           '</title></head><body><nav epub:type="toc" id="toc"><h1>İçindekiler</h1><ol>' +
           nav_ol + '</ol></nav>\n'
           '<nav epub:type="landmarks" id="landmarks" hidden="hidden"><ol>'
           '<li><a epub:type="cover" href="cover.xhtml">Kapak</a></li>'
           '<li><a epub:type="bodymatter" href="' + ilk_sayfa + '">Başla</a></li>'
           '</ol></nav></body></html>\n')
    files['OEBPS/nav.xhtml'] = nav.encode('utf-8')
    manifest.insert(0, ('nav', 'nav.xhtml', 'application/xhtml+xml', ' properties="nav"'))
    manifest.append(('css', 'style.css', 'text/css', ''))

    # content.opf
    man = '\n'.join('  <item id="%s" href="%s" media-type="%s"%s/>' % (i, h, mt, ex)
                    for i, h, mt, ex in manifest)
    spn = '\n'.join('  <itemref idref="%s"/>' % s for s in spine)
    opf = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
           'unique-identifier="bookid" xml:lang="tr" '
           'prefix="tdm: http://www.w3.org/ns/tdmrep#">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           '  <dc:identifier id="bookid">urn:bilge-yonga:' + folder + '</dc:identifier>\n'
           '  <dc:title>' + escape(title) + '</dc:title>\n'
           '  <dc:creator>Ergin, Oğuz</dc:creator>\n'
           '  <dc:language>tr</dc:language>\n'
           '  <dc:publisher>Bilge ve Yonga — Bilgisayar Mimarisi Çocuk Kitapları</dc:publisher>\n'
           '  <dc:rights>' + EPUB_HAKLAR + '</dc:rights>\n'
           '  <dc:date>2026-07-13</dc:date>\n'
           '  <dc:subject>Bilgisayar mimarisi</dc:subject>\n'
           '  <dc:subject>Çocuk kitabı</dc:subject>\n'
           '  <dc:subject>Bilgisayar bilimi</dc:subject>\n'
           '  <dc:subject>Açık erişim</dc:subject>\n'
           '  <dc:contributor id="gorsel-yonetimi">' + EPUB_KATKI +
           '</dc:contributor>\n'
           '  <meta refines="#gorsel-yonetimi" property="role" '
           'scheme="marc:relators">art</meta>\n'
           '  <meta property="dcterms:rightsHolder">Prof. Dr. Oğuz Ergin</meta>\n'
           '  <meta property="dcterms:license">' + CC_URI + '</meta>\n'
           '  <link rel="cc:license" href="' + CC_URI + '"/>\n'
           '  <meta property="tdm:reservation">1</meta>\n'
           '  <meta property="tdm:policy">'
           'https://bilgeveyonga.oguzergin.net/tdm-policy.json</meta>\n'
           '  <dc:description>' + escape(subtitle) + '</dc:description>\n'
           '  <meta property="dcterms:modified">2026-07-26T00:00:00Z</meta>\n'
           '  <meta name="cover" content="img-cover"/>\n'
           # Sabit duzen: sayfa tasarlandigi gibi tek ekranda gorunur.
           # spread=none olmasa Apple Books iki sayfayi yan yana dizer.
           '  <meta property="rendition:layout">pre-paginated</meta>\n'
           '  <meta property="rendition:orientation">landscape</meta>\n'
           '  <meta property="rendition:spread">none</meta>\n'
           '</metadata>\n<manifest>\n' + man + '\n</manifest>\n'
           '<spine page-progression-direction="ltr">\n' + spn +
           '\n</spine>\n</package>\n')
    files['OEBPS/content.opf'] = opf.encode('utf-8')

    files['META-INF/container.xml'] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '  <rootfiles><rootfile full-path="OEBPS/content.opf" '
        'media-type="application/oebps-package+xml"/></rootfiles>\n</container>\n').encode('utf-8')

    # Eski iBooks surumleri rendition:layout yerine bu dosyaya bakiyor.
    files['META-INF/com.apple.ibooks.display-options.xml'] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<display_options>\n  <platform name="*">\n'
        '    <option name="fixed-layout">true</option>\n'
        '    <option name="open-to-spread">false</option>\n'
        '  </platform>\n</display_options>\n').encode('utf-8')

    out = d / epub_name
    with zipfile.ZipFile(out, 'w') as z:
        # mimetype ILK ve sikistirmasiz olmali
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        for arc, data in files.items():
            z.writestr(arc, data, compress_type=zipfile.ZIP_DEFLATED)
    return epub_name, imgcount + 1


READER_TPL = r'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bilge ve Yonga — __BRAND__</title>
<link rel="icon" href="../amblem.ico?v=2" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="../amblem-32.png?v=2">
<link rel="apple-touch-icon" href="../amblem-180.png?v=2">
<link rel="manifest" href="../manifest.json">
<script>if("serviceWorker" in navigator){addEventListener("load",function(){navigator.serviceWorker.register("../sw.js").catch(function(){});});}</script>
<!-- BVY-TELIF-BASLANGIC -->
<script src="../kunye.js" defer></script>
<!-- Olcum: izne bagli, varsayilan KAPALI. Sartname bolum J. -->
<script src="../olcum-tercihi.js" defer></script>
<!-- BVY-TELIF-BITIS -->
<meta name="theme-color" content="#0C1226">
<script>try{var _t=localStorage.getItem('theme');if(_t)document.documentElement.setAttribute('data-theme',_t);}catch(e){}</script>
<style>
@font-face{font-family:"Andika";src:url("../fontlar/Andika-Regular.woff2") format("woff2");
  font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Andika";src:url("../fontlar/Andika-Bold.woff2") format("woff2");
  font-weight:700;font-style:normal;font-display:swap}
:root{
  /* Varsayılan: karanlık (ana sayfadaki seçim localStorage ile devralınır) */
  --paper:#FBF2E1; --paper-ink:#33294A;
  --glow:#159FCB; --amber:#F3AC2E; --coral:#F16A50;
  --ground:#0C1226; --stage:#121b38; --chrome:#EAF0F6; --chrome-soft:#9AA6C6;
  --edge:rgba(180,200,240,.16); --shadow:rgba(0,0,0,.5);
  --ff-disp:"Segoe UI",Verdana,system-ui,sans-serif;
  /* Gövde fontu Andika: SIL'in okuma öğrenenler için tasarladığı, harfleri
     bilerek ayrılmış (I/İ/ı/l/1, G/C/Ç), tek katlı a ve g'li font. Georgia
     okunaklıydı ama yetişkin kitabı harfleriydi; bir okur çocuğunun harfleri
     karıştırdığını yazınca değiştirildi. OFL, siteye gömülebiliyor. */
  --ff-body:"Andika","Georgia",serif;
  /* Kağıt kartın içinde kullanılan renkler. Arayüz renkleri (--chrome)
     karanlık temada neredeyse beyaz; krem kağıt üzerinde okunmuyordu. */
  --kagit-koyu:#2A2340; --kagit-solgun:#6A6180;
  --kagit-cizgi:rgba(51,41,74,.22);
  --kehribar-koyu:#9C5A12; --parlak-koyu:#0C7699;
}
:root[data-theme="light"]{ --ground:#E7EEF3; --stage:#F3ECDD; --chrome:#182253; --chrome-soft:#5A6382;
  --edge:rgba(24,34,83,.14); --shadow:rgba(24,34,83,.20); }
:root[data-theme="dark"]{ --ground:#0C1226; --stage:#121b38; --chrome:#EAF0F6; --chrome-soft:#9AA6C6;
  --edge:rgba(180,200,240,.16); --shadow:rgba(0,0,0,.5); }

*{box-sizing:border-box}
body{margin:0}
.reader{
  min-height:100vh; color:var(--chrome);
  font-family:var(--ff-disp);
  display:flex; flex-direction:column;
  -webkit-font-smoothing:antialiased;
  background:
    radial-gradient(1200px 720px at 16% 10%, rgba(21,159,203,.11), transparent 62%),
    radial-gradient(1100px 820px at 86% 92%, rgba(241,106,80,.10), transparent 62%),
    var(--ground);
}
.progress{height:4px; background:transparent}
.progress i{display:block; height:100%; background:linear-gradient(90deg,var(--glow),var(--amber));
  width:0; transition:width .35s ease}

.bar{display:flex; align-items:center; gap:clamp(12px,1.2vw,20px);
  padding:clamp(14px,1.2vw,22px) clamp(20px,2vw,40px)}
.back{display:inline-flex; align-items:center; text-decoration:none; font-weight:700;
  font-size:clamp(.82rem,.9vw,1.08rem); color:var(--chrome-soft);
  border:1.5px solid var(--edge); border-radius:999px; padding:.5em .9em; transition:.16s}
.back:hover{border-color:var(--glow); color:var(--glow)}
.brand{display:flex; align-items:baseline; gap:9px; font-weight:700; letter-spacing:.02em;
  font-size:clamp(1rem,1.05vw,1.4rem)}
.brand b{color:var(--glow)} .brand span{color:var(--chrome-soft);
  font-size:clamp(.82rem,.85vw,1.08rem); font-weight:600}
.count{margin-left:auto; font-variant-numeric:tabular-nums; font-weight:700;
  color:var(--chrome-soft); font-size:clamp(.9rem,.95vw,1.2rem)}
.dl{display:inline-flex; align-items:center; gap:.5em; text-decoration:none;
  font-weight:700; font-size:clamp(.86rem,.92vw,1.14rem); color:var(--chrome);
  border:1.5px solid var(--edge); padding:.55em 1em; border-radius:999px; background:transparent;
  cursor:pointer; transition:.18s}
.dl:hover{border-color:var(--glow); color:var(--glow)}
.dl svg{width:1.15em;height:1.15em}

/* Ust cubuk dar ekranda sigmiyordu ve sayfayi yatay olarak 167 piksel
   tasiriyordu. Uzun kitap adi artik kirpiliyor, indirme dugmeleri
   kuculuyor, gerekirse cubuk saran duzene geciyor. */
.bar{flex-wrap:wrap; min-width:0}
.brand{min-width:0; flex:1 1 auto}
.brand span:not(.kno){min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.count{flex:none}
@media (max-width:640px){
  .bar{gap:8px; padding:10px 12px}
  .brand span:not(.kno){display:none}   /* kitap adi zaten kapakta yaziyor; rozet kalir */
  .back{padding:.4em .7em; font-size:.78rem}
  .count{font-size:.82rem}
  .dl{padding:.45em .7em; font-size:.82rem}
  .dl svg{width:1em; height:1em}
}

/* Uzun kart (Deneme Zamanı) ortalanınca ekranın üstüne taşıyor ve o
   bölüm okunamıyordu. 'safe center' taşmayı üst kenardan kesmiyor,
   overflow-y de gerekirse kaydırma veriyor. */
.stage{flex:1; display:flex; align-items:center; align-items:safe center;
  overflow-y:auto; justify-content:center;
  padding:8px clamp(64px,6vw,110px) 14px; position:relative}
.stage::before{content:""; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(760px 560px at 50% 45%, rgba(255,241,214,.07), transparent 72%)}
.arrow{position:absolute; top:50%; transform:translateY(-50%); z-index:6;
  width:60px; height:60px; border-radius:50%; border:none; cursor:pointer;
  background:var(--stage); color:var(--chrome); box-shadow:0 6px 22px var(--shadow);
  font-size:1.9rem; line-height:1; display:grid; place-items:center; transition:.16s}
.arrow.prev{left:clamp(10px,2vw,28px)} .arrow.next{right:clamp(10px,2vw,28px)}
.arrow:hover:not(:disabled){background:var(--glow); color:#fff; transform:translateY(-50%) scale(1.08)}
.arrow:disabled{opacity:.3; cursor:default}
.arrow:focus-visible{outline:3px solid var(--amber); outline-offset:3px}

.book{width:min(1760px,97vw); margin-inline:auto; position:relative; z-index:1}
.slide{display:none}
.slide.on{display:block; animation:fade .38s ease}
@keyframes fade{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
@media (prefers-reduced-motion:reduce){ .slide.on{animation:none} .progress i{transition:none} }

.spread{display:grid; grid-template-columns:minmax(0,1fr) clamp(300px,28vw,500px);
  gap:clamp(20px,3vw,52px); align-items:center; justify-items:center}
.spread .art{width:auto; height:auto; max-width:100%; max-height:72vh; aspect-ratio:16/9; margin:0}
.spread .card{width:100%; margin:0}

.art{width:100%; aspect-ratio:16/9; border-radius:18px; overflow:hidden;
  box-shadow:0 16px 46px var(--shadow); background:#0002}
.art img{width:100%; height:100%; object-fit:cover; display:block}

.card{background:var(--paper); color:var(--paper-ink); position:relative;
  border-radius:16px; padding:clamp(24px,2.4vw,40px) clamp(26px,2.6vw,46px);
  box-shadow:0 10px 30px var(--shadow)}
.spread .card{padding-bottom:clamp(46px,4vw,62px)}
.eyebrow{font-family:var(--ff-disp); font-weight:800; font-size:.76rem; letter-spacing:.18em;
  text-transform:uppercase; color:var(--coral); margin:0 0 6px}
.pageno{position:absolute; right:clamp(20px,2vw,32px); bottom:clamp(16px,1.6vw,24px);
  font-family:var(--ff-disp); font-weight:800; font-size:.72rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--coral); background:rgba(241,106,80,.12);
  padding:4px 12px; border-radius:999px}
.card h2{font-family:var(--ff-disp); font-weight:800; font-size:clamp(1.35rem,1.8vw,1.85rem);
  margin:0 0 16px; color:var(--paper-ink); text-wrap:balance; line-height:1.15}
.card p,.card .metin{font-family:var(--ff-body); font-size:clamp(1.12rem,1.25vw,1.4rem); line-height:1.74;
  margin:0; max-width:42ch}
.card .term{font-style:normal; font-weight:600; color:#C24A18; font-family:var(--ff-disp)}
/* Konusani ayirt etme: kaynak metinde {B} ve {Y} isaretleriyle belirtilir.
   Turuncu terimlere, yesil buyruklara ayrildigi icin konusanlara gul ve
   mavi verildi; ikisi de krem zeminde rahat okunuyor. */
.card .say{font-style:normal}
.card .say.b{color:#A03356}
.card .say.y{color:#1D5C86}
.card .say .who{display:inline-block; width:1.25em; height:1.25em; border-radius:50%;
  vertical-align:-.28em; margin-right:.28em; object-fit:contain}
/* Sira degisiminde replik yeni satirda baslar; simge cizgi gibi sola oturur. */
.card .say.turn{display:inline}
.card .ara{display:block; height:.5em}
.card .say.b .who{background:#F7C9C0}
.card .say.y .who{background:#CFE6F2}
/* Ucuncu karakterler (Ayse Teyze, Murat Bey, Risko, Sisko, Islemci...) tek tek
   portre tasimadigi icin tarafsiz bir konusma balonu simgesi ve mor murekkep
   kullaniyor. Ad zaten metinde geciyor; simge "baskasi konusuyor" diyor. */
.card .say.d{color:#6B3FA0}
.card .say.d .who{background:none; padding:.06em}
/* Replik icindeki terim, konusanin renginde ve koyu olur. Turuncu terim rengi
   mavi/gul repligin icinde yabanci duruyordu (konusan renkleri sonradan
   eklendi). Anlatim icindeki terim turuncu kalir. */
.card .say .term{color:inherit; font-weight:800}
.card .cmd{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; font-size:.9em;
  background:rgba(24,34,83,.07); color:#1F6F4A; padding:.08em .34em; border-radius:5px}
.card .code{display:block; font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; font-size:.84em;
  background:rgba(24,34,83,.06); color:#22405F; padding:.6em .85em; border-radius:10px;
  margin:.5em 0 0; white-space:pre; overflow-x:auto; line-height:1.5}

.cover .art{aspect-ratio:16/9; max-height:84vh; width:auto; margin-inline:auto; position:relative}
/* Katman sirasi onemli: perde ::after ile uretildigi icin agac sirasinda en
   sondadir ve z-index verilmezse yazinin ustune biner, baslik solgun gorunur.
   Bu yuzden resim 0, perde 1, yazi 2 katmaninda duruyor. */
.cover .art img{position:relative; z-index:0}
.cover .art::after{content:""; position:absolute; inset:0; z-index:1; pointer-events:none;
  background:linear-gradient(180deg,transparent 34%,rgba(10,14,32,.55) 62%,rgba(8,11,26,.92) 100%);
  border-radius:18px}
.cover-tag{position:absolute; left:24px; bottom:22px; right:24px; z-index:2}
.cover-tag .eyebrow{color:var(--amber); text-shadow:0 1px 3px #000, 0 2px 10px #000c}
.cover-tag h1{font-family:var(--ff-disp); font-weight:800; color:#fff; margin:2px 0 0;
  font-size:clamp(1.5rem,4vw,2.3rem); line-height:1.08;
  text-shadow:0 1px 3px #000, 0 3px 18px #000e; text-wrap:balance}
.cover-tag .csub{color:#fdf3df; font-family:var(--ff-body); font-style:italic;
  margin:8px 0 0; font-size:1.02rem; text-shadow:0 1px 3px #000, 0 2px 12px #000d; max-width:44ch}

.summary .card{margin:0 auto; max-width:940px}
/* Telif satiri: md kuyrugunda tutarsizdi (26 kitapta vardi, 8'inde ayirici
   yoktu ve ozet listesine madde olarak siziyordu, yildizlari da duz metin
   goruunuyordu). Artik uretici yaziyor, listenin disinda ve sade. */
.summary .telif{margin:22px 0 0; text-align:center; color:var(--paper-ink);
  opacity:.55; font-size:.82rem; font-family:var(--ff-body)}
.summary h2{color:var(--paper-ink); font-size:clamp(1.4rem,1.9vw,1.75rem);
  display:flex; align-items:center; gap:10px; margin:0}
.slist{list-style:none; margin:18px 0 0; padding:0; display:grid; gap:14px}
/* Deneme Zamanı: bölüm sonu soruları ve küçük etkileşimli alan.
   Puan, süre ve hesap yok; yanıtlar tek dokunuşla açılıyor. */
.dene-alt{margin:.2em 0 .6em; color:var(--kagit-solgun); font-size:.95rem}
.dlist{font-family:var(--ff-body); font-size:clamp(1.04rem,1.15vw,1.2rem); line-height:1.6;
  color:var(--kagit-koyu); padding-left:1.3em; margin:.4em 0 .8em}
.dlist li{margin:.45em 0}
.yanit{margin-top:26px; border-top:2px solid var(--kagit-cizgi); padding-top:16px}
.yanit summary{cursor:pointer; font-family:var(--ff-disp); font-weight:800;
  color:var(--kehribar-koyu); font-size:1rem; list-style:none; display:inline-flex;
  align-items:center; gap:6px; padding:6px 14px; border-radius:999px;
  border:1.5px solid color-mix(in srgb,var(--kehribar-koyu) 45%,transparent)}
.yanit summary:hover{background:color-mix(in srgb,var(--kehribar-koyu) 10%,transparent)}
.yanit .dlist{margin-top:12px}
.yanit summary::-webkit-details-marker{display:none}
.yanit summary::before{content:"\25B8  "}
.yanit[open] summary::before{content:"\25BE  "}
.dene{margin:12px 0 4px; padding:12px 10px; border:1px solid var(--kagit-cizgi); border-radius:18px;
  background:color-mix(in srgb,var(--paper-ink) 4%,transparent)}
/* Oran baştan bildiriliyor: geç yüklenirken sayfa zıplamasın. */
.dene-afis{display:block; width:100%; max-width:520px; margin:6px auto 12px;
  aspect-ratio:16/9; border-radius:16px}
.card .dene-yonerge{margin:0 0 12px; max-width:none; font-size:.94rem; color:var(--kagit-solgun); text-align:center}
.dene-tahta{display:flex; align-items:stretch; justify-content:center; gap:16px; flex-wrap:wrap}
.dene-sol,.dene-sag{display:flex; flex-direction:column; align-items:center; justify-content:center}
.dene-sag{min-width:150px; padding:10px 18px; border-radius:16px;
  border:2px solid var(--kagit-cizgi); background:color-mix(in srgb,var(--paper-ink) 5%,transparent)}
.card .dene-etiket{margin:0 0 8px; max-width:none; font-family:var(--ff-disp); font-size:.76rem;
  letter-spacing:.05em; text-transform:uppercase; color:var(--kagit-solgun)}
.dene-kutular{display:flex; gap:12px; justify-content:center; flex-wrap:wrap}
.dene-kutu{width:66px; height:78px; border-radius:14px; cursor:pointer;
  border:2px solid var(--kagit-cizgi); background:transparent; color:var(--kagit-solgun);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;
  font-family:var(--ff-disp); transition:transform .15s, border-color .15s, color .15s}
.dene-kutu .bit{font-size:1.8rem; font-weight:800; line-height:1}
.dene-kutu .agirlik{font-size:.72rem; opacity:.7}
/* Dar ekranda dört kutucuk tek satırda kalsın; sarınca üçe bir bölünüyordu. */
@media (max-width:520px){ .dene-kutular{gap:8px} .dene-kutu{width:58px; height:70px} }
.dene-kutu.acik{border-color:var(--parlak-koyu); color:var(--parlak-koyu); transform:translateY(-3px)}
.card .dene-sonuc{margin:0; max-width:none; font-family:var(--ff-disp); font-weight:800; line-height:1;
  font-size:clamp(2.4rem,4.6vw,3.2rem); color:var(--parlak-koyu)}
/* Kapi denemesi */
.dene-kapi-duzen{display:flex; align-items:center; justify-content:center; gap:6px; flex-wrap:wrap}
.dene-girisler{display:flex; flex-direction:column; gap:16px}
.dene-sema{width:min(240px,44vw); height:auto; overflow:visible}
.dene-sema .tel{fill:none; stroke:var(--kagit-cizgi); stroke-width:4; stroke-linecap:round}
.dene-sema .tel.canli{stroke:var(--parlak-koyu)}
.dene-sema .govde{fill:none; stroke:var(--kagit-koyu); stroke-width:4; stroke-linejoin:round}
@media (max-width:520px){ .dene-sema{width:min(200px,60vw)} .dene-girisler{gap:10px} }
.dene-secim{display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin:0 0 14px}
.dene-secim button{font-family:var(--ff-disp); font-weight:800; font-size:.82rem; letter-spacing:.04em;
  padding:8px 14px; border-radius:999px; cursor:pointer; background:transparent;
  border:1px solid var(--kagit-cizgi); color:var(--kagit-solgun)}
.dene-secim button.secili{border-color:var(--parlak-koyu); color:var(--parlak-koyu)}
.dene-lamba{margin:0; font-size:2.6rem; line-height:1; filter:grayscale(1) opacity(.4);
  transition:filter .15s ease}
.dene-lamba.yanik{filter:none}
.card .dene-cikis{margin:.4em 0 0; max-width:none; font-family:var(--ff-disp); font-weight:800;
  font-size:1.05rem; text-align:center; color:var(--kagit-koyu)}
.card .dene-ipucu{margin:12px 0 0; max-width:none; text-align:center; font-size:.9rem;
  min-height:1.2em; color:var(--kehribar-koyu)}
.slist li{font-family:var(--ff-body); font-size:clamp(1.06rem,1.2vw,1.22rem); line-height:1.55;
  padding-left:14px; border-left:3px solid var(--amber)}
.slist li b{font-family:var(--ff-disp)}

/* min-width:0 sart: esnek kutu icindeki oge bunsuz icerigin altina kuculemez,
   serit de sayfayi yatay olarak genisletir (telefonda 190 piksel tasma). */
.strip{display:flex; gap:10px; overflow-x:auto; padding:14px 20px 20px;
  scroll-behavior:smooth; min-width:0}
.strip::-webkit-scrollbar{height:8px}
.strip::-webkit-scrollbar-thumb{background:var(--edge); border-radius:8px}
.thumb{flex:none; width:104px; aspect-ratio:16/9; border-radius:9px; overflow:hidden;
  border:2.5px solid transparent; cursor:pointer; background:var(--stage); padding:0;
  position:relative; transition:.16s; opacity:.6}
.thumb img{width:100%; height:100%; object-fit:cover; display:block}
.thumb.sum{display:grid; place-items:center; color:var(--chrome-soft); font-size:1.5rem}
.thumb:hover{opacity:1}
.thumb.on{opacity:1; border-color:var(--amber); transform:translateY(-3px)}
.thumb .n{position:absolute; left:5px; top:4px; font-size:.62rem; font-weight:800;
  color:#fff; background:#0009; border-radius:5px; padding:1px 5px; font-variant-numeric:tabular-nums}

.hint{text-align:center; color:var(--chrome-soft); font-size:clamp(.8rem,.85vw,1.02rem);
  padding:0 0 clamp(16px,1.4vw,24px)}
.hint kbd{font-family:var(--ff-disp); border:1px solid var(--edge); border-bottom-width:2px;
  border-radius:5px; padding:1px .5em; font-size:.86em}

/* kitap numarasi rozeti (ust bar) */
.brand .kno{background:var(--accent); color:#fff; font-family:var(--ff-disp); font-weight:800;
  font-size:clamp(.72rem,.8vw,.98rem); padding:3px 11px; border-radius:999px; letter-spacing:.02em}

/* onceki/sonraki kitap gezinmesi */
.booknav{display:flex; align-items:stretch; justify-content:center; gap:12px;
  padding:2px clamp(20px,2vw,40px) 12px; flex-wrap:wrap}
.bn{flex:1 1 0; max-width:360px; display:flex; flex-direction:column; gap:2px; text-decoration:none;
  border:1.5px solid var(--edge); border-radius:14px; padding:11px 18px; background:transparent;
  color:var(--chrome); transition:transform .16s, border-color .16s, box-shadow .16s}
.bn span{font-size:.7rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:var(--chrome-soft)}
.bn b{font-family:var(--ff-disp); font-weight:800; font-size:clamp(.9rem,1vw,1.08rem); line-height:1.15}
.bn.next{text-align:right}
.bn:hover{border-color:var(--accent); transform:translateY(-2px); box-shadow:0 10px 24px -14px var(--accent)}
.bn:focus-visible{outline:3px solid var(--accent); outline-offset:2px}
.bn.home{flex:0 0 auto; align-self:center; max-width:none; justify-content:center;
  border-radius:999px; color:var(--chrome-soft); font-weight:700; padding:11px 20px}
.bn.home b{font-size:.92rem}
.bn.disabled{flex:1 1 0; max-width:360px; border:1.5px dashed var(--edge); opacity:.3; pointer-events:none}
@media (max-width:640px){ .bn{flex-basis:44%} .bn.home{order:-1; flex-basis:100%} }

/* gorus bildirme */
.gorus{text-align:center; padding:4px clamp(20px,2vw,40px) 22px}
.gorus a{display:inline-flex; align-items:center; gap:8px; text-decoration:none;
  border:1.5px solid var(--edge); border-radius:999px; padding:9px 20px;
  color:var(--chrome-soft); font-weight:700; font-size:.9rem;
  transition:border-color .16s, color .16s, transform .16s}
.gorus a:hover{border-color:var(--accent); color:var(--chrome); transform:translateY(-1px)}
.gorus a:focus-visible{outline:3px solid var(--accent); outline-offset:2px}
.gorus p{margin:8px 0 0; color:var(--chrome-soft); font-size:.78rem; opacity:.8}

@media (max-width:880px){
  .stage{padding:8px 16px 12px}
  .spread{grid-template-columns:1fr; gap:0}
  .spread .art{width:100%; height:auto; max-width:none; max-height:none; aspect-ratio:16/9}
  .spread .card{width:92%; max-width:none; margin:-26px auto 0}
}
@media (max-width:640px){
  .arrow{position:fixed; top:auto; bottom:86px; transform:none; width:52px; height:52px; font-size:1.6rem}
  .arrow.prev{left:12px} .arrow.next{right:12px}
  .arrow:hover:not(:disabled){transform:scale(1.06)}
  .stage{padding:4px 10px 10px}
  .spread .card{width:100%; padding:20px 22px 22px}
  .card p,.card .metin{max-width:none}
  .cover .art{max-height:68vh}
}
</style>
</head>
<body>

<div class="reader" style="--accent:__ACCENT__">
  <div class="progress"><i id="bar"></i></div>
  <div class="bar">
    <a class="back" href="__BACK__">‹ Seri</a>
    <div class="brand"><b>Bilge</b> ve <b>Yonga</b> <span class="kno">Kitap __NO__</span> <span>__BRAND__</span></div>
    <div class="count"><span id="cur">1</span> / <span id="tot">1</span></div>
    <a class="dl" href="__EPUB__" download title="E-kitap (EPUB) indir">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
        stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M14 3v6h6"/></svg>E-kitap</a>
    <a class="dl" href="__PDF__" target="_blank" rel="noopener" title="Kitabı PDF olarak aç">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
        stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 11l5 4 5-4"/>
        <path d="M4 20h16"/></svg>PDF</a>
  </div>

  <div class="stage">
    <button class="arrow prev" id="prev" aria-label="Önceki sayfa">‹</button>
    <div class="book" id="book"></div>
    <button class="arrow next" id="next" aria-label="Sonraki sayfa">›</button>
  </div>

  <div class="strip" id="strip"></div>
  <div class="booknav">__BOOKNAV__</div>
  <div class="hint">Oklarla veya <kbd>←</kbd> <kbd>→</kbd> tuşlarıyla gezin · alttaki küçük resimlere dokun</div>
  <div class="gorus">
    <a href="__GORUS__">✉ Bu kitap hakkında görüş bildir</a>
    <p>Beğendiğiniz, karışık bulduğunuz ya da yanlış olduğunu düşündüğünüz her şeyi yazabilirsiniz.</p>
  </div>
</div>

<script>
const PAGES = __DATA__;
let i = 0;
const book = document.getElementById('book');
const strip = document.getElementById('strip');
const tot = PAGES.length;
document.getElementById('tot').textContent = tot;
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fmt(s){var t=esc(s);
  // Kod parcalari once saklanir: konusan kalibi tirnak arar ve HTML
  // ozniteliklerindeki tirnaklara takilirsa repligi ortasindan keser.
  var KOD=[];
  function sakla(h){KOD.push(h);return '\u0001'+(KOD.length-1)+'\u0001';}
  t=t.replace(/```\n?([\s\S]*?)```/g,function(m,c){
    return sakla('<span class="code">'+c.replace(/\n+$/,'')+'</span>');});
  t=t.replace(/`([^`\n]+)`/g,function(m,c){
    return sakla('<code class="cmd">'+c+'</code>');});
  // {B}"..." / {Y}"..." -> konusan kabugu (simge + renk). Isaretsiz alintilar
  // (ekran icerigi, terim) oldugu gibi kalir; asla tahmin yurutulmez.
  // Konusan degistiginde replik yeni satirda basliyor ve basina karakter
  // simgesi geliyor: simge, Turkce konusma cizgisinin yapisal isini yapar.
  // Ayni kisinin suren repligi ayni satirda kalir, rengini korur, simge
  // yinelenmez. Boylece sira degisimi bosluktan, kimlik simgeden okunur.
  var oncekiKonusan = '';
  var BALON = '<svg class="who" viewBox="0 0 24 24" role="img" aria-label="Başka biri konuşuyor">'
    + '<path fill="currentColor" d="M12 3C6.9 3 3 6.3 3 10.3c0 2.3 1.3 4.4 3.4 5.7L5.6 20l3.9-2.1'
    + 'c.8.2 1.6.3 2.5.3 5.1 0 9-3.3 9-7.3S17.1 3 12 3z"/></svg>';
  t=t.replace(/\{([BYD])\}("[^"]*")/g,function(m,k,q,konum){
    var kim = k==='B' ? {s:'b', ad:'Bilge', im:'../bilge.png?v=10'}
            : k==='Y' ? {s:'y', ad:'Yonga', im:'../yonga.png?v=10'}
                      : {s:'d', ad:'', im:null};
    var degisti = (k!==oncekiKonusan);
    oncekiKonusan = k;
    if(!degisti) return '<span class="say '+kim.s+'">'+q+'</span>';
    var simge = kim.im
      ? '<img class="who" src="'+kim.im+'" alt="'+kim.ad+' konuşuyor">'
      : BALON;
    var basta = (t.slice(0, konum).trim() === '');
    return (basta ? '' : '<span class="ara"></span>')
      + '<span class="say turn '+kim.s+'">' + simge + q + '</span>';
  });
  t=t.replace(/\*\*(.+?)\*\*/g,'<em class="term">$1</em>');
  return t.replace(/\u0001(\d+)\u0001/g,function(m,i){return KOD[+i];});}

function deneKur(kap){
  if(!kap || kap.dataset.kuruldu) return;
  kap.dataset.kuruldu = '1';
  if(kap.dataset.dene === 'kapi'){ deneKapi(kap); return; }
  if(kap.dataset.dene !== 'basamak') return;
  const degerler = [8,4,2,1], durum = [0,0,0,0];
  kap.innerHTML = '<p class="dene-yonerge">Kutucuklara dokun, sayının ne olduğunu gör.</p>'
    + '<div class="dene-tahta">'
    +   '<div class="dene-sol">'
    +     '<p class="dene-etiket">İkilik taban</p>'
    +     '<div class="dene-kutular"></div>'
    +   '</div>'
    +   '<div class="dene-sag">'
    +     '<p class="dene-etiket">Onluk taban</p>'
    +     '<p class="dene-sonuc">0</p>'
    +   '</div>'
    + '</div>';
  const sira = kap.querySelector('.dene-kutular');
  const sonuc = kap.querySelector('.dene-sonuc');
  degerler.forEach((d,i)=>{
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'dene-kutu';
    b.setAttribute('aria-label', d + ' basamağı');
    b.innerHTML = '<span class="bit">0</span><span class="agirlik">'+d+'</span>';
    b.addEventListener('click', (e)=>{
      durum[i] = durum[i] ? 0 : 1;
      b.classList.toggle('acik', !!durum[i]);
      b.querySelector('.bit').textContent = durum[i];
      sonuc.textContent = durum.reduce((a,v,j)=>a+v*degerler[j], 0);
      if(e.detail) b.blur();
    });
    sira.appendChild(b);
  });
}

// Kapi denemesi: cocuk kapiyi secer, girisleri acip kapatir, lambaya bakar.
// Kitap sifir-bir dilini kullanmiyor (1.02a'dan once geliyor), burada da
// "acik/kapali" deniyor.
function deneKapi(kap){
  const KAPILAR = [
    {ad:'VE',    tek:false, hesap:(a,b)=>a&&b},
    {ad:'VEYA',  tek:false, hesap:(a,b)=>a||b},
    {ad:'DEĞİL', tek:true,  hesap:(a)=>!a}
  ];
  // Kapinin kendi simgesi ortada durur; A ile B solda, girislere bagli,
  // ampul sagda cikisa bagli. Ust siradan kapi secilince asagidaki simge
  // ve tel sayisi degisir. Simgeler SVG: her olcekte keskin kalir.
  const GOVDE = {
    'VE':    'M22,10 H58 A30,30 0 0 1 58,70 H22 Z',
    'VEYA':  'M22,10 Q46,40 22,70 Q68,69 98,40 Q68,11 22,10 Z',
    'DEĞİL': 'M26,10 L84,40 L26,70 Z'
  };
  // 1.02a'da isaretin sayi karsiligi da yazilir; 1.01c'de yazilmaz.
  const sayi = kap.dataset.sayi === '1';
  const yaz = v => v ? (sayi ? 'açık (1)' : 'açık') : (sayi ? 'kapalı (0)' : 'kapalı');
  let secili = 0;
  const giris = [0,0];
  const gorulen = [new Set(), new Set(), new Set()];
  kap.innerHTML = '<p class="dene-yonerge">Bir kapı seç, düğmelere dokun, lambaya bak.</p>'
    + '<div class="dene-secim"></div>'
    + '<div class="dene-kapi-duzen">'
    +   '<div class="dene-girisler"></div>'
    +   '<svg class="dene-sema" viewBox="0 0 132 80" aria-hidden="true">'
    +     '<path class="tel" id="tel-a" d="M0,25 H22"></path>'
    +     '<path class="tel" id="tel-b" d="M0,55 H22"></path>'
    +     '<path class="tel" id="tel-c" d="M98,40 H132"></path>'
    +     '<path class="govde" id="govde" d=""></path>'
    +     '<circle class="govde" id="yuvarlacik" cx="91" cy="40" r="7"></circle>'
    +   '</svg>'
    +   '<div class="dene-sag">'
    +     '<p class="dene-etiket">Çıkış</p>'
    +     '<p class="dene-lamba" aria-hidden="true">💡</p>'
    +     '<p class="dene-cikis"></p>'
    +   '</div>'
    + '</div>'
    + '<p class="dene-ipucu" role="status"></p>';
  const secim = kap.querySelector('.dene-secim');
  const sira = kap.querySelector('.dene-girisler');
  const lamba = kap.querySelector('.dene-lamba');
  const cikis = kap.querySelector('.dene-cikis');
  const ipucu = kap.querySelector('.dene-ipucu');
  const telA = kap.querySelector('#tel-a'), telB = kap.querySelector('#tel-b');
  const telC = kap.querySelector('#tel-c'), govde = kap.querySelector('#govde');
  const yuvarlacik = kap.querySelector('#yuvarlacik');

  const dugmeler = [];
  ['A','B'].forEach((ad,i)=>{
    const b = document.createElement('button');
    b.type='button'; b.className='dene-kutu';
    b.innerHTML = '<span class="bit">'+ad+'</span><span class="agirlik">'+yaz(0)+'</span>';
    b.addEventListener('click', (e)=>{
      giris[i] = giris[i] ? 0 : 1;
      b.classList.toggle('acik', !!giris[i]);
      b.querySelector('.agirlik').textContent = yaz(giris[i]);
      b.setAttribute('aria-label', ad + ' girişi ' + (giris[i]?'açık':'kapalı'));
      yenile();
      if(e.detail) b.blur();
    });
    dugmeler.push(b); sira.appendChild(b);
  });

  KAPILAR.forEach((k,i)=>{
    const b = document.createElement('button');
    b.type='button'; b.textContent = k.ad + ' kapısı';
    b.addEventListener('click', (e)=>{
      secili = i;
      secim.querySelectorAll('button').forEach((o,j)=>o.classList.toggle('secili', j===i));
      yenile();
      if(e.detail) b.blur();
    });
    if(i===0) b.classList.add('secili');
    secim.appendChild(b);
  });

  function yenile(){
    const k = KAPILAR[secili];
    // hidden yetmiyor: .dene-kutu kendi display'ini kuruyor, dugme
    // gizlenmiyordu.
    dugmeler[1].style.display = k.tek ? 'none' : '';
    const acik = k.tek ? k.hesap(giris[0]) : k.hesap(giris[0], giris[1]);
    govde.setAttribute('d', GOVDE[k.ad]);
    yuvarlacik.style.display = k.tek ? '' : 'none';
    // Teller govdeye degmeli: VEYA'nin arka kenari icbukey oldugu icin
    // girisler 31'e kadar gider, VE'de 22'de biter; cikis da her kapinin
    // kendi sag ucundan baslar.
    const uc = {'VE':[22,88], 'VEYA':[31,98], 'DEĞİL':[26,98]}[k.ad];
    telA.setAttribute('d', k.tek ? 'M0,40 H'+uc[0] : 'M0,25 H'+uc[0]);
    telB.setAttribute('d', 'M0,55 H'+uc[0]);
    telB.style.display = k.tek ? 'none' : '';
    telC.setAttribute('d', 'M'+uc[1]+',40 H132');
    telA.classList.toggle('canli', !!giris[0]);
    telB.classList.toggle('canli', !!giris[1]);
    telC.classList.toggle('canli', !!acik);
    lamba.classList.toggle('yanik', !!acik);
    cikis.textContent = yaz(acik);
    gorulen[secili].add(k.tek ? String(giris[0]) : giris[0]+'-'+giris[1]);
    const hepsi = k.tek ? 2 : 4;
    ipucu.textContent = gorulen[secili].size >= hepsi
      ? k.ad + ' kapısının bütün durumlarını denedin.' : '';
  }
  yenile();
}

PAGES.forEach((p, idx)=>{
  const s = document.createElement('div');
  s.className = 'slide' + (p.type==='cover'?' cover':(p.type==='summary'||p.type==='deneme')?' summary':'');
  const lz = idx===0 ? '' : ' loading="lazy" decoding="async"';
  if(p.type==='cover'){
    s.innerHTML = '<div class="art"><img src="'+p.img+'" alt="Kapak"'+lz+'>'
      +'<div class="cover-tag"><p class="eyebrow">'+esc(p.eyebrow)+'</p>'
      +'<h1>'+esc(p.title)+'</h1><p class="csub">'+esc(p.sub)+'</p></div></div>';
  } else if(p.type==='deneme'){
    const sor = p.sorular.map(s=>'<li>'+s.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')+'</li>').join('');
    const yan = p.yanitlar.map(s=>'<li>'+s.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')+'</li>').join('');
    s.innerHTML = '<div class="card"><h2>✏️ '+esc(p.title)+'</h2>'
      + '<img class="dene-afis" src="../sus/'+p.afis+'" alt="" aria-hidden="true"'+lz+'>'
      + '<p class="dene-alt">Şimdi sıra sende.</p>'
      + '<ol class="dlist">'+sor+'</ol>'
      + (p.widget||'')
      + '<details class="yanit"><summary>Yanıtlar (dokun)</summary><ol class="dlist">'+yan+'</ol></details>'
      + '<p class="telif">© Oğuz Ergin · Bilge ve Yonga · CC BY-NC-ND 4.0</p></div>';
  } else if(p.type==='summary'){
    const lis = p.lines.map(l=>'<li>'+l.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')+'</li>').join('');
    s.innerHTML = '<div class="card"><h2>🎓 '+esc(p.title)+'</h2><ul class="slist">'+lis+'</ul>'
      + '<p class="telif">© Oğuz Ergin · Bilge ve Yonga · CC BY-NC-ND 4.0</p></div>';
  } else {
    s.innerHTML = '<div class="spread"><div class="art"><img src="'+p.img+'" alt="Sayfa '+p.no+'"'+lz+'></div>'
      +'<div class="card">'+(p.title?'<h2>'+esc(p.title)+'</h2>':'')
      +'<div class="metin">'+fmt(p.text)+'</div><span class="pageno">Sayfa '+p.no+'</span></div></div>';
  }
  book.appendChild(s);
  if(p.type==='deneme'){ deneKur(s.querySelector('[data-dene]')); }

  const t = document.createElement('button');
  t.className = 'thumb' + ((p.type==='summary'||p.type==='deneme')?' sum':'');
  if(p.type==='summary'){ t.innerHTML = '🎓'; }
  else if(p.type==='deneme'){ t.innerHTML = '✏️'; }
  else { t.innerHTML = '<img src="'+p.thumb+'" alt="" loading="lazy" decoding="async"><span class="n">'
      +(p.type==='cover'?'K':p.no)+'</span>'; }
  t.addEventListener('click', ()=>go(idx));
  strip.appendChild(t);
});

/* Önden indirme: kitap açılınca kalan sayfa görselleri arka planda
 * sırayla çekiliyor. Yavaş bağlantıdan okuyan okurlar "metin geldi,
 * resim gelmedi" diye bildirdi. Hizmet çalışanı çekilen her görseli
 * sakladığı için bir kez inince sayfa çevirmek anında oluyor ve
 * bağlantı kesilse bile kitap sonuna kadar okunabiliyor. Görseller
 * TEK TEK ve düşük öncelikle çekiliyor; hepsini birden istemek okunan
 * sayfanın kendi isteklerinin önüne geçiyor. */
function ondenIndir(){
  const kuyruk = PAGES.map(p=>p.img).filter(Boolean).slice(1);
  let n = 0;
  (function sonraki(){
    if(n >= kuyruk.length) return;
    const im = new Image();
    im.fetchPriority = 'low';
    im.decoding = 'async';
    im.onload = im.onerror = ()=>{ n++; setTimeout(sonraki, 120); };
    im.src = kuyruk[n];
  })();
}
if('requestIdleCallback' in window) requestIdleCallback(ondenIndir, {timeout:2500});
else setTimeout(ondenIndir, 1500);

const slides = [...book.children];
const thumbs = [...strip.children];
const prev = document.getElementById('prev');
const next = document.getElementById('next');
function go(n){
  i = Math.max(0, Math.min(tot-1, n));
  slides.forEach((s,k)=>s.classList.toggle('on', k===i));
  thumbs.forEach((t,k)=>t.classList.toggle('on', k===i));
  document.getElementById('cur').textContent = i+1;
  document.getElementById('bar').style.width = ((i+1)/tot*100)+'%';
  prev.disabled = i===0; next.disabled = i===tot-1;
  thumbs[i].scrollIntoView({inline:'center', block:'nearest'});
}
// Fare ile tiklandiktan sonra odak dugmede kalirsa bosluk tusu sayfa
// cevirmek yerine dugmeyi calistirir. Klavyeyle gelen tiklama (detail 0)
// odagi korur, fare tiklamasi birakir.
function odakBirak(e){ if(e.detail) e.currentTarget.blur(); }
prev.addEventListener('click', e=>{ odakBirak(e); go(i-1); });
next.addEventListener('click', e=>{ odakBirak(e); go(i+1); });
document.addEventListener('keydown', e=>{
  // Bosluk ve PageDown ileri, Shift+Bosluk ve PageUp geri. Dugme ya da
  // baglanti odaktayken bosluk onu calistirsin diye karisilmaz.
  const od = document.activeElement;
  const tus = od && (od.tagName==='BUTTON' || od.tagName==='A' || od.tagName==='INPUT' || od.tagName==='SELECT');
  if(e.key==='ArrowRight' || e.key==='PageDown') go(i+1);
  else if(e.key==='ArrowLeft' || e.key==='PageUp') go(i-1);
  else if(e.key===' ' && !tus){ e.preventDefault(); e.shiftKey ? go(i-1) : go(i+1); }
  else if(e.key==='Home') go(0);
  else if(e.key==='End') go(tot-1);
});
let x0=null;
book.addEventListener('touchstart', e=>x0=e.touches[0].clientX, {passive:true});
book.addEventListener('touchend', e=>{
  if(x0===null) return;
  const dx = e.changedTouches[0].clientX - x0;
  if(Math.abs(dx)>45){ dx<0 ? go(i+1) : go(i-1); }
  x0=null;
});
go(0);
</script>
</body>
</html>
'''


GORUS_ADRES = 'bilgi@oguzergin.net'


def _gorus_href(konu):
    """Kitaba ozel konu satiri tasiyan e-posta baglantisi."""
    return 'mailto:%s?subject=%s' % (
        GORUS_ADRES, quote('Bilge ve Yonga · %s hakkında görüşüm' % konu))


def _booknav_html(prev, nxt):
    """prev/nxt: None ya da (folder, no, title)."""
    if prev:
        pf, pno, pt = prev
        left = (f'<a class="bn prev" href="{pf}.html" title="Kitap {pno}">'
                f'<span>‹ Önceki kitap</span><b>{escape(pt)}</b></a>')
    else:
        left = '<span class="bn disabled"></span>'
    home = '<a class="bn home" href="../index.html"><b>Tüm seri</b></a>'
    if nxt:
        nf, nno, nt = nxt
        right = (f'<a class="bn next" href="{nf}.html" title="Kitap {nno}">'
                 f'<span>Sonraki kitap ›</span><b>{escape(nt)}</b></a>')
    else:
        right = '<span class="bn disabled"></span>'
    return left + home + right


# Google Scholar atif ustverisi. Mimari kitabi alti ay Scholar'a cikmadi;
# nedenlerinden biri sitede citation_* etiketinin hic olmamasiydi.
# citation_doi BILEREK YOK: DOI ciltlere ait, tek tek kitaplara degil. Ayni
# DOI'yi 11 kitabin sayfasina yazmak Scholar'da kayitlari birbirine karistirir.
# Kitabin hangi cilde ait oldugu citation_inbook_title ile belirtiliyor.
def _citation_meta(folder, no, title, medya):
    seri = no.split('.')[0]
    cilt = CILTLER.get(seri)
    ad = SERIES[seri][0] if seri in SERIES else ''
    kok = 'https://bilgeveyonga.oguzergin.net'
    m = [
        ('citation_title', title),
        ('citation_author', 'Ergin, Oğuz'),
        ('citation_publication_date', '2026'),
        ('citation_language', 'tr'),
        ('citation_public_url', '{}/okuyucu/{}.html'.format(kok, folder)),
        ('citation_pdf_url', '{}/{}.pdf'.format(kok, medya)),
    ]
    if cilt:
        m.append(('citation_inbook_title',
                  'Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları '
                  'Serisi — Cilt {}: {}'.format(seri, ad)))
    return ''.join('<meta name="{}" content="{}">'.format(k, escape(v, {'"': '&quot;'}))
                   for k, v in m)


def build_reader(folder, no, title, subtitle, glow, prev=None, nxt=None):
    d = REPO / folder
    pdf = find_pdf(d)
    pages = parse_book(folder, no, title, subtitle)
    data = json.dumps(pages, ensure_ascii=False)
    pdf_href = f'../{folder}/{quote(pdf)}' if pdf else '#'
    epub_href = f'../{folder}/{quote(Path(pdf).stem + ".epub")}' if pdf else '#'
    html = (READER_TPL
            .replace('__BRAND__', title)
            .replace('__NO__', no)
            .replace('__ACCENT__', glow)
            .replace('__BACK__', '../index.html')
            .replace('__PDF__', pdf_href)
            .replace('__EPUB__', epub_href)
            .replace('__GORUS__', _gorus_href('Kitap %s · %s' % (no, title)))
            .replace('__BOOKNAV__', _booknav_html(prev, nxt))
            .replace('__DATA__', data))

    # Sartname B.1 + D.5: telif meta blogu ve kitap yapisal verisi.
    # D.3 tutarlilik kurali: ayni telif blogu her sayfada bulunur.
    medya = f'{folder}/{quote(Path(pdf).stem)}' if pdf else folder
    ld = (BVY_KITAP_LD
          .replace('__NO__', no)
          .replace('__SLUG__', folder)
          .replace('__MEDYA__', medya)
          .replace('__AD__', json.dumps(title, ensure_ascii=False)[1:-1])
          .replace('__ACIKLAMA__', json.dumps(subtitle, ensure_ascii=False)[1:-1])
          .replace('__SAYFA__', str(sum(1 for p in pages if p.get('type') == 'page'))))
    html = html.replace('</head>', BVY_TELIF_META
                        + _citation_meta(folder, no, title, medya)
                        + ld + '\n</head>', 1)

    out = OKU / f'{folder}.html'
    out.write_text(html, encoding='utf-8')
    return len(pages), out.name


def _surum(anahtar, tur='kitaplar'):
    """surumler.json'dan kitap ya da cilt surumu. Kayit yoksa bos doner
    (henuz yayimlanmamis kitaplarda satir gorunmesin)."""
    yol = REPO / 'surumler.json'
    if not yol.exists():
        return ''
    k = json.loads(yol.read_text(encoding='utf-8'))[tur].get(str(anahtar))
    if not k:
        return ''
    return 'Sürüm %s, %s' % (k['surum'], _kisa_tarih(k['tarih']))


AYLAR = {'Ocak': 'Oca', 'Şubat': 'Şub', 'Mart': 'Mar', 'Nisan': 'Nis',
         'Mayıs': 'May', 'Haziran': 'Haz', 'Temmuz': 'Tem', 'Ağustos': 'Ağu',
         'Eylül': 'Eyl', 'Ekim': 'Eki', 'Kasım': 'Kas', 'Aralık': 'Ara'}


def _surum_no(anahtar, tur='kitaplar'):
    """Yalnizca numara: 1.1. Kayit yoksa bos doner."""
    k = _surum_kayit(anahtar, tur)
    return k['surum'] if k else ''


def _surum_tarih(anahtar, tur='kitaplar'):
    """Yalnizca kisa tarih: 5 Agu 2026."""
    k = _surum_kayit(anahtar, tur)
    return _kisa_tarih(k['tarih']) if k else ''


def _surum_kayit(anahtar, tur='kitaplar'):
    yol = REPO / 'surumler.json'
    if not yol.exists():
        return None
    return json.loads(yol.read_text(encoding='utf-8'))[tur].get(anahtar)


def _kisa_tarih(tarih):
    """'5 Ağustos 2026' -> '5 Ağu 2026'. Kart dar, ay adi kisalir."""
    for uzun, kisa in AYLAR.items():
        if uzun in tarih:
            return tarih.replace(uzun, kisa)
    return tarih


def _card_html(folder, no, title, sub, glow):
    d = REPO / folder
    pdf = find_pdf(d)
    pdf_href = f'{folder}/{quote(pdf)}' if pdf else '#'
    epub_href = f'{folder}/{quote(Path(pdf).stem + ".epub")}' if pdf else '#'
    read_href = f'okuyucu/{folder}.html'
    kapak = folder.split('-')[0]  # kitap1.07
    return (
        '      <article class="book" style="--bg:' + glow + '">\n'
        '        <div class="book-cover">\n'
        f'          <a href="{read_href}"><img src="kapaklar/{kapak}.jpg'
        f'{_damga(REPO / "kapaklar" / (kapak + ".jpg"))}" '
        f'alt="{title} kapağı" loading="lazy"></a>\n'
        '        </div>\n'
        '        <div class="book-meta">\n'
        '          <div class="book-ust">\n'
        f'            <span class="book-no">Kitap {no}</span>\n'
        + (f'            <span class="book-surum" title="{_surum(folder)} tarihinde güncellendi">'
           f'Sürüm {_surum_no(folder)}</span>\n'
           if _surum_no(folder) else '')
        + '          </div>\n'
        f'          <h3><a class="kart-bag" href="{read_href}">{title}</a></h3>\n'
        f'          <p>{sub}</p>\n'
        + '          <div class="book-actions">\n'
        f'            <a class="btn-read" href="{read_href}">Oku</a>\n'
        '            <div class="book-dl">\n'
        f'              <a href="{epub_href}" download>E-kitap</a>\n'
        f'              <a href="{pdf_href}" target="_blank" rel="noopener">PDF</a>\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>\n'
        '      </article>')


def _deste_anahtar(folder):
    return folder.split('-')[0]


def build_deste():
    """Deste kapaklarini 900 piksele olceklenmis olarak deste/ altina yazar.
    Doner: (varsayilan kartlarin HTML'i, havuz verisi JSON)."""
    out = REPO / 'deste'
    out.mkdir(exist_ok=True)
    adlar = {}
    for folder, no, title, sub, glow in BOOKS:
        a = _deste_anahtar(folder)
        if a != DESTE_ON and a not in DESTE_HAVUZ:
            continue
        kaynak = REPO / folder / 'resimler' / 'GPT_Kapak.jpg'
        if not kaynak.exists():
            raise SystemExit('deste kapagi bulunamadi: %s' % kaynak)
        (out / (a + '.jpg')).write_bytes(
            _jpeg_bytes(kaynak, DESTE_GENISLIK, 86))
        adlar[a] = title

    def kart(a, slot, on=False):
        alt = ('Bilge ve Yonga kumsalda yan yana' if on else '')
        return ('      <img class="card s%d" src="deste/%s.jpg" alt="%s" '
                'data-cap="%s">' % (slot, a, escape(alt), escape(adlar[a])))

    # varsayilan deste: betik calismazsa da anlamli bir sira gorunur
    varsayilan = [DESTE_ON] + ['kitap2.02', 'kitap3.07', 'kitap2.06', 'kitap3.01b']
    kartlar = '\n'.join(kart(a, i, on=(i == 0))
                        for i, a in enumerate(varsayilan))
    havuz = json.dumps([{'src': 'deste/%s.jpg' % a, 'cap': adlar[a]}
                        for a in DESTE_HAVUZ], ensure_ascii=False)
    return kartlar, havuz


def uyar_bayat_klasor():
    """BOOKS listesinde olmayan kitap klasorlerini bildirir.

    1.01 -> 1.01a numaralandirmasindan kalan klasor Drive esitlemesi yuzunden
    uc kez geri geldi ve yerel olcumleri yanaltti (alfabetik ilk klasor o
    oldugu icin denetimler eski PDF/EPUB'i okudu). Siteye giremiyor, ama
    sessiz kalmasi da dogru degil.
    """
    kayitli = {k[0] for k in BOOKS}
    for d in sorted(REPO.glob('kitap*')):
        if d.is_dir() and d.name not in kayitli:
            print(f'  [UYARI] BOOKS listesinde olmayan klasor: {d.name}')
            print( '          Siteye girmiyor. Bayat kopya olabilir, denetle.')


# Yeniden adlandirilan kitaplarin eski adresleri. Bayat okuyucu temizligi
# elle birakilan yonlendirmeyi de siliyordu; bu yuzden yonlendirmeler de
# kurulumda uretilir ve temizlikten SONRA yazilir.
YONLENDIRMELER = {
    'kitap4.04-virgulun-dansi': 'kitap4.04a-virgulun-dansi',
    'kitap3.10-tasiyicilar': 'kitap3.10a-tasiyicilar',
    'kitap3.01-iki-dunyanin-koprusu': 'kitap3.01b-iki-dunyanin-koprusu',
    'kitap1.02-milyarlarca-kucuk-anahtar': 'kitap1.02a-milyarlarca-kucuk-anahtar',
}


def yaz_yonlendirmeler():
    """Eski okuyucu adreslerine yeni sayfaya goturen sayfa birakir."""
    for eski, yeni in YONLENDIRMELER.items():
        (OKU / (eski + '.html')).write_text(
            '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
            '<title>Bilge ve Yonga</title>\n'
            '<link rel="canonical" href="{0}.html">\n'
            '<meta http-equiv="refresh" content="0; url={0}.html">\n'
            '</head>\n<body>\n<p>Bu kitabın adresi değişti. Yeni adres: '
            '<a href="{0}.html">{0}.html</a></p>\n</body>\n</html>\n'.format(yeni),
            encoding='utf-8')
    return list(YONLENDIRMELER)


def temizle_bayat_okuyucular():
    """BOOKS listesinde olmayan okuyucu dosyalarini siler.

    Kitap yeniden adlandirildiginda (or. 1.01 -> 1.01a) eski okuyucu diskte
    kaliyor, sonraki `git add -A` ile yeniden izlenmeye basliyor ve sitede
    olu bir adres olarak duruyordu. Iki kez yasandi, artik kurulumda
    kendiliginden temizleniyor.
    """
    gecerli = {folder + '.html' for folder, *_ in BOOKS}
    silinen = []
    for f in OKU.glob('kitap*.html'):
        if f.name not in gecerli:
            f.unlink()
            silinen.append(f.name)
    if silinen:
        print('  bayat okuyucu silindi: ' + ', '.join(silinen))
    return silinen


# Zenodo ciltleri. DOI olarak KAVRAM DOI'si yazilir: butun surumleri temsil
# eder ve her zaman en guncele cozulur. Surum DOI'si (kayit numarasi) hicbir
# yere yazilmaz; mimari kitabinda aylarca surum DOI'si kullanilip atif verenler
# ilk taslaga yonlendirilmisti.
CILTLER = {
    '1': {'doi': '10.5281/zenodo.21725876', 'kayit': 21936612, 'isbn': '978-625-00-4591-6',
          'dosya': 'Bilge ve Yonga - Cilt 1 - Kumdan Bilgisayara.pdf',
          'sayfa': 249, 'mb': 45},
    '2': {'doi': '10.5281/zenodo.21725924', 'kayit': 21936797, 'isbn': '978-625-90813-0-4',
          'dosya': 'Bilge ve Yonga - Cilt 2 - Hız ve Güç.pdf',
          'sayfa': 170, 'mb': 34},
    '3': {'doi': '10.5281/zenodo.21725978', 'kayit': 21936988, 'isbn': '978-625-90813-1-1',
          'dosya': 'Bilge ve Yonga - Cilt 3 - Buyrukların Dünyası.pdf',
          'sayfa': 217, 'mb': 38},
    '4': {'doi': '10.5281/zenodo.21854810', 'kayit': 21937158, 'isbn': '978-625-90813-2-8',
          'dosya': 'Bilge ve Yonga - Cilt 4 - İşlemcinin İçi.pdf',
          'sayfa': 225, 'mb': 43},
}


# Yol haritasindaki ciltler (`_notlar/seri-yol-haritasi.md`). Renkler
# yayimlanmis dort cildin renk cemberinde bos biraktigi yerlerden secildi.
GELECEK_CILTLER = [
    ('5', 'Durmayan Tezgâh', 'Sıra sıra dizilen işler hiç beklemeden akar', '#199e99'),
    ('6', 'Yakın Raf, Uzak Depo', 'Bilgisayar en çok kullandığını nerede saklar?', '#cc3d42'),
    ('7', 'Gözler, Kulaklar ve Eller', 'Bilgisayar dışarıyı nasıl duyar, dışarıya nasıl dokunur?', '#d64594'),
    ('8', 'Hep Birlikte', 'Bir işi bölüşmenin kuralları ve karışıklıkları', '#4c57bd'),
    ('9', 'Öğrenen Makineler', 'Yapay zekâ hangi donanımın üstünde çalışır?', '#d1a31f'),
]


def build_gelecek():
    """Gelecek ciltler seridi. Baglanti ve tarih verilmez."""
    p = ['  <div class="gelecek">',
         '    <p class="gelecek-not">Seri burada bitmiyor. Ders kitabının '
         'bölüm sırasını izleyen beş cilt daha planlandı.</p>',
         '    <ul class="gelecek-liste">']
    for no, ad, ozet, renk in GELECEK_CILTLER:
        p.append('      <li style="--accent:{}">'
                 '<span class="gelecek-no">{}. Cilt</span>'
                 '<span class="gelecek-ad">{}</span>'
                 '<span class="gelecek-ozet">{}</span></li>'
                 .format(renk, no, ad, ozet))
    p.append('    </ul>')
    p.append('  </div>')
    return '\n'.join(p)


def build_ciltler():
    """Ana sayfadaki cilt kartlarini uretir."""
    p = ['  <div class="cilt-grid">']
    for key, c in CILTLER.items():
        ad, _desc, renk = SERIES[key]
        n = len([b for b in BOOKS if b[1].split('.')[0] == key])
        if not n:
            continue
        p.append('    <article class="cilt" style="--accent:{}">'.format(renk))
        p.append('      <div class="cilt-ust">')
        p.append('        <span class="cilt-no">{}. Cilt</span>'.format(key))
        if _surum_no(key, 'ciltler'):
            p.append('        <span class="cilt-surum" title="{} tarihinde '
                     'güncellendi">Sürüm {}</span>'
                     .format(_surum(key, 'ciltler'), _surum_no(key, 'ciltler')))
        p.append('      </div>')
        # Kartin tamami DOI kaydina goturur. Indirme baglantisi degil: karta
        # dokununca 45 MB'lik dosyanin inmeye baslamasi istenmeyen bir surpriz
        # olur. DOI sayfasinda surumler, ISBN ve indirme zaten duruyor.
        if c['doi']:
            p.append('      <h3><a class="kart-bag" href="https://doi.org/{}" '
                     'target="_blank" rel="noopener">{}</a></h3>'
                     .format(c['doi'], ad))
        else:
            p.append('      <h3>{}</h3>'.format(ad))
        p.append('      <p class="cilt-bilgi">{} kitap · {} sayfa · '
                 'PDF, {} MB</p>'.format(n, c['sayfa'], c['mb']))
        if c['doi']:
            indir = ('https://zenodo.org/api/records/{}/files/{}/content'
                     .format(c['kayit'], quote(c['dosya'])))
            p.append('      <p class="cilt-doi"><a href="https://doi.org/{0}" '
                     'target="_blank" rel="noopener">doi.org/{0}</a></p>'
                     .format(c['doi']))
            # ISBN kalici numaradir, baglanti degil; duz metin olarak durur.
            if c.get('isbn'):
                p.append('      <p class="cilt-isbn">ISBN {}</p>'.format(c['isbn']))
            p.append('      <a class="cilt-btn" href="{}">Cildi indir</a>'.format(indir))
        else:
            p.append('      <p class="cilt-doi cilt-bekliyor">DOI alma süreci '
                     'sürüyor; numara gelince buraya eklenecek.</p>')
        p.append('    </article>')
    p.append('  </div>')
    return '\n'.join(p)


def build_index():
    """Kitaplari alt serilere gore bolumleyip index.html'i kurar."""
    tpl = (REPO / '_template_site.html').read_text(encoding='utf-8')
    blocks = []
    for key, (s_title, s_desc, s_color) in SERIES.items():
        books = [b for b in BOOKS if b[1].split('.')[0] == key]
        if not books:
            continue
        cards = '\n'.join(_card_html(*b) for b in books)
        blocks.append(
            f'  <div class="series-head" style="--accent:{s_color}">\n'
            f'    <span class="series-no">{key}. Seri</span>\n'
            f'    <h3>{s_title}</h3>\n'
            f'    <p>{s_desc}</p>\n'
            '  </div>\n'
            '  <div class="books-grid">\n' + cards + '\n  </div>')
    tpl = tpl.replace('__SERIES__', '\n\n'.join(blocks))
    kartlar, havuz = build_deste()
    tpl = tpl.replace('__DESTE__', kartlar)
    tpl = tpl.replace('__DESTE_HAVUZ__', havuz)
    tpl = tpl.replace('__CILTLER__', build_ciltler())
    tpl = tpl.replace('__GELECEK__', build_gelecek())
    tpl = tpl.replace('__COUNT__', str(len(BOOKS)))
    (REPO / 'index.html').write_text(tpl, encoding='utf-8')
    temizle_bayat_okuyucular()
    yaz_yonlendirmeler()
    uyar_bayat_klasor()


def build_sw():
    """sw-sablon.js dosyasini surum damgasiyla sw.js olarak yazar.

    Surum, index.html'in ozetinden VE sayfa gorsellerinin yol+boyut
    dokumunden turetilir; site her degistiginde hizmet calisani yenilenir
    ve eski onbellekler silinir.

    Damga once yalnizca index.html'den turetiliyordu. Gorsellerin JPEG
    kalitesi dusurulup dosyalar yariya indiginde index degismedigi icin
    damga da degismedi; onbellek 'once onbellek' calistigi icin siteyi
    daha once acmis okurlar eski buyuk dosyalari okumaya devam edecekti.
    Gorsel dokumu de ozete katilinca bu sessiz bayatlama bitiyor.
    """
    import hashlib
    sablon = REPO / 'sw-sablon.js'
    if not sablon.exists():
        return
    h = hashlib.sha1((REPO / 'index.html').read_bytes())
    for jpg in sorted(REPO.glob('kitap*/resimler/GPT_*.jpg')):
        h.update(('%s|%d;' % (jpg.name, jpg.stat().st_size)).encode())
    ozet = h.hexdigest()[:10]
    (REPO / 'sw.js').write_text(
        sablon.read_text(encoding='utf-8').replace('__SURUM__', ozet),
        encoding='utf-8')
    print('sw.js yazildi (surum %s)' % ozet)


if __name__ == '__main__':
    total = 0
    for i, (folder, no, title, sub, glow) in enumerate(BOOKS):
        prev = (BOOKS[i-1][0], BOOKS[i-1][1], BOOKS[i-1][2]) if i > 0 else None
        nxt = (BOOKS[i+1][0], BOOKS[i+1][1], BOOKS[i+1][2]) if i < len(BOOKS)-1 else None
        n, name = build_reader(folder, no, title, sub, glow, prev, nxt)
        ename, ecount = build_epub(folder, no, title, sub)
        total += n
        print(f'  okuyucu/{name}  ({n} sayfa)  +  {folder}/{ename}  ({ecount} görsel)')
    build_index()
    build_sw()
    print(f'index.html + {len(BOOKS)} okuyucu + {len(BOOKS)} EPUB, {total} sayfa toplam')
    for u in UYARILAR:
        print('  UYARI  ' + u)
