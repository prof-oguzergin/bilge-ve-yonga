/* ==========================================================================
   olcum-tercihi.js — Bilge ve Yonga ölçüm (analitik) tercihi bildirimi
   --------------------------------------------------------------------------
   NE YAPAR
     · GoatCounter betiğini SAYFAYA HİÇ YÜKLEMEZ; ziyaretçi açıkça izin
       verene kadar hiçbir istek gönderilmez.
     · Sayfanın altında ince bir şerit olarak bir tercih bildirimi gösterir.
       Modal değildir, içeriği engellemez, okumayı durdurmaz.
     · Tercihi localStorage'da 'analytics-consent' anahtarıyla saklar
       ("on" / "off"). Sürüm 'analytics-consent-version' anahtarında tutulur.
     · Her sayfadaki "Ölçüm tercihi" bağlantısı bildirimi yeniden açar
       (data-bvy-olcum özniteliği taşıyan herhangi bir bağlantı).
     · Ölçüm kapatıldığında o oturumda başka istek gönderilmez.

   KURULUM
     1. index.html ve okuyucu/*.html içindeki şu iki satır KALDIRILIR:
          <script data-goatcounter="…" async src="//gc.zgo.at/count.js"></script>
          <script>document.addEventListener('click', … goatcounter.count …)</script>
     2. Yerine </body> etiketinden hemen önce şu satır eklenir:
          <script src="/olcum-tercihi.js" defer></script>
        (okuyucu sayfalarında: <script src="../olcum-tercihi.js" defer></script>)

   Dayanak: 05-kvkk-aydinlatma-ve-cerez-politikasi.md, Ek E.2 ve E.3.
   © 2026 Prof. Dr. Oğuz Ergin · CC BY-NC-ND 4.0
   ========================================================================== */
(function () {
  'use strict';

  var ANAHTAR = 'analytics-consent';
  var SURUM_ANAHTARI = 'analytics-consent-version';
  var SURUM = '1';                       /* esaslı değişiklikte artırın */
  var SAYAC = 'https://bilgeveyonga.goatcounter.com/count';
  var BETIK = 'https://gc.zgo.at/count.js';

  var altKlasorde = /\/okuyucu\//.test(location.pathname);
  var GIZLILIK = (altKlasorde ? '../' : '') + 'gizlilik.html';

  var yuklendi = false;

  /* ---------------------------------------------------------------- depo */
  function oku(a) { try { return localStorage.getItem(a); } catch (e) { return null; } }
  function yaz(a, d) { try { localStorage.setItem(a, d); } catch (e) { /* yoksay */ } }

  function tercih() {
    if (oku(SURUM_ANAHTARI) !== SURUM) { return null; }   /* sürüm değişti */
    var d = oku(ANAHTAR);
    return (d === 'on' || d === 'off') ? d : null;
  }

  /* ------------------------------------------------------------- ölçüm */
  function olcumuBaslat() {
    if (yuklendi) { return; }
    yuklendi = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = BETIK;
    s.setAttribute('data-goatcounter', SAYAC);
    document.body.appendChild(s);

    document.addEventListener('click', function (e) {
      if (tercih() !== 'on') { return; }
      var a = e.target.closest ? e.target.closest('a[href$=".pdf"],a[href$=".epub"]') : null;
      if (!a) { return; }
      var h = a.getAttribute('href') || '';
      var pdf = /\.pdf$/i.test(h);
      var m = h.match(/kitap[0-9.]+[ab]?-[a-z0-9-]+/i);
      var b = m ? m[0] : 'bilinmeyen';
      if (window.goatcounter && window.goatcounter.count) {
        window.goatcounter.count({
          path: (pdf ? 'indir-pdf/' : 'indir-epub/') + b,
          title: (pdf ? 'PDF indir: ' : 'EPUB indir: ') + b,
          event: true
        });
      }
    });
  }

  function olcumuDurdur() {
    /* Betik yüklenmişse sayma işlevini anında etkisiz kılar. */
    if (window.goatcounter) { window.goatcounter.count = function () {}; }
    window.goatcounter = window.goatcounter || {};
    window.goatcounter.no_onload = true;
  }

  /* -------------------------------------------------------------- stil */
  function stilEkle() {
    if (document.getElementById('bvy-olcum-stil')) { return; }
    var s = document.createElement('style');
    s.id = 'bvy-olcum-stil';
    s.textContent = [
      '#bvy-olcum{position:fixed;left:0;right:0;bottom:0;z-index:9999;',
      '  background:var(--surface,#182348);color:var(--text,#F2EBD9);',
      '  border-top:2px solid var(--glow,#33C6E6);',
      '  box-shadow:0 -12px 40px -20px rgba(0,0,0,.6);',
      '  font-family:var(--font-body,"Segoe UI",system-ui,sans-serif);',
      '  font-size:15px;line-height:1.5;padding:14px clamp(16px,3vw,32px)}',
      '#bvy-olcum .bvy-ic{max-width:900px;margin:0 auto;display:flex;',
      '  flex-wrap:wrap;gap:14px 24px;align-items:center;',
      '  justify-content:space-between}',
      /* Metin taşarsa YALNIZCA metin kayar; iki düğme her zaman görünür kalır. */
      '#bvy-olcum .bvy-metin{flex:1 1 360px;min-width:0;max-width:62ch;max-height:38vh;',
      '  overflow-y:auto;overscroll-behavior:contain}',
      '#bvy-olcum h2{margin:0 0 4px;font-size:1rem;font-weight:800;',
      '  font-family:var(--font-display,inherit);line-height:1.25}',
      '#bvy-olcum p{margin:0 0 3px}',
      '#bvy-olcum .bvy-kucuk{font-size:.86em;opacity:.82}',
      '#bvy-olcum a{color:var(--glow,#33C6E6)}',
      /* İki düğme HER ZAMAN eşit genişliktedir: kap sabit, düğmeler flex:1 1 0 */
      '#bvy-olcum .bvy-dugmeler{flex:0 0 auto;display:flex;gap:12px;',
      '  flex-wrap:nowrap;width:340px;max-width:100%}',
      '#bvy-olcum button{font:inherit;font-weight:700;cursor:pointer;',
      '  border-radius:999px;background:transparent;',
      '  color:var(--text,#F2EBD9);transition:.16s}',
      '#bvy-olcum button[data-secim]{flex:1 1 0;min-width:0;padding:11px 14px;',
      '  border:2px solid var(--glow,#33C6E6);text-align:center}',
      '#bvy-olcum button:hover{background:var(--glow,#33C6E6);color:#08111f}',
      '#bvy-olcum button:focus-visible{outline:3px solid var(--amber,#F3AC2E);',
      '  outline-offset:3px}',
      '#bvy-olcum .bvy-kapat{position:absolute;right:10px;top:8px;',
      '  padding:4px 10px;border:0;font-size:1.1rem;opacity:.7;',
      '  background:transparent;color:inherit}',
      '#bvy-olcum .bvy-kapat:hover{opacity:1;background:transparent;',
      '  color:var(--glow,#33C6E6)}',
      '@media (max-width:640px){#bvy-olcum .bvy-dugmeler{width:100%}',
      '  #bvy-olcum .bvy-metin{max-height:30vh}',
      '  #bvy-olcum{padding:14px 16px 16px}}'
      /* Bilinçli olarak giriş animasyonu YOK: animasyonun duraklatıldığı
         durumlarda (arka plan sekmesi, azaltılmış hareket, bazı gömülü
         tarayıcılar) şerit ekran dışında takılı kalabilir ve reddetme
         seçeneği görünmez olurdu. Bildirim her koşulda ilk karede görünür. */
    ].join('');
    document.head.appendChild(s);
  }

  /* --------------------------------------------------------- bildirim */
  function bildirimGoster() {
    if (document.getElementById('bvy-olcum')) { return; }
    stilEkle();

    var d = document.createElement('div');
    d.id = 'bvy-olcum';
    d.setAttribute('role', 'region');
    d.setAttribute('aria-label', 'Ölçüm tercihi');
    d.style.position = 'fixed';
    d.innerHTML = [
      '<button class="bvy-kapat" type="button" aria-label="Bildirimi kapat">×</button>',
      '<div class="bvy-ic">',
      '  <div class="bvy-metin">',
      '    <h2>Bu sitede çerez yok</h2>',
      '    <p>Tarayıcınıza çerez yerleştirmiyoruz, sizden hiçbir bilgi istemiyoruz. ',
      '    Yalnızca <strong>hangi kitapların okunduğunu sayan</strong> bir ölçüm var; ',
      '    kim olduğunuzu kaydetmez, reklam göstermez, sizi izlemez. ',
      '    <strong>Şu anda kapalı.</strong></p>',
      '    <p class="bvy-kucuk">Açarsanız ziyaret bilgisi Finlandiya ya da ',
      '    Almanya\'daki bir sunucuya gider. Seçiminiz ne olursa olsun bütün ',
      '    kitaplar açık. <a href="' + GIZLILIK + '">Ayrıntılar</a></p>',
      '  </div>',
      '  <div class="bvy-dugmeler">',
      '    <button type="button" data-secim="off">Kapalı kalsın</button>',
      '    <button type="button" data-secim="on">Ölçüme izin ver</button>',
      '  </div>',
      '</div>'
    ].join('');
    document.body.appendChild(d);

    d.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('button') : null;
      if (!b) { return; }
      if (b.classList.contains('bvy-kapat')) {
        /* Sessizlik onay değildir: kapatmak ölçümü AÇMAZ ve tercihi KAYDETMEZ. */
        d.remove();
        return;
      }
      var secim = b.getAttribute('data-secim');
      if (secim !== 'on' && secim !== 'off') { return; }
      yaz(ANAHTAR, secim);
      yaz(SURUM_ANAHTARI, SURUM);
      d.remove();
      if (secim === 'on') { olcumuBaslat(); } else { olcumuDurdur(); }
    });

    var ilk = d.querySelector('button[data-secim="off"]');
    if (ilk) { ilk.focus({ preventScroll: true }); }
  }

  /* ---------------------------------------------------------- başlangıç */
  function baslat() {
    var t = tercih();
    if (t === 'on') {
      olcumuBaslat();
    } else if (t === 'off') {
      olcumuDurdur();
    } else {
      bildirimGoster();                 /* varsayılan: KAPALI */
    }

    /* Altbilgideki "Ölçüm tercihi" bağlantıları bildirimi yeniden açar. */
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('[data-bvy-olcum]') : null;
      if (!a) { return; }
      e.preventDefault();
      try { localStorage.removeItem(ANAHTAR); } catch (err) { /* yoksay */ }
      olcumuDurdur();
      bildirimGoster();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', baslat);
  } else {
    baslat();
  }
})();
