# Üstveri betikleri

Görsellere ve PDF'lere telif, lisans ve veri madenciliği bilgisini gömen
betikler.

## Çalıştırma sırası

**Üstveri gömme her zaman `build_web.py`den SONRA çalışır.**

    python build_web.py
    python betikler/gorsel-telif-goml.py --epub-ici --yedek-yok .
    python betikler/pdf-ustveri-duzelt.py --yedek-yok .

Sıra önemlidir: `build_web.py` her kurulumda `deste/` ve `okuyucu/thumbs/`
klasörlerini yeniden üretir ve EPUB'ları yeniden paketler. Üretilen bu dosyalar
gömülü üstveriyi taşımaz, bu yüzden gömme adımı sonra gelir.

## Ne gömülüyor

`dc:rights`, `cc:license`, `xmpRights:Marked`, `xmpRights:UsageTerms`,
`plus:Licensor`, `Iptc4xmpCore` iletişim bilgisi ve `tdm:reservation=1`.

JPEG için ham APP1 bölütü değiştirilir, görüntü yeniden kodlanmaz; piksel
verisi bit düzeyinde aynı kalır.

EPUB'lar için `--epub-ici` gerekir. EPUB bir zip paketidir ve içindeki görseller
depodaki kopyalardan ayrı durur; bu seçenek olmadan onlar üstverisiz kalır.

## Filigran

`--filigran-kapak` seçeneği kapaklara görünür damga basar ve o görselleri
yeniden kodlar. Kullanılmıyor.
