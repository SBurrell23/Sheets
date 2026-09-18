window.PS = window.PS || {};
(function (PS) {
  "use strict";
  // Inline rather than files: index.html has to work from file://, where an
  // <img src> to a sibling folder is fine but a fetch is not -- and drawing in
  // currentColor means the art follows the theme for free.
  var ART = {
    "all-songs":
      '<path d="M4 5.5h10M4 10h10M4 14.5h6"/>' +
      '<circle cx="15.8" cy="18" r="2.6"/><path d="M18.4 18V7.4l3.2 1.2"/>',
    "folk-songs":
      '<path d="M12 21c-3 0-5.2-2-5.2-4.6 0-1.9 1.2-3 1.2-4.4S6.8 9.5 6.8 7.6C6.8 5 9 3.2 12 3.2' +
      's5.2 1.8 5.2 4.4c0 1.9-1.2 3-1.2 4.4s1.2 2.5 1.2 4.4C17.2 19 15 21 12 21z"/>' +
      '<circle cx="12" cy="13.4" r="1.7"/><path d="M12 3.2V1.6"/>',
    "classical":
      '<path d="M3.6 20.4h16.8M4.8 4.2h14.4M6 6.4h12"/>' +
      '<path d="M7.4 6.4v12M10 6.4v12M12.6 6.4v12M15.2 6.4v12M17.8 6.4v12"/>',
    "ragtime":
      '<rect x="2.6" y="5.4" width="18.8" height="13.2" rx="1.6"/>' +
      '<path d="M9 5.4v13.2M15 5.4v13.2"/>' +
      '<rect x="6.7" y="5.4" width="2.5" height="7.6" rx=".5" fill="currentColor" stroke="none"/>' +
      '<rect x="12.7" y="5.4" width="2.5" height="7.6" rx=".5" fill="currentColor" stroke="none"/>' +
      '<rect x="17.4" y="5.4" width="2.5" height="7.6" rx=".5" fill="currentColor" stroke="none"/>',
    "ai-music":
      '<path d="M8.6 2.4l1.3 3.6 3.6 1.3-3.6 1.3-1.3 3.6-1.3-3.6L3.7 7.3l3.6-1.3z"/>' +
      '<circle cx="13.6" cy="18.3" r="2.4"/><path d="M16 18.3v-7.1l3.8 1.4"/>'
  };
  var ART_FALLBACK =
    '<circle cx="8.5" cy="17.5" r="3"/><path d="M11.5 17.5V4.5l7 2.4"/>';

  PS.artFor = function (cid) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" ' +
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
           (ART[cid] || ART_FALLBACK) + '</svg>';
  };
})(window.PS);
