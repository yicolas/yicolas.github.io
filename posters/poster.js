// Scale the fixed 1800x1200 poster canvas to the width of its frame,
// and a tiny SVG line-chart helper shared by the field-report posters.
(function () {
  function fit() {
    var stage = document.querySelector('.stage');
    var inner = document.querySelector('.stage-inner');
    var poster = document.querySelector('.poster');
    if (!stage || !inner || !poster) return;
    var W = poster.offsetWidth, H = poster.offsetHeight;
    var avail = stage.clientWidth - 40;
    var s = Math.min(1, avail / W);
    poster.style.transform = 'scale(' + s + ')';
    inner.style.width = (W * s) + 'px';
    inner.style.height = (H * s) + 'px';
  }
  window.addEventListener('resize', fit);
  document.addEventListener('DOMContentLoaded', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();

var SVGNS = 'http://www.w3.org/2000/svg';
function el(tag, attrs, parent, text) {
  var n = document.createElementNS(SVGNS, tag);
  for (var k in attrs) n.setAttribute(k, attrs[k]);
  if (text != null) n.textContent = text;
  if (parent) parent.appendChild(n);
  return n;
}

// lineChart: opts = {svg, w, h, m:{t,r,b,l}, x:[min,max], y:[min,max],
//   xticks:[], yticks:[], xlabel, ylabel, ink, grid, series:[{pts, color, width, dots, r, dash}]}
// returns {sx, sy, g} so callers can add annotations in data space.
function lineChart(o) {
  var svg = o.svg, m = o.m || { t: 10, r: 10, b: 36, l: 48 };
  svg.setAttribute('viewBox', '0 0 ' + o.w + ' ' + o.h);
  svg.setAttribute('width', o.w); svg.setAttribute('height', o.h);
  var iw = o.w - m.l - m.r, ih = o.h - m.t - m.b;
  var sx = function (v) { return m.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * iw; };
  var sy = function (v) { return m.t + ih - (v - o.y[0]) / (o.y[1] - o.y[0]) * ih; };
  var ink = o.ink || '#222', grid = o.grid || 'rgba(0,0,0,.08)';
  var g = el('g', {}, svg);
  (o.yticks || []).forEach(function (t) {
    el('line', { x1: m.l, x2: m.l + iw, y1: sy(t), y2: sy(t), stroke: grid, 'stroke-width': 1 }, g);
    el('text', { x: m.l - 7, y: sy(t) + 4, 'text-anchor': 'end', 'font-size': 12, fill: ink, opacity: .7 }, g, o.yfmt ? o.yfmt(t) : t);
  });
  (o.xticks || []).forEach(function (t) {
    el('line', { x1: sx(t), x2: sx(t), y1: m.t + ih, y2: m.t + ih + 5, stroke: ink, 'stroke-width': 1 }, g);
    el('text', { x: sx(t), y: m.t + ih + 19, 'text-anchor': 'middle', 'font-size': 12, fill: ink, opacity: .7 }, g, o.xfmt ? o.xfmt(t) : t);
  });
  el('line', { x1: m.l, x2: m.l + iw, y1: m.t + ih, y2: m.t + ih, stroke: ink, 'stroke-width': 1.2 }, g);
  if (o.xlabel) el('text', { x: m.l + iw, y: o.h - 4, 'text-anchor': 'end', 'font-size': 12.5, fill: ink }, g, o.xlabel);
  if (o.ylabel) el('text', { x: m.l - 40, y: m.t - 2, 'text-anchor': 'start', 'font-size': 12.5, fill: ink }, g, o.ylabel);
  (o.series || []).forEach(function (s) {
    if (s.dots) {
      s.pts.forEach(function (p) {
        el('circle', { cx: sx(p[0]), cy: sy(p[1]), r: s.r || 3.4, fill: s.color, stroke: s.stroke || 'none', 'stroke-width': 1.2 }, g);
      });
    } else {
      var d = s.pts.map(function (p, i) { return (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join('');
      el('path', { d: d, fill: 'none', stroke: s.color, 'stroke-width': s.width || 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', 'stroke-dasharray': s.dash || 'none' }, g);
    }
  });
  return { sx: sx, sy: sy, g: g, m: m, iw: iw, ih: ih };
}

// Light smoothing for digitized curves (centred moving average).
function smooth(pts, k) {
  return pts.map(function (p, i) {
    var a = Math.max(0, i - k), b = Math.min(pts.length - 1, i + k), s = 0;
    for (var j = a; j <= b; j++) s += pts[j][1];
    return [p[0], s / (b - a + 1)];
  });
}
