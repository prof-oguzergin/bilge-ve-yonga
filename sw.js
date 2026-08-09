/* Bilge ve Yonga — hizmet çalışanı (service worker)
 *
 * Amaç: siteyi telefonun ana ekranına eklenebilir kılmak ve okunan
 * kitapların çevrimdışı açılmasını sağlamak. Uygulama mağazası yok,
 * hesap yok, ölçüm yok.
 *
 * Bu dosya build_web.py tarafından 1e24f3b6d1 damgası değiştirilerek
 * sw.js olarak yazılır. Sürüm değişince eski önbellekler silinir.
 */
const SURUM = '1e24f3b6d1';
const KABUK = 'bvy-kabuk-' + SURUM;   // sayfalar ve simgeler
const ICERIK = 'bvy-icerik-' + SURUM; // okunan kitapların görselleri

/* Sayfalar önbellekten açılır; sunucuya ancak bu süre geçtiyse sorulur.
 * Her açılışta sunucuya bağlanmamak hem hızlı hem de okurun izini
 * azaltıyor. Bir gün, düzeltmelerin okura geç kalmaması için üst sınır. */
const TAZELEME_ARALIGI = 24 * 60 * 60 * 1000;
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
async function tazelemeVaktiGeldiMi() {
  const c = await caches.open(KABUK);
  const d = await c.match(DAMGA_ANAHTARI);
  if (!d) return true;
  const son = Number(await d.text());
  return !son || (Date.now() - son) > TAZELEME_ARALIGI;
}

async function damgaVur() {
  const c = await caches.open(KABUK);
  await c.put(DAMGA_ANAHTARI, new Response(String(Date.now())));
}

async function sayfaVer(istek) {
  const c = await caches.open(KABUK);
  const saklanan = await c.match(istek);

  if (saklanan) {
    /* Süresi dolduysa arka planda tazele; okur beklemez. */
    if (await tazelemeVaktiGeldiMi()) {
      damgaVur();
      fetch(istek).then((y) => {
        if (y && y.status === 200) c.put(istek, y.clone());
      }).catch(() => {});
    }
    return saklanan;
  }

  /* Önbellekte yoksa ağdan al, sakla. Çevrimdışıysa ana sayfaya düş. */
  try {
    const y = await fetch(istek);
    if (y && y.status === 200) c.put(istek, y.clone());
    damgaVur();
    return y;
  } catch (hata) {
    return (await c.match('./index.html')) || Response.error();
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
