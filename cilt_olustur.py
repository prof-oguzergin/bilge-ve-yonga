"""Alt seri basina toplu cilt PDF'i uretir (Zenodo/DOI ve ISBN icin).

Ciltler DEPOYA GIRMEZ: uc cilt birlikte ~330 MB tutar ve Pages'in 1 GB
sinirini zorlar. Cikti Drive'daki _ciltler klasorune yazilir, ciltler
Zenodo'da yayimlanir, site oraya baglanir.

Sayfa duzeni (cilt basina):
  1. cilt kapagi (alt seri rengi + kitap kapaklarindan olusan izgara)
  2. kunye (cilt adi, DOI, ISBN, lisans)
  3. icindekiler
  4+ her kitap: kapak -> icerik sayfalari -> "Bugun Ne Ogrendik?"
  son-1. tum seriler ozeti (site baglantisi)
  son. arka kapak
"""
import importlib.util
import io
import os
import re
import sys
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

REPO = Path(__file__).resolve().parent
CIKTI = Path(r'G:\My Drive\Yazdığımız Kitaplar\Çocuk Kitapları'
             r'\Bilgisayar Mimarisi Serisi\_ciltler')

# pdf_olustur ve build_web'in cizim islevleri yeniden kullaniliyor
_s = importlib.util.spec_from_file_location('po', REPO / 'pdf_olustur.py')
po = importlib.util.module_from_spec(_s)
sys.modules['po'] = po
_s.loader.exec_module(po)
_s2 = importlib.util.spec_from_file_location('bw', REPO / 'build_web.py')
bw = importlib.util.module_from_spec(_s2)
sys.modules['bw'] = bw
_s2.loader.exec_module(bw)

W, H = po.PAGE_W, po.PAGE_H
FN, FB = po.FONT_N, po.FONT_B


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def koyult(rgb, k=0.55):
    return tuple(x * k for x in rgb)


def kitaplar(seri):
    """build_web'deki BOOKS sirasina gore o alt serinin kitaplari."""
    return [b for b in bw.BOOKS if b[1].split('.')[0] == seri]


def thumb(yol, px=300):
    im = PILImage.open(yol).convert('RGB')
    im.thumbnail((px, px * 10), PILImage.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=82)
    b.seek(0)
    return ImageReader(b)


# ─── cilt kapagi ─────────────────────────────────────────────────────────────
def cilt_kapak(c, seri, ad, alt, renk, kitap_listesi):
    rgb = hex_rgb(renk)
    c.saveState()
    c.setFillColorRGB(*koyult(rgb, 0.42))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()

    # Kapak izgarasi sagda. Genislik kenar bosluguna gore hesaplanir; eskiden
    # sabit orandi ve dorduncu sutun sayfadan tasiyordu.
    n = len(kitap_listesi)
    KENAR, ARA, SUT = 44, 9, 3
    alan = W * 0.42 - KENAR
    kw = (alan - (SUT - 1) * ARA) / SUT
    kh = kw * (H / W)
    satir = (n + SUT - 1) // SUT
    x0 = W - KENAR - alan
    y0 = H / 2 + (satir * kh + (satir - 1) * ARA) / 2 - kh
    c.saveState()
    for i, (klasor, no, baslik, _sub, _g) in enumerate(kitap_listesi):
        p = po.find_cover_image(po.BASE_DIR / klasor / 'resimler')
        if not p:
            continue
        x = x0 + (i % SUT) * (kw + ARA)
        y = y0 - (i // SUT) * (kh + ARA)
        try:
            c.drawImage(thumb(p, 260), x, y, width=kw, height=kh,
                        preserveAspectRatio=True, anchor='c', mask='auto')
        except Exception:
            pass
    c.restoreState()

    # sol tarafta baslik blogu
    c.saveState()
    c.setFillColorRGB(*koyult(rgb, 0.42))
    c.setFillAlpha(0.86)
    c.rect(0, 0, W * 0.56, H, fill=1, stroke=0)
    c.restoreState()

    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FN, 17)
    c.drawString(56, H - 76, 'Bilge ve Yonga')
    c.setFont(FN, 12)
    c.setFillColorRGB(*[min(1, x + 0.45) for x in rgb])
    c.drawString(56, H - 98, 'Bilgisayar Mimarisi Çocuk Kitapları Serisi')

    # Baslik blogu dikeyde ortalanir; eskiden ust yariya sabitlenmisti ve
    # sol altta genis bir bosluk kaliyordu.
    bas = po.wrap_text(c, ad, FB, 46, W * 0.46)
    altl = po.wrap_text(c, alt, FN, 15, W * 0.44)
    yuk = len(bas) * 52 + 12 + len(altl) * 21 + 34
    y = H / 2 + yuk / 2

    c.setFillColorRGB(1, 1, 1)
    c.setFont(FB, 46)
    for satir_metin in bas:
        c.drawString(56, y, satir_metin)
        y -= 52

    c.setFont(FN, 15)
    c.setFillColorRGB(0.93, 0.93, 0.93)
    y -= 12
    for satir_metin in altl:
        c.drawString(56, y, satir_metin)
        y -= 21

    c.setFont(FB, 19)
    c.setFillColorRGB(*[min(1, x + 0.5) for x in rgb])
    c.drawString(56, y - 22, '%d kitap bir arada' % len(kitap_listesi))

    c.setFont(FN, 12)
    c.setFillColorRGB(0.86, 0.86, 0.86)
    c.drawString(56, 74, 'Açık erişim · CC BY-NC-ND 4.0 · bilgeveyonga.oguzergin.net')
    c.setFont(FB, 20)
    c.setFillColorRGB(1, 1, 0.92)
    c.drawString(56, 42, 'Prof. Dr. Oğuz Ergin')
    c.restoreState()


# ─── kunye ───────────────────────────────────────────────────────────────────

def cilt_surumu(seri: str) -> str:
    """Cildin kunyesine basilacak surum satiri. Kayit yoksa bos doner."""
    import json
    yol = Path(__file__).with_name('surumler.json')
    if not yol.exists():
        return ''
    k = json.loads(yol.read_text(encoding='utf-8'))['ciltler'].get(str(seri))
    return 'Sürüm %s, %s' % (k['surum'], k['tarih']) if k else ''


def cilt_kunye(c, cilt_adi, doi, isbn, surum=""):
    """Kitap kunyesinin cilt surumu: DOI/ISBN kunye blogunun icinde durur ve
    atif satiri seriyi degil bu cildi gosterir."""
    satirlar = []
    for bicim, boy, metin in po.KUNYE_SATIRLARI:
        satirlar.append((bicim, boy, metin))
        if metin == 'Ankara, 2026':
            if surum:
                satirlar.append(('n', 10, surum))
            satirlar.append(('', 0, ''))
            satirlar.append(('b', 10, 'DOI: %s' % (doi or '(atanacak)')))
            satirlar.append(('b', 10, 'ISBN: %s' % (isbn or '(atanacak)')))
    # atif satirlari cilde gore yenilenir
    yeni = []
    for bicim, boy, metin in satirlar:
        if metin.startswith('Atıf: Ergin'):
            yeni.append((bicim, boy, 'Atıf: Ergin, O. (2026). Bilge ve Yonga: '
                                     'Bilgisayar Mimarisi Çocuk'))
            continue
        if metin.startswith('Kitapları Serisi. https'):
            yeni.append((bicim, boy, 'Kitapları Serisi — %s.' % cilt_adi))
            yeni.append((bicim, boy, ('https://doi.org/%s' % doi) if doi
                         else 'https://bilgeveyonga.oguzergin.net'))
            continue
        yeni.append((bicim, boy, metin))

    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()
    c.saveState()
    c.setFillColorRGB(0.20, 0.16, 0.29)
    y = H - 44
    for bicim, boy, metin in yeni:
        if not metin:
            y -= 8
            continue
        c.setFont(FB if bicim == 'b' else FN, boy)
        c.drawString(52, y, metin.replace('{kitap}', cilt_adi))
        y -= boy + 5.0
    c.restoreState()


# ─── icindekiler ─────────────────────────────────────────────────────────────
def icindekiler(c, ad, renk, kitap_listesi):
    rgb = hex_rgb(renk)
    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*koyult(rgb, 0.75))
    c.rect(0, H - 96, W, 96, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FB, 30)
    c.drawString(56, H - 62, 'İçindekiler')
    c.setFont(FN, 14)
    c.drawRightString(W - 56, H - 58, ad)

    # Adim, kitap sayisina gore hesaplanir. Eskiden sabit 42 punto idi ve
    # 11 kitapli ciltlerde son kitap alt sinira takilip listeye girmiyordu.
    ust, altsinir = H - 138, 52
    adim = min(42.0, (ust - altsinir) / max(1, len(kitap_listesi)))
    c.setFillColorRGB(0.20, 0.16, 0.29)
    y = ust
    for klasor, no, baslik, alt, _g in kitap_listesi:
        c.setFont(FB, 15)
        c.drawString(64, y, no)
        c.drawString(120, y, baslik)
        c.setFont(FN, 10.5)
        c.setFillColorRGB(0.42, 0.38, 0.48)
        c.drawString(120, y - 16, alt[:100])
        c.setFillColorRGB(0.20, 0.16, 0.29)
        y -= adim
    c.restoreState()


# ─── cilt ────────────────────────────────────────────────────────────────────
# DOI olarak KAVRAM DOI'si yazilir, surum DOI'si degil. Kavram DOI butun
# surumleri temsil eder ve her zaman en guncele cozulur; surum DOI'si tek bir
# surume cakilir. (Mimari kitabinda aylarca surum DOI'si kullanilip atif
# verenler ilk taslaga yonlendirilmisti.)
CILTLER = [
    ('1', 'Kumdan Bilgisayara', '10.5281/zenodo.21725876'),
    ('2', 'Hız ve Güç', '10.5281/zenodo.21725924'),
    ('3', 'Buyrukların Dünyası', '10.5281/zenodo.21725978'),
    ('4', 'İşlemcinin İçi', '10.5281/zenodo.21854810'),
]


def cilt_uret(seri, cilt_adi, doi='', isbn=''):
    ad, alt, renk = bw.SERIES[seri]
    kl = kitaplar(seri)
    CIKTI.mkdir(parents=True, exist_ok=True)
    dosya = CIKTI / ('Bilge ve Yonga - Cilt %s - %s.pdf' % (seri, cilt_adi))

    c = canvas.Canvas(str(dosya), pagesize=(W, H))
    c.setTitle('Bilge ve Yonga — Cilt %s: %s' % (seri, cilt_adi))
    c.setAuthor('Prof. Dr. Oğuz Ergin')
    c.setCreator('Prof. Dr. Oğuz Ergin')
    c.setSubject('Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi — '
                 'Cilt %s: %s (%d kitap)' % (seri, cilt_adi, len(kl)))
    c.setKeywords('bilgisayar mimarisi, çocuk kitabı, Bilge ve Yonga, açık erişim, '
                  'CC BY-NC-ND 4.0, Oğuz Ergin, STEM, bilgisayar bilimi, 7-12 yaş, RISC-V')

    cilt_kapak(c, seri, cilt_adi, alt, renk, kl)
    c.showPage()
    cilt_kunye(c, 'Cilt %s: %s' % (seri, cilt_adi), doi, isbn,
               cilt_surumu(seri))
    c.showPage()
    icindekiler(c, cilt_adi, renk, kl)
    c.showPage()

    sayfa = 3
    for klasor, no, baslik, _alt, _g in kl:
        # Gorseller Drive'daki kaynak klasorde: depoda yalnizca JPEG surumleri
        # var ve find_image PNG asillarini arar.
        kd = po.BASE_DIR / klasor
        md = list(kd.glob('kitap*.md'))[0]
        meta, pages = po.parse_md(md)
        res = kd / 'resimler'
        po.draw_cover(c, meta, po.find_cover_image(res), no)
        c.showPage()
        sayfa += 1
        for i, page in enumerate(pages, start=1):
            img = po.find_image(res, i)
            if img:
                po.draw_full_page_image(c, img)
                po.draw_text_band(c, page['text'])
            else:
                po.draw_text_only_page(c, page['title'], page['text'])
            c.showPage()
            sayfa += 1
        if meta.get('ogrendik'):
            po.draw_ogrendik_page(c, meta['ogrendik'])
            c.showPage()
            sayfa += 1

    po.draw_seriler_ozet_page(c, kl[0][1])
    c.showPage()
    po.draw_back_cover(c, {'title': 'Cilt %s: %s' % (seri, cilt_adi)}, kl[0][1])
    c.showPage()
    c.save()

    try:
        import pikepdf
        with pikepdf.open(str(dosya), allow_overwriting_input=True) as pdf:
            pdf.Root['/PageLayout'] = pikepdf.Name('/SinglePage')
            pdf.Root['/ViewerPreferences'] = pikepdf.Dictionary({
                '/FitWindow': True, '/CenterWindow': True, '/DisplayDocTitle': True})
            pdf.save(str(dosya))
    except Exception as e:
        print('    (viewer ayari eklenemedi: %s)' % e)

    mb = dosya.stat().st_size / 1048576
    print('  ✓ %-52s %3d kitap, %4d sayfa, %6.1f MB'
          % (dosya.name, len(kl), sayfa + 2, mb))
    return dosya


if __name__ == '__main__':
    print('=' * 72)
    print('Bilge ve Yonga — cilt uretimi')
    print('=' * 72)
    for seri, ad, doi in CILTLER:
        cilt_uret(seri, ad, doi=doi)
    print()
    print('cikti:', CIKTI)
