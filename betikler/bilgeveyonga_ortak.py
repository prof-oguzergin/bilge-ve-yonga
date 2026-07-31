# -*- coding: utf-8 -*-
"""
bilgeveyonga_ortak.py — Bilge ve Yonga üstveri betikleri için ortak sabitler.

Bu dosya tek başına çalıştırılmaz. Diğer betikler buradan içe aktarır.
Telif, lisans ve künye metinlerinin TEK KAYNAĞI burasıdır; bir metin
değişecekse yalnızca bu dosya düzenlenir.

Yazar: Bilge ve Yonga hukuki uygulama paketi
Sürüm: 1.0 (2026-07-26)
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# 1. KİMLİK
# --------------------------------------------------------------------------

ESER_SAHIBI = "Prof. Dr. Oğuz Ergin"
ESER_SAHIBI_SIRALI = "Ergin, Oğuz"          # katalog biçimi (dc:creator)
TELIF_YILI = "2026"
YAYIN_YERI = "Ankara"
SERI_ADI = "Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi"
YAYINCI = "Bilge ve Yonga — Bilgisayar Mimarisi Çocuk Kitapları"

SITE = "https://bilgeveyonga.oguzergin.net"
SITE_ALAN = "bilgeveyonga.oguzergin.net"

ILETISIM_GENEL = "bilgi@oguzergin.net"

# YAYIM ÖNCESİ KARAR: Telif politikası (belge 02) ticari izin başvuruları için
# ayrı bir kutu öngörür: lisans@oguzergin.net. Kutu açılana kadar genel adres
# kullanılır — yayımlanan hiçbir metin çalışmayan bir adresi göstermemelidir.
# Kutu açıldığında yalnızca aşağıdaki satır değiştirilir ve üstveri betikleri
# yeniden çalıştırılır.
ILETISIM_LISANS = "bilgi@oguzergin.net"      # kutu açılınca: "lisans@oguzergin.net"

# --------------------------------------------------------------------------
# 2. LİSANS VE POLİTİKA ADRESLERİ
# --------------------------------------------------------------------------

LISANS_KISA = "CC BY-NC-ND 4.0"
LISANS_UZUN = (
    "Creative Commons Atıf-GayriTicari-Türetilemez 4.0 Uluslararası "
    "(CC BY-NC-ND 4.0)"
)
LISANS_URI = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
LISANS_URI_TR = "https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr"
LISANS_METNI_TR = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.tr"

SAYFA_TELIF = f"{SITE}/telif-ve-lisans.html"
SAYFA_KULLANIM = f"{SITE}/kullanim-kosullari.html"
SAYFA_YZ = f"{SITE}/yapay-zeka-bildirimi.html"
SAYFA_TICARI = f"{SITE}/ticari-kullanim.html"
TDM_POLITIKA = f"{SITE}/tdm-policy.json"
TDM_REP = f"{SITE}/.well-known/tdmrep.json"

# --------------------------------------------------------------------------
# 3. TELİF VE KÜNYE METİNLERİ
# 02-telif-lisans-ve-ticari-kullanim-politikasi.md, bölüm 2.3-2.5 ile birebir.
# --------------------------------------------------------------------------

TELIF_TEK_SATIR = (
    f"Bilge ve Yonga © {TELIF_YILI} {ESER_SAHIBI} · {LISANS_KISA}"
)

TELIF_KISA = (
    f"© {TELIF_YILI} {ESER_SAHIBI} · Bilge ve Yonga · {LISANS_KISA}\n"
    f"Lisansın kapsamadığı tüm haklar saklıdır · {SITE_ALAN}/telif-ve-lisans.html"
)

TELIF_BILDIRIMI = (
    f"© {TELIF_YILI} {ESER_SAHIBI}. Tüm eserler {LISANS_KISA} lisansı ile açık "
    f"erişime sunulmuştur. Lisansın kapsamadığı tüm haklar saklıdır."
)

# XMP dc:rights ve EPUB dc:rights için tek paragraflık biçim
HAKLAR_PARAGRAF = (
    f"© {TELIF_YILI} {ESER_SAHIBI}. Bu eser {LISANS_UZUN} lisansı ile açık "
    f"erişime sunulmuştur ({LISANS_URI_TR}). Lisansın kapsamadığı tüm haklar "
    f"saklıdır: \"Bilge ve Yonga\" seri adı, \"Bilge\" ve \"Yonga\" karakter "
    f"adları ile figürleri, marka hakları, eser sahibinin adı ve unvanı ve "
    f"manevi haklar lisans kapsamı dışındadır. Metin ve veri madenciliği ile "
    f"yapay zekâ modeli eğitimi bakımından haklar açıkça saklı tutulmuştur. "
    f"Ticari kullanım izni: {ILETISIM_LISANS}"
)

HAKLAR_PARAGRAF_EN = (
    f"© {TELIF_YILI} Prof. Dr. Oguz Ergin. Licensed under Creative Commons "
    f"Attribution-NonCommercial-NoDerivatives 4.0 International "
    f"(CC BY-NC-ND 4.0), {LISANS_URI}. All rights not granted by the licence "
    f"are reserved, including trademark rights in the series name "
    f"\"Bilge ve Yonga\" and the character names and figures \"Bilge\" and "
    f"\"Yonga\", moral rights, and rights of reproduction and extraction for "
    f"text and data mining and AI model training, which are expressly "
    f"reserved. Commercial licensing: {ILETISIM_LISANS}"
)

# xmpRights:UsageTerms — kısa, çift dilli
KULLANIM_KOSULLARI_KISA = (
    f"Ad belirterek, değiştirmeden ve ticari olmayan amaçla paylaşabilirsiniz "
    f"({LISANS_KISA}). Ticari kullanım, uyarlama, çeviri, karakterlerin ticari "
    f"sunumu ve yapay zekâ eğitimi ayrı yazılı izne bağlıdır: {ILETISIM_LISANS} "
    f"— Share with attribution, unmodified, for non-commercial purposes only. "
    f"Commercial use, adaptation, translation, merchandising and AI training "
    f"require separate written permission."
)

# PDF ve EPUB künye (colophon) sayfası — 02 numaralı belgenin 2.3 bölümü
KUNYE_SATIRLARI = [
    ("baslik", "Künye"),
    ("telif", f"© {TELIF_YILI} {ESER_SAHIBI}"),
    ("seri", SERI_ADI),
    ("yer", f"{YAYIN_YERI}, {TELIF_YILI}"),
    ("bosluk", ""),
    ("govde", f"Bu eser, {LISANS_UZUN} lisansı ile açık erişime sunulmuştur."),
    ("baglanti", f"Lisans metni: {LISANS_URI_TR}"),
    ("bosluk", ""),
    ("vurgu", "LİSANSIN KAPSAMADIĞI TÜM HAKLAR SAKLIDIR."),
    ("govde",
     "“Bilge ve Yonga” seri adı, “Bilge” ve “Yonga” karakter adları ile "
     "figürleri, seri amblemi, marka hakları, eser sahibinin adı ve unvanı ile "
     "manevi haklar bu lisansın kapsamı dışındadır ve ayrı yazılı izne bağlıdır."),
    ("bosluk", ""),
    ("govde",
     "Metin ve veri madenciliği ile yapay zekâ modeli eğitimi bakımından "
     "haklar açıkça saklı tutulmuştur."),
    ("bosluk", ""),
    ("govde",
     "Eserler olduğu gibi sunulmaktadır; belirli bir amaca uygunluk konusunda "
     "garanti verilmez."),
    ("bosluk", ""),
    ("govde", f"Ticari kullanım izni ve sorularınız için: {ILETISIM_LISANS}"),
    ("govde", f"Telif ve lisans politikası: {SITE_ALAN}/telif-ve-lisans.html"),
]

ATIF_METNI = (
    f"Ergin, O. ({TELIF_YILI}). {SERI_ADI}. {SITE}"
)

ANAHTAR_KELIMELER = (
    "bilgisayar mimarisi, çocuk kitabı, Bilge ve Yonga, açık erişim, "
    "CC BY-NC-ND 4.0, Oğuz Ergin, STEM, bilgisayar bilimi, 7-12 yaş"
)

VARSAYILAN_KONU = (
    f"{SERI_ADI} — bilgisayar mimarisini 7-12 yaş grubuna anlatan açık erişimli "
    f"çocuk kitabı."
)

# --------------------------------------------------------------------------
# 4. AD ALANLARI (XML / XMP)
# --------------------------------------------------------------------------

NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "xmp": "http://ns.adobe.com/xap/1.0/",
    "xmpRights": "http://ns.adobe.com/xap/1.0/rights/",
    "xmpMM": "http://ns.adobe.com/xap/1.0/mm/",
    "pdf": "http://ns.adobe.com/pdf/1.3/",
    "photoshop": "http://ns.adobe.com/photoshop/1.0/",
    "Iptc4xmpCore": "http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/",
    "plus": "http://ns.useplus.org/ldf/xmp/1.0/",
    "cc": "http://creativecommons.org/ns#",
    "tdm": "http://www.w3.org/ns/tdmrep#",
}

TDM_REZERVASYON = "1"


def xml_kacir(s: str) -> str:
    """XML metin düğümü için kaçırma."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def xml_kacir_oznitelik(s: str) -> str:
    return xml_kacir(s).replace('"', "&quot;")
