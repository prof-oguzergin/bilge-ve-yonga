/* Bilge ve Yonga — hizmet çalışanı (service worker)
 *
 * Amaç: siteyi telefonun ana ekranına eklenebilir kılmak ve okunan
 * kitapların çevrimdışı açılmasını sağlamak. Uygulama mağazası yok,
 * hesap yok, ölçüm yok.
 *
 * Bu dosya build_web.py tarafından __SURUM__ damgası değiştirilerek
 * sw.js olarak yazılır. Sürüm değişince eski önbellekler silinir.
 */
const SURUM = '__SURUM__';
const KABUK = 'bvy-kabuk-' + SURUM;   // sayfalar ve simgeler
const ICERIK = 'bvy-icerik-' + SURUM; // okunan kitapların görselleri

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
  e.waitUntil(
    caches.open(KABUK)
      .then((c) => c.addAll(KABUK_DOSYALARI))
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

self.addEventListener('fetch', (e) => {
  const istek = e.request;
  if (istek.method !== 'GET') return;

  const url = new URL(istek.url);
  if (url.origin !== self.location.origin) return;

  /* PDF ve EPUB indirilen dosyalardır, önbelleğe alınmaz. */
  if (/\.(pdf|epub)$/i.test(url.pathname)) return;

  /* Sayfalar: önce ağ, olmazsa önbellek. Böylece güncelleme hemen görünür,
   * çevrimdışıyken de sayfa açılır. */
  if (istek.mode === 'navigate') {
    e.respondWith(
      fetch(istek)
        .then((y) => {
          const kopya = y.clone();
          caches.open(KABUK).then((c) => c.put(istek, kopya));
          return y;
        })
        .catch(() => caches.match(istek).then((y) => y || caches.match('./index.html')))
    );
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
