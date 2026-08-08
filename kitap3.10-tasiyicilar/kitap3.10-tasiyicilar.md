# Taşıyıcılar

**Seri:** Bilgisayar Mimarisi Serisi — Alt Seri 3: Buyrukların Dünyası — Kitap 3.10
**Yaş grubu:** 9–12 (okuma bilen)
**Ana tema:** Veri aktarma buyrukları (YÜKLE/SAKLA, İngilizcesi load/store): bellekten yazmaca, yazmaçtan belleğe
**Karakterler:** Bilge (8 yaşında, kıvırcık kahverengi saçlı, gözlüklü kız) ve Yonga (küçük, yuvarlak, mavi-gümüş renkli sevimli robot)

---

## Sayfa 1 — Büyük Kütüphane

**Metin:**
Bilge ve Yonga büyük bir kütüphanedeydi. Raflar tavan yüksekliğine kadar kitapla doluydu.

{Y}"Bu kütüphane bana içimdekileri hatırlatıyor!" dedi Yonga. {Y}"Burası benim belleğim gibi!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Devasa, ahşap raflı, tavan yüksekliğinde kitapların dizili olduğu bir kütüphane. Yüksek pencerelerden güneş ışığı giriyor. Kıvırcık kahverengi saçlı, gözlüklü Bilge boyundan yüksek raflara bakıyor, ağzı açık. Yonga yanında duruyor, göğsündeki ekranda kütüphane raflarının minyatür yansıması görünüyor. Ahşap ve altın sarısı sıcak tonlar.

---

## Sayfa 2 — Okuma Masası

**Metin:**
{Y}"Kütüphanede kitaplar nerede durur?" diye sordu Yonga.

{B}"Raflarda!" dedi Bilge. {B}"Ama okumak için masaya getirmem gerekiyor. Rafta okuyamam!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Bilge uzak raftan bir kitap alıyor, küçük okuma masasına getiriyor. Masanın üstü küçük ve düzenli, sadece birkaç kitap sığıyor. Yonga masanın başında oturuyor, "İşte tam da bu!" der gibi gülümsüyor. Kütüphane arka planda devam ediyor. Pastel yeşil ve kahverengi tonlar.

---

## Sayfa 3 — Bellek ve Yazmaçlar

**Metin:**
{Y}"Bilgisayarda da tam aynı şey var." dedi Yonga. {Y}"Bellek kütüphane gibidir: büyük, çok şey tutar ama uzak. Yazmaçlar ise masa gibidir: küçük ama tam önünde!"

Bilge gözlerini kıstı. {B}"Yazmaçlar mı? Onları biliyorum!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. İki bölümlü bir illüstrasyon: sol tarafta devasa "BELLEK" kütüphanesi (binlerce kitap), sağ tarafta küçük "YAZMAÇLAR" masası (sadece 32 slot). Ortada Yonga bir köprü gibi duruyor, iki yana işaret ediyor. Bellek büyük ama soluk renkli (uzak), yazmaçlar küçük ama canlı ve parlak (yakın). Oklar iki yönlü.

---

## Sayfa 4 — Hızlı ama Az

**Metin:**
{Y}"Yazmaçlar çok hızlı çalışır." dedi Yonga. {Y}"Ama sayıları az! RISC-V'te 32 yazmaç var."

{Y}"Bellek ise milyonlarca, hatta milyarlarca sayı tutar." dedi Yonga. {Y}"Ama biraz daha yavaş."

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. İki yarışçı atlet çizilmiş: biri küçük, çevik, hızlı (yazmaç, "32 slot"), diğeri büyük ve güçlü ama daha yavaş (bellek, "milyarlarca bayt"). Aralarında bir yarış pisti var, küçük atlet ileride. Yonga "Küçük ama hızlı!" diye küçük atletin yanında duruyor. Bilge tribünden izliyor. Canlı atletizm renkleri.

---

## Sayfa 5 — YÜKLE Buyruğu

**Metin:**
{B}"Peki bellekteki sayıyı nasıl kullanırız?" diye sordu Bilge.

{Y}"Önce onu yazmaçlara getirmen gerekiyor." dedi Yonga. {Y}"Bu işe **YÜKLE** (İngilizcesi load) diyoruz!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Kütüphane rafından bir kitap alınıyor, hamal figürü omzuna alıyor, okuma masasına taşıyor. Kitabın üzerinde "42" yazıyor. Masada Bilge bekliyor. Yonga "lw x5, 100(x0): bellekteki 42'yi x5 yazmacına yükle!" diyor, küçük bir açıklama balonu içinde. Pastel sarı ve kahverengi tonlar.

---

## Sayfa 6 — Hamal Gibi

**Metin:**
Yonga devam etti: {Y}"YÜKLE buyruğu şunu der: 'Git, şu adresteki sayıyı al, getir, yazmaçlara koy!'"

{B}"Hamal gibi!" dedi Bilge gülerek. {B}"Bellekten yazmaçlara taşıyıcı!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Sevimli bir hamal figürü, küçük, kasketi ve iş önlüğüyle, büyük "BELLEK" deposundan bir kutu alıyor, üzerinde adres yazıyor: "0x1000". Kutuyu küçük "YAZMAÇLAR" masasına bırakıyor. Kutu içinde "42" sayısı görünüyor. Bilge ve Yonga hamalı alkışlıyor. Turuncu ve kahverengi depo ortamı.

---

## Sayfa 7 — SAKLA Buyruğu

**Metin:**
{B}"Peki işim bitince sayıyı nereye koyarım?" diye sordu Bilge.

{Y}"Bellekte saklarsın, **SAKLA** (İngilizcesi store) buyruğu!" dedi Yonga. {Y}"Yazmaçtan belleğe taşırsın!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Bilge okuma masasındaki kitabı tamamlamış, kütüphane rafına geri götürüyor. Kitabın kapağında "99" yazıyor (değiştirilmiş değer). Yonga "sw x5, 200(x0): x5'teki sayıyı belleğin 200. adresine sakla!" diyor. Raf etiketi güncelleniyor. Yeşil ve bej tonlar, düzenli kütüphane ortamı.

---

## Sayfa 8 — İki Yönlü Yol

**Metin:**
{B}"İki yönlü bir yol var." dedi Bilge. {B}"Bellekten yazmaçlara ve yazmaçlardan belleğe!"

{Y}"Aynen öyle!" dedi Yonga. {Y}"**YÜKLE** ve **SAKLA**: taşıyıcıların iki yönlü yolculuğu."

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Büyük bir çift yönlü yol: solda "BELLEK" deposu, sağda "YAZMAÇLAR" masası. Üst yol "YÜKLE" etiketiyle bellekten yazmaçlara, alt yol "SAKLA" etiketiyle yazmaçlardan belleğe gidiyor. Yolda sevimli küçük taşıyıcı figürleri koşturuyor. Canlı mavi ve turuncu renkler.

---

## Sayfa 9 — Neden Bellekte Değil?

**Metin:**
{B}"Neden doğrudan bellekte işlem yapamayız?" diye sordu Bilge.

Yonga anlattı: {Y}"Çünkü bellek yavaştır! Doğrudan orada hesaplama yapsak, her işlem için beklememiz gerekirdi."

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. İki seçenek gösteriliyor: 1. seçenek, kütüphanede ayakta durarak sayfaları rafta çevirmeye çalışmak (yavaş, rahatsız, bacaklar yorgun). 2. seçenek, kitabı masaya getirip oturmak (hızlı, rahat, verimli). Bilge iki sahneye bakıyor, ikinci seçeneği tercih ediyor. Komik ama açıklayıcı bir karşılaştırma.

---

## Sayfa 10 — RISC Döngüsü

**Metin:**
{Y}"RISC felsefesi şunu der: 'Hesaplamayı hep yazmaçlarda yap!'." dedi Yonga.

{Y}"Bellekten al, işle, geri koy. Bu döngü her şeyin temelidir."

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Üç adımlı bir döngü dairesi çizilmiş: 1. "YÜKLE, bellekten al" (mavi ok, deposundan yazmaçlara), 2. "HESAPLA, yazmaçlarda işle" (yeşil ok, yazmaç üzerinde), 3. "SAKLA, belleğe geri koy" (turuncu ok, yazmacından depoya). Ortada "RISC Felsefesi" yazan küçük bir madalyon. Yonga döngüyü işaret ediyor.

---

## Sayfa 11 — Adresleme

**Metin:**
{B}"Adresleme nasıl çalışıyor?" diye sordu Bilge. {B}"Bellekte her sayı nasıl bulunuyor?"

Yonga güldü. {Y}"Kütüphanede her kitabın numarası var ya: raf 3, sıra 7, konum 2. Bellekte de her yerin bir **adresi** var!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Kütüphane rafı detaylı çizilmiş, her rafdaki kitabın sırtında adres numaraları var: 0x1000, 0x1004, 0x1008... Yonga bir adres kartı tutuyor "0x1004" yazıyor. O adresteki kutudan "73" sayısı çıkıyor. Bilge numaraları okuyarak ilgili rafı buluyor. Canlı, düzenli kütüphane atmosferi.

---

## Sayfa 12 — Ne Kadar Veri?

**Metin:**
{B}"Ne kadar veri taşınır?" diye sordu Bilge.

{Y}"İstediğin kadar: bayt (8 bit), yarım sözcük (16 bit), tam sözcük (32 bit) ya da çift sözcük (64 bit)!" dedi Yonga.

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Dört farklı boyda kutu yan yana: çok küçük "bayt" kutusu, küçük "16 bit" kutusu, orta "32 bit" kutusu, büyük "64 bit" kutusu. Her kutunun üzerinde boyutu yazıyor. Hamal figürü en büyük kutuyu taşımaya çalışıyor, biraz zorlanıyor ama gülerek yapıyor. Bilge küçük kutuyu kolayca taşıyor. Pastel renkler.

---

## Sayfa 13 — Kütüphaneden Çıkış

**Metin:**
Bilge kütüphaneden çıkarken raflara son bir kez baktı. Artık sadece kitap görmüyordu, veri adresleri, YÜKLE ve SAKLA görüyordu.

{Y}"Taşıyıcılar sayesinde, her şey olması gereken yerde, tam zamanında hazır olur!" dedi Yonga.

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Kütüphane kapısından çıkarken Bilge ve Yonga el ele, gün ışığına doğru yürüyorlar. Bilge'nin gözlüklerinde kütüphane raflarının yansıması var, ama artık her kitabın sırtında sayısal adresler görünüyor. Yonga'nın ekranında "YÜKLE ↔ SAKLA" yazıyor. Dışarıda güneşli, açık hava. Altın sarısı ve açık mavi tonlar.

---

## Bugün Ne Öğrendik?

📚 **Bellek** büyük bir kütüphane gibidir: milyarlarca veriyi tutar ama yavaştır.

📋 **Yazmaçlar** küçük bir masa gibidir: az veri tutar ama çok hızlıdır.

⬇️ **YÜKLE (load):** Bellekten bir adresten veriyi alıp yazmaca taşır.

⬆️ **SAKLA (store):** Yazmaçtaki veriyi belleğin bir adresine geri koyar.

⚡ Bilgisayar hesaplamayı hep **yazmaçlarda** yapar; belleğe sadece al/koy için gider.

🏠 Bellekteki her konumun bir **adresi** vardır, tıpkı kütüphanedeki kitapların raf numarası gibi.

📏 Veri farklı boyutlarda taşınır: küçücük bir **bayt**, ondan büyük bir **yarım sözcük**, daha büyük bir **tam sözcük**, en büyük de bir **çift sözcük**; tıpkı küçük, orta ve büyük kutular gibi!

🔄 **RISC felsefesi:** Bellekten al → Yazmaçta işle → Belleğe geri koy. Bu döngü her şeyin temelidir!
