/* ==========================================================================
   kunye.js — Bilge ve Yonga okuyucu sayfası künyesi
   --------------------------------------------------------------------------
   Site kökünde durur. 32 okuyucu sayfasının her biri bu dosyayı tek satırla
   çağırır:

       <script src="../kunye.js" defer></script>

   Metin burada TEK YERDE tutulur; değişirse yalnızca bu dosya güncellenir,
   32 sayfaya dokunulmaz.

   Betik, okuyucu sayfasındaki .reader kabının sonuna künye bloğunu ve
   ölçüm tercihi bağlantısını ekler. Sayfanın kendi CSS değişkenlerini
   (--chrome-soft, --edge, --accent, --ff-disp) kullandığı için hem açık hem
   karanlık temada doğru görünür.

   © 2026 Prof. Dr. Oğuz Ergin · CC BY-NC-ND 4.0
   ========================================================================== */
(function () {
  'use strict';

  if (document.getElementById('bvy-kunye')) { return; }

  /* Sayfa kökte mi, alt klasörde mi? Okuyucu sayfaları /okuyucu/ altındadır. */
  var altKlasorde = /\/okuyucu\//.test(location.pathname);
  var K = altKlasorde ? '../' : '';

  var YIL = 2026;
  var EPOSTA = 'bilgi@oguzergin.net';
  var LISANS = 'https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr';

  var stil = document.createElement('style');
  stil.textContent = [
    '#bvy-kunye{border-top:1px solid var(--edge,rgba(180,200,240,.16));',
    '  margin-top:6px;padding:20px clamp(20px,2vw,40px) 30px;',
    '  font-family:var(--ff-disp,system-ui,sans-serif);',
    '  color:var(--chrome-soft,#9AA6C6);font-size:.82rem;line-height:1.65;',
    '  text-align:center}',
    '#bvy-kunye p{margin:0 0 6px}',
    '#bvy-kunye .bvy-telif{font-weight:700;color:var(--chrome,inherit)}',
    '#bvy-kunye .bvy-sakli{opacity:.92}',
    '#bvy-kunye a{color:inherit;text-decoration:none;',
    '  border-bottom:1px solid var(--edge,rgba(180,200,240,.3));',
    '  transition:color .16s,border-color .16s}',
    '#bvy-kunye a:hover{color:var(--accent,#33C6E6);',
    '  border-color:var(--accent,#33C6E6)}',
    '#bvy-kunye a:focus-visible{outline:2px solid var(--accent,#33C6E6);',
    '  outline-offset:3px;border-radius:3px}',
    '#bvy-kunye .bvy-baglar{margin-top:10px;display:flex;flex-wrap:wrap;',
    '  gap:6px 14px;justify-content:center}',
    '#bvy-kunye .bvy-atif{margin-top:10px;font-size:.76rem;opacity:.75}',
    '@media (max-width:520px){#bvy-kunye{font-size:.78rem}}'
  ].join('');
  document.head.appendChild(stil);

  var bag = function (yol, ad) {
    return '<a href="' + K + yol + '">' + ad + '</a>';
  };

  var el = document.createElement('footer');
  el.id = 'bvy-kunye';
  el.setAttribute('role', 'contentinfo');
  el.innerHTML = [
    '<p class="bvy-telif">© ' + YIL + ' Prof. Dr. Oğuz Ergin · ',
    'Bilge ve Yonga · ',
    '<a href="' + LISANS + '" rel="license noopener" target="_blank">',
    'CC BY-NC-ND 4.0</a></p>',

    '<p class="bvy-sakli">Ad belirterek, değiştirmeden ve ticari olmayan ',
    'amaçla paylaşabilirsiniz. <strong>Lisansın kapsamadığı tüm haklar ',
    'saklıdır</strong> — “Bilge ve Yonga” seri adı, karakter adları ve ',
    'figürleri, marka ve manevi haklar ile yapay zekâ eğitimi hakları dâhil.</p>',

    '<p>Ticari kullanım izni: ',
    '<a href="mailto:' + EPOSTA + '?subject=Ticari%20kullan%C4%B1m%20izni">',
    EPOSTA + '</a></p>',

    '<div class="bvy-baglar">',
    bag('telif-ve-lisans.html', 'Telif ve Lisans'),
    bag('kullanim-kosullari.html', 'Kullanım Koşulları'),
    bag('ticari-kullanim.html', 'Ticari Kullanım'),
    bag('yapay-zeka-bildirimi.html', 'Yapay Zekâ Bildirimi'),
    bag('egitimciler.html', 'Öğretmenler için'),
    bag('gizlilik.html', 'Gizlilik ve Çerez'),
    '<a href="#" data-bvy-olcum>Ölçüm tercihi</a>',
    '</div>',

    '<p class="bvy-atif">Atıf: Ergin, O. (' + YIL + '). ',
    '<i>Bilge ve Yonga: Bilgisayar Mimarisi Çocuk Kitapları Serisi.</i> ',
    'bilgeveyonga.oguzergin.net</p>'
  ].join('');

  var kap = document.querySelector('.reader') || document.body;
  kap.appendChild(el);
})();
