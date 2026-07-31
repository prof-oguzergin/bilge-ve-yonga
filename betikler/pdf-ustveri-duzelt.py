# -*- coding: utf-8 -*-
"""
pdf-ustveri-duzelt.py — Bilge ve Yonga PDF dosyalarının üstverisini düzeltir.

NE YAPAR
    Verilen klasörü (varsayılan: bulunduğu deponun kökü) tarar, bulduğu her PDF
    için:
      1. Orijinali yedekler,
      2. Belge bilgisi (DocInfo) alanlarını doldurur:
         /Title /Author /Subject /Keywords /Creator /Producer /ModDate,
      3. Telif ve lisans bilgisini taşıyan tam bir XMP paketi gömer:
         dc:rights, dc:creator, dc:title, dc:publisher, dc:language,
         xmpRights:Marked, xmpRights:WebStatement, xmpRights:UsageTerms,
         xmpRights:Owner, cc:license, cc:attributionName, cc:attributionURL,
         cc:morePermissions, tdm:reservation, tdm:policy,
      4. İşlem raporu basar.

    Mevcut durumda /Creator alanı "anonymous", /Subject alanı "unspecified" ve
    XMP paketi yoktur. Bu betik ikisini de düzeltir.

KULLANIM (Windows PowerShell)
    # Önce ne yapılacağını göster, dosyaya dokunma:
    python pdf-ustveri-duzelt.py "C:\\repo\\bilgeveyonga" --kontrol

    # Uygula:
    python pdf-ustveri-duzelt.py "C:\\repo\\bilgeveyonga"

    # Yedekleri başka bir yere koy:
    python pdf-ustveri-duzelt.py "C:\\repo\\bilgeveyonga" --yedek "D:\\yedek\\pdf"

    # Kitap açıklamalarını dosyadan oku:
    python pdf-ustveri-duzelt.py "C:\\repo\\bilgeveyonga" --kitap-bilgi kitaplar.json

GEREKSİNİM
    pypdf >= 5.0        (pip install "pypdf>=5.0")
    Not: XMP paketi pypdf'in PdfWriter.xmp_metadata özelliğiyle yazılır;
    pikepdf gerekmez. pikepdf kuruluysa da kullanılmaz.

--kitap-bilgi JSON BİÇİMİ
    Anahtar: PDF dosya adı (uzantısız) veya bulunduğu klasör adı.
    {
      "Kumdan Bilgisayar":   {"konu": "Bir avuç kumdan yongaya uzanan üretim yolculuğu",
                              "seri": "1. Seri — Kumdan Bilgisayara",
                              "kitap_no": "1.1a"},
      "kitap1.01a-kumdan-bilgisayar": {"konu": "..."}
    }
    Alanların hepsi isteğe bağlıdır; eksik alan varsayılanla doldurulur.

ÇIKIŞ KODU
    0  hepsi başarılı
    1  en az bir dosyada hata
    2  kullanım hatası (klasör yok, pypdf kurulu değil, vb.)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bilgeveyonga_ortak as OY  # noqa: E402

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:  # pragma: no cover
    print("HATA: pypdf kurulu değil.  Kurulum:  pip install \"pypdf>=5.0\"",
          file=sys.stderr)
    raise SystemExit(2)


# ==========================================================================
# XMP paketi
# ==========================================================================

XMP_SABLON = """<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Bilge ve Yonga ustveri betigi 1.0">
 <rdf:RDF xmlns:rdf="{rdf}">
  <rdf:Description rdf:about=""
    xmlns:dc="{dc}"
    xmlns:dcterms="{dcterms}"
    xmlns:xmp="{xmp}"
    xmlns:xmpRights="{xmpRights}"
    xmlns:pdf="{pdf}"
    xmlns:photoshop="{photoshop}"
    xmlns:cc="{cc}"
    xmlns:tdm="{tdm}">

   <dc:title>
    <rdf:Alt><rdf:li xml:lang="x-default">{baslik}</rdf:li></rdf:Alt>
   </dc:title>
   <dc:creator>
    <rdf:Seq><rdf:li>{yazar}</rdf:li></rdf:Seq>
   </dc:creator>
   <dc:description>
    <rdf:Alt><rdf:li xml:lang="tr">{konu}</rdf:li></rdf:Alt>
   </dc:description>
   <dc:publisher>
    <rdf:Bag><rdf:li>{yayinci}</rdf:li></rdf:Bag>
   </dc:publisher>
   <dc:language>
    <rdf:Bag><rdf:li>tr</rdf:li></rdf:Bag>
   </dc:language>
   <dc:subject>
    <rdf:Bag>{anahtarlar}</rdf:Bag>
   </dc:subject>
   <dc:date>
    <rdf:Seq><rdf:li>{tarih}</rdf:li></rdf:Seq>
   </dc:date>
   <dc:rights>
    <rdf:Alt>
     <rdf:li xml:lang="tr">{haklar_tr}</rdf:li>
     <rdf:li xml:lang="x-default">{haklar_en}</rdf:li>
    </rdf:Alt>
   </dc:rights>
   <dc:type>
    <rdf:Bag><rdf:li>Text</rdf:li></rdf:Bag>
   </dc:type>

   <dcterms:rightsHolder>{yazar}</dcterms:rightsHolder>
   <dcterms:license rdf:resource="{lisans_uri}"/>
   <dcterms:bibliographicCitation>{atif}</dcterms:bibliographicCitation>

   <xmp:CreatorTool>{uretici}</xmp:CreatorTool>
   <xmp:CreateDate>{olusturma}</xmp:CreateDate>
   <xmp:ModifyDate>{degistirme}</xmp:ModifyDate>
   <xmp:MetadataDate>{degistirme}</xmp:MetadataDate>

   <xmpRights:Marked>True</xmpRights:Marked>
   <xmpRights:WebStatement>{web_beyani}</xmpRights:WebStatement>
   <xmpRights:Owner>
    <rdf:Bag><rdf:li>{yazar}</rdf:li></rdf:Bag>
   </xmpRights:Owner>
   <xmpRights:UsageTerms>
    <rdf:Alt><rdf:li xml:lang="x-default">{kullanim}</rdf:li></rdf:Alt>
   </xmpRights:UsageTerms>

   <photoshop:Credit>{yazar}</photoshop:Credit>
   <photoshop:Source>{site}</photoshop:Source>

   <cc:license rdf:resource="{lisans_uri}"/>
   <cc:attributionName>{yazar}</cc:attributionName>
   <cc:attributionURL rdf:resource="{site}/"/>
   <cc:morePermissions rdf:resource="{ticari}"/>
   <cc:useGuidelines rdf:resource="{telif_sayfa}"/>

   <tdm:reservation>{tdm_rez}</tdm:reservation>
   <tdm:policy>{tdm_pol}</tdm:policy>

   <pdf:Keywords>{anahtar_duz}</pdf:Keywords>
   <pdf:Producer>{producer}</pdf:Producer>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""


def xmp_uret(baslik: str, konu: str, olusturma_iso: str,
             degistirme_iso: str, producer: str) -> bytes:
    k = OY.xml_kacir
    anahtarlar = "".join(
        f"<rdf:li>{k(a.strip())}</rdf:li>"
        for a in OY.ANAHTAR_KELIMELER.split(",") if a.strip()
    )
    paket = XMP_SABLON.format(
        rdf=OY.NS["rdf"], dc=OY.NS["dc"], dcterms=OY.NS["dcterms"],
        xmp=OY.NS["xmp"], xmpRights=OY.NS["xmpRights"], pdf=OY.NS["pdf"],
        photoshop=OY.NS["photoshop"], cc=OY.NS["cc"], tdm=OY.NS["tdm"],
        baslik=k(baslik),
        yazar=k(OY.ESER_SAHIBI),
        konu=k(konu),
        yayinci=k(OY.YAYINCI),
        anahtarlar=anahtarlar,
        anahtar_duz=k(OY.ANAHTAR_KELIMELER),
        tarih=olusturma_iso,
        haklar_tr=k(OY.HAKLAR_PARAGRAF),
        haklar_en=k(OY.HAKLAR_PARAGRAF_EN),
        lisans_uri=OY.LISANS_URI,
        atif=k(OY.ATIF_METNI),
        uretici=k(OY.ESER_SAHIBI),
        olusturma=olusturma_iso,
        degistirme=degistirme_iso,
        web_beyani=OY.SAYFA_TELIF,
        kullanim=k(OY.KULLANIM_KOSULLARI_KISA),
        site=OY.SITE,
        ticari=OY.SAYFA_TICARI,
        telif_sayfa=OY.SAYFA_TELIF,
        tdm_rez=OY.TDM_REZERVASYON,
        tdm_pol=OY.TDM_POLITIKA,
        producer=k(producer),
    )
    return paket.encode("utf-8")


# ==========================================================================
# Yardımcılar
# ==========================================================================

def pdf_tarihi_iso(deger: str | None) -> str:
    """PDF 'D:YYYYMMDDHHmmSS+ZZ'zz'' biçimini ISO 8601'e çevirir."""
    simdi = _dt.datetime.now().astimezone().replace(microsecond=0).isoformat()
    if not deger:
        return simdi
    s = str(deger).strip()
    if s.startswith("D:"):
        s = s[2:]
    try:
        tarih = _dt.datetime.strptime(s[:14], "%Y%m%d%H%M%S")
    except ValueError:
        return simdi
    kuyruk = s[14:].replace("'", "")
    if kuyruk[:1] in ("+", "-") and len(kuyruk) >= 5:
        ofset = f"{kuyruk[0]}{kuyruk[1:3]}:{kuyruk[3:5]}"
    elif kuyruk[:1] == "Z":
        ofset = "+00:00"
    else:
        ofset = ""
    return tarih.isoformat() + ofset


def pdf_tarihi_simdi() -> str:
    yerel = _dt.datetime.now().astimezone()
    ofs = yerel.strftime("%z")  # +0300
    return "D:" + yerel.strftime("%Y%m%d%H%M%S") + f"{ofs[:3]}'{ofs[3:]}'"


def baslik_bul(pdf: Path, mevcut: str | None) -> str:
    """Kitap adını mevcut /Title alanından, olmazsa dosya adından türetir."""
    if mevcut:
        temiz = str(mevcut).strip()
        if temiz and temiz.lower() not in ("untitled", "unspecified", "anonymous"):
            return temiz
    ad = pdf.stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(p for p in ad.split() if p)


def bilgi_getir(bilgi: dict, pdf: Path) -> dict:
    """--kitap-bilgi sözlüğünden bu PDF'e ait kaydı bulur."""
    for anahtar in (pdf.stem, pdf.parent.name, pdf.name):
        if anahtar in bilgi:
            return bilgi[anahtar] or {}
    return {}


# ==========================================================================
# Ana işlem
# ==========================================================================

def pdf_isle(pdf: Path, kok: Path, yedek_kok: Path | None,
             bilgi: dict, kontrol: bool) -> tuple[str, str]:
    """Tek PDF'i işler. (durum, aciklama) döndürür."""
    try:
        okuyucu = PdfReader(str(pdf))
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"okunamadı: {hata}"

    eski = okuyucu.metadata or {}
    kayit = bilgi_getir(bilgi, pdf)

    baslik = kayit.get("baslik") or baslik_bul(pdf, eski.get("/Title"))
    konu = kayit.get("konu") or OY.VARSAYILAN_KONU
    kitap_no = kayit.get("kitap_no")
    seri = kayit.get("seri")

    tam_baslik = baslik
    if kitap_no:
        tam_baslik = f"{baslik} (Bilge ve Yonga · Kitap {kitap_no})"

    if seri:
        tam_konu = f"{konu} — {seri}, {OY.SERI_ADI}"
    elif kayit.get("konu"):
        tam_konu = f"{konu} — {OY.SERI_ADI}"
    else:
        tam_konu = konu

    olusturma = pdf_tarihi_iso(eski.get("/CreationDate"))
    simdi_pdf = pdf_tarihi_simdi()
    simdi_iso = _dt.datetime.now().astimezone().replace(microsecond=0).isoformat()
    producer = str(eski.get("/Producer") or "ReportLab PDF Library - (opensource)")

    if kontrol:
        return "KONTROL", f"{tam_baslik} | XMP eklenecek, /Creator ve /Subject düzeltilecek"

    # --- yedek -------------------------------------------------------------
    if yedek_kok is not None:
        try:
            goreli = pdf.relative_to(kok)
        except ValueError:
            goreli = Path(pdf.name)
        hedef = yedek_kok / goreli
        hedef.parent.mkdir(parents=True, exist_ok=True)
        if not hedef.exists():          # var olan yedeğin üstüne yazma
            shutil.copy2(pdf, hedef)

    # --- yaz ---------------------------------------------------------------
    try:
        yazici = PdfWriter(clone_from=str(pdf))
        yazici.add_metadata({
            "/Title": tam_baslik,
            "/Author": OY.ESER_SAHIBI,
            "/Subject": tam_konu,
            "/Keywords": OY.ANAHTAR_KELIMELER,
            "/Creator": OY.ESER_SAHIBI,
            "/Producer": producer,
            "/CreationDate": str(eski.get("/CreationDate") or simdi_pdf),
            "/ModDate": simdi_pdf,
            # Standart olmayan ama okunabilir ek alanlar:
            "/Copyright": OY.TELIF_BILDIRIMI,
            "/License": OY.LISANS_URI,
            "/Publisher": OY.YAYINCI,
            "/Contact": OY.ILETISIM_LISANS,
        })
        yazici.xmp_metadata = xmp_uret(
            baslik=tam_baslik, konu=tam_konu,
            olusturma_iso=olusturma, degistirme_iso=simdi_iso,
            producer=producer,
        )
        gecici = pdf.with_suffix(".pdf.yeni")
        with open(gecici, "wb") as f:
            yazici.write(f)
        gecici.replace(pdf)
    except Exception as hata:  # noqa: BLE001
        return "HATA", f"yazılamadı: {hata}"

    return "TAMAM", tam_baslik


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Bilge ve Yonga PDF üstverisi düzeltme betiği",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("klasor", nargs="?", default=".",
                    help="Taranacak kök klasör (varsayılan: bulunulan klasör)")
    ap.add_argument("--yedek", default=None,
                    help="Yedek klasörü (varsayılan: <klasor>/_yedek-pdf)")
    ap.add_argument("--yedek-yok", action="store_true",
                    help="Yedek alma (ÖNERİLMEZ)")
    ap.add_argument("--kontrol", action="store_true",
                    help="Hiçbir dosyaya dokunma, ne yapılacağını yaz")
    ap.add_argument("--kitap-bilgi", default=None,
                    help="Kitap açıklamalarını içeren JSON dosyası")
    ap.add_argument("--desen", default="*.pdf",
                    help="Dosya deseni (varsayılan: *.pdf)")
    a = ap.parse_args()

    kok = Path(a.klasor).resolve()
    if not kok.is_dir():
        print(f"HATA: klasör bulunamadı: {kok}", file=sys.stderr)
        return 2

    yedek_kok: Path | None = None
    if not a.yedek_yok and not a.kontrol:
        yedek_kok = Path(a.yedek).resolve() if a.yedek else (kok / "_yedek-pdf")
        yedek_kok.mkdir(parents=True, exist_ok=True)

    bilgi: dict = {}
    if a.kitap_bilgi:
        yol = Path(a.kitap_bilgi)
        if not yol.is_file():
            print(f"HATA: --kitap-bilgi dosyası yok: {yol}", file=sys.stderr)
            return 2
        bilgi = json.loads(yol.read_text(encoding="utf-8"))

    atlanacak = {"_yedek-pdf", "_yedek-epub", "_yedek", ".git", "node_modules"}
    if yedek_kok is not None:
        atlanacak.add(yedek_kok.name)

    pdfler = sorted(
        p for p in kok.rglob(a.desen)
        if p.is_file() and not set(p.relative_to(kok).parts) & atlanacak
    )

    if not pdfler:
        print(f"Uyarı: {kok} altında PDF bulunamadı.")
        return 0

    print("=" * 78)
    print("Bilge ve Yonga — PDF üstveri düzeltme")
    print(f"Klasör : {kok}")
    print(f"Yedek  : {yedek_kok if yedek_kok else '(yok)'}")
    print(f"Kip    : {'KONTROL (dosyaya dokunulmaz)' if a.kontrol else 'UYGULA'}")
    print(f"Dosya  : {len(pdfler)} PDF")
    print("=" * 78)

    tamam = hatali = 0
    for i, pdf in enumerate(pdfler, 1):
        durum, aciklama = pdf_isle(pdf, kok, yedek_kok, bilgi, a.kontrol)
        if durum == "HATA":
            hatali += 1
        else:
            tamam += 1
        goreli = pdf.relative_to(kok)
        print(f"[{i:>2}/{len(pdfler)}] {durum:<7} {goreli}")
        print(f"          {aciklama}")

    print("=" * 78)
    print(f"Başarılı: {tamam}   Hatalı: {hatali}")
    if not a.kontrol and yedek_kok is not None:
        print(f"Orijinaller: {yedek_kok}")
    print("=" * 78)
    print("Doğrulama:")
    print('  python -c "from pypdf import PdfReader; r=PdfReader(r\'<PDF>\');'
          ' print(dict(r.metadata)); print(r.xmp_metadata.dc_rights)"')
    return 1 if hatali else 0


if __name__ == "__main__":
    raise SystemExit(main())
