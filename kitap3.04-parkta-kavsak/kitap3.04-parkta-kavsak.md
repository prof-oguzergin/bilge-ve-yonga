# Parkta Kavşak

**Seri:** Bilgisayar Mimarisi Serisi — Alt Seri 3: Buyrukların Dünyası — Kitap 3.4
**Yaş grubu:** 9–12 (okuma bilen)
**Ana tema:** Dallanma ve atlama buyrukları (if-else, döngüler), altyordamlar (fonksiyon çağrısı) ve yığıtlar
**Karakterler:** Bilge (8 yaşında, kıvırcık kahverengi saçlı, yuvarlak gözlüklü kız), Yonga (küçük yuvarlak mavi-gümüş robot)

---

## Sayfa 1 — Kavşakta Dur

**Metin:**
Bilge ve Yonga parkta yürürken bir kavşağa geldiler.

{B}"Sola dönersek göl, sağa dönersek kafe." dedi Bilge.
{B}"Hangisine gitsek?"

Yonga güldü: {Y}"Bu tam bir **dallanma** işlemi!
Bilgisayarlar da her an böyle seçimler yapar.
'Koşul doğruysa sol yola git, yanlışsa sağa.'"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A sunny park path splits into two directions. Left path leads to a shimmering lake, right path leads to a cozy café. Bilge stands at the fork looking left and right, deciding. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — stands at the split with a tiny signpost showing two arrows. ONLY ONE ROBOT IN THE SCENE. Warm outdoor watercolor, bright greens and blues.

---

## Sayfa 2 — Eğer… O Zaman…

**Metin:**
{Y}"Programlarda bu seçime **if-else** denir." dedi Yonga.

{Y}"'Eğer hava yağmurluysa, şemsiye al.
Değilse, güneş gözlüğü tak.'"

{B}"Bilgisayar bunu nasıl anlar?" diye sordu Bilge.

{Y}"**BEQ** buyruğuyla: eşitse dallan (İngilizcesi 'Branch if Equal').
**BNE** buyruğuyla: eşit değilse dallan (İngilizcesi 'Branch if Not Equal').
**BLT** buyruğuyla: küçükse dallan (İngilizcesi 'Branch if Less Than')."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A split decision scene at the top of the page: a rainy cloud leads to umbrella path, a sunny sky leads to sunglasses path. Below, the same scene is shown as a processor making a BEQ decision — two register values compared, one path highlighted. Bilge holds an umbrella on one path, sunglasses on the other. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — stands at the comparison point. ONLY ONE ROBOT IN THE SCENE. Split-path illustration, cheerful colors.

---

## Sayfa 3 — Dallanma Buyruğu Nasıl Çalışır?

**Metin:**
{Y}"BEQ x5, x6, 20." dedi Yonga.

{Y}"Bu şu anlama gelir:
Eğer x5 ve x6 **eşitse**, Program Sayacını 20 adres ileri götür.
Eşit **değilse**, bir sonraki buyruğa geç, hiç atlamadan devam et."

{B}"Demek atlama olmadığında ek bir işlem yapılmıyor." dedi Bilge.

{Y}"Evet! Zaten bir sonraki buyruğa devam etmek varsayılandır."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A vertical list of instruction boxes (representing program memory). An arrow from a BEQ instruction shows two possibilities: if equal, a curved arrow jumps 20 boxes forward; if not equal, the arrow just moves to the next box. The comparison (x5 vs x6) is shown as a balance scale. Bilge sketches this on paper. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — demonstrates with the arrow. ONLY ONE ROBOT IN THE SCENE. Instructional illustration, clear blues.

---

## Sayfa 4 — Tekrar Tekrar

**Metin:**
{B}"Döngüler ne?" diye sordu Bilge.

{Y}"Döngü, birkaç adımı belirli sayıda ya da bir koşul bozulana kadar tekrarlamak demek." dedi Yonga.

{Y}"'10 kez zıpla' demek gibi.
Nasıl mı? Dallanma buyruğuyla!
Her turda sayacı bir artır. Sayaç 10'a ulaşınca koşul bozulur ve döngü durur."

{B}"Döngü, geriye doğru bir atlama!" dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cartoon frog jumps on numbered lily pads (1 through 10). A curved arrow goes from lily pad 10 back toward lily pad 1, but with a stop sign at "10" showing the loop ends. Beside the scene, a simple loop diagram shows: counter=0, jump back if counter < 10, counter++. Bilge counts on her fingers. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — sits on lily pad 5, mid-jump. ONLY ONE ROBOT IN THE SCENE. Fun lily pad colors, cheerful greens and blues.

---

## Sayfa 5 — JAL ile Atlamak

**Metin:**
{Y}"Koşulsuz atlama da var." dedi Yonga.
{Y}"**JAL**: 'Jump And Link', atla ve bağlantıyı kaydet.

'Şu adrese git' der, koşul yok, doğrudan gider.
Ama 'bağlantı kaydet' kısmı çok önemli:
Geri dönmek için nereden geldiğini hatırlıyor!"

{B}"Hansel ile Gretel gibi." dedi Bilge. {B}"Orman yoluna taşlar bıraktılar!"

{Y}"Aynen öyle! JAL de dönüş adresini ra (x1) yazmacına bırakır."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A fairy-tale forest path illustration. A small character (representing JAL instruction) walks down the forest path, dropping glowing pebbles behind (representing the return address saved in ra register). At the end of the path is a function (shown as a small house). An arrow shows the character going in, then following the pebbles back out. Bilge watches from outside the forest. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — drops a glowing pebble. ONLY ONE ROBOT IN THE SCENE. Fairy-tale forest colors, magical greens and golds.

---

## Sayfa 6 — Altyordam Çağırmak

**Metin:**
{Y}"Programlarda aynı işi tekrar tekrar yazmak yerine, o işi bir kez yazarsın ve defalarca çağırırsın.
Buna **altyordam** ya da **fonksiyon** denir." dedi Yonga.

{B}"Tarif defteri gibi!" dedi Bilge.
{B}"'Pasta yap' tarifini bir kez yazarsın,
sonra 'pasta yap' dersin: tarife bakarsın, yaparsın, geri dönersin."

{Y}"Harika benzetme! Çağırma → gitme → yapma → geri dönme."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A recipe book scene. A cook (main program) stands in a kitchen, calls out "Make cake!" — a dotted arrow leads to the recipe page (subroutine/function). The recipe is shown as a small cozy booklet. After following the recipe, an arrow returns the cook back to the kitchen with a finished cake. Bilge acts as the cook, Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — is the recipe booklet helper. ONLY ONE ROBOT IN THE SCENE. Warm kitchen colors.

---

## Sayfa 7 — Gitmek Kolay, Dönmek Zor

**Metin:**
{B}"Bir fonksiyon çağırıyorum." dedi Bilge.
{B}"Fonksiyon başka bir fonksiyon çağırıyor.
O da başka bir fonksiyon çağırıyor.
Sonunda nasıl geri döneceğimi bilebilir miyim?"

{Y}"İşte yığıt tam burada devreye giriyor!" dedi Yonga.
{Y}"JAL dönüş adresini önce **ra** yazmacına yazar.
Fonksiyon başka bir fonksiyon çağıracaksa **ra**'daki adresi yığıta koyar.
Geri dönerken yığıttan alır.
Kim son koyduysa birinci çıkar!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A series of nested function calls illustrated as Russian nesting dolls (matryoshka). The outermost doll calls a second, which calls a third. Return addresses are shown as folded notes stacked on a pile (the stack). When opening from inside out, each note is read in reverse order. Bilge holds the outermost doll looking amazed. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — manages the stack of notes. ONLY ONE ROBOT IN THE SCENE. Colorful matryoshka doll illustration.

---

## Sayfa 8 — Yığıta Koy, Yığıttan Al

**Metin:**
{Y}"Fonksiyon çağrılırken şunlar yığıta konur." dedi Yonga:

{Y}"1. Dönüş adresi (nereden gelindi)
2. Kullanılan yazmaçların değerleri (ezilmesin diye)
3. Fonksiyonun yerel değişkenleri"

{B}"Ve geri dönerken?" diye sordu Bilge.

{Y}"Tam tersi sırayla yığıttan çıkarılır:
yazmaçlar eski değerlerine döner, yürütme kaldığı yerden devam eder."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cartoon stack (pile of plates scene). KOY (push) onto stack: labeled plates added on top — "return address", "saved x5", "saved x6", "local var". AL (pop) from stack: plates removed top-to-bottom in reverse order. sp arrow moves down when pushing (KOY), up when popping (AL). Bilge stacks the plates carefully. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — pops them back off and hands them to Bilge. ONLY ONE ROBOT IN THE SCENE. Cafeteria stack colors.

---

## Sayfa 9 — Çerçeve İşaretçisi

**Metin:**
{Y}"Her fonksiyon çağrısı için yığıtta bir **çerçeve** oluşur." dedi Yonga.
{Y}"Çerçeve o fonksiyonun kendi odası gibidir:
dönüş adresi, kayıtlı yazmaçlar, yerel değişkenler hepsi orada."

{Y}"**fp** (çerçeve işaretçisi) o odanın kapısını gösterir." dedi Yonga.
{Y}"**sp** ise kulenin en üstünü gösterir: en son konulan neredeyse orası."

{B}"Bir apartman gibi." dedi Bilge. {B}"Her fonksiyon kendi dairesinde."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cartoon apartment building cross-section. Each floor is a stack frame belonging to a different function call. The top floor (most recent function) is labeled "current frame." An fp arrow points to the bottom of the current floor (frame base), an sp arrow points to the very top where new items are being added. Bilge stands outside the building looking at the floors. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — stands on the roof (sp position). ONLY ONE ROBOT IN THE SCENE. Apartment building cross-section, warm brick tones.

---

## Sayfa 10 — JALR ile Yazmaçtan Atlamak

**Metin:**
{Y}"JAL'ın bir kardeşi var: **JALR**." dedi Yonga.
{Y}"JAL doğrudan bir adrese atlar.
JALR ise bir yazmaçtaki adrese atlar.

Bu çok güçlüdür!
Çünkü hangi fonksiyonu çağıracağını önceden bilmesen de olur:
sadece adresi yazmaca koyarsın, JALR oraya gider."

{B}"Telefon rehberi gibi." dedi Bilge.
{B}"Numarayı önceden bilmiyorsun, rehbere bakıyorsun, arıyorsun."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A cartoon phone book scene. Character holds a phone book (register with stored address) and dials whatever number is on the open page. Compare: JAL is shown as dialing a hardcoded number, JALR is shown as looking up a number first then dialing. Both make a call (jump) but in different ways. Bilge holds the phone book. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — dials the phone. ONLY ONE ROBOT IN THE SCENE. Retro telephone colors.

---

## Sayfa 11 — Bütün Bunlar Bir if-else İçin

**Metin:**
Bilge durup düşündü: {B}"Bir if-else cümlesi yazdığımda
aslında arka planda ne kadar çok işlem yapılıyor!"

{Y}"Yazdığımız programı işlemcinin diline çeviren bir araç var: **derleyici**." dedi Yonga. {Y}"Derleyici senin if-else'ini karşılaştırma buyruğuna ve dallanma buyruğuna çevirir. Koşul tutmuyorsa BEQ ya da BNE ile öteki dala atlar. Tüm mantık sıfır ve birlerle!"

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Left side: a simple if-else written in colorful block code style ("if score > 10: celebrate, else: try again"). Right side: the same logic translated into assembly instructions with BLT/JAL instructions shown as colorful boxes. A translation arrow connects left to right. Bilge writes on the left, Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — writes the translation on the right. ONLY ONE ROBOT IN THE SCENE. Code translation visual, clean bright colors.

---

## Sayfa 12 — Döngüler de Aynı Şekilde

**Metin:**
{B}"Bir for döngüsü yazdığımda da aynı mı?" diye sordu Bilge.

{Y}"Evet! Derleyici şuna çevirir:
1. Sayacı sıfırla: x5 = 0
2. Döngü başı: x5 < 10 mı? Değilse döngü sonundaki buyruğa atla.
3. Döngü gövdesini yürüt.
4. Sayacı artır: x5 = x5 + 1
5. Döngü başına geri atla (JAL ya da geriye dallanma)."

{B}"Vay be! Her döngü aslında bir geri atlama." dedi Bilge.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. A circular racetrack with 10 segments. A cartoon runner starts at segment 0, runs each segment, and a scoreboard shows "lap count: x5." At segment 10, a finish line and exit gate appear. A backward curved arrow shows the loop — the runner returns to segment start each lap until x5 reaches 10. Bilge stands at the finish line timer. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — holds a lap counter. ONLY ONE ROBOT IN THE SCENE. Racing track illustration, dynamic colors.

---

## Sayfa 13 — Bir Günlük Macera

**Metin:**
O akşam Bilge'nin annesi ona "Odanı topla" dediğinde gülümsedi.

{B}"Bu bir fonksiyon çağrısı." diye düşündü.
{B}"Ana program (annem) alt programa (ben) çağrı yaptı.
Ben işimi bitirince geri dönüp rapor vereceğim."

{B}"Bitti!" diyerek mutfağa koştu.

Annesinin yüzündeki gülümseme bir dönüş değeri gibiydi.

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Home scene: Mom stands in the hallway calling toward Bilge's room (function call illustrated with a speech bubble showing "Clean your room!"). Bilge happily tidies her room (subroutine executing). Then Bilge runs back to the kitchen and reports "Done!" to Mom who smiles (return value). The scene is warm and domestic. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — peeks from Bilge's doorway watching. ONLY ONE ROBOT IN THE SCENE. Warm home colors.

---

## Sayfa 14 — Bilgisayar Gibi Düşünmek

**Metin:**
Bilge yatarken düşündü:

{B}"Dallan, atla, geri dön.
Koşul doğruysa bir yol, yanlışsa başka yol.
Tekrar et, dur, devam et.

Belki de ben de her gün böyle çalışıyorum:
kararlar veriyorum, görevleri tamamlıyorum, sonuçları bildiriyorum.

Bilgisayar benden o kadar da farklı değil."

**Resim:**
Horizontal children's book illustration, watercolor style, edge-to-edge, NO white border, NO frame. Bilge lies in bed daydreaming. In her dream bubble above her head: a simplified flowchart of her day — wake up (start), breakfast (if hungry: eat, else skip), school (loop: attend each class), homework (subroutine: do tasks, return done), sleep (end). The flowchart is colorful and child-friendly. Yonga — a small chubby rounded robot, light blue-silver metallic body, spiral/swirl on belly, big round blue eyes, dome head, short stubby arms, NO TEXT on body, NO antenna — floats in the dream bubble drawing the flowchart. ONLY ONE ROBOT IN THE SCENE. Dreamy purples and blues.

---

## Bugün Ne Öğrendik?


🔀 **Dallanma:** Bir koşul doğruysa (ya da yanlışsa) farklı bir buyruğa atlamak. BEQ, BNE, BLT gibi buyruklar kullanılır.

🔁 **Döngü:** Bir işlemi belirli kez ya da koşul bozulana kadar tekrarlamak, geriye doğru dallanmayla gerçekleşir.

🦘 **JAL:** Koşulsuz atlama. Dönüş adresini ra yazmacına kaydeder.

📇 **JALR:** Yazmaçtaki adrese atlama. Hangi fonksiyona gidileceği önceden bilinmese de olur.

📋 **Altyordam (fonksiyon):** Defalarca çağrılabilen, iş bitince geri dönen kod bloğu.

🗂️ **Yığıt çerçevesi:** Her fonksiyon çağrısı için yığıtta ayrılan alan: dönüş adresi, kayıtlı yazmaçlar, yerel değişkenler burada.

📌 **sp (yığıt işaretçisi):** Yığıtın en üstünü gösterir.

🔙 **ra (dönüş adresi yazmacı):** Fonksiyonun geri döneceği adresi saklar.

---

## Deneme Zamanı

1. Bir koşul doğruysa başka bir buyruğa atlamaya ne denir?

2. Döngü hangi yöne dallanmayla olur?

3. JAL dönüş adresini nereye yazar?

4. Her fonksiyon çağrısı için yığıtta ayrılan alanın adı nedir?

**Yanıtlar**

1. Dallanma.
2. Geriye doğru.
3. ra yazmacına.
4. Yığıt çerçevesi.
