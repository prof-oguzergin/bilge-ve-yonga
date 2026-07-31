# -*- coding: utf-8 -*-
"""
gorsel-telif-goml.py — JPEG/PNG görsellerine telif, lisans ve TDM üstverisi gömer.

NE YAPAR
    Verilen klasördeki her JPEG ve PNG dosyasına:
      · XMP paketi  (dc:rights, dc:creator, dc:title, xmpRights:Marked,
                     xmpRights:WebStatement, xmpRights:UsageTerms,
                     xmpRights:Owner, photoshop:Credit/Source,
                     Iptc4xmpCore:CreatorWorkURL, plus:*, cc:license,
                     cc:attributionName/URL, tdm:reservation, tdm:policy)
      · EXIF alanları (JPEG): Artist, Copyright, ImageDescription, Software
      gömer.

    XMP, IPTC'nin bugünkü standart taşıyıcısıdır (IPTC Photo Metadata Standard
    XMP üzerine kuruludur); bu nedenle ayrıca eski IPTC-IIM (APP13) bloğu
    yazılmaz.

ÖNEMLİ — KAYIPSIZ ÇALIŞIR
    Betik görüntüyü yeniden KODLAMAZ. JPEG'de yalnızca APP1 bölütlerini
    (segment) değiştirir, PNG'de yalnızca bir iTXt yığını (chunk) ekler.
    Görüntü verisi bit düzeyinde aynı kalır, dosya boyutu yalnızca birkaç
    kilobayt artar.

KULLANIM (Windows PowerShell)
    # Ne yapılacağını göster:
    python gorsel-telif-goml.py "C:\\repo\\bilgeveyonga" --kontrol

    # Uygula:
    python gorsel-telif-goml.py "C:\\repo\\bilgeveyonga"

    # EPUB dosyalarının İÇİNDEKİ görselleri de işle:
    python gorsel-telif-goml.py "C:\\repo\\bilgeveyonga" --epub-ici

    # Kapak görsellerine görünür filigran da bas (YENİDEN KODLAR — bkz. not):
    python gorsel-telif-goml.py "C:\\repo\\bilgeveyonga" --filigran-kapak

GEREKSİNİM
    XMP + EXIF gömme  : yalnızca standart kütüphane (Pillow yalnızca EXIF
                        yapısını kurmak için kullanılır; kuruluysa kullanılır,
                        değilse EXIF atlanır ve XMP yine yazılır)
    Filigran          : Pillow  (pip install Pillow)

FİLİGRAN NOTU
    --filigran-kapak yalnızca dosya adı "kapak"/"cover" içeren görsellere
    uygulanır ve bu görselleri YENİDEN KODLAR (kalite 92, EXIF/XMP korunur).
    İç sayfa görsellerine filigran ÖNERİLMEZ: çocuk kitabında okunabilirliği
    ve resmin bütünlüğünü bozar.

ÇIKIŞ KODU
    0 hepsi başarılı · 1 en az bir hata · 2 kullanım hatası
"""

from __future__ import annotations

import argparse
import io
import shutil
import struct
import sys
import unicodedata
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bilgeveyonga_ortak as OY  # noqa: E402

try:
    from PIL import Image
    PILLOW_VAR = True
except ImportError:  # pragma: no cover
    PILLOW_VAR = False

XMP_ONEK = b"http://ns.adobe.com/xap/1.0/\x00"
EXIF_ONEK = b"Exif\x00\x00"
PNG_IMZA = b"\x89PNG\r\n\x1a\n"
PNG_XMP_ANAHTAR = b"XML:com.adobe.xmp"


# ==========================================================================
# XMP paketi
# ==========================================================================

GORSEL_XMP = """<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Bilge ve Yonga gorsel ustveri 1.0">
 <rdf:RDF xmlns:rdf="{rdf}">
  <rdf:Description rdf:about=""
    xmlns:dc="{dc}"
    xmlns:xmp="{xmp}"
    xmlns:xmpRights="{xmpRights}"
    xmlns:photoshop="{photoshop}"
    xmlns:Iptc4xmpCore="{iptc}"
    xmlns:plus="{plus}"
    xmlns:cc="{cc}"
    xmlns:tdm="{tdm}">

   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{baslik}</rdf:li></rdf:Alt></dc:title>
   <dc:creator><rdf:Seq><rdf:li>{yazar}</rdf:li></rdf:Seq></dc:creator>
   <dc:description><rdf:Alt><rdf:li xml:lang="tr">{aciklama}</rdf:li></rdf:Alt></dc:description>
   <dc:rights><rdf:Alt>
     <rdf:li xml:lang="tr">{haklar_tr}</rdf:li>
     <rdf:li xml:lang="x-default">{haklar_en}</rdf:li>
   </rdf:Alt></dc:rights>
   <dc:publisher><rdf:Bag><rdf:li>{yayinci}</rdf:li></rdf:Bag></dc:publisher>
   <dc:type><rdf:Bag><rdf:li>Image</rdf:li></rdf:Bag></dc:type>

   <xmp:CreatorTool>{yazar}</xmp:CreatorTool>

   <xmpRights:Marked>True</xmpRights:Marked>
   <xmpRights:WebStatement>{web_beyani}</xmpRights:WebStatement>
   <xmpRights:Owner><rdf:Bag><rdf:li>{yazar}</rdf:li></rdf:Bag></xmpRights:Owner>
   <xmpRights:UsageTerms><rdf:Alt>
     <rdf:li xml:lang="x-default">{kullanim}</rdf:li>
   </rdf:Alt></xmpRights:UsageTerms>

   <photoshop:Credit>{yazar}</photoshop:Credit>
   <photoshop:Source>{site}</photoshop:Source>
   <photoshop:Headline>{baslik}</photoshop:Headline>

   <Iptc4xmpCore:CreatorContactInfo rdf:parseType="Resource">
    <Iptc4xmpCore:CiEmailWork>{eposta}</Iptc4xmpCore:CiEmailWork>
    <Iptc4xmpCore:CiUrlWork>{site}/</Iptc4xmpCore:CiUrlWork>
   </Iptc4xmpCore:CreatorContactInfo>

   <plus:Licensor><rdf:Seq><rdf:li rdf:parseType="Resource">
     <plus:LicensorName>{yazar}</plus:LicensorName>
     <plus:LicensorURL>{telif_sayfa}</plus:LicensorURL>
   </rdf:li></rdf:Seq></plus:Licensor>

   <cc:license rdf:resource="{lisans_uri}"/>
   <cc:attributionName>{yazar}</cc:attributionName>
   <cc:attributionURL rdf:resource="{site}/"/>
   <cc:morePermissions rdf:resource="{ticari}"/>

   <tdm:reservation>{tdm_rez}</tdm:reservation>
   <tdm:policy>{tdm_pol}</tdm:policy>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""


def xmp_uret(baslik: str, aciklama: str) -> bytes:
    k = OY.xml_kacir
    return GORSEL_XMP.format(
        rdf=OY.NS["rdf"], dc=OY.NS["dc"], xmp=OY.NS["xmp"],
        xmpRights=OY.NS["xmpRights"], photoshop=OY.NS["photoshop"],
        iptc=OY.NS["Iptc4xmpCore"], plus=OY.NS["plus"], cc=OY.NS["cc"],
        tdm=OY.NS["tdm"],
        baslik=k(baslik), yazar=k(OY.ESER_SAHIBI), aciklama=k(aciklama),
        haklar_tr=k(OY.HAKLAR_PARAGRAF), haklar_en=k(OY.HAKLAR_PARAGRAF_EN),
        yayinci=k(OY.YAYINCI), web_beyani=OY.SAYFA_TELIF,
        kullanim=k(OY.KULLANIM_KOSULLARI_KISA), site=OY.SITE,
        eposta=OY.ILETISIM_LISANS, telif_sayfa=OY.SAYFA_TELIF,
        lisans_uri=OY.LISANS_URI, ticari=OY.SAYFA_TICARI,
        tdm_rez=OY.TDM_REZERVASYON, tdm_pol=OY.TDM_POLITIKA,
    ).encode("utf-8")


# ==========================================================================
# EXIF — ASCII alanlar (EXIF ASCII tipi Türkçe harf taşımaz, sadeleştirilir)
# ==========================================================================

def ascii_sadelestir(s: str) -> str:
    esleme = str.maketrans({
        "ı": "i", "İ": "I", "ş": "s", "Ş": "S", "ğ": "g", "Ğ": "G",
        "ç": "c", "Ç": "C", "ö": "o", "Ö": "O", "ü": "u", "Ü": "U",
        "â": "a", "î": "i", "û": "u", "©": "(c)", "—": "-", "–": "-",
        "·": "-", "“": '"', "”": '"', "’": "'", "‘": "'", "…": "...",
    })
    s = s.translate(esleme)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s


EXIF_TELIF = ascii_sadelestir(
    f"© {OY.TELIF_YILI} {OY.ESER_SAHIBI}. CC BY-NC-ND 4.0 "
    f"({OY.LISANS_URI}). Lisansin kapsamadigi tum haklar saklidir. "
    f"Ticari kullanim ve yapay zeka egitimi izne baglidir: {OY.ILETISIM_LISANS}"
)
EXIF_SANATCI = ascii_sadelestir(OY.ESER_SAHIBI)
EXIF_YAZILIM = ascii_sadelestir(f"{OY.SITE_ALAN} — Bilge ve Yonga")


def exif_uret(aciklama: str, mevcut: bytes | None) -> bytes | None:
    """EXIF APP1 gövdesi üretir ('Exif\\x00\\x00' önekiyle)."""
    if not PILLOW_VAR:
        return None
    try:
        e = Image.Exif()
        if mevcut:
            try:
                e.load(mevcut)
            except Exception:  # noqa: BLE001
                e = Image.Exif()
        e[0x013B] = EXIF_SANATCI                    # Artist
        e[0x8298] = EXIF_TELIF                      # Copyright
        e[0x010E] = ascii_sadelestir(aciklama)      # ImageDescription
        e[0x0131] = EXIF_YAZILIM                    # Software
        return e.tobytes()
    except Exception:  # noqa: BLE001
        return None


# ==========================================================================
# JPEG — kayıpsız APP1 değişimi
# ==========================================================================

def jpeg_isle(veri: bytes, baslik: str, aciklama: str) -> bytes:
    if not veri.startswith(b"\xff\xd8"):
        raise ValueError("JPEG değil (SOI yok)")

    i = 2
    bolutler: list[tuple[int, bytes]] = []
    mevcut_exif: bytes | None = None
    while i < len(veri) - 1:
        if veri[i] != 0xFF:
            break
        isaret = veri[i + 1]
        if isaret in (0xD8, 0x01) or 0xD0 <= isaret <= 0xD7:
            i += 2
            continue
        if isaret == 0xDA:                     # SOS — görüntü verisi başlıyor
            break
        if i + 4 > len(veri):
            break
        uzunluk = struct.unpack(">H", veri[i + 2:i + 4])[0]
        govde = veri[i + 4:i + 2 + uzunluk]
        if isaret == 0xE1:                     # APP1
            if govde.startswith(XMP_ONEK):
                pass                           # eski XMP atılır
            elif govde.startswith(EXIF_ONEK):
                mevcut_exif = govde
            else:
                bolutler.append((isaret, govde))
        else:
            bolutler.append((isaret, govde))
        i += 2 + uzunluk

    kuyruk = veri[i:]

    yeni_exif = exif_uret(aciklama, mevcut_exif)
    yeni_xmp = XMP_ONEK + xmp_uret(baslik, aciklama)
    if len(yeni_xmp) + 2 > 0xFFFF:
        raise ValueError("XMP paketi tek APP1 bölütüne sığmıyor")

    cikti = bytearray(b"\xff\xd8")

    def bolut_yaz(isaret: int, govde: bytes) -> None:
        cikti.extend(b"\xff" + bytes([isaret]))
        cikti.extend(struct.pack(">H", len(govde) + 2))
        cikti.extend(govde)

    # JFIF/APP0 varsa önce o gelmeli
    app0 = [b for m, b in bolutler if m == 0xE0]
    for govde in app0:
        bolut_yaz(0xE0, govde)
    if yeni_exif:
        bolut_yaz(0xE1, yeni_exif)
    bolut_yaz(0xE1, yeni_xmp)
    for isaret, govde in bolutler:
        if isaret == 0xE0:
            continue
        bolut_yaz(isaret, govde)
    cikti.extend(kuyruk)
    return bytes(cikti)


# ==========================================================================
# PNG — iTXt yığını
# ==========================================================================

def _png_yigin(tur: bytes, veri: bytes) -> bytes:
    import zlib
    return (struct.pack(">I", len(veri)) + tur + veri
            + struct.pack(">I", zlib.crc32(tur + veri) & 0xFFFFFFFF))


def png_isle(veri: bytes, baslik: str, aciklama: str) -> bytes:
    if not veri.startswith(PNG_IMZA):
        raise ValueError("PNG değil")
    xmp = xmp_uret(baslik, aciklama)
    itxt = (PNG_XMP_ANAHTAR + b"\x00" + b"\x00" + b"\x00" + b"\x00" + b"\x00"
            + xmp)
    yeni_yigin = _png_yigin(b"iTXt", itxt)

    cikti = bytearray(PNG_IMZA)
    i = len(PNG_IMZA)
    eklendi = False
    while i < len(veri):
        uzunluk = struct.unpack(">I", veri[i:i + 4])[0]
        tur = veri[i + 4:i + 8]
        blok = veri[i:i + 12 + uzunluk]
        i += 12 + uzunluk
        if tur == b"iTXt" and PNG_XMP_ANAHTAR in blok[:40]:
            continue                            # eski XMP atılır
        cikti.extend(blok)
        if tur == b"IHDR" and not eklendi:
            cikti.extend(yeni_yigin)
            eklendi = True
    if not eklendi:
        raise ValueError("PNG IHDR bulunamadı")
    return bytes(cikti)


# ==========================================================================
# Görünür filigran (yalnızca kapaklar, opsiyonel)
# ==========================================================================

def filigran_bas(veri: bytes) -> bytes:
    if not PILLOW_VAR:
        raise ValueError("filigran için Pillow gerekli")
    from PIL import ImageDraw, ImageFont
    gorsel = Image.open(io.BytesIO(veri)).convert("RGB")
    g, y = gorsel.size
    metin = OY.SITE_ALAN
    punto = max(11, int(g * 0.016))
    try:
        yazitipi = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", punto)
    except Exception:  # noqa: BLE001
        yazitipi = ImageFont.load_default()
    katman = Image.new("RGBA", gorsel.size, (0, 0, 0, 0))
    ciz = ImageDraw.Draw(katman)
    kutu = ciz.textbbox((0, 0), metin, font=yazitipi)
    mg, my = kutu[2] - kutu[0], kutu[3] - kutu[1]
    px, py = g - mg - int(g * 0.018), y - my - int(y * 0.022)
    ciz.text((px + 1, py + 1), metin, font=yazitipi, fill=(0, 0, 0, 90))
    ciz.text((px, py), metin, font=yazitipi, fill=(255, 255, 255, 190))
    birlesik = Image.alpha_composite(gorsel.convert("RGBA"), katman).convert("RGB")
    tampon = io.BytesIO()
    birlesik.save(tampon, format="JPEG", quality=92, subsampling=0,
                  optimize=True)
    return tampon.getvalue()


# ==========================================================================
# Dosya/klasör yürütmesi
# ==========================================================================

def baslik_uret(ad: str) -> str:
    return f"Bilge ve Yonga — {Path(ad).stem}"


def aciklama_uret(ad: str) -> str:
    return (f"{OY.SERI_ADI} görseli. Görsel, tek bir karakter foyune bagli "
            f"kalinarak yapay zeka araclariyla uretilmis ve eser sahibi "
            f"tarafindan secilerek duzenlenmistir.")


def veri_isle(ad: str, veri: bytes, filigran: bool) -> bytes:
    baslik = baslik_uret(ad)
    aciklama = aciklama_uret(ad)
    dusuk = ad.lower()
    if dusuk.endswith((".jpg", ".jpeg")):
        if filigran and ("kapak" in dusuk or "cover" in dusuk):
            veri = filigran_bas(veri)
        return jpeg_isle(veri, baslik, aciklama)
    if dusuk.endswith(".png"):
        return png_isle(veri, baslik, aciklama)
    raise ValueError("desteklenmeyen biçim")


def dosya_isle(yol: Path, kok: Path, yedek_kok: Path | None,
               filigran: bool, kontrol: bool) -> tuple[str, str]:
    try:
        veri = yol.read_bytes()
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"okunamadı: {hata}"

    if XMP_ONEK in veri[:65536] or PNG_XMP_ANAHTAR in veri[:4096]:
        if b"tdm:reservation" in veri[:200000]:
            return "ATLANDI", "telif üstverisi zaten var"

    if kontrol:
        return "KONTROL", f"{len(veri):,} bayt · XMP + EXIF eklenecek"

    if yedek_kok is not None:
        try:
            goreli = yol.relative_to(kok)
        except ValueError:
            goreli = Path(yol.name)
        hedef = yedek_kok / goreli
        hedef.parent.mkdir(parents=True, exist_ok=True)
        if not hedef.exists():
            shutil.copy2(yol, hedef)

    try:
        yeni = veri_isle(yol.name, veri, filigran)
        gecici = yol.with_suffix(yol.suffix + ".yeni")
        gecici.write_bytes(yeni)
        gecici.replace(yol)
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"işlenemedi: {hata}"

    fark = len(yeni) - len(veri)
    return "TAMAM", f"{len(veri):,} → {len(yeni):,} bayt ({fark:+,})"


def epub_ici_isle(epub: Path, kok: Path, yedek_kok: Path | None,
                  filigran: bool, kontrol: bool) -> tuple[str, str]:
    try:
        with zipfile.ZipFile(epub, "r") as z:
            girisler = [(b, z.read(b.filename)) for b in z.infolist()]
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"okunamadı: {hata}"

    hedefler = [b.filename for b, _ in girisler
                if b.filename.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not hedefler:
        return "ATLANDI", "içinde görsel yok"

    if kontrol:
        return "KONTROL", f"{len(hedefler)} görsel işlenecek"

    if yedek_kok is not None:
        try:
            goreli = epub.relative_to(kok)
        except ValueError:
            goreli = Path(epub.name)
        hedef = yedek_kok / goreli
        hedef.parent.mkdir(parents=True, exist_ok=True)
        if not hedef.exists():
            shutil.copy2(epub, hedef)

    sayac = 0
    try:
        gecici = epub.with_suffix(".epub.yeni")
        with zipfile.ZipFile(gecici, "w") as y:
            y.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                       compress_type=zipfile.ZIP_STORED)
            for bilgi, veri in girisler:
                if bilgi.filename == "mimetype":
                    continue
                if bilgi.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    if b"tdm:reservation" not in veri[:200000]:
                        try:
                            veri = veri_isle(bilgi.filename, veri, filigran)
                            sayac += 1
                        except Exception:  # noqa: BLE001
                            pass
                yb = zipfile.ZipInfo(bilgi.filename, date_time=bilgi.date_time)
                yb.external_attr = bilgi.external_attr
                yb.compress_type = (zipfile.ZIP_STORED
                                    if bilgi.compress_type == zipfile.ZIP_STORED
                                    else zipfile.ZIP_DEFLATED)
                y.writestr(yb, veri)
        gecici.replace(epub)
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"yazılamadı: {hata}"
    return "TAMAM", f"{sayac} görsele üstveri gömüldü"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Bilge ve Yonga görsel telif üstverisi gömme betiği")
    ap.add_argument("klasor", nargs="?", default=".")
    ap.add_argument("--yedek", default=None,
                    help="Yedek klasörü (varsayılan: <klasor>/_yedek-gorsel)")
    ap.add_argument("--yedek-yok", action="store_true")
    ap.add_argument("--kontrol", action="store_true")
    ap.add_argument("--epub-ici", action="store_true",
                    help="EPUB dosyalarının içindeki görselleri de işle")
    ap.add_argument("--filigran-kapak", action="store_true",
                    help="Kapak görsellerine görünür filigran bas "
                         "(bu görselleri yeniden kodlar)")
    a = ap.parse_args()

    kok = Path(a.klasor).resolve()
    if not kok.is_dir():
        print(f"HATA: klasör bulunamadı: {kok}", file=sys.stderr)
        return 2

    if a.filigran_kapak and not PILLOW_VAR:
        print("HATA: --filigran-kapak için Pillow gerekli: pip install Pillow",
              file=sys.stderr)
        return 2

    yedek_kok: Path | None = None
    if not a.yedek_yok and not a.kontrol:
        yedek_kok = Path(a.yedek).resolve() if a.yedek else kok / "_yedek-gorsel"
        yedek_kok.mkdir(parents=True, exist_ok=True)

    atlanacak = {"_yedek-pdf", "_yedek-pdf-kunye", "_yedek-epub",
                 "_yedek-gorsel", "_yedek", ".git", "node_modules"}

    gorseller = sorted(
        p for p in kok.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
        and not set(p.relative_to(kok).parts) & atlanacak
    )
    epubler = sorted(
        p for p in kok.rglob("*.epub")
        if p.is_file() and not set(p.relative_to(kok).parts) & atlanacak
    ) if a.epub_ici else []

    print("=" * 78)
    print("Bilge ve Yonga — görsel telif üstverisi")
    print(f"Klasör : {kok}")
    print(f"Yedek  : {yedek_kok if yedek_kok else '(yok)'}")
    print(f"Kip    : {'KONTROL' if a.kontrol else 'UYGULA'}")
    print(f"Pillow : {'var (EXIF yazılacak)' if PILLOW_VAR else 'YOK (yalnızca XMP)'}")
    print(f"Dosya  : {len(gorseller)} görsel"
          + (f" + {len(epubler)} EPUB" if a.epub_ici else ""))
    print("=" * 78)

    tamam = atlandi = hatali = 0
    toplam = len(gorseller) + len(epubler)
    sira = 0
    for yol in gorseller:
        sira += 1
        durum, aciklama = dosya_isle(yol, kok, yedek_kok, a.filigran_kapak,
                                     a.kontrol)
        if durum == "HATA":
            hatali += 1
        elif durum == "ATLANDI":
            atlandi += 1
        else:
            tamam += 1
        print(f"[{sira:>4}/{toplam}] {durum:<8} {yol.relative_to(kok)}  — {aciklama}")

    for yol in epubler:
        sira += 1
        durum, aciklama = epub_ici_isle(yol, kok, yedek_kok, a.filigran_kapak,
                                        a.kontrol)
        if durum == "HATA":
            hatali += 1
        elif durum == "ATLANDI":
            atlandi += 1
        else:
            tamam += 1
        print(f"[{sira:>4}/{toplam}] {durum:<8} {yol.relative_to(kok)}  — {aciklama}")

    print("=" * 78)
    print(f"Başarılı: {tamam}   Atlanan: {atlandi}   Hatalı: {hatali}")
    print("=" * 78)
    print("Doğrulama (exiftool kuruluysa):")
    print('  exiftool -XMP-dc:Rights -XMP-cc:license -XMP-xmpRights:Marked '
          '-EXIF:Copyright "<gorsel.jpg>"')
    return 1 if hatali else 0


if __name__ == "__main__":
    raise SystemExit(main())
