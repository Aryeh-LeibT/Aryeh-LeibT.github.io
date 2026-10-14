/* Election-night state maps. Loads a local SVG (/images/maps/) and /data/elections/<id>.json.
   No libraries. A race is only shown as won when status is "called" AND called_by names a source. */
(function () {
  "use strict";
  var main = document.querySelector("[data-map]");
  if (!main) return;
  var he = document.documentElement.lang === "he";
  var id = main.dataset.map, svgUrl = main.dataset.svg;
  var T = he ? {
    leading: "מוביל/ה", called: "הוכרע", none: "אין עדיין תוצאות", reporting: "נספרו", by: "לפי", src: "מקור",
    upd: "עודכן", il: "שעון ישראל", seats: "מושבים", won: "זכו", lead: "מובילים", senate: "סנאט", senate_special: "סנאט (בחירות מיוחדות)",
    governor: "מושל", house: "בית הנבחרים", norace: "אין מרוץ השנה", other: "אחרים", D: "דמוקרטים", R: "רפובליקנים"
  } : {
    leading: "Leading", called: "Called", none: "No results yet", reporting: "reporting", by: "by", src: "Source",
    upd: "Updated", il: "Israel time", seats: "seats", won: "won", lead: "leading", senate: "Senate", senate_special: "Senate (special)",
    governor: "Governor", house: "House", norace: "No race this year", other: "Other", D: "Democrats", R: "Republicans"
  };
  function fmtTime(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    return d.toLocaleString(he ? "he-IL" : "en-GB", { timeZone: "Asia/Jerusalem", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) + " (" + T.il + ")";
  }
  function isCalled(r) { return r && r.status === "called" && !!r.called_by; }
  function partyKey(c) { return c ? String(c.party || "").replace(/[^A-Za-z0-9]/g, "") : ""; }
  function num(n) { return n == null ? "–" : Number(n).toLocaleString(he ? "he-IL" : "en-US"); }

  var tip = document.createElement("div");
  tip.className = "em-tip"; tip.setAttribute("role", "status"); tip.hidden = true;
  var data, raceKey = main.dataset.race || null;

  /* Returns {r, leader, label} for one state under the current race. */
  function view(code) {
    var s = data.states[code]; if (!s) return null;
    var r = s.races ? (s.races[raceKey] || (raceKey === "senate" ? s.races.senate_special : null)) : s;
    if (!r) return { s: s, r: null, leader: null, text: T.norace };
    var leader = null, text;
    if (raceKey === "house") {
      var t = r.tally || {}, best = null;
      ["D", "R", "other"].forEach(function (p) { var v = t[p] ? t[p].won + t[p].leading : 0; if (v > 0 && (!best || v > best.v)) best = { p: p, v: v }; });
      if (best) leader = { party: best.p === "other" ? "OTH" : best.p, name: T[best.p] };
      text = r.seats + " " + T.seats + ": " + ["D", "R", "other"].map(function (p) { return T[p] + " " + (t[p] ? t[p].won : 0) + " " + T.won + " / " + (t[p] ? t[p].leading : 0) + " " + T.lead; }).join(" · ");
    } else if (r.status === "no results" || !r.candidates || !r.candidates.length || !r.candidates[0].votes) {
      text = T.none;
    } else {
      leader = r.candidates[0];
      text = r.candidates.slice(0, 3).map(function (c) { return c.name + (c.party ? " (" + c.party + ")" : "") + " " + (c.pct != null ? c.pct.toFixed(1) + "%" : num(c.votes)); }).join(" · ");
    }
    var st = r.status === "no results" || !leader ? T.none : isCalled(r) ? T.called + " (" + T.by + " " + r.called_by + ")" : T.leading;
    if (leader && r.status !== "no results") text = (leader.name || "") + ": " + st + " · " + text;
    if (r.reporting_pct != null) text += " · " + r.reporting_pct + "% " + T.reporting;
    return { s: s, r: r, leader: r.status === "no results" ? null : leader, text: text, st: st };
  }

  function paint(svgEl) {
    svgEl.querySelectorAll("[data-st]").forEach(function (p) {
      var v = view(p.dataset.st); p.removeAttribute("class");
      p.classList.add("em-st");
      if (!v || !v.r) { p.classList.add("em-norace"); }
      else if (v.leader) { p.classList.add("em-p-" + partyKey(v.leader), isCalled(v.r) ? "em-called" : "em-leading"); }
      else p.classList.add("em-none");
      p.setAttribute("aria-label", (v ? v.s.name + ". " + v.text : p.dataset.st));
    });
  }

  function table() {
    var tb = main.querySelector("[data-map-table] tbody"); if (!tb) return;
    tb.textContent = "";
    Object.keys(data.states).sort(function (a, b) { return data.states[a].name.localeCompare(data.states[b].name); }).forEach(function (k) {
      var v = view(k); if (!v || (!v.r && raceKey)) return;
      var tr = document.createElement("tr");
      [v.s.name, v.leader ? v.leader.name + (v.leader.party && raceKey !== "house" ? " (" + v.leader.party + ")" : "") : "–", v.st || T.none,
       v.r.reporting_pct != null ? v.r.reporting_pct + "%" : "–", v.text, fmtTime(v.r.updated_at)].forEach(function (c, i) {
        var td = document.createElement(i ? "td" : "th"); if (!i) td.scope = "row"; td.textContent = c; tr.appendChild(td);
      });
      var tdS = document.createElement("td"), a = document.createElement("a");
      a.href = v.r.source_url; a.rel = "noopener"; a.textContent = v.r.source_name; tdS.appendChild(a); tr.appendChild(tdS);
      tb.appendChild(tr);
    });
  }

  function show(p, ev) {
    var v = view(p.dataset.st); if (!v) return;
    tip.textContent = v.s.name + " · " + v.text;
    tip.hidden = false;
    var box = main.querySelector(".em-map").getBoundingClientRect(), r = p.getBoundingClientRect();
    var x = ev && ev.clientX ? ev.clientX : r.left + r.width / 2, y = ev && ev.clientY ? ev.clientY : r.top;
    tip.style.left = Math.max(0, Math.min(x - box.left, box.width - 240)) + "px";
    tip.style.top = (y - box.top + 14) + "px";
  }

  function render(svgEl) {
    paint(svgEl); table();
    var u = main.querySelector("[data-map-updated]"); if (u) { u.textContent = fmtTime(data.updated_at); u.setAttribute("datetime", data.updated_at); }
  }

  Promise.all([
    fetch(svgUrl).then(function (r) { return r.text(); }),
    fetch("/data/elections/" + id + ".json", { cache: "no-cache" }).then(function (r) { return r.json(); })
  ]).then(function (res) {
    data = res[1];
    var holder = main.querySelector(".em-map");
    holder.innerHTML = res[0]; holder.appendChild(tip);
    var svgEl = holder.querySelector("svg");
    var NS="http://www.w3.org/2000/svg", defs=document.createElementNS(NS,"defs");
    defs.innerHTML='<pattern id="em-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="var(--em-norace)" style="fill:var(--em-norace)"/><line x1="0" y1="0" x2="0" y2="6" stroke="#ffffff" stroke-width="2"/></pattern>';
    svgEl.insertBefore(defs, svgEl.firstChild);
    svgEl.setAttribute("aria-label", main.dataset.mapLabel || svgEl.getAttribute("aria-label"));
    render(svgEl);
    svgEl.addEventListener("mousemove", function (e) { if (e.target.dataset && e.target.dataset.st) show(e.target, e); });
    svgEl.addEventListener("mouseleave", function () { tip.hidden = true; });
    svgEl.addEventListener("focusin", function (e) { if (e.target.dataset.st) show(e.target); });
    svgEl.addEventListener("focusout", function () { tip.hidden = true; });
    svgEl.addEventListener("click", function (e) { if (e.target.dataset && e.target.dataset.st) show(e.target, e); });
    svgEl.addEventListener("keydown", function (e) { if ((e.key === "Enter" || e.key === " ") && e.target.dataset.st) { e.preventDefault(); show(e.target); } if (e.key === "Escape") tip.hidden = true; });
    main.querySelectorAll("[data-race-btn]").forEach(function (b) {
      b.addEventListener("click", function () {
        raceKey = b.dataset.raceBtn;
        main.querySelectorAll("[data-race-btn]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        render(svgEl);
      });
    });
  }).catch(function () { /* the static table stays */ });
})();
