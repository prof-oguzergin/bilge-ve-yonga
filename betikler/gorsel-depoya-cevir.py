# -*- coding: utf-8 -*-
"""Drive'daki PNG asillarini depodaki JPEG surumlerine cevirir.

Depo yalnizca kucuk JPEG'leri tasir (Pages'in boyut siniri); PNG asillar
Drive'da durur. Kitap PDF'i Drive'daki PNG'den uretildigi icin bir kare
yenilendiginde PDF hemen degisiyor ama site eski goruntuyu gostermeye
devam ediyordu: aradaki bu cevirme adimi elle yapiliyordu ve bir kez
atlandi. Artik betik.

    python betikler/gorsel-depoya-cevir.py                 # butun kitaplar
    python betikler/gorsel-depoya-cevir.py kitap4.07-...   # tek kitap

Yalnizca PNG'si JPEG'den yeni olan kareler cevrilir; ötekiler ellenmez,
boylece gomulu telif ustverisi bosuna silinmez.
"""
import sys
from pathlib import Path

from PIL import Image

DEPO = Path(__file__).resolve().parent.parent
KAYNAK = Path(r'G:\My Drive\Yazdığımız Kitaplar\Çocuk Kitapları'
              r'\Bilgisayar Mimarisi Serisi')
GEN = 1600          # depodaki JPEG genisligi
KALITE = 82


def cevir(png: Path, jpg: Path) -> bool:
    if jpg.exists() and jpg.stat().st_mtime >= png.stat().st_mtime:
        return False
    im = Image.open(png).convert('RGB')
    if im.width != GEN:
        im = im.resize((GEN, round(im.height * GEN / im.width)), Image.LANCZOS)
    jpg.parent.mkdir(parents=True, exist_ok=True)
    im.save(jpg, 'JPEG', quality=KALITE, optimize=True, progressive=True)
    return True


def main():
    hedefler = sys.argv[1:]
    klasorler = [d for d in sorted(KAYNAK.iterdir())
                 if d.is_dir() and d.name.startswith('kitap')
                 and (not hedefler or d.name in hedefler)]
    toplam = 0
    for d in klasorler:
        kaynak_res = d / 'resimler'
        hedef_res = DEPO / d.name / 'resimler'
        if not kaynak_res.is_dir():
            continue
        n = 0
        for png in sorted(kaynak_res.glob('*.png')):
            if cevir(png, hedef_res / (png.stem + '.jpg')):
                n += 1
        if n:
            print('  %-46s %2d kare' % (d.name, n))
            toplam += n
    print('çevrilen kare:', toplam)


main()
