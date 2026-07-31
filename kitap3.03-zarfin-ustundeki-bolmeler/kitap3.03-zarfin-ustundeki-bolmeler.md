# Zarfın Üstündeki Bölmeler

**Seri:** Bilgisayar Mimarisi Serisi — Alt Seri 3: Buyrukların Dünyası — Kitap 3.3
**Yaş grubu:** 9–12 (okuma bilen)
**Ana tema:** Buyruk biçimleri (R, I, S, B, U, J), veri aktarma (yükle/sakla), aritmetik, mantık ve kaydırma buyrukları
**Karakterler:** Bilge (8 yaşında, kıvırcık kahverengi saçlı, yuvarlak gözlüklü kız), Yonga (küçük yuvarlak mavi-gümüş robot)

---

## Sayfa 1 — Mektupların Şeklinden Anlamak

**Metin:**
{B}"Yonga, işlemci bir buyruğu aldığında ne yapacağını nasıl anlıyor?" diye sordu Bilge.

{Y}"Buyruğun şekline bakarak!" dedi Yonga.
{Y}"Her buyruk aslında 32 tane sıfır ve birden oluşur.
Bu bitleri belirli gruplara böldüğünde anlam çıkar,
tıpkı bir zarfın üzerindeki bölmeler gibi: ad, adres, posta kodu."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A large cartoon envelope is shown open, with its address fields divided into labeled sections: "name", "street", "city", "postal code". Next to it, a glowing 32-bit instruction shown as colored blocks divided into sections. Bilge compares the two side by side. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — points at the matching sections. ONLY ONE ROBOT IN THE SCENE. Warm post office colors.

---

## Sayfa 2 — İlk Bölme

**Metin:**
{Y}"Her buyruğun en önemli bölümü **işlem kodu**dur," dedi Yonga.
(İngilizcesi opcode: ne tür işlem yapılacağını söyler)

{Y}"İşlem kodu, zarfın ilk satırı gibi: 'Bu ne tür bir mektup?
Fatura mı, davetiye mi, haber mi?'

İşlemci işlem koduna bakarak 'Bu bir toplama buyruğu' ya da
'Bu bir bellek okuma buyruğu' diye anlar."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A colorful 32-bit instruction bar at the top, with the leftmost section (opcode) glowing brightly in orange. Below it, three envelopes: one red (arithmetic), one blue (memory), one green (branch) — each representing a different type of instruction. Bilge holds a magnifying glass over the opcode section. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — sorts the envelopes. ONLY ONE ROBOT IN THE SCENE. Colorful sorting scene.

---

## Sayfa 3 — Neden Altı Biçim Var?

**Metin:**
{B}"Neden tek bir biçim yetmiyor?" diye sordu Bilge.

{Y}"Gönderdiğin şey değişince zarf da değişir," dedi Yonga. {Y}"Bir kartpostalda yalnız adres vardır. Bir kargoda ağırlık, boy, gönderen de yazar. Buyruklar da öyle: kimi üç yazmaç ister, kimi bir sayı taşır, kimi gidilecek yeri söyler. Bu yüzden altı zarf biçimi var. Her biri başka şey taşır ama hepsi 32 bit boyundadır."

{B}"Zarflar farklı ama hepsi aynı posta kutusuna sığıyor!" dedi Bilge.

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Bir masanın üstünde altı farklı zarf yan yana duruyor: kartpostal, ince mektup, kalın kargo zarfı, pencereli zarf, uçak postası zarfı, küçük paket. Hepsi farklı bölmelere ve farklı sayıda çizgiye sahip ama hepsi tam olarak aynı ende. Yanlarında hepsinin sığdığı tek bir posta kutusu var. Bilge zarfları karşılaştırıyor, Yonga posta kutusunu gösteriyor.

---

## Sayfa 4 — R Biçimi ve Yazmaç İşlemleri

**Metin:**
{Y}"RISC-V'te altı farklı buyruk biçimi var," dedi Yonga.
{Y}"İlki **R biçimi**: 'Register' sözcüğü yazmaç anlamına gelir.

R biçiminde üç yazmaç alanı var:
- **rs1**: Birinci kaynak yazmaç
- **rs2**: İkinci kaynak yazmaç
- **rd**: Hedef yazmaç (sonuç buraya gider)

Örneğin: 'x5 + x6 → x7' tam bir R biçimi buyruğu!"

{B}"Bunu nasıl yazarız?" diye sordu Bilge.
{Y}"Mühendisler kısaca `ADD x7, x5, x6` yazar. Kural şu: en başta hedef yazmaç durur, arkasından iki kaynak gelir. Sonucun gideceği yer hep en öndedir!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Three labeled gift boxes: "rs1" (contains the number 10), "rs2" (contains the number 7), and "rd" (empty, waiting). A big cartoon plus machine takes the contents of rs1 and rs2 and puts the result (17) into rd. The instruction bar at top shows the R-format layout with colored sections. Bilge operates the plus machine. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — labels the boxes. ONLY ONE ROBOT IN THE SCENE. Bright primary colors.

---

## Sayfa 5 — I Biçimi ve Anlık Sayı

**Metin:**
{Y}"**I biçimi** biraz farklı," dedi Yonga.
{Y}"'I' harfi İngilizce 'immediate' sözcüğünden gelir, anlık demektir. Sayı buyruğun içinde gömülüdür.

Örneğin 'x5 + 5 → x6' buyruğunda
5 sayısı bellekte ya da yazmaçta değil,
buyruğun ta kendisinin içindedir!"

{B}"Vay canına!" dedi Bilge. {B}"Sayıyı yanında getiriyor."

{Y}"Tıpkı 'bana 3 tane ver' demek gibi,
3'ü dışarıdan aramana gerek yok, zaten söyledin!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cartoon postman figure carries a letter. Inside the letter, a big colorful number "5" is already printed (the immediate value). The postman doesn't need to go to a register box — the number is right there in the letter. A register box labeled rs1 holds "10" and the result box rd receives "15". Bilge laughs in delight at the convenience. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — shows off the letter's built-in number. ONLY ONE ROBOT IN THE SCENE. Friendly postal scene colors.

---

## Sayfa 6 — Yükle ve Sakla

**Metin:**
{Y}"Veri aktarma buyrukları iki yönlü çalışır," dedi Yonga.

{Y}"**YÜKLE** (İngilizcesi load): Bellekten oku, yazmaca koy.
Örnek: 'Adres 100'deki sayıyı x5'e yükle.'"

{Y}"**SAKLA** (İngilizcesi store): Yazmaçtaki değeri belleğe yaz.
Örnek: 'x5'teki sayıyı adres 200'e sakla.'"

{B}"İkisi birbirinin tersi," dedi Bilge.
{B}"Bir kütüphaneden kitap almak ve kitap iade etmek gibi!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cozy library scene. Left action (YÜKLE): a small figure takes a book from a shelf (memory) and places it on a reading desk (register). Right action (SAKLA): the figure takes a book from the reading desk and returns it to the shelf. Arrows show the two directions clearly. Bilge stands in the middle as librarian. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — stamps the books. ONLY ONE ROBOT IN THE SCENE. Warm library colors, wooden shelves.

---

## Sayfa 7 — S ve B Biçimleri

**Metin:**
{Y}"**S biçimi** saklama buyrukları içindir," dedi Yonga.
{Y}"Adresi bulmak için kullanılan kayma değeri buyruğun içinde iki parçaya bölünmüş halde saklanır."

{B}"Neden bölünmüş?" diye sordu Bilge.

{Y}"Çünkü RISC-V'te her şey 32 bite sıkıştırılmıştır.
Yer az, akıllıca kullanmak gerekir!"

{Y}"**B biçimi** ise **dallanma** buyrukları içindir," dedi Yonga.
{Y}"'Koşul doğruysa şu adrese zıpla' demek için kullanılır."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Two instruction format bars shown side by side with different colorful section breakdowns. S-format shows its split address field highlighted with matching colors. B-format shows a branch arrow leading to a different address in a memory map. Bilge sketches the formats on a chalkboard. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — points at each section. ONLY ONE ROBOT IN THE SCENE. Educational chalkboard scene, bright colors.

---

## Sayfa 8 — U ve J Biçimleri

**Metin:**
{Y}"Sırada son iki biçim var," dedi Yonga.

{Y}"**U biçimi** büyük anlık sayılar içindir.
Bazen adres ya da büyük değer oluşturmak için gerekir."

{Y}"**J biçimi** ise **atlama** içindir, fonksiyon çağırmak gibi.
'Şu adrese git, işini bitir, geri dön' demek için."

{B}"Altı biçim, altı farklı zarf," dedi Bilge.
{B}"R, I, S, B, U, J, bunları ezberliyorum!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Six colorful envelopes arranged in a row, each labeled with a letter (R, I, S, B, U, J) and a small icon showing its purpose (R=three boxes, I=built-in number, S=shelf, B=fork in road, U=big number, J=jumping arrow). Bilge points at them one by one counting on her fingers. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — holds up a sorting chart. ONLY ONE ROBOT IN THE SCENE. Six distinct envelope colors.

---

## Sayfa 9 — Alanlar Hep Aynı Yerde

**Metin:**
{B}"İşlemci hangi zarfın geldiğini nereden biliyor?" diye sordu Bilge.

{Y}"En akıllı kısmı burada," dedi Yonga. {Y}"Altı biçim farklı, ama bazı bölmeler hepsinde aynı yerde durur. Hedef yazmaç hep aynı bitlerde, birinci kaynak hep aynı bitlerde. Böylece işlemci zarfın türünü daha anlamadan o bölmeleri okumaya başlar. Zaman kazanır."

{B}"Bakmadan uzanıp alıyor," dedi Bilge. {B}"Kalemin hep aynı gözde durduğunu bildiğin gibi!"

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Altı zarf üst üste hizalanmış duruyor, hepsi aynı ende. Zarfların üzerinde aynı dikey sütunda duran iki bölme parlak turuncu ve parlak yeşille vurgulanmış; öteki bölmeler soluk. Vurgulu bölmeler bütün zarflarda tam olarak aynı hizada olduğu için dikey iki ışık şeridi oluşuyor. Bilge şeritleri parmağıyla yukarıdan aşağı izliyor, Yonga yanında gülümsüyor.

---

## Sayfa 10 — Adresleme Kipleri

**Metin:**
{Y}"Peki bir buyruk, bellekteki adresi nasıl gösterir?" dedi Yonga.
{Y}"Koca bir adres 32 bitlik buyruğa sığmaz. Bu yüzden bir yazmaçtaki adresten yola çıkarız. Buna **adresleme kipi** denir:

**Taban + Kayma**: 'Şu yazmaçtaki adrese 8 ekle, oraya git.' Yükleme ve saklama böyle çalışır.
**Yazmaç Dolaylı**: Kaymayı sıfır yap, doğrudan yazmaçtaki adrese git.
**PC Göreceli**: 'Şu anki konumdan 20 adres ileriye git.' Dallanmalar böyle çalışır."

{B}"Demek adresi baştan değil, yakınından yazıyoruz!" dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Three cartoon characters each give directions to the same destination (a red house): Character 1 holds a box labeled x6 containing an address and adds "+8" to it to point at the house. Character 2 holds a box labeled x5 which contains the address directly (offset zero). Character 3 stands at a signpost and says "20 steps forward from here." All three arrows lead to the same red house. Bilge and Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — watch the three characters. ONLY ONE ROBOT IN THE SCENE. Map-style illustration, warm colors.

---

## Sayfa 11 — Bir Buyruğu Bit Bit Çözelim

**Metin:**
{Y}"Hadi bir buyruğu birlikte çözelim," dedi Yonga ve havaya otuz iki kutuluk bir şerit çizdi.

{Y}"Şu buyruk geldi: `ADD x7, x5, x6`. En sağdaki bölme işlem kodu, 'bu bir yazmaç işlemi' diyor. Öteki bölmelerde hedef x7 ile kaynaklar x5 ve x6 duruyor."

{B}"Kalan bölme ne?" diye sordu Bilge.

{Y}"Hangi işlem olduğunu söylüyor: toplama mı, çıkarma mı. İşlem kodu aileyi seçer, o bölme de tek tek işi."

**Resim:**
Sıcak renkli, yumuşak çizgili, dijital suluboya tarzında çocuk kitabı illüstrasyonu. Havada süzülen uzun bir şerit otuz iki küçük kutuya bölünmüş. Şeridin bölmeleri farklı renklerle gruplanmış ve her gruptan aşağı doğru ince bir ok iniyor; okların ucunda sırasıyla küçük etiketler var: bir yazmaç kutusu üstünde 7, bir tanesi 5, bir tanesi 6. En sağdaki grup ayrı renkte ve daha parlak. Bilge şeridin altında durmuş yukarı bakıyor, Yonga şeridin yanında elini kaldırmış gösteriyor.

---

## Sayfa 12 — Şifreler Çözüldü!

**Metin:**
Bilge ellerini birbirine vurdu:
{B}"Anladım! Her buyruk aslında 32 bit.
Bu bitlerin biçimi (R, I, S, B, U, J) ne tür buyruk olduğunu söylüyor.
İçinde işlem kodu, kaynak yazmaçlar, hedef yazmaç ve bazen anlık sayı var."

{Y}"Ve işlemci bu şifreyi saniyede milyarlarca kez çözüyor," dedi Yonga.

{B}"Müthiş," dedi Bilge. {B}"Her bit bir anlam taşıyor."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A large glowing 32-bit instruction bar at the top, with each section (opcode, rd, rs1, rs2, and the instruction's other small sub-fields) highlighted in different colors with tiny labels. Below it, the instruction "decodes" into a beautiful illustrated action: two register boxes combining into a result box. Bilge holds the decoded instruction like a puzzle piece clicking into place. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — beams proudly. ONLY ONE ROBOT IN THE SCENE. Puzzle-reveal colors, satisfying warm tones.

---

## Sayfa 13 — Büyük Resim

**Metin:**
O gece Bilge duvara bir şema yapıştırdı:

```
Bir buyruk: 32 bit
        ↓
 Altı zarf biçimi
        ↓
    İşlem kodu
   Hedef yazmaç
 Kaynak yazmaçlar
    Anlık sayı
```

{B}"Zarfın üstündeki her bölme bir soruya yanıt veriyor," dedi Bilge,
{B}"ve işlemci hepsini bir bakışta okuyor."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Bilge stands in front of a large colorful wall chart about ONE 32-bit instruction: at the top a long strip of 32 small boxes, below it six differently shaped envelopes in a row (all the same width), and below that four labelled fields branching out (opcode, destination register, source registers, immediate number). Each branch uses a different color. No text or letters anywhere on the chart; only the strip, the envelopes, colored boxes and arrows. Each branch uses a different color. The chart looks hand-drawn and warm, like a school project. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — admires the chart from the side. ONLY ONE ROBOT IN THE SCENE. Educational wall chart, warm lamplight.

---

## Bugün Ne Öğrendik?


🏷️ **İşlem kodu** (İngilizcesi opcode): Buyruğun ne tür işlem yapacağını belirten bit grubu.

🧮 **R biçimi:** İki kaynak yazmaç + bir hedef yazmaç. Örnek: ADD, SUB.

✍️ **Buyruk yazımı:** Önce hedef yazmaç, sonra kaynaklar. `ADD x7, x5, x6` demek "x5 ile x6'yı topla, sonucu x7'ye yaz" demektir.

🔢 **I biçimi:** Bir kaynak yazmaç + buyruğun içine gömülü anlık sayı. Örnek: ADDI.

📥 **S biçimi:** Saklama buyrukları için. Adresi bulmaya yarayan kayma değeri iki parçada.

🔀 **B biçimi:** Dallanma buyrukları (koşullu atlama).

🔝 **U biçimi:** Büyük anlık sayılar için.

🦘 **J biçimi:** Koşulsuz atlama / fonksiyon çağrısı.

⬇️ **YÜKLE / SAKLA:** Bellekten yazmaca al / yazmaçtan belleğe yaz.

📏 **Altı biçim, tek boy:** Zarflar farklı şeyler taşır ama hepsi 32 bittir.

📐 **Alanlar hep aynı yerde:** Hedef ve birinci kaynak her biçimde aynı bitlerde durur; işlemci buyruğun türünü anlamadan onları okumaya başlar.

🗺️ **Adresleme kipleri:** Bir bellek adresini farklı şekillerde belirtme yolları.
