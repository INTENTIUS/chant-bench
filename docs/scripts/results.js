// Picking a tool scrolls its panels into view.
//
// The board and the panels are one control: the radios drive which panel set is
// shown, entirely in CSS. But a <label> cannot navigate, so on a short viewport
// you could click a row and see nothing move — the thing that changed was below
// the fold. This is the only behaviour on the page that needs script, and
// without it the page still works, it just does not follow you down.
document.addEventListener("DOMContentLoaded", function () {
  var panels = document.querySelector(".cb-panelsets");
  if (!panels) return;
  document.querySelectorAll(".cb-pick").forEach(function (input) {
    input.addEventListener("change", function () {
      // Only when the panels are not already on screen: scrolling a reader back
      // to something they can see is worse than not scrolling at all.
      var top = panels.getBoundingClientRect().top;
      if (top < 0 || top > window.innerHeight * 0.6) {
        panels.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
});
