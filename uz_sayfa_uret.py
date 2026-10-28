# -*- coding: utf-8 -*-
"""Özbekçe sayfa (uz.html) ve Özbekçe PDF'lerin siteye kopyası.

Kaynak Drive'daki ceviriler/ozbekce klasörüdür: her kitabın md'sinden başlık ve
konu satırı okunur, PDF'i uz/ altına ASCII adla kopyalanır, sayfa yeniden yazılır.
build_web.py'den bağımsızdır; Özbekçe kitap eklenince yalnız bu betik çalıştırılır.
"""
import html
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent
KAYNAK = Path(r"G:\My Drive\Yazdığımız Kitaplar\Çocuk Kitapları\Bilgisayar Mimarisi Serisi\ceviriler\ozbekce")
HEDEF = REPO / "uz"
JILDLAR = {"1": "1-jild: Qumdan kompyutergacha"}


def kisalt(s, n=95):
    """Kart için konu satırının ilk bölümü: ilk noktalı virgül ya da noktada keser."""
    s = re.split(r"[;.?]\s", s + " ")[0].strip().rstrip(".;")
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def kitaplar():
    for k in sorted(KAYNAK.glob("kitap*")):
        if not k.is_dir():
            continue
        md = k / (k.name + ".md")
        pdf = next(iter(sorted(k.glob("*(qoralama).pdf"))), None)
        if not md.exists() or pdf is None:
            print("  [atlandı]", k.name)
            continue
        t = md.read_text(encoding="utf-8")
        ad = re.search(r"^# (.+)$", t, re.M).group(1).strip()
        konu = re.search(r"^\*\*Asosiy mavzu:\*\*\s*(.+)$", t, re.M)
        kod = k.name.split("-")[0]
        no = kod.replace("kitap", "")
        no = re.sub(r"^(\d)\.0?(\d+)", lambda m: m.group(1) + "." + m.group(2), no)
        kapak = k / "resimler" / "GPT_Kapak.png"
        yield {"kapak_yerel": kapak if kapak.exists() else None, "kod": kod, "no": no, "ad": ad, "konu": kisalt(konu.group(1).strip()) if konu else "",
               "pdf": pdf, "dosya": k.name + ".pdf", "jild": kod[5]}


def kart(b):
    return f'''    <li class="uzk">
      <img src="{b["kart"]}" width="480" height="270" alt="" loading="lazy">
      <div class="uzk-ic">
        <span class="uzk-no">{html.escape(b["no"])}</span>
        <h3>{html.escape(b["ad"])}</h3>
        <p>{html.escape(b["konu"])}</p>
        <a class="uzk-btn" href="uz/{b["dosya"]}" download>PDF yuklab olish</a>
      </div>
    </li>'''


SABLON = """<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bilge va Yonga: oʻzbekcha kitoblar</title>
<meta name="description" content="Kompyuter qanday ishlashini 7 yosh va undan katta bolalarga tushuntiradigan rasmli kitoblar. Bepul va ochiq.">
<link rel="canonical" href="https://bilgeveyonga.oguzergin.net/uz.html">
<link rel="alternate" hreflang="tr" href="https://bilgeveyonga.oguzergin.net/">
<link rel="alternate" hreflang="uz" href="https://bilgeveyonga.oguzergin.net/uz.html">
<link rel="icon" href="amblem.ico?v=1" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="amblem-32.png?v=1">
<link rel="apple-touch-icon" href="amblem-180.png?v=1">
<meta name="theme-color" content="#0D1530">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bilge va Yonga">
<meta property="og:url" content="https://bilgeveyonga.oguzergin.net/uz.html">
<meta property="og:title" content="Bilge va Yonga: oʻzbekcha kitoblar">
<meta property="og:description" content="Kompyuter qanday ishlashini bolalarga tushuntiradigan rasmli kitoblar. Bepul va ochiq.">
<meta property="og:image" content="https://bilgeveyonga.oguzergin.net/og-image.png">
<meta property="og:locale" content="uz_UZ">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="Prof. Dr. Oğuz Ergin">
<link rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/">
<meta name="robots" content="index, follow, noai, noimageai">
<script>try{var _t=localStorage.getItem('theme');if(_t)document.documentElement.setAttribute('data-theme',_t);}catch(e){}</script>
<link rel="stylesheet" href="belge.css">
<style>
.uzl{list-style:none;padding:0;margin:18px 0 40px;display:grid;gap:18px;
  grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.uzk{background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;
  display:flex;flex-direction:column}
.uzk img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.uzk-ic{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.uzk-no{font-weight:800;color:var(--glow);font-size:.85rem}
.uzk h3{margin:0;font-family:var(--font-display);font-size:1.12rem;line-height:1.3}
.uzk p{margin:0;color:var(--muted);font-size:.92rem;line-height:1.5;flex:1}
.uzk-btn{margin-top:8px;align-self:stretch;text-align:center;text-decoration:none;font-weight:800;
  border-radius:999px;padding:.55em 1em;background:var(--glow);color:#0D1530}
.uzk-btn:hover{filter:brightness(1.08)}
.uzbag{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 6px}
.uzbag a{text-decoration:none;font-weight:700;border:1.5px solid var(--line);border-radius:999px;
  padding:.5em 1em;color:var(--text)}
.uzbag a:hover{border-color:var(--glow);color:var(--glow)}
</style>
</head>
<body>

<header class="ust">
  <a class="marka" href="uz.html">
    <img src="bilge.png?v=10" width="30" height="30" alt="">
    Bilge <span>va</span> Yonga
    <img src="yonga.png?v=10" width="30" height="30" alt="">
  </a>
  <button class="tema" id="tt" type="button" aria-label="Yorugʻ mavzuga oʻtish"><span id="tt-ad">Yorugʻ</span></button>
  <a class="geri" href="index.html" lang="tr">Türkçe ›</a>
</header>

<main class="sayfa">
  <div class="baslik">
    <p class="etiket">OʻZBEKCHA</p>
    <h1>Bilge va Yonga</h1>
    <p class="ozet">Kompyuter qanday ishlashini 7 yosh va undan katta bolalarga tushuntiradigan rasmli kitoblar.</p>
  </div>

  <p>Sakkiz yoshli qiziquvchan qiz Bilge va kichkina robot Yonga bolalarni kompyuterning ichiga sayohatga olib boradi: chip qumdan qanday yasaladi, milliardlab mitti kalitlar qanday hisoblaydi, xotira maʼlumotni qanday saqlaydi. Turkum toʻrt jildda jamlangan 51 ta kitobdan iborat. Barcha kitoblar bepul va ochiq.</p>
  <p>Bu sahifada birinchi jildning oʻzbekcha tarjimasi joylashgan. Kitoblarni yuklab olib, oilada, sinfda va kutubxonada bemalol oʻqishingiz mumkin.</p>

  <div class="kutu bilgi"><p><strong>Tarjima hali qoralama.</strong> Oʻzbekcha matnlar hozircha ona tili oʻzbek tili boʻlgan muharrir tekshiruvidan oʻtmagan. Xato yoki taklifingiz boʻlsa, <a href="mailto:bilgi@oguzergin.net">bilgi@oguzergin.net</a> manziliga yozing.</p></div>

{BOLUMLER}

  <h2>Turkcha kitoblar</h2>
  <p>Turkumning barcha 51 ta turkcha kitobini saytimizda bepul oʻqishingiz va yuklab olishingiz mumkin. Audiokitoblar YouTubeʼda.</p>
  <div class="uzbag">
    <a href="index.html" lang="tr">Türkçe kitaplar</a>
    <a href="https://www.youtube.com/@BilgeveYonga" rel="noopener">YouTube: @BilgeveYonga</a>
  </div>

  <h2>Litsenziya</h2>
  <p>Barcha kitoblar <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.uz" rel="license">CC BY-NC-ND 4.0</a> litsenziyasi asosida ochiq. Manbani koʻrsatib, oʻzgartirmasdan va tijorat maqsadisiz tarqatish mumkin.</p>
  <p>Muallif: Prof. Dr. Oğuz Ergin · <a href="mailto:bilgi@oguzergin.net">bilgi@oguzergin.net</a></p>
</main>

<script>
(function(){
  var kok=document.documentElement, dgm=document.getElementById('tt');
  if(!dgm) return;
  function yoz(){var k=(kok.getAttribute('data-theme')||'dark')==='dark';
    var ad=document.getElementById('tt-ad');
    if(ad)ad.textContent=k?'Yorugʻ':'Qorongʻi';
    dgm.setAttribute('aria-label',(k?'Yorugʻ':'Qorongʻi')+' mavzuga oʻtish');}
  yoz();
  dgm.addEventListener('click',function(){
    var y=(kok.getAttribute('data-theme')||'dark')==='dark'?'light':'dark';
    kok.setAttribute('data-theme',y);
    try{localStorage.setItem('theme',y);}catch(e){}
    yoz();
  });
})();
</script>
</body>
</html>
"""


def main():
    HEDEF.mkdir(exist_ok=True)
    liste = list(kitaplar())
    bolumler = []
    for b in liste:
        if b["kapak_yerel"]:
            (HEDEF / "kapaklar").mkdir(exist_ok=True)
            from PIL import Image
            Image.open(b["kapak_yerel"]).convert("RGB").resize((480, 270), Image.LANCZOS).save(
                HEDEF / "kapaklar" / (b["kod"] + ".jpg"), quality=86)
            b["kart"] = "uz/kapaklar/" + b["kod"] + ".jpg"
        else:
            b["kart"] = "kapaklar/" + b["kod"] + ".jpg"
    for j, baslik in JILDLAR.items():
        kart_lari = [kart(b) for b in liste if b["jild"] == j]
        if kart_lari:
            bolumler.append(f'  <h2>{html.escape(baslik)}</h2>\n  <ul class="uzl">\n' + "\n".join(kart_lari) + "\n  </ul>")
    from PIL import Image
    (HEDEF / "kapaklar").mkdir(exist_ok=True)
    for b in liste:
        shutil.copyfile(b["pdf"], HEDEF / b["dosya"])
    (REPO / "uz.html").write_text(SABLON.replace("{BOLUMLER}", "\n\n".join(bolumler)), encoding="utf-8")
    print(f"  uz.html yazıldı, {len(liste)} kitap, PDF'ler uz/ altında")


if __name__ == "__main__":
    main()
