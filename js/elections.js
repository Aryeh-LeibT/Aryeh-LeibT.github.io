/* Election Tracker: reads /data/elections/<id>/*.json and draws plain SVG charts. No libraries. */
(function () {
  "use strict";
  var main = document.querySelector("[data-election]");
  var hub = document.querySelector(".el-hub");
  var he = document.documentElement.lang === "he";

  // Countdown on the hub
  if (hub) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    hub.querySelectorAll(".el-countdown").forEach(function (el) {
      var d = new Date(el.dataset.date + "T00:00:00");
      var n = Math.round((d - today) / 86400000);
      el.textContent = n > 0 ? (he ? "בעוד " + n + " ימים" : n + " days to go") : n === 0 ? (he ? "היום" : "Today") : (he ? "הסתיימו" : "Done");
    });
  }

  /* Bader-Ofer allocation. lists: [{name, votes, pair?}], returns {name: seats}. */
  function baderOfer(lists, seats) {
    seats = seats || 120;
    var total = lists.reduce(function (a, l) { return a + l.votes; }, 0);
    var passed = lists.filter(function (l) { return l.votes >= 0.0325 * total; });
    var units = {};
    passed.forEach(function (l) { var k = l.pair || l.name; (units[k] = units[k] || []).push(l); });
    function alloc(groups, n) {
      var keys = Object.keys(groups), v = {}, s = {}, V = 0;
      keys.forEach(function (k) { v[k] = groups[k]; V += v[k]; });
      var q = V / n, used = 0;
      keys.forEach(function (k) { s[k] = Math.floor(v[k] / q); used += s[k]; });
      while (used < n) {
        var best = keys.reduce(function (b, k) { return v[k] / (s[k] + 1) > v[b] / (s[b] + 1) ? k : b; });
        s[best]++; used++;
      }
      return s;
    }
    var uv = {}; Object.keys(units).forEach(function (k) { uv[k] = units[k].reduce(function (a, l) { return a + l.votes; }, 0); });
    var us = alloc(uv, seats), out = {};
    Object.keys(units).forEach(function (k) {
      if (units[k].length === 1) { out[units[k][0].name] = us[k]; return; }
      var inner = {}; units[k].forEach(function (l) { inner[l.name] = l.votes; });
      var r = alloc(inner, us[k]); Object.keys(r).forEach(function (n) { out[n] = r[n]; });
    });
    return out;
  }
  window.ElectionMath = { baderOfer: baderOfer };

  if (!main) return;
  var id = main.dataset.election, target = main.querySelector("[data-chart-target]");
  var NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }

  function bars(rows) {
    var h = rows.length * 40 + 10, s = svg("svg", { viewBox: "0 0 400 " + h, role: "img" });
    var max = Math.max.apply(null, rows.map(function (r) { return r.value; })) || 1;
    rows.forEach(function (r, i) {
      var w = (r.value / max) * 240, y = i * 40 + 5;
      var x = he ? 400 - w : 0;
      s.appendChild(svg("rect", { x: x, y: y, width: w, height: 26, fill: "var(--accent, #243f5c)" }));
      var t = svg("text", { x: he ? 400 - w - 6 : w + 6, y: y + 18, "font-size": 13, fill: "currentColor", "text-anchor": he ? "end" : "start" });
      t.textContent = r.name + " " + r.value + (r.unit || "");
      s.appendChild(t);
    });
    return s;
  }

  function hemicycle(rows, total) {
    total = total || 120;
    var s = svg("svg", { viewBox: "0 0 400 210", role: "img" }), seatsArr = [];
    rows.forEach(function (r, i) { for (var k = 0; k < r.seats; k++) seatsArr.push(r.color || ["#243f5c", "#8a6d3b", "#5b7f5b", "#9b4d4d", "#6d6d9b", "#4d8a8a"][i % 6]); });
    var ringsN = 6, idx = 0, placed = [];
    for (var ring = 0; ring < ringsN; ring++) {
      var rad = 80 + ring * 20, n = Math.round(total * rad / (6 * 130));
      for (var j = 0; j < n; j++) { var a = Math.PI * (j / Math.max(n - 1, 1)); placed.push({ a: a, r: rad }); }
    }
    placed.sort(function (p, q) { return q.a - p.a; }).slice(0, total).forEach(function (p) {
      s.appendChild(svg("circle", { cx: 200 + p.r * Math.cos(p.a) * (he ? -1 : 1), cy: 200 - p.r * Math.sin(p.a), r: 6, fill: seatsArr[idx++] || "#ddd" }));
    });
    return s;
  }

  Promise.all(["results", "seats"].map(function (f) {
    return fetch("/data/elections/" + id + "/" + f + ".json", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : { rows: [] }; });
  })).then(function (d) {
    var results = d[0].rows || [], seats = d[1].rows || [];
    if (main.dataset.chart === "hemicycle" && seats.length) target.appendChild(hemicycle(seats));
    else if (results.length) target.appendChild(bars(results));
    if (target.firstChild) target.removeAttribute("aria-hidden");
  }).catch(function () { /* the HTML table fallback stays */ });
})();
