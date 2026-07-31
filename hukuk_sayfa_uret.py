"""Hukuki belgeleri site sayfalarina cevirir.

Kaynak: Av. Mehmet Arin Gulum'un uygulama sartnamesi v1.0 (26 Tem 2026),
bolum A. Donusturme kurallari A.2'den birebir alinmistir.

Metinlerin sozcuklerine dokunulmaz; yalnizca bicim donusturulur, sartnamenin
"yayimlanmaz" dedigi bolumler atilir ve karara baglanmis alanlar doldurulur.

Kullanim:  python hukuk_sayfa_uret.py [--kuru]
"""
import io
import os
import re
import shutil
import sys
from html import escape

PAKET = r'C:\Users\Z GAMES\Downloads\bilgeveyonga'
KOK = os.path.dirname(os.path.abspath(__file__))
KURU = '--kuru' in sys.argv

YURURLUK = '27 Temmuz 2026'          # sartname A.2/6: fiilen yayimlandigi tarih
SURUM = '1.0'
ADRES = 'TOBB ETÜ, Söğütözü Cad. No:43, Söğütözü, Ankara'

# Sartname A.1 — alti sayfa
SAYFALAR = [
    ('telif-ve-lisans', '02-telif-lisans-ve-ticari-kullanim-politikasi.md',
     'Telif ve Lisans', 'HUKUKİ METİN',
     'Serinin telif bildirimi, CC BY-NC-ND 4.0 lisansının kapsamı, '
     '"ticari olmayan" kaydının yorumu ve ticari kullanım izni.'),
    ('kullanim-kosullari', '01-kullanim-kosullari.md',
     'Kullanım Koşulları', 'HUKUKİ METİN',
     'Bilge ve Yonga sitesinin kullanım koşulları: serbest kullanımlar, '
     'sitenin kendisine ilişkin kurallar ve ihlal bildirim kanalı.'),
    ('ticari-kullanim', '03-ticari-kullanim-izin-basvurusu.md',
     'Ticari Kullanım İzni', 'BAŞVURU',
     'Bilge ve Yonga kitaplarını ticari olarak kullanmak için izin '
     'başvurusu: hangi bilgiler gerekir, süreç nasıl işler.'),
    ('yapay-zeka-bildirimi', '06-yapay-zeka-ve-veri-madenciligi-rezervasyonu.md',
     'Yapay Zekâ ve Veri Madenciliği Bildirimi', 'BİLDİRİM',
     'Bilge ve Yonga içeriğinin yapay zekâ modeli eğitimi ve veri '
     'madenciliği bakımından hakları açıkça saklı tutulmuştur.'),
    ('egitimciler', '08-egitimciler-icin-kullanim-ve-atif-rehberi.md',
     'Öğretmenler, Veliler ve Kütüphaneler İçin Rehber', 'REHBER',
     'Kitapları sınıfta, evde ve kütüphanede izin almadan nasıl '
     'kullanabilirsiniz? Neyin serbest olduğunu anlatan kısa rehber.'),
    ('gizlilik', '05-kvkk-aydinlatma-ve-cerez-politikasi.md',
     'Gizlilik ve Çerez Politikası', 'AYDINLATMA METNİ',
     'Bilge ve Yonga sitesinde çerez yoktur. KVKK aydınlatma metni, '
     'ölçüm tercihi ve veri sorumlusu künyesi.'),
]

# Sartname A.2/3: bu bolumler yayimlanmaz (ic calisma notu)
ATILACAK = ('HUKUKİ DAYANAKLAR', 'DOĞRULANAMAYAN ATIFLAR',
            'YAYIMDAN ÖNCE DOLDURULACAK ALANLAR')

# Karara baglanmis alanlar (bkz. TASLAK_hukuk_kararlari.md)
DEGISTIR = [
    # lisans@ acilmayacak, bilgi@ yeterli
    ('`lisans@oguzergin.net` [bu adres ticari izin başvuruları için '
     'ayrılmıştır; açılana kadar `bilgi@oguzergin.net` kullanılır]',
     '`bilgi@oguzergin.net`'),
    ('[Ayrı bir lisans adresi açılırsa buraya yazılacak: lisans@oguzergin.net]',
     '`bilgi@oguzergin.net`'),
    ('[lisans@oguzergin.net]', '`bilgi@oguzergin.net`'),
    ('lisans@oguzergin.net', 'bilgi@oguzergin.net'),
    # tebligat adresi
    ("[Türkiye'de tebligata elverişli açık adres — Ankara]", ADRES),
    ('[TEBLİGAT ADRESİ — yayımdan önce doldurulacak]', ADRES),
    ('[TEBLİGAT ADRESİ]', ADRES),
    ('[POSTA ADRESİ — sözleşme aşaması için ayrıca bildirilir]', ADRES),
    # yanit suresi taahhut edilmiyor
    ('[Beş iş günü]', 'En kısa sürede'),
    # ISBN yok
    ("[Serinin ISBN'i yoktur / ISBN: ________]", "Serinin ISBN'i henüz yoktur."),
    # yururluk tarihi
    ('[Sitede yayımlandığı tarih — örn. 1 Ağustos 2026]', YURURLUK),
    ('[yürürlük tarihi]', YURURLUK),
    # ticari izin sayfasinin gercek adresi
    ('[belge adresi — `bilgeveyonga.oguzergin.net/ticari-izin`]',
     '`bilgeveyonga.oguzergin.net/ticari-kullanim.html`'),
    # marka tescili henuz yapilmadi; bos parantez yayimlanmaz (A.2/4)
    ('Marka tescil durumu: [MARKA BAŞVURU TARİHİ VE NUMARASI — başvuru '
     'yapıldığında doldurulacak].',
     'Marka tescil başvurusu bu metnin yürürlük tarihi itibarıyla henüz '
     'yapılmamıştır.'),
    ('[MARKA BAŞVURU TARİHİ VE NUMARASI]', 'Henüz başvurulmadı'),
    # tarih ispati Asama 5'te alinacak
    ('[Arşiv bağlantıları alındıktan sonra buraya eklenecek.]',
     'Arşiv bağlantıları yayım tarihinden sonra eklenecektir.'),
    ('[Zaman damgası seri numarası buraya yazılacak.]',
     'Zaman damgası seri numarası alındığında eklenecektir.'),
]

# Basvuru formunun bos alanlari ve ornek dugme etiketleri: bunlar bizim
# doldurmadigimiz karar alanlari degil, okurun dolduracagi yerler.
FORM_ALANI = re.compile(
    r'^\[(…+|GG\.?AA\.?YYYY|GGAAYYYY|Başvuran adı|BasvuranAdi|Kullanım türü|'
    r'Ek olarak sunulur|Kurgusal adres|Örnek:.*| Kapalı kalsın | Ölçüme izin ver |'
    r'Gizlilik ve Çerez Politikası)\]$')


def markdown_ici(s):
    """Satir ici bicimlendirme. Kacislar once yapilir."""
    s = escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\*\w])\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+|[^)]+\.html[^)]*)\)',
               r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<![">=\w])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', s)
    return s


def tablo_html(satirlar):
    """Markdown tablosunu tablo-kap icinde tabloya cevirir (A.2/2)."""
    hucre = [[h.strip() for h in s.strip().strip('|').split('|')]
             for s in satirlar]
    hucre = [h for h in hucre
             if not all(re.fullmatch(r':?-{2,}:?', c or '-') for c in h)]
    if not hucre:
        return ''
    bas, govde = hucre[0], hucre[1:]
    basliksiz = all(not c for c in bas)
    out = ['<div class="tablo-kap"><table>']
    if not basliksiz:
        out.append('<thead><tr>' +
                   ''.join('<th>' + markdown_ici(c) + '</th>' for c in bas) +
                   '</tr></thead>')
    else:
        govde = hucre
    out.append('<tbody>')
    for satir in govde:
        out.append('<tr>' + ''.join('<td>' + markdown_ici(c) + '</td>'
                                    for c in satir) + '</tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)


def kutu_sinifi(metin):
    """Alinti blogunun turu (A.2/2): uyari mi, olur mu, duz mu."""
    d = metin.lower()
    if any(k in d for k in ('dikkat', 'uyarı', 'yasak', 'ihlal', 'risk',
                            'unutmayın', 'önemli')):
        return 'kutu uyari'
    if any(k in d for k in ('izin almanıza gerek yok', 'serbesttir',
                            'gerek yoktur', 'yapabilirsiniz')):
        return 'kutu olur'
    return 'kutu'


def govde_uret(md):
    """Markdown govdesini HTML'e cevirir; (govde, icindekiler) dondurur."""
    # 1) yayimlanmayacak bolumleri at
    for b in ATILACAK:
        i = md.find('\n## ' + b)
        if i > 0:
            md = md[:i]
    # 2) karara baglanmis alanlar
    for a, b in DEGISTIR:
        md = md.replace(a, b)
    # 3) baslik satirini ve ilk kunye tablosunu at (sablon zaten tasiyor)
    satirlar = md.split('\n')
    if satirlar and satirlar[0].startswith('# '):
        satirlar = satirlar[1:]

    html, icindekiler, sayac = [], [], 0
    i, n = 0, len(satirlar)
    ilk_h2_gecti = False
    while i < n:
        s = satirlar[i]
        d = s.strip()

        if not d or d == '---':
            i += 1
            continue

        if d.startswith('## '):
            sayac += 1
            ilk_h2_gecti = True
            bas = d[3:].strip()
            kimlik = 'b%d' % sayac
            html.append('<h2 id="%s">%s</h2>' % (kimlik, markdown_ici(bas)))
            icindekiler.append('<li><a href="#%s">%s</a></li>'
                               % (kimlik, markdown_ici(bas)))
            i += 1
            continue

        if d.startswith('#### '):
            html.append('<h4>' + markdown_ici(d[5:].strip()) + '</h4>')
            i += 1
            continue
        if d.startswith('### '):
            html.append('<h3>' + markdown_ici(d[4:].strip()) + '</h3>')
            i += 1
            continue

        # kunye tablosu: ilk h2'den once gelen tablo atlanir
        if d.startswith('|'):
            blok = []
            while i < n and satirlar[i].strip().startswith('|'):
                blok.append(satirlar[i])
                i += 1
            if ilk_h2_gecti:
                html.append(tablo_html(blok))
            continue

        if d.startswith('>'):
            blok = []
            while i < n and (satirlar[i].strip().startswith('>')
                             or not satirlar[i].strip()):
                if not satirlar[i].strip():
                    if (i + 1 < n
                            and satirlar[i + 1].strip().startswith('>')):
                        blok.append('')
                        i += 1
                        continue
                    break
                blok.append(re.sub(r'^>\s?', '', satirlar[i].strip()))
                i += 1
            duz = '\n'.join(blok)
            ic = ''.join('<p>' + markdown_ici(p.strip()) + '</p>'
                         for p in re.split(r'\n\s*\n', duz) if p.strip())
            html.append('<div class="%s">%s</div>' % (kutu_sinifi(duz), ic))
            continue

        if re.match(r'^[-*+] ', d) or re.match(r'^\d+\. ', d):
            sirali = bool(re.match(r'^\d+\. ', d))
            etiket = 'ol' if sirali else 'ul'
            html.append('<%s>' % etiket)
            while i < n:
                c = satirlar[i].strip()
                if not c:
                    if i + 1 < n and re.match(r'^([-*+] |\d+\. )',
                                              satirlar[i + 1].strip()):
                        i += 1
                        continue
                    break
                if not re.match(r'^([-*+] |\d+\. )', c):
                    break
                html.append('<li>' + markdown_ici(
                    re.sub(r'^([-*+] |\d+\. )', '', c)) + '</li>')
                i += 1
            html.append('</%s>' % etiket)
            continue

        # duz paragraf
        blok = []
        while i < n and satirlar[i].strip() and not re.match(
                r'^(#{2,4} |\||>|[-*+] |\d+\. |---)', satirlar[i].strip()):
            blok.append(satirlar[i].strip())
            i += 1
        if blok:
            html.append('<p>' + markdown_ici(' '.join(blok)) + '</p>')
    return '\n'.join(html), '\n'.join(icindekiler)


def main():
    sablon = io.open(os.path.join(PAKET, 'uygulama', 'kok',
                                  '_sayfa-sablonu.html'),
                     encoding='utf-8').read()
    if not KURU:
        shutil.copy(os.path.join(PAKET, 'uygulama', 'kok', 'belge.css'),
                    os.path.join(KOK, 'belge.css'))
        print('  belge.css koke kopyalandi')

    for slug, kaynak, baslik, etiket, aciklama in SAYFALAR:
        md = io.open(os.path.join(PAKET, 'belgeler', kaynak),
                     encoding='utf-8').read()
        govde, icindekiler = govde_uret(md)

        # "Kisaca" bolumu ozet seride tasinir (A.2/2)
        m = re.search(r'<h2 id="b1">Kısaca</h2>(.*?)(?=<h2 )', govde, re.S)
        ozet_serit = ''
        if m:
            ozet_serit = ('<div class="ozet-serit">' + m.group(1).strip()
                          + '</div>')
            govde = govde.replace(m.group(0), '')
            # numaralari kaydirmadan icindekilerden Kisaca satirini cikar
            icindekiler = re.sub(
                r'<li><a href="#b1">Kısaca</a></li>\s*', '', icindekiler)

        sayfa = (sablon
                 .replace('{{SAYFA_BASLIGI}}', escape(baslik, quote=True))
                 .replace('{{META_ACIKLAMA}}', escape(aciklama, quote=True))
                 .replace('{{SLUG}}', slug)
                 .replace('{{ETIKET}}', escape(etiket))
                 .replace('{{OZET}}', escape(aciklama))
                 .replace('{{ICINDEKILER}}', icindekiler)
                 .replace('{{GOVDE}}', ozet_serit + '\n' + govde)
                 .replace('{{YURURLUK}}', YURURLUK)
                 .replace('{{SURUM}}', SURUM))

        # sablonun kendi yorum bloğu siteye gitmez
        sayfa = re.sub(r'<!--\s*ŞABLON.*?-->\s*', '', sayfa, count=1, flags=re.S)

        kalan = re.findall(r'\[[^\]\n]{3,80}\]', sayfa)
        kalan = [k for k in kalan if not k.startswith('[^')
                 and not FORM_ALANI.match(k)]
        durum = 'DOLDURULMAMIŞ ALAN: %d' % len(kalan) if kalan else 'temiz'
        print('  %-24s %6d bayt  %2d bölüm  %s'
              % (slug + '.html', len(sayfa), icindekiler.count('<li>'), durum))
        for k in kalan[:3]:
            print('      !', k[:70])
        if not KURU:
            io.open(os.path.join(KOK, slug + '.html'), 'w',
                    encoding='utf-8').write(sayfa)


main()
