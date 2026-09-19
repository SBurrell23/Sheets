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
    // An open hymnal: a hymn is indexed and sung from the book, and a book reads
    // at 24px where a church or a cross does not.
    "hymns":
      '<path d="M12 6.6C10.2 5.1 7.9 4.4 5 4.4c-.8 0-1.4.6-1.4 1.3v11.5c0 .8.6 1.3 1.4 1.3' +
      ' 2.9 0 5.2.7 7 2.2 1.8-1.5 4.1-2.2 7-2.2.8 0 1.4-.5 1.4-1.3V5.7c0-.7-.6-1.3-1.4-1.3' +
      '-2.9 0-5.2.7-7 2.2z"/>' +
      '<path d="M12 6.6v14.1"/>',
    // A star over a simple tree. Reads at 24px where a wreath or a bell does not.
    "christmas":
      '<path d="M12 2.2l1 2.1 2.3.34-1.65 1.6.39 2.26L12 7.43 9.96 8.5l.39-2.26L8.7 4.64l2.3-.34z"/>' +
      '<path d="M12 10.1 8.7 14.4h6.6zM12 13.9 7 19.6h10z"/>' +
      '<path d="M10.4 19.6v2.2h3.2v-2.2"/>',
    // A grand piano seen from above, keyboard at the near edge. Ragtime already
    // owns the keyboard-from-the-front, and a book or a staff would collide with
    // hymns and all-songs; the plan view is the one piano shape still free.
    "piano-miniatures":
      '<path d="M5 20.4V6.6c0-1.1.9-2 2-2h6.2C17.6 4.6 21 8.2 21 12.7c0 4.2-3.1 7.7-7.1 7.7z"/>' +
      '<path d="M5 16.8h7.3v3.6"/>' +
      '<path d="M7.4 16.8v3.6M9.8 16.8v3.6"/>',
    // Irish & Scottish had no entry and was falling through to the generic
    // quaver. A shamrock. Drawn as three plain lobes meeting at a centre
    // rather than interlocking heart curves: at 22px in a category card the
    // clever version came out an illegible knot, and three circles and a stem
    // still read as a clover at that size.
    "irish-scottish":
      '<circle cx="12" cy="6.9" r="3.3"/>' +
      '<circle cx="8.2" cy="12.2" r="3.3"/>' +
      '<circle cx="15.8" cy="12.2" r="3.3"/>' +
      '<path d="M12 12.6c.3 3.6-.7 6.2-2.9 8"/>',
    // Favorites gets the same star as the one on the score, so the header card,
    // the category card and the thing you click on the sheet are one symbol.
    "favorites":
      '<path d="M12 3.1l2.7 5.5 6.1.9-4.4 4.3 1.04 6.06L12 17l-5.44 2.86L7.6 13.8 3.2 9.5l6.1-.9z"/>',
    // A cornet from the side: mouthpiece, lead pipe, three valve stems, bell.
    // Every other instrument shape on this page is already taken -- the keyboard
    // from the front is ragtime's, the grand piano in plan is the miniatures' --
    // and a horn is what this repertoire sounds like anyway.
    "jazz-standards":
      '<path d="M2.9 11.3v4.2"/>' +
      '<path d="M2.9 13.4h10.7"/>' +
      '<path d="M13.6 9.4 20.6 6.2v14.4l-7-3.2z"/>' +
      '<path d="M6.8 13.4V9.2M9.6 13.4V9.2M12.4 13.4V9.2"/>',
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
