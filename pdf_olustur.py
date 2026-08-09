#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bilgisayar Mimarisi Serisi - Cocuk Kitaplari PDF Olusturucu
Her kitap icin ayri PDF uretir.
"""
import sys, io, os
# Windows konsolunda UTF-8 cikti icin
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass

import os
import re
import glob
import json
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage

# ─── Sabitler ───────────────────────────────────────────────────────────────
BASE_DIR = Path("G:/My Drive/Yazdığımız Kitaplar/Çocuk Kitapları/Bilgisayar Mimarisi Serisi")
# Gövde fontu Andika (SIL, OFL): okuma öğrenenler için tasarlandı, harfleri
# bilerek ayrılmış. Segoe Print el yazısı havası veriyordu ama büyük I ile
# küçük l aynı çizgiydi; Türkçede I, İ, ı, i ayrımı kritik olduğu için
# değiştirildi. Font depoda taşınıyor, sistemden bağımsız.
FONT_DIR = Path(__file__).resolve().parent / "fontlar"
FONT_NORMAL = FONT_DIR / "Andika-Regular.ttf"
FONT_BOLD   = FONT_DIR / "Andika-Bold.ttf"

# Gemini resimleri 2752x1536 (oran 1.792) -- sayfayi buna gore ayarla
# A4 yuksekligini koruyup eni orana gore hesapla
PAGE_H = 595.28  # A4 kisa kenari (pt)
PAGE_W = PAGE_H * 1.792  # = ~1066.7 pt (Gemini oranina uygun)
TEXT_BAND_RATIO = 0.25            # sayfanın alt %25'i metin bandı için başlangıç
BAND_ALPHA   = 0.65
TEXT_SIZE    = 16                 # yalnizca metin-only sayfalar ve kunye icin
# Metin bandinin uyarlamali boylari (buyukten kucuge) ve bant butcesi.
BANT_BOYLAR  = (22, 20, 19, 18, 16)
BANT_BUTCE   = 0.22               # sayfa yuksekliginin en cok bu kadari
LINE_SPACING = 22
BACK_COLOR   = (0.1, 0.137, 0.494)   # #1a237e koyu mavi
IMG_MAX_PX   = 1600               # resim en uzun kenarı (piksel)
IMG_JPEG_Q   = 80                 # JPEG sıkıştırma kalitesi
SITE_URL     = "bilgeveyonga.oguzergin.net"  # tüm kitapların yayımlandığı adres

# ─── Font kayıt ─────────────────────────────────────────────────────────────
def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont("SegoeP",  str(FONT_NORMAL)))
        pdfmetrics.registerFont(TTFont("SegoePB", str(FONT_BOLD)))
        return True
    except Exception as e:
        print(f"  [UYARI] Segoe Print yüklenemedi ({e}), Helvetica kullanılacak.")
        return False

FONTS_OK = register_fonts()
FONT_N = "SegoeP"  if FONTS_OK else "Helvetica"
FONT_B = "SegoePB" if FONTS_OK else "Helvetica-Bold"

# ─── MD ayrıştırıcı ─────────────────────────────────────────────────────────
def parse_md(md_path: Path):
    """MD dosyasını okuyup {meta, pages} döndürür."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    meta = {}
    pages = []   # her eleman: {"title": str, "text": str}

    # Başlık (ilk # satırı)
    for l in lines:
        if l.startswith("# "):
            meta["title"] = l[2:].strip()
            break

    # Meta alanları (**Seri:** vb.)
    for l in lines:
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", l)
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()

    # Sayfa blokları — ## Sayfa N ile başlayan bölümler
    page_splits = re.split(r"\n## Sayfa \d+", text)
    # İlk parça meta bilgisidir, atla
    for block in page_splits[1:]:
        # Başlık kısmı (— ile ayrılmış)
        title_match = re.match(r"\s*—\s*(.+)", block.split("\n")[0])
        page_title = title_match.group(1).strip() if title_match else ""

        # Metin: **Metin:** ile **Resim:** (veya ---) arasındaki kısım.
        # Metin alt satırda ya da **Metin:** ile aynı satırda olabilir (3.11 böyle).
        metin_match = re.search(r"\*\*Metin:\*\*[ \t]*\n?(.*?)(?=\*\*Resim:\*\*|^---|\Z)",
                                block, re.DOTALL | re.MULTILINE)
        metin = metin_match.group(1).strip() if metin_match else ""
        # **vurgu** işaretlerini kaldır (PDF metin bandı düz metin; yıldız görünmesin)
        metin = re.sub(r"\*\*(.+?)\*\*", r"\1", metin)
        # {B} ve {Y} konuşan işaretleri yalnızca tarayıcı okuyucusunda gösterilir
        metin = re.sub(r"\{[BYD]\}", "", metin)
        # Madde imi: PDF markdown listesi cozmuyor, ham "-" gorunmesin
        metin = re.sub(r"(?m)^[-*+] ", "• ", metin)
        # kod işaretlerini de kaldır: üç ters kesme bloğu ve tek ters kesme
        metin = re.sub(r"```\n?([\s\S]*?)```", r"\1", metin)
        metin = re.sub(r"`([^`\n]+)`", r"\1", metin)

        pages.append({"title": page_title, "text": metin})

    # "Deneme Zamanı" bölümünü ara (bölüm sonu soruları)
    deneme_match = re.search(r"## Deneme Zamanı\n(.*?)(?=^---|\Z)",
                             text, re.DOTALL | re.MULTILINE)
    deneme_lines = []
    if deneme_match:
        for line in deneme_match.group(1).strip().splitlines():
            line = line.strip()
            if not line:
                continue
            line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
            deneme_lines.append(line)

    # "Bugün Ne Öğrendik?" bölümünü ara
    ogrendik_match = re.search(r"## Bugün Ne Öğrendik\?\n(.*?)(?=^---|\Z)",
                                text, re.DOTALL | re.MULTILINE)
    if ogrendik_match:
        ogrendik_text = ogrendik_match.group(1).strip()
        # Markdown bold ve emoji temizle, satır satır al
        ogrendik_lines = []
        for line in ogrendik_text.splitlines():
            line = line.strip()
            if line:
                # **bold** -> düz metin
                line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
                # Emojileri ve desteklenmeyen Unicode'ları madde işaretine çevir
                # Satır başındaki tüm non-ASCII, non-Latin karakterleri temizle
                line = re.sub(r'^[^\x20-\x7E\u00C0-\u024F\u011E\u011F\u0130\u0131\u015E\u015F\u00D6\u00F6\u00DC\u00FC\u00C7\u00E7]+\s*', '\u2022 ', line)
                ogrendik_lines.append(line)
        meta["ogrendik"] = ogrendik_lines
        meta["deneme"] = deneme_lines

    return meta, pages

# ─── Resim seçici ───────────────────────────────────────────────────────────
def find_image(resimler_dir: Path, page_num: int):
    """
    Sayfa numarası için en güncel versiyonu döndürür.
    Gemini_Sayfa_N ile başlayan tüm dosyaları bulur, en son değiştirileni seçer.
    """
    if not resimler_dir.exists():
        return None
    # Sayfa numarasıyla eşleşen tüm dosyaları bul (GPT ve Gemini önekleri)
    candidates = []
    for f in resimler_dir.iterdir():
        if f.suffix.lower() != '.png':
            continue
        for prefix in (f"GPT_Sayfa_{page_num}", f"Gemini_Sayfa_{page_num}"):
            if f.name.startswith(prefix):
                # "Sayfa_1" ile "Sayfa_10" karışmasın
                rest = f.stem[len(prefix):]
                if rest == "" or rest.startswith("_"):
                    # Eski versiyonları atla
                    if "Eski" not in f.name:
                        candidates.append(f)
                break
    if not candidates:
        return None
    # En son değiştirileni döndür
    return max(candidates, key=lambda p: p.stat().st_mtime)

# ─── Yardımcı: resmi küçült ve JPEG sıkıştır ─────────────────────────────────
def compress_image(img_path: Path) -> io.BytesIO:
    """PNG resmi kenarlardan kirpip, küçültüp JPEG olarak sıkıştırır."""
    pil = PILImage.open(img_path).convert("RGB")
    iw, ih = pil.size
    # Kenarlardan %3 kirp (Gemini logosu + beyaz cerceve temizligi)
    margin_x = int(iw * 0.03)
    margin_y = int(ih * 0.03)
    pil = pil.crop((margin_x, margin_y, iw - margin_x, ih - margin_y))
    iw, ih = pil.size
    # En uzun kenarı IMG_MAX_PX'e küçült
    if max(iw, ih) > IMG_MAX_PX:
        ratio = IMG_MAX_PX / max(iw, ih)
        pil = pil.resize((int(iw * ratio), int(ih * ratio)), PILImage.LANCZOS)
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=IMG_JPEG_Q, optimize=True)
    buf.seek(0)
    return buf

# ─── Yardımcı: resmi sayfaya doldur (crop ile) ──────────────────────────────
def draw_full_page_image(c: canvas.Canvas, img_path: Path):
    """
    Resmi A4 landscape sayfasına kenar boşluksuz sığdırır.
    Resim önce sıkıştırılır (küçültme + JPEG).
    """
    try:
        buf = compress_image(img_path)
        img_reader = ImageReader(buf)
        iw, ih = img_reader.getSize()
    except Exception:
        return

    # Ölçek faktörü: sayfayı tamamen kapla
    scale = max(PAGE_W / iw, PAGE_H / ih)
    draw_w = iw * scale
    draw_h = ih * scale
    # Ortalama
    x = (PAGE_W - draw_w) / 2
    y = (PAGE_H - draw_h) / 2
    c.drawImage(img_reader, x, y, width=draw_w, height=draw_h,
                preserveAspectRatio=False)

# ─── Yardımcı: metin bandı ──────────────────────────────────────────────────
def draw_text_band(c: canvas.Canvas, text: str):
    """
    Sayfanın altına yarı saydam bant çizer, içine sarmalı metin yazar.
    Bant yüksekliği metne göre dinamik hesaplanır.
    """
    if not text:
        return

    margin_x = 30   # sol-sağ iç boşluk
    usable_w = PAGE_W - 2 * margin_x
    pad_y    = 12   # alt-üst iç boşluk

    # Yazı boyu uyarlamalı: banda bir bütçe konur, o bütçeye sığan EN BÜYÜK boy
    # seçilir. Eskiden her sayfada sabit 16 pt idi ve satıra ~121 karakter
    # düşüyordu; kısa metinli sayfalarda bandın boş yeri değerlendirilmiyordu.
    # En kötü durum değişmez: sabit 16 pt de uzun sayfalarda bandı %23'e
    # çıkarıyordu. (Okur geri bildirimi, 1 Ağustos 2026: EPUB'ın puntosu
    # PDF'ten daha okunaklı geliyor.)
    for boy in BANT_BOYLAR:
        satir_ara = boy * 1.38
        wrapped = wrap_text(c, text, FONT_N, boy, usable_w)
        band_h = len(wrapped) * satir_ara + 2 * pad_y
        if band_h <= PAGE_H * BANT_BUTCE:
            break
    n_lines  = len(wrapped)
    band_h   = max(band_h, 50)

    # Saydam dikdörtgen (ReportLab'da alpha için setFillAlpha)
    c.saveState()
    c.setFillColorRGB(0, 0, 0, alpha=BAND_ALPHA)
    c.rect(0, 0, PAGE_W, band_h, fill=1, stroke=0)
    c.restoreState()

    # Metni yaz
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_N, boy)
    y_cur = pad_y + (n_lines - 1) * satir_ara
    for line in wrapped:
        c.drawString(margin_x, y_cur, line)
        y_cur -= satir_ara
    c.restoreState()

# ─── Kelime sarma ───────────────────────────────────────────────────────────
def wrap_text(c: canvas.Canvas, text: str, font: str, size: int, max_w: float):
    """Metni verilen genişliğe sığacak şekilde satırlara böler."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [text]

# ─── Düz metin sayfası (resim yoksa) ─────────────────────────────────────────
def draw_text_only_page(c: canvas.Canvas, title: str, text: str):
    """Beyaz arka plan üzerine başlık + metin yazar."""
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Başlık
    c.saveState()
    c.setFillColorRGB(0.1, 0.1, 0.5)
    c.setFont(FONT_B, 20)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 60, title)
    c.restoreState()

    # Metin
    margin = 60
    usable_w = PAGE_W - 2 * margin
    wrapped  = wrap_text(c, text, FONT_N, TEXT_SIZE + 2, usable_w)
    c.saveState()
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont(FONT_N, TEXT_SIZE + 2)
    y_cur = PAGE_H - 110
    for line in wrapped:
        c.drawString(margin, y_cur, line)
        y_cur -= LINE_SPACING + 4
    c.restoreState()

# ─── Kapak resmi seçici ──────────────────────────────────────────────────────
def find_cover_image(resimler_dir: Path):
    """Öncelik sırası: GPT_Kapak, Gemini_Kapak_Yeni, Gemini_Kapak, yoksa Sayfa 1 resmi."""
    if not resimler_dir.exists():
        return None
    for ad in ("GPT_Kapak.png", "Gemini_Kapak_Yeni.png", "Gemini_Kapak.png"):
        kapak = resimler_dir / ad
        if kapak.exists():
            return kapak
    return find_image(resimler_dir, 1)

# ─── Kapak sayfası ──────────────────────────────────────────────────────────
def draw_cover(c: canvas.Canvas, meta: dict, cover_img: Path | None, kitap_no: str = ""):
    if cover_img:
        draw_full_page_image(c, cover_img)
        # Üstte sadece başlık arkasına ince yarı saydam şerit
        c.saveState()
        c.setFillColorRGB(0, 0, 0, alpha=0.45)
        c.rect(0, PAGE_H * 0.70, PAGE_W, PAGE_H * 0.22, fill=1, stroke=0)
        c.restoreState()
        # Altta yazar adı arkasına ince şerit
        c.saveState()
        c.setFillColorRGB(0, 0, 0, alpha=0.45)
        c.rect(0, 0, PAGE_W, 65, fill=1, stroke=0)
        c.restoreState()
    else:
        # Düz mavi arka plan
        c.saveState()
        c.setFillColorRGB(*BACK_COLOR)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.restoreState()

    # Kitap adı — üst kısımda
    title = meta.get("title", "Kitap")
    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 38)
    c.drawCentredString(PAGE_W / 2, PAGE_H * 0.82, title)
    c.restoreState()

    # Seri adı + alt seri
    alt_seri, _ = find_alt_seri(kitap_no)
    if alt_seri:
        seri_text = f"Bilge ve Yonga'nın Maceraları  —  {alt_seri['ad']}"
    else:
        seri_text = meta.get("Seri", "Bilgisayar Mimarisi Serisi")
    c.saveState()
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.setFont(FONT_N, 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H * 0.74, seri_text)
    c.restoreState()

    # Yazar — alt kısımda
    c.saveState()
    c.setFillColorRGB(1, 1, 0.9)
    c.setFont(FONT_B, 20)
    c.drawCentredString(PAGE_W / 2, 35, "Prof. Dr. Oğuz Ergin")
    c.restoreState()

# ─── Arka kapak ─────────────────────────────────────────────────────────────
def draw_back_cover(c: canvas.Canvas, meta: dict, kitap_no: str = ""):
    c.saveState()
    c.setFillColorRGB(*BACK_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Seri logosu / metni
    alt_seri, _ = find_alt_seri(kitap_no)
    alt_seri_ad = alt_seri["ad"] if alt_seri else "Çocuk Kitapları"

    c.saveState()
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 28)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 40, "Bilge ve Yonga'nın Maceraları")
    c.setFont(FONT_N, 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0, alt_seri_ad)
    c.setFont(FONT_N, 14)
    c.setFillColorRGB(0.8, 0.8, 0.8)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 40, "Prof. Dr. Oğuz Ergin")
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 65,
                        "© 2026 · CC BY-NC-ND 4.0")
    c.restoreState()

# ─── Künye sayfası ──────────────────────────────────────────────────────────
# Metin Av. Mehmet Arın Gülüm'ün hazırladığı uygulama şartnamesinin G.2
# bölümünden BİREBİR alınmıştır; sözcükleri değiştirilmez.
# Surumler surumler.json'da tutulur: her kitabin ve her cildin kendi numarasi
# vardir. Kitabin metni degisince o kitabin ikinci hanesi artar; icinde
# degisiklik olan cildin de ikinci hanesi artar.
def kitap_surumu(klasor_adi: str) -> str:
    """Kunyeye basilacak surum satiri. Kayit yoksa satir bos doner."""
    yol = Path(__file__).with_name("surumler.json")
    if not yol.exists():
        return ""
    kayit = json.loads(yol.read_text(encoding="utf-8"))["kitaplar"].get(klasor_adi)
    return "Sürüm %s, %s" % (kayit["surum"], kayit["tarih"]) if kayit else ""


KUNYE_SATIRLARI = [
    ("b", 15, "KÜNYE"),
    ("", 0, ""),
    ("b", 11, "© 2026 Prof. Dr. Oğuz Ergin"),
    ("b", 11, "{kitap}"),
    ("n", 10, "Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi"),
    ("n", 10, "Ankara, 2026"),
    ("", 0, ""),
    ("n", 10, "Bu eser, Creative Commons Atıf-GayriTicari-Türetilemez 4.0 Uluslararası"),
    ("n", 10, "(CC BY-NC-ND 4.0) lisansı ile açık erişime sunulmuştur."),
    ("n", 10, "Lisans metni: https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr"),
    ("", 0, ""),
    ("b", 10, "LİSANSIN KAPSAMADIĞI TÜM HAKLAR SAKLIDIR."),
    ("n", 10, "“Bilge ve Yonga” seri adı, “Bilge” ve “Yonga” karakter adları ile"),
    ("n", 10, "figürleri, seri amblemi, marka hakları, eser sahibinin adı ve unvanı ile"),
    ("n", 10, "manevi haklar bu lisansın kapsamı dışındadır ve ayrı yazılı izne bağlıdır."),
    ("", 0, ""),
    ("n", 10, "Metin ve veri madenciliği ile yapay zekâ modeli eğitimi bakımından haklar"),
    ("n", 10, "açıkça saklı tutulmuştur."),
    ("", 0, ""),
    ("n", 10, "Eserler olduğu gibi sunulmaktadır; belirli bir amaca uygunluk konusunda"),
    ("n", 10, "garanti verilmez."),
    ("", 0, ""),
    ("n", 10, "Ticari kullanım izni ve sorularınız için: bilgi@oguzergin.net"),
    ("n", 10, "Telif ve lisans politikası: bilgeveyonga.oguzergin.net/telif-ve-lisans.html"),
    ("", 0, ""),
    ("n", 10, "Atıf: Ergin, O. (2026). Bilge ve Yonga: Bilgisayar Mimarisi Çocuk"),
    ("n", 10, "Kitapları Serisi. https://bilgeveyonga.oguzergin.net"),
    ("", 0, ""),
    ("n", 9,  "Bilge ve Yonga © 2026 Prof. Dr. Oğuz Ergin · CC BY-NC-ND 4.0"),
]


def draw_kunye_page(c: canvas.Canvas, kitap_adi: str, surum: str = ""):
    """Krem zeminli künye sayfası çizer (şartname G.3, üretim hattı çözümü)."""
    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    c.saveState()
    c.setFillColorRGB(0.20, 0.16, 0.29)
    y = PAGE_H - 52
    for bicim, boy, metin in KUNYE_SATIRLARI:
        if not metin:
            y -= 9
            continue
        c.setFont(FONT_B if bicim == "b" else FONT_N, boy)
        c.drawString(52, y, metin.replace("{kitap}", kitap_adi))
        if metin == "Ankara, 2026" and surum:
            y -= boy + 5.0
            c.drawString(52, y, surum)
        y -= boy + 5.5
    c.restoreState()

# ─── "Bugün Ne Öğrendik?" sayfası ─────────────────────────────────────────────
def draw_ogrendik_page(c: canvas.Canvas, ogrendik_lines: list,
                       baslik: str = "Bugün Ne Öğrendik?"):
    """Kitabın sonuna özet ya da deneme sayfası çizer."""
    # Arka plan: yumuşak krem rengi
    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Başlık
    c.saveState()
    c.setFillColorRGB(0.1, 0.137, 0.494)
    c.setFont(FONT_B, 30)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 70, baslik)
    c.restoreState()

    # Dekoratif çizgi
    c.saveState()
    c.setStrokeColorRGB(0.1, 0.137, 0.494)
    c.setLineWidth(2)
    c.line(PAGE_W * 0.2, PAGE_H - 85, PAGE_W * 0.8, PAGE_H - 85)
    c.restoreState()

    # Maddeleri yaz
    margin_x = 80
    usable_w = PAGE_W - 2 * margin_x
    y_cur = PAGE_H - 130
    item_spacing = 8

    c.saveState()
    c.setFillColorRGB(0.15, 0.15, 0.15)

    for line in ogrendik_lines:
        # "Yanıtlar" bir madde değil, alt başlıktır: üstünde boşluk bırakılır,
        # ayrı renkte ve kalın basılır. Böylece sorulardan ayrılır.
        if line.strip().rstrip(':') == "Yanıtlar":
            y_cur -= 18
            c.saveState()
            c.setFillColorRGB(0.72, 0.42, 0.10)
            c.setFont(FONT_B, TEXT_SIZE + 6)
            c.drawString(margin_x, y_cur, "Yanıtlar")
            c.setStrokeColorRGB(0.72, 0.42, 0.10)
            c.setLineWidth(1)
            c.line(margin_x, y_cur - 6, margin_x + 120, y_cur - 6)
            c.restoreState()
            y_cur -= (TEXT_SIZE + 16)
            continue

        # Satırı sarma
        wrapped = wrap_text(c, line, FONT_N, TEXT_SIZE + 2, usable_w)
        for wl in wrapped:
            c.setFont(FONT_N, TEXT_SIZE + 2)
            c.drawString(margin_x, y_cur, wl)
            y_cur -= LINE_SPACING + 2
        y_cur -= item_spacing

    c.restoreState()

# ─── Alt Seri Tanımları ────────────────────────────────────────────────────
# ─── Alt seriler ────────────────────────────────────────────────────────────
# Kitap listesi DİSKTEN türetilir: her kitapXX.YY[h]-* klasörü bir kitaptır ve
# başlığı kendi md dosyasının ilk satırından okunur. Böylece yeni kitap eklemek
# için burada bir şey değiştirmek gerekmez; yalnızca isterseniz aşağıdaki
# açıklama sözlüğüne bir satır eklersiniz. (Eskiden liste elle tutuluyordu ve
# 3.11 eklenmeyi unutulduğu için hiçbir PDF'in seri sayfasında görünmüyordu.)
SERI_BILGI = [
    ("Kumdan Bilgisayara",    "1", (0.18, 0.55, 0.78)),
    ("Hız ve Güç",            "2", (0.85, 0.45, 0.15)),
    ("Buyrukların Dünyası",   "3", (0.30, 0.65, 0.30)),
    ("İşlemcinin İçi",        "4", (0.54, 0.31, 0.75)),
]

ACIKLAMALAR = {
    '1.1a': 'Silisyumdan yonga nasıl yapılır?',
    '1.1b': 'Yarı iletken ve transistörün doğuşu',
    '1.2a': 'Transistörler ve ikili sayı sistemi',
    '1.3': 'Bilgisayarın temel bileşenleri',
    '1.4': 'Buyruk yürütüm döngüsü',
    '1.5': 'Donanım ve yazılım katmanları',
    '1.6': 'Moore Yasası ve transistör artışı',
    '1.7': 'Basit ve karmaşık buyruk felsefeleri',
    '1.8': 'RISC-V ve açık kaynak donanım',
    '1.9': 'Güç tüketimi eğilimleri ve güç duvarı',
    '1.10': 'Yapay zeka hızlandırıcıları: GPU, TPU, NPU',
    '2.1': 'Güvenilirlik ve hata düzeltme',
    '2.2': 'Saat hızı ve başarım',
    '2.3': 'Gecikme, işlem hacmi ve koşutluk',
    '2.4': 'Başarım: adım boyu × saat hızı',
    '2.5': 'Amdahl Yasası ve darboğaz',
    '2.6': 'Sınama programları ve bilgisayar karşılaştırma',
    '2.7': 'Başarım eğilimleri ve çok çekirdekli çözüm',
    '2.8': 'Gustafson Yasası ve işi büyüterek hızlanma',
    '2.9': 'Bellek duvarı ve önbellek çözümü',
    '2.10': 'Gerçek dünya işlemci karşılaştırmaları',
    '3.1b': 'Buyruk kümesi mimarisi ve Getir-Çöz-Yürüt',
    '3.2': 'Yazmaçlar, bellek düzeni ve bayt sırası',
    '3.3': 'Buyruk biçimleri ve adresleme kipleri',
    '3.4': 'Dallanma, döngüler ve altyordamlar',
    '3.5': 'Derleme zinciri: derleyici, çevirici, bağlayıcı',
    '3.6': 'Aritmetik buyruklar: toplama, çıkarma, çarpma',
    '3.7': 'Mantık buyrukları: VE, VEYA, DEĞİL',
    '3.8': 'x0 yazmacı ve sıfırın gücü',
    '3.9': 'Yığıt ve altyordamlar',
    '3.10': 'Veri aktarma buyrukları: yükle ve sakla',
    '3.11': 'Hata ayıklama: ara nokta, adım adım yürütme',
}


def _klasor_no(ad: str):
    """kitap1.01a-kumdan-bilgisayar -> ('1', '1.1a')"""
    m = re.match(r"kitap(\d+)\.(\d+)([a-z]?)-", ad)
    if not m:
        return None, None
    return m.group(1), "%s.%d%s" % (m.group(1), int(m.group(2)), m.group(3))


def _kitap_basligi(dizin):
    try:
        for satir in (dizin / (dizin.name + ".md")).read_text(encoding="utf-8").splitlines():
            if satir.startswith("# "):
                return satir[2:].strip()
    except Exception:
        pass
    return dizin.name


def _ana_tema(dizin):
    """Kitabın md dosyasındaki '**Ana tema:**' satırı; liste sayfasında
    açıklama olarak kullanılır. Sözlüğü elle güncellemek unutuluyordu."""
    try:
        for satir in (dizin / (dizin.name + ".md")).read_text(
                encoding="utf-8").splitlines():
            if satir.startswith("**Ana tema:**"):
                return satir.split("**", 2)[2].lstrip(": ").strip()
    except Exception:
        pass
    return ""


def _alt_serileri_kur():
    seriler = []
    for ad, anahtar, renk in SERI_BILGI:
        kitaplar = []
        for d in sorted(BASE_DIR.glob("kitap%s.*" % anahtar)):
            if not d.is_dir():
                continue
            seri_no, no = _klasor_no(d.name)
            if seri_no != anahtar:
                continue
            kitaplar.append((no, _kitap_basligi(d),
                             ACIKLAMALAR.get(no) or _ana_tema(d)))
        if kitaplar:
            seriler.append({"ad": ad, "no": anahtar, "renk": renk,
                            "kitaplar": kitaplar})
    return seriler


ALT_SERILER = _alt_serileri_kur()


def find_alt_seri(kitap_no: str):
    """Kitap numarasından alt seriyi ve seri içi sırasını bulur."""
    for seri in ALT_SERILER:
        for idx, (no, title, desc) in enumerate(seri["kitaplar"]):
            if no == kitap_no:
                return seri, idx
    return None, None


def _kapak_yolu(kitap_no: str):
    """Kitap numarasından yayımlanmış (GPT kapaklı) kitabın kapak dosyasını bulur."""
    # Numara harf eki tasiyabilir (1.1a, 1.1b). Klasor adinda iki hane + harf var.
    m = re.fullmatch(r"(\d+)\.(\d+)([a-z]?)", kitap_no.strip())
    if not m:
        return None
    maj, min_, harf = m.group(1), int(m.group(2)), m.group(3)
    pattern = f"kitap{maj}.{min_:02d}{harf}-*"
    for d in BASE_DIR.glob(pattern):
        p = d / "resimler" / "GPT_Kapak.png"
        if p.exists():
            return p
    return None


def _kapak_thumb(path: Path, px_w: int = 380):
    """Kapak görselini PDF'e gömmek için küçültülmüş JPEG'e çevirir."""
    im = PILImage.open(path).convert("RGB")
    w, h = im.size
    ph = max(1, round(h * px_w / w))
    im = im.resize((px_w, ph), PILImage.LANCZOS)
    bio = io.BytesIO()
    im.save(bio, format="JPEG", quality=78)
    bio.seek(0)
    return ImageReader(bio)


def draw_seri_page(c: canvas.Canvas, current_kitap_no: str):
    """Alt serideki YAYIMLANMIŞ kitapları kapak görselleriyle listeleyen sayfa.

    Henüz yayımlanmamış kitaplar ve diğer alt seriler bu sayfada anılmaz;
    yalnızca 'yeni maceralar yolda' notu düşülür.
    """
    seri, _ = find_alt_seri(current_kitap_no)
    if not seri:
        return

    seri_renk = seri["renk"]

    # Arka plan: yumuşak krem
    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Ana seri adı (üstte küçük)
    c.saveState()
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont(FONT_N, 13)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 40, "Bilge ve Yonga'nın Maceraları")
    c.restoreState()

    # Alt seri başlığı
    c.saveState()
    c.setFillColorRGB(*seri_renk)
    c.setFont(FONT_B, 26)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 75, seri["ad"])
    c.restoreState()

    # Dekoratif çizgi (alt seri renginde)
    c.saveState()
    c.setStrokeColorRGB(*seri_renk)
    c.setLineWidth(2)
    c.line(PAGE_W * 0.25, PAGE_H - 90, PAGE_W * 0.75, PAGE_H - 90)
    c.restoreState()

    # Yayımlanmış kitaplar (kapak görseli olanlar); mevcut kitap kapaksız olsa da listeye girer
    yayinda = []
    for no, title, desc in seri["kitaplar"]:
        kapak = _kapak_yolu(no)
        if kapak or no == current_kitap_no:
            yayinda.append((no, title, desc, kapak))
    if not yayinda:
        return

    # Kart düzeni: iki sütun, kapak solda, yazı sağda. Satır yüksekliği kitap
    # sayısından hesaplanıyor; sabit olduğunda 12 kitaplık seri sayfaya
    # sığmıyor, alttaki notun üstüne biniyordu.
    y_top = PAGE_H - 118
    y_bot = 58
    rows = (len(yayinda) + 1) // 2
    row_h = (y_top - y_bot) / rows
    COVER_H = min(73.7, row_h - 15)
    COVER_W = COVER_H * 16 / 9
    kenar = 62
    col_w = (PAGE_W - 2 * kenar - 24) / 2
    col_x = [kenar, kenar + col_w + 24]
    yazi_w = col_w - COVER_W - 14
    baslik_punto = 12.5 if row_h >= 66 else 11
    aciklama_punto = 10 if row_h >= 66 else 8.6

    for i, (no, title, desc, kapak) in enumerate(yayinda):
        col = i // rows
        row = i % rows
        x = col_x[col]
        img_y = y_top - row * row_h - COVER_H
        is_current = (no == current_kitap_no)

        c.saveState()
        if kapak:
            c.drawImage(_kapak_thumb(kapak), x, img_y, width=COVER_W, height=COVER_H)
            if is_current:
                c.setStrokeColorRGB(*seri_renk)
                c.setLineWidth(2.5)
                c.rect(x - 2, img_y - 2, COVER_W + 4, COVER_H + 4, fill=0, stroke=1)

        tx = x + COVER_W + 14
        if is_current:
            c.setFillColorRGB(*seri_renk)
            font_b = FONT_B
            marker = ">> "
        else:
            c.setFillColorRGB(0.2, 0.2, 0.2)
            font_b = FONT_N
            marker = ""
        c.setFont(font_b, baslik_punto)
        baslik = f"{marker}Kitap {no}: {title}"
        while (c.stringWidth(baslik, font_b, baslik_punto) > yazi_w
               and len(baslik) > 12):
            baslik = baslik[:-2] + "…"
        c.drawString(tx, img_y + COVER_H - baslik_punto - 4, baslik)

        c.setFont(FONT_N, aciklama_punto)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        satirlar = wrap_text(c, desc, FONT_N, aciklama_punto, yazi_w)[:2]
        if len(satirlar) == 2 and c.stringWidth(desc, FONT_N, aciklama_punto) > 2 * yazi_w:
            satirlar[1] = satirlar[1].rstrip() + "…"
        ay = img_y + COVER_H - baslik_punto - 20
        for satir in satirlar:
            c.drawString(tx, ay, satir)
            ay -= aciklama_punto + 3
        c.restoreState()

    # Altta yeni kitap muştusu. Liste artık diskten türetildiği için "eksik kitap"
    # koşulu hiç sağlanmıyordu; seri sürdüğü için not koşulsuz gösteriliyor.
    if True:
        c.saveState()
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.setFont(FONT_B, 13)
        c.drawCentredString(PAGE_W / 2, 42, "Bilge ve Yonga'nın yeni maceraları yolda!")
        c.restoreState()

def draw_seriler_ozet_page(c: canvas.Canvas, current_kitap_no: str):
    """Yayımlanmış TÜM alt serileri kapak görselleriyle tanıtan kapanış sayfası + site bağlantısı.

    Yalnızca kapağı olan (yayımlanmış) kitaplar çizilir; kapağı olmayan seriler
    (henüz görselleri üretilmemiş) bu sayfada anılmaz.
    """
    # Yayımlanmış serileri topla (en az bir kapağı olanlar)
    yayin_seriler = []
    for seri in ALT_SERILER:
        kapaklar = [(no, title, _kapak_yolu(no)) for (no, title, desc) in seri["kitaplar"]]
        kapaklar = [(no, title, k) for (no, title, k) in kapaklar if k]
        if kapaklar:
            yayin_seriler.append((seri, kapaklar))
    if not yayin_seriler:
        return

    # Arka plan: yumuşak krem
    c.saveState()
    c.setFillColorRGB(1.0, 0.98, 0.93)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()

    # Üst başlık
    c.saveState()
    c.setFillColorRGB(0.1, 0.137, 0.494)
    c.setFont(FONT_B, 25)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 48, "Bilge ve Yonga'nın Tüm Maceraları")
    c.setFont(FONT_N, 12.5)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 68, "Her kitap tek bir fikri, baştan sona bir hikâyeyle anlatır")
    c.restoreState()

    # Seri blokları — dikeyde ortalanmış dağıt
    n = len(yayin_seriler)
    region_top = PAGE_H - 100      # başlığın altı
    region_bot = 70               # site şeridinin üstü
    block_h = (region_top - region_bot) / n
    # Kapak ölçüsü en kalabalık seriye göre; bütün sıralar aynı ölçüde
    # ve sayfa içinde kalıyor.
    en_kalabalik = max(len(k) for _, k in yayin_seriler)
    kapak_gap = 5.0
    kapak_w = min(94.0, (PAGE_W - 72 - (en_kalabalik - 1) * kapak_gap) / en_kalabalik)
    for bi, (seri, kapaklar) in enumerate(yayin_seriler):
        by = region_top - bi * block_h - 18
        renk = seri["renk"]
        # Seri adı ortada; altında kaçıncı cilt olduğu ve kitap sayısı
        c.saveState()
        c.setFillColorRGB(*renk)
        c.setFont(FONT_B, 19)
        c.drawCentredString(PAGE_W / 2, by, seri["ad"])
        c.setFont(FONT_N, 10.5)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(PAGE_W / 2, by - 15,
                            f"{seri['no']}. Cilt  ·  {len(kapaklar)} kitap")
        c.restoreState()
        # Kapak satırı
        m = len(kapaklar)
        cw = kapak_w
        ch = cw * 9 / 16
        gap = kapak_gap
        row_w = m * cw + (m - 1) * gap
        x0 = (PAGE_W - row_w) / 2
        # Kapaklar kendi başlığına yakın, bir sonraki başlığa uzak
        cy = by - 24 - ch
        for i, (no, title, k) in enumerate(kapaklar):
            x = x0 + i * (cw + gap)
            try:
                c.drawImage(_kapak_thumb(k, px_w=200), x, cy, width=cw, height=ch)
            except Exception:
                continue
            if no == current_kitap_no:
                c.saveState()
                c.setStrokeColorRGB(*renk)
                c.setLineWidth(2.5)
                c.rect(x - 1.5, cy - 1.5, cw + 3, ch + 3, fill=0, stroke=1)
                c.restoreState()

    # Altta site çağrısı — vurgulu şerit
    c.saveState()
    c.setFillColorRGB(0.1, 0.137, 0.494)
    c.rect(0, 0, PAGE_W, 52, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 16)
    c.drawCentredString(PAGE_W / 2, 28, "Bütün kitaplar ücretsiz, çevrimiçi:")
    c.setFont(FONT_B, 15)
    c.setFillColorRGB(1, 0.85, 0.4)
    c.drawCentredString(PAGE_W / 2, 9, SITE_URL)
    c.restoreState()


# ─── Ana PDF oluşturucu ──────────────────────────────────────────────────────
def build_pdf(kitap_dir: Path):
    # MD dosyasını bul
    md_files = list(kitap_dir.glob("*.md"))
    if not md_files:
        print(f"  [ATLANDI] MD bulunamadi: {kitap_dir.name}")
        return

    md_path = md_files[0]
    resimler_dir = kitap_dir / "resimler"

    meta, pages = parse_md(md_path)
    # Yeni format: kitap1.06-... → "1.6", eski format: kitap01-... → "1" (→ "1.1")
    m = re.search(r"kitap(\d+)\.(\d+)([a-z]?)", kitap_dir.name)
    if m:
        # Sondaki harf de numaranın parçası: 1.02b → "1.2b". Atılırsa seri
        # listesindeki kayıtla eşleşmiyor ve vurgu çerçevesi çizilmiyor.
        kitap_no_str = f"{m.group(1)}.{int(m.group(2))}{m.group(3)}"
    else:
        m2 = re.search(r"kitap(\d+)", kitap_dir.name)
        if m2:
            old_no = int(m2.group(1))
            # Eski numaraları yeni seri numaralarına çevir
            if 1 <= old_no <= 5:
                kitap_no_str = f"1.{old_no}"
            elif 6 <= old_no <= 10:
                kitap_no_str = f"2.{old_no - 5}"
            elif 11 <= old_no <= 15:
                kitap_no_str = f"3.{old_no - 10}"
            else:
                kitap_no_str = str(old_no)
        else:
            kitap_no_str = "??"

    # PDF çıktı yolu
    title_safe = re.sub(r'[<>:"/\\|?*]', '-', meta.get("title", kitap_dir.name))
    pdf_path = kitap_dir / f"{title_safe}.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=(PAGE_W, PAGE_H))
    # Üstveri — şartname F.3. Eskiden /Creator "anonymous", /Subject
    # "unspecified" ve /Keywords boş kalıyordu; dosya siteden koptuğunda
    # kime ait olduğunu söyleyemiyordu.
    kitap_adi = meta.get("title", "Kitap")
    c.setTitle(kitap_adi)
    c.setAuthor("Prof. Dr. Oğuz Ergin")
    c.setCreator("Prof. Dr. Oğuz Ergin")
    c.setSubject(f"{kitap_adi} — Bilge ve Yonga: Bilgisayar Mimarisi "
                 f"Çocuk Kitapları Serisi")
    c.setKeywords("bilgisayar mimarisi, çocuk kitabı, Bilge ve Yonga, "
                  "açık erişim, CC BY-NC-ND 4.0, Oğuz Ergin, STEM, "
                  "bilgisayar bilimi, 7-12 yaş")

    # ── Kapak ──
    cover_img = find_cover_image(resimler_dir)
    draw_cover(c, meta, cover_img, kitap_no_str)
    c.showPage()

    # ── İçerik sayfaları ──
    for i, page in enumerate(pages, start=1):
        img_path = find_image(resimler_dir, i)

        if img_path:
            draw_full_page_image(c, img_path)
            draw_text_band(c, page["text"])
        else:
            draw_text_only_page(c, page["title"], page["text"])

        c.showPage()

    # ── "Bugün Ne Öğrendik?" sayfası ──
    ogrendik = meta.get("ogrendik")
    if ogrendik:
        draw_ogrendik_page(c, ogrendik)
        c.showPage()

    # ── "Deneme Zamanı" sayfası ──
    deneme = meta.get("deneme")
    if deneme:
        draw_ogrendik_page(c, deneme, "Deneme Zamanı")
        c.showPage()

    # ── Seri kitaplar sayfası (mevcut alt seri) ──
    draw_seri_page(c, kitap_no_str)
    c.showPage()

    # ── Tüm seriler özeti + site bağlantısı ──
    draw_seriler_ozet_page(c, kitap_no_str)
    c.showPage()

    # ── Künye (şartname G.3) ──
    draw_kunye_page(c, kitap_adi, kitap_surumu(kitap_dir.name))
    c.showPage()

    # ── Arka kapak ──
    draw_back_cover(c, meta, kitap_no_str)
    c.showPage()

    c.save()
    print(f"  ✓ {pdf_path.name}  ({len(pages)} sayfa içerik)")

    # PDF viewer ayarlarını pikepdf ile ekle
    try:
        import pikepdf
        with pikepdf.open(str(pdf_path), allow_overwriting_input=True) as pdf:
            pdf.Root['/PageLayout'] = pikepdf.Name('/SinglePage')
            pdf.Root['/PageMode'] = pikepdf.Name('/FullScreen')
            pdf.Root['/ViewerPreferences'] = pikepdf.Dictionary({
                '/FitWindow': True,
                '/CenterWindow': True,
                '/DisplayDocTitle': True,
            })
            pdf.save(str(pdf_path))
        print(f"    (tam ekran + tek sayfa ayarlandı)")
    except ImportError:
        print(f"    (pikepdf yüklü değil, viewer ayarları eklenmedi)")
    except Exception as e:
        print(f"    (viewer ayarı eklenemedi: {e})")

# ─── Tüm kitapları tara ──────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Bilgisayar Mimarisi Serisi - PDF Olusturucu")
    print("=" * 60)

    kitap_dirs = sorted(BASE_DIR.glob("kitap*"))
    if not kitap_dirs:
        print("HATA: Hicbir kitap klasoru bulunamadi!")
        return

    for kitap_dir in kitap_dirs:
        if not kitap_dir.is_dir():
            continue
        print(f"\n[{kitap_dir.name}]")
        try:
            build_pdf(kitap_dir)
        except Exception as e:
            print(f"  [HATA] {e}")
            import traceback; traceback.print_exc()

    print("\n" + "=" * 60)
    print("Tamamlandı.")

if __name__ == "__main__":
    main()
