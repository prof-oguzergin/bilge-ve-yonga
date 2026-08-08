# Mektup Fabrikası

**Seri:** Bilgisayar Mimarisi Serisi — Alt Seri 3: Buyrukların Dünyası — Kitap 3.5
**Yaş grubu:** 9–12 (okuma bilen)
**Ana tema:** Derleme zinciri: derleyici, çevirici, bağlayıcı ve yükleyici; kaynak koddan çalışan programa giden yol
**Karakterler:** Bilge (8 yaşında, kıvırcık kahverengi saçlı, yuvarlak gözlüklü kız), Yonga (küçük yuvarlak mavi-gümüş robot)

---

## Sayfa 1 — Türkçeden Makineye

**Metin:**
{B}"Yonga, ben Python ya da C yazıyorum.
İşlemci ise yalnızca sıfır ve birleri anlıyor.
Bu ikisi arasında büyük bir uçurum var.
Kim köprü kuruyor?" dedi Bilge.

{Y}"Çok katmanlı bir fabrika!" dedi Yonga heyecanla.
{Y}"Adına **derleme zinciri** diyoruz.
Mektubu verirsin fabrikaya, öbür taraftan makine kodu çıkar!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A large colorful factory building with a conveyor belt going through it. On the left, Bilge feeds in a sheet of paper with colorful human-readable code. The factory has several stations inside (visible through windows). On the right, a glowing chip/executable emerges. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, stands at the entrance waving Bilge's paper inside. ONLY ONE ROBOT IN THE SCENE. Industrial but cheerful colors.

---

## Sayfa 2 — Fabrika Dört İstasyondan Oluşur

**Metin:**
Yonga dört parmak kaldırdı:

{Y}"**1. Derleyici**: Bilge'nin yazdığı program → RISC-V çevirici dili (İngilizcesi assembly)
**2. Çevirici**: RISC-V çevirici dili → makine kodu (sıfır ve birler)
**3. Bağlayıcı**: Parça parça dosyaları birleştir
**4. Yükleyici**: Programı belleğe yerleştir ve çalıştır"

{B}"Dört istasyon, tek ürün." dedi Bilge. {B}"Çalışan program!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A factory floor cross-section with four numbered workstations in a row, connected by a conveyor belt. Station 1 (Compiler) has a translator at a desk with dictionaries. Station 2 (Assembler) has a machine converting text to binary blocks. Station 3 (Linker) has a worker stitching puzzle pieces together. Station 4 (Loader) has a crane placing the final product onto a memory shelf. Bilge walks along the top watching. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, oversees from a supervisor platform. ONLY ONE ROBOT IN THE SCENE. Colorful factory illustration.

---

## Sayfa 3 — Büyük Çevirmen

**Metin:**
{Y}"Derleyici devasa bir çevirmendir." dedi Yonga.

{Y}"Sen şunu yazarsın:"

`int toplam = 3 + 5;`

{Y}"Derleyici bunu RISC-V çevirici diline çevirir:"

```
addi x5, x0, 3   # x5'e 3 koy
addi x6, x0, 5   # x6'ya 5 koy
add  x7, x5, x6  # x5+x6 → x7
```

{Y}"# işaretinden sonrası bilgisayara değil bize yazılır." dedi Yonga.

{B}"Anlıyorum!" dedi Bilge. {B}"Derleyici cümleyi sözcük sözcük değil,
anlam anlam çeviriyor!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cheerful translator character sits at a big desk surrounded by dictionaries and grammar books. On the left of the desk, a card with a simple math statement in colorful blocks. On the right, the same statement translated into three çevirici dili instruction cards. The translator carefully checks meaning, not just words, with a thoughtful expression. Bilge watches over the translator's shoulder. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, hands the input card to the translator. ONLY ONE ROBOT IN THE SCENE. Warm library/study colors.

---

## Sayfa 4 — Makineye En Yakın Dil

**Metin:**
{B}"Çevirici dili nedir?" diye sordu Bilge.

{Y}"İnsanın okuyabildiği en alt düzey dildir." dedi Yonga.
{Y}"`add x7, x5, x6` gibi kısa sözcükler kullanır.
İnsan yine de anlayabilir ama artık çok makineye yakın.

Her çevirici dili satırı tam olarak **bir makine buyruğuna** karşılık gelir."

{B}"Derleyici ile makine arasındaki köprü." dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A bridge illustration. On the left bank: a human programmer with colorful code in a high-level language. On the right bank: a glowing chip with binary 0s and 1s. In the middle of the bridge: çevirici dili (assembly) cards, short, readable but technical. The bridge is labeled "Çevirici Dili." Bilge stands on the left bank, peering toward the right. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, stands in the middle of the bridge. ONLY ONE ROBOT IN THE SCENE. River and bridge watercolor.

---

## Sayfa 5 — Sözcükleri Bitlere Dönüştürmek

**Metin:**
{Y}"Çevirici, çevirici dilindeki satırları alır ve, her birini 32 bitlik bir makine koduna dönüştürür.

`add x7, x5, x6` → `00000000011000101000001110110011`

Bu 32 bit bilgisayarın anlayacağı tek dildir." dedi Yonga.

Bilge gözlerini açtı: {B}"Bu kadar sıfır ve biri nasıl okuyorlar?"

{Y}"Okumuyorlar." güldü Yonga. {Y}"İşlemci doğrudan elektrik sinyali olarak yorumluyor!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. An assembler machine (looks like a printing press). On the left: çevirici dili instruction cards go in ("add x7, x5, x6"). On the right: a long strip of 0s and 1s comes out, glowing blue-white. The machine stamps each instruction into its binary form. Bilge examines the binary strip with a magnifying glass, looking puzzled but fascinated. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, operates the press lever. ONLY ONE ROBOT IN THE SCENE. Print shop industrial colors.

---

## Sayfa 6 — Nesne Dosyası

**Metin:**
{Y}"Çevirici çalışınca elimizde **nesne dosyası** kalır." dedi Yonga.
{Y}"İçinde makine kodu var ama henüz tam değil.
Bazı yerler boş: başka dosyalardaki fonksiyonlara atıf var."

{B}"Sanki bir kitabın bölümleri ayrı ayrı basılmış, ama henüz ciltsiz." dedi Bilge.

{Y}"Aynen öyle! Bağlayıcı onları ciltleyecek."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Three loose book chapters spread on a table, each with binary code printed on the pages. Some pages have gaps or placeholder stickers reading "TO BE FILLED." A bookbinder's tools (needle, thread, cover) wait nearby. Bilge holds up one chapter. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, arranges the chapters in order. ONLY ONE ROBOT IN THE SCENE. Bookbinding workshop colors.

---

## Sayfa 7 — Her Şeyi Birleştirmek

**Metin:**
{Y}"**Bağlayıcı** tüm nesne dosyalarını alır, artı gerekli **kütüphane** dosyalarını,
(kütüphane = hazır yazılmış, tekrar kullanılabilen kod paketi)
ve hepsini birleştirerek bir **çalıştırılabilir dosya** üretir.

Boş yerler doldurulur. Adresler hesaplanır.
Her şey birbirine bağlanır." dedi Yonga.

{B}"Kitap ciltlendi!" dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A bookbinder at work: three separate chapters plus a shelf of pre-made library books are combined into one complete, beautifully bound book. The linker character expertly sews them together. Filled-in pages replace the "TO BE FILLED" stickers. The final book glows with a golden aura. Bilge watches in delight. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, ties the last knot. ONLY ONE ROBOT IN THE SCENE. Warm binding workshop colors.

---

## Sayfa 8 — Kütüphaneler

**Metin:**
{Y}"Kütüphaneler çok önemli." dedi Yonga.
{Y}"Her programcı her şeyi sıfırdan yazmak zorunda değildir.
'Ekrana yaz', 'dosya aç', 'internet bağlantısı kur' gibi
binlerce hazır işlev kütüphanelerde bekler.

Bağlayıcı bunlardan yalnızca ihtiyaç duyduklarını senin programına ekler."

{B}"Her seferinde tekerleği yeniden icat etmemek gibi." dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A giant library with tall shelves full of small labeled jars/bottles. Each jar contains a ready-made function: "print to screen," "open file," "connect internet," etc. A programmer character reaches out and takes only the jars needed for their program. Unused jars stay on the shelf. Bilge browses the shelves. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, hands jars down from a high shelf. ONLY ONE ROBOT IN THE SCENE. Apothecary/library colors, warm browns and golds.

---

## Sayfa 9 — Programa Hayat Vermek

**Metin:**
{Y}"Son adım: **yükleyici**." dedi Yonga.

{Y}"Çalıştırılabilir dosya hâlâ disk üzerindedir.
Çalışması için belleğe taşınması gerekir.

Yükleyici programı diskten alır,
belleğin uygun yerine yerleştirir,
Program Sayacını programın başlangıcına ayarlar
ve… çalıştırır!"

{B}"Çalıştır!" dedi Bilge parmaklarını şıklatarak.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A launcher scene: a rocket (the program) sits on a launch pad (disk). A loader character carries the rocket to a launch platform (memory). The rocket is carefully placed, countdown begins, engines light up. LAUNCH! The rocket soars into the sky (CPU executing). Bilge presses a big green launch button. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, gives a thumbs up from the control room. ONLY ONE ROBOT IN THE SCENE. Launch scene, bright blues and oranges.

---

## Sayfa 10 — Ne Kadar Zaman Alır?

**Metin:**
{B}"Bütün bu derleme zinciri ne kadar sürer?" diye sordu Bilge.

{Y}"Küçük bir program için saniyenin binde biri bile sürmez." dedi Yonga.
{Y}"Büyük bir işletim sistemi için saatler gerekebilir!
Ama sen 'Çalıştır' düğmesine bastığında tüm bu süreç
ya önceden tamamlanmıştır ya da anında gerçekleşir."

{B}"Python bunu anında yapıyor." dedi Bilge.
{B}"C önceden yapıyor."

{Y}"Harika! Buna **derlenen** ve **yorumlanan** dil farkı denir."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Two side-by-side scenes. Left (compiled: C): A factory works overnight, produces a finished product ready to run instantly at dawn. Right (interpreted: Python): A chef cooks while you watch, reading the recipe line by line in real time. Both end up with a meal (running program) but via different timing. Bilge watches both scenes. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, points at both with a comparison chart. ONLY ONE ROBOT IN THE SCENE. Split illustration, warm cooking and factory tones.

---

## Sayfa 11 — Hata İletileri

**Metin:**
{Y}"Derleyici bazen hata iletisi verir." dedi Yonga.

{Y}"Bu aslında çok iyi bir şey!
Demek ki derleyici bir hata olduğunu anladı
ve sana söylüyor.
Makine koduna çevirmeden önce yakaladı.

İletiyi okursan hatayı bulabilirsin."

{B}"Demek derleyici bir tür öğretmen." dedi Bilge.
{B}"'Burada yanlış yaptın' diyor."

{Y}"Sabırlı ve yorulmaz bir öğretmen!" dedi Yonga.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A friendly teacher character (the compiler) sits at a desk reviewing a student's paper. Red circles and friendly notes appear on the paper: "Missing semicolon here!", "Unknown variable here!" The teacher points at each error helpfully, not sternly. Bilge receives the marked paper looking thoughtful (not upset). Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, reads the error notes. ONLY ONE ROBOT IN THE SCENE. Warm classroom colors.

---

## Sayfa 12 — Büyük Resim Tekrar

**Metin:**
Bilge duvara büyük bir şema çizdi:

```
    Senin Programın
           ↓
       Derleyici
           ↓
   Çevirici Dili Kodu
           ↓
        Çevirici
           ↓
    Nesne Dosyaları
           ↓
Bağlayıcı + Kütüphaneler
           ↓
 Çalıştırılabilir Dosya
           ↓
       Yükleyici
           ↓
      Çalışıyor! 🎉
```

{B}"Şimdi anladım neden program yazmak bu kadar güçlü." dedi Bilge.
{B}"Arkasında devasa bir fabrika var."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Bilge stands proudly in front of a large hand-drawn wall chart showing the full compilation pipeline as a vertical flowchart with colorful arrows. Each step has a small icon (translator, press, bookbinder, rocket). The final step at the bottom shows a glowing computer screen running a program. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, points at the chart with a laser pointer. ONLY ONE ROBOT IN THE SCENE. Educational wall chart, warm lamplight.

---

## Sayfa 13 — Fabrika Çalışmaya Devam Ediyor

**Metin:**
O gece Bilge masasındaki bilgisayara baktı.

{B}"Bu şu an yüzlerce program çalıştırıyor.
Her biri bir zamanlar birinin yazdığı koddu.
Sonra derleyici çevirdi, çevirici ikili koda çevirdi,
bağlayıcı birleştirdi, yükleyici yerleştirdi.

Ve şimdi hepsi, sessizce, elektrik hızında çalışıyor."

Derin bir nefes aldı. Büyüleyiciydi.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Night scene: Bilge at her desk, the computer screen glowing softly. Inside the screen, a cutaway shows many tiny programs running simultaneously, each a tiny rocket, each following its own path, all going at once. Above each tiny rocket, a ghostly chain shows its journey: code → çevirici dili → binary → linked → loaded. Yonga, a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna, sits on Bilge's shoulder in awe. ONLY ONE ROBOT IN THE SCENE. Dreamy night colors, soft glow.

---

## Bugün Ne Öğrendik?


🏭 **Derleme zinciri:** Kaynak koddan çalışan programa giden fabrika: Derleyici → Çevirici → Bağlayıcı → Yükleyici.

🔄 **Derleyici:** Bilge'nin yazdığı programı çevirici diline çevirir.

📝 **Çevirici dili:** İnsanın okuyabildiği en alt düzey dil. Her satır bir makine buyruğuna karşılık gelir.

⚙️ **Çevirici:** Çevirici dilini makine koduna (0 ve 1'lere) dönüştürür. Çıktısı nesne dosyasıdır.

🧩 **Nesne dosyası:** İçinde makine kodu olan ama henüz tam olmayan dosya; bazı adresleri boş.

🔗 **Bağlayıcı:** Birden fazla nesne dosyasını ve kütüphane dosyalarını birleştirerek çalıştırılabilir dosya üretir.

📚 **Kütüphane:** Hazır, tekrar kullanılabilir kod paketi. Her seferinde sıfırdan yazmak gerekmez.

🚚 **Yükleyici:** Çalıştırılabilir dosyayı diskten belleğe taşır ve programı başlatır.

⚖️ **Derlenen dil ile yorumlanan dil:** C önceden derlenir (hızlı çalışır). Python çalışırken satır satır yorumlanır (daha esnek).
