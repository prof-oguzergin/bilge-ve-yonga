/* Bilge ve Yonga — hizmet çalışanı (service worker)
 *
 * Amaç: siteyi telefonun ana ekranına eklenebilir kılmak ve okunan
 * kitapların çevrimdışı açılmasını sağlamak. Uygulama mağazası yok,
 * hesap yok, ölçüm yok.
 *
 * Bu dosya build_web.py tarafından d2851786dc damgası değiştirilerek
 * sw.js olarak yazılır. Sürüm değişince eski önbellekler silinir.
 */
const SURUM = 'd2851786dc';
const KABUK = 'bvy-kabuk-' + SURUM;   // sayfalar ve simgeler
const ICERIK = 'bvy-icerik-' + SURUM; // okunan kitapların görselleri

/* Son bağlanma damgası. Sayfa artık her açılışta ağdan isteniyor, bu
 * damga yalnızca kaydı tutuyor. */
const DAMGA_ANAHTARI = '__son-tazeleme';

/* Kurulumda yalnızca kabuk saklanır. Kitap görselleri okundukça birikir;
 * 3,6 GB'lık siteyi baştan indirmek olmaz. */
const KABUK_DOSYALARI = [
  './',
  './index.html',
  './manifest.json',
  './amblem-32.png',
  './amblem-192.png',
  './amblem-512.png',
  './amblem-maskable-512.png',
];

self.addEventListener('install', (e) => {
  /* Tek tek saklanir: addAll butun listeyi atomik ister ve tek bir dosya
   * takilirsa kurulum tumden duser. Kabuk eksik kalsa bile site calisir. */
  e.waitUntil(
    caches.open(KABUK)
      .then((c) => Promise.allSettled(
        KABUK_DOSYALARI.map((u) => fetch(u, { cache: 'reload' })
          .then((y) => (y && y.status === 200) ? c.put(u, y) : null))
      ))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((adlar) => Promise.all(
        adlar.filter((a) => a !== KABUK && a !== ICERIK).map((a) => caches.delete(a))
      ))
      .then(() => self.clients.claim())
  );
});

/* Son tazeleme damgası önbellekte küçük bir yanıt olarak durur;
 * hizmet çalışanının localStorage'ı yoktur. */
async function damgaVur() {
  const c = await caches.open(KABUK);
  await c.put(DAMGA_ANAHTARI, new Response(String(Date.now())));
}

/* Sayfa: önce ağ, kısa süre bekler, tutmazsa önbellek.
 *
 * Önce önbellek veriliyordu ve sunucuya günde bir kez soruluyordu; bir
 * metin düzeltmesi okura bir gün gecikmeyle ulaşıyordu (9 Ağu 2026'da
 * 1.02b'nin cümle düzeltmeleri böyle görünmedi). Sayfalar küçük, ağ
 * açıkken beklemek göze batmıyor; çevrimdışı okuma da bozulmuyor,
 * çünkü ağ yanıt vermezse önbellekteki kopya veriliyor.
 * Görseller ve PDF'ler bu kuralın dışında; onlar hâlâ önbellekten. */
const AG_BEKLEME = 2500;

async function sayfaVer(istek) {
  const c = await caches.open(KABUK);

  try {
    const y = await Promise.race([
      fetch(istek),
      new Promise((_, red) => setTimeout(() => red(new Error('yavaş')), AG_BEKLEME)),
    ]);
    if (y && y.status === 200) c.put(istek, y.clone());
    damgaVur();
    return y;
  } catch (hata) {
    const saklanan = await c.match(istek);
    return saklanan || (await c.match('./index.html')) || Response.error();
  }
}

self.addEventListener('fetch', (e) => {
  const istek = e.request;
  if (istek.method !== 'GET') return;

  const url = new URL(istek.url);
  if (url.origin !== self.location.origin) return;

  /* PDF ve EPUB indirilen dosyalardır, önbelleğe alınmaz. */
  if (/\.(pdf|epub)$/i.test(url.pathname)) return;

  if (istek.mode === 'navigate') {
    e.respondWith(sayfaVer(istek));
    return;
  }

  /* Görseller ve küçük dosyalar: önce önbellek, yoksa ağdan alıp sakla. */
  e.respondWith(
    caches.match(istek).then((bulunan) => bulunan || fetch(istek).then((y) => {
      if (y && y.status === 200 && y.type === 'basic') {
        const kopya = y.clone();
        const hedef = istek.destination === 'image' ? ICERIK : KABUK;
        caches.open(hedef).then((c) => c.put(istek, kopya));
      }
      return y;
    }).catch(() => bulunan))
  );
});
