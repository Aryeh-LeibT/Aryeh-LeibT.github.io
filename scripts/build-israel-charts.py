#!/usr/bin/env python3
"""Builds the Israel tracker's votes/seats charts as static SVG + tables from
data/elections/israel-2026-polls.json into the EN and HE pages (between chart markers).
Re-run after any data update. No libraries, no CDNs."""
import json, pathlib, re, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data/elections/israel-2026-polls.json"
if not SRC.exists():  # offline during the legal pre-election poll blackout; leave the pages untouched
    raise SystemExit(f"{SRC.relative_to(ROOT)} is missing (poll blackout?); pages left unchanged.")
D = json.loads(SRC.read_text(encoding="utf-8"))
COL = {"coal": "#9a7b4f", "opp": "#2f5577", "arab": "#5f8a63", "none": "#8c8c8c", "gov": "#9a7b4f", "other": "#6f7f8f"}
ORDER = ["coal", "none", "arab", "opp"]
T = {
 "en": dict(h2="Polls and projected seats", ribbon="Each poll as a 120-seat strip, grouped by bloc",
   ribbon_d="One row per poll. Each cell is one seat. The line marks seat 61, a Knesset majority.",
   gauge="Poll average by bloc", bars="Poll average by list (bar) and each poll (dots)",
   last="Last time: 2022 official results", last_d="Share of valid votes; the dashed line is the 3.25% threshold. Seats won in brackets.",
   avg="Poll average", seats="seats", poll="Poll", party="List", bloc="Bloc", n="Sample", moe="Margin", date="Date",
   votes="Votes", pct="% of valid votes", src="Source", updated="Last updated", note_avg="Poll average, not a result and not a final count. ",
   method="Method: ", maj="61 = majority", single="(single source, not yet confirmed)", notavg="not in the average",
   live="Election night: live count", live_empty="The Central Elections Committee count starts on the night of 27 October 2026. Counted votes and projected seats will appear here with the time of each update; nothing shown here is final until the committee publishes official results.",
   below="below threshold", table="Table", gaugeh="Bloc", unknown="not reported", rib_row="seats in this poll"),
 "he": dict(h2="סקרים ומנדטים צפויים", ribbon="כל סקר כרצועה של 120 מנדטים, לפי גושים",
   ribbon_d="שורה לכל סקר. כל משבצת היא מנדט אחד. הקו מסמן את המנדט ה־61, רוב בכנסת.",
   gauge="ממוצע הסקרים לפי גושים", bars="ממוצע הסקרים לכל רשימה (עמודה) וכל סקר בנפרד (נקודות)",
   last="בפעם הקודמת: התוצאות הרשמיות של 2022", last_d="אחוז מהקולות הכשרים; הקו המקווקו הוא אחוז החסימה, 3.25%. בסוגריים: המנדטים שהתקבלו.",
   avg="ממוצע סקרים", seats="מנדטים", poll="סקר", party="רשימה", bloc="גוש", n="מדגם", moe="טעות דגימה", date="תאריך",
   votes="קולות", pct="% מהקולות הכשרים", src="מקור", updated="עדכון אחרון", note_avg="ממוצע סקרים, לא תוצאה ולא ספירה סופית. ",
   method="שיטה: ", maj="61 = רוב", single="(מקור יחיד, טרם אומת)", notavg="לא נכלל בממוצע",
   live="ליל הבחירות: ספירה חיה", live_empty="ספירת ועדת הבחירות המרכזית תתחיל בליל 27 באוקטובר 2026. הקולות שנספרו והמנדטים הצפויים יופיעו כאן עם שעת כל עדכון; שום נתון כאן אינו סופי עד שהוועדה תפרסם את התוצאות הרשמיות.",
   below="מתחת לאחוז החסימה", table="טבלה", gaugeh="גוש", unknown="לא פורסם", rib_row="מנדטים בסקר זה"),
}
METHOD_HE = "ממוצע פשוט, לא משוקלל, של מספרי המנדטים שפרסם כל סקר. רשימה שסקר הציג מתחת לאחוז החסימה נספרת אצלו כ־0. זה אינו מודל של אחוזי הצבעה ואינו חלוקה לפי בדר־עופר; המספרים מעוגלים לספרה אחת אחרי הנקודה ואינם מסתכמים בהכרח ב־120."
OUTLET_HE = {"Channel 12 News": "חדשות 12", "Maariv": "מעריב", "Channel 13 News": "חדשות 13", "Walla": "וואלה", "Kan 11 News": "כאן חדשות", "Channel 14 News": "חדשות 14", "Zman Yisrael": "זמן ישראל"}
POLLSTER_HE = {"Midgam (Mano Geva)": "מדגם (מנו גבע)", "Lazar Research / Panel4All": "מכון לזר / פאנל4אול", "not named in the cited reports": "לא צוין בדיווחים", "Kantar Israel": "קנטאר ישראל", "Next Data (analysis: Shlomo Filber)": "NEXT DATA (ניתוח: שלמה פילבר)", "HaMidgam Project, Stat-Net, Askaria and HaMadad (Shmuel Rosner, Noah Slepkov)": "המדד (שמואל רוזנר, נח סלפקוב) עם סטט־נט, פרויקט המדגם ואסקריא", "Tatika Research & Media (Yossi Tatika) / Adgenda": "טאטיקה מחקרים ומדיה (יוסי טאטיקה) / אדג'נדה"}
e = html.escape

def fmtdate(s, L):
    y, m, d = s.split("-")
    mon_en = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    mon_he = ["בינואר","בפברואר","במרץ","באפריל","במאי","ביוני","ביולי","באוגוסט","בספטמבר","באוקטובר","בנובמבר","בדצמבר"]
    return f"{int(d)} {(mon_he if L=='he' else mon_en)[int(m)-1]} {y}"

def build(L):
    t, rtl, W = T[L], L == "he", 640
    def X(x, w=0): return W - x - w if rtl else x
    anc = lambda a: a  # an RTL document already mirrors start/end for SVG text
    NUM = ' direction="ltr" text-anchor="end"' if rtl else ' text-anchor="start"'  # numbers read left-to-right
    pn = lambda k: D["parties"][k]["he"] if rtl else k
    bn = lambda b: D["blocs"][b][L]
    ol = lambda p: OUTLET_HE.get(p["outlet"], p["outlet"]) if rtl else p["outlet"]
    polls = [p for p in D["polls"] if p["in_average"]]
    allp = D["polls"]
    avg = {k: sum(p["values"].get(k, 0) for p in polls) / len(polls) for k in D["parties"]}
    parties = sorted(D["parties"], key=lambda k: (ORDER.index(D["parties"][k]["bloc"]), -avg[k]))
    blocavg = {b: sum(avg[k] for k in parties if D["parties"][k]["bloc"] == b) for b in ORDER}
    f1 = lambda v: f"{v:.1f}"
    upd = D["updated"]
    out = [f'<div class="ilc" data-ilc>', f'<p class="el-updated">{t["updated"]}: <time datetime="{upd}">{fmtdate(upd[:10], L)}, {upd[11:16]}</time> · {t["note_avg"]}</p>']
    # 1. bloc gauge
    s = [f'<svg viewBox="0 0 {W} 92" role="img" aria-labelledby="ilc-g-t"><title id="ilc-g-t">{t["gauge"]}</title>']
    x = 0; sc = W / 120
    for b in ORDER:
        w = blocavg[b] * sc
        s.append(f'<rect x="{X(x,w):.1f}" y="22" width="{w:.1f}" height="30" fill="{COL[b]}"/>')
        if w > 40: s.append(f'<text x="{X(x+w/2):.1f}" y="42" text-anchor="middle" fill="#fff" font-size="13">{f1(blocavg[b])}</text>')
        x += w
    m = 61 * sc
    s.append(f'<line x1="{X(m):.1f}" x2="{X(m):.1f}" y1="12" y2="62" stroke="currentColor" stroke-width="2"/><text x="{X(m):.1f}" y="10" text-anchor="middle" font-size="12" fill="currentColor">{t["maj"]}</text>')
    lx = 0
    for b in ORDER:
        s.append(f'<rect x="{X(lx,10):.1f}" y="72" width="10" height="10" fill="{COL[b]}"/><text x="{X(lx+14):.1f}" y="81" font-size="11" text-anchor="{anc("start")}" fill="currentColor">{e(bn(b))}</text>')
        lx += 160
    s.append("</svg>")
    out += [f'<h3>{t["gauge"]} <span class="ilc-tag">{t["avg"]}</span></h3>', "".join(s)]
    rows = "".join(f'<tr><td>{e(bn(b))}</td><td>{f1(blocavg[b])}</td>' + "".join(f'<td>{sum(p["values"].get(k,0) for k in parties if D["parties"][k]["bloc"]==b)}</td>' for p in polls) + "</tr>" for b in ORDER)
    out.append(f'<details class="ilc-tbl"><summary>{t["table"]}</summary><table class="el-table"><caption>{t["gauge"]} ({t["seats"]})</caption><thead><tr><th scope="col">{t["gaugeh"]}</th><th scope="col">{t["avg"]}</th>' + "".join(f'<th scope="col">{e(ol(p))}</th>' for p in polls) + f'</tr></thead><tbody>{rows}</tbody></table></details>')
    # 2. poll strips
    cw, rh, lab = 4, 22, 150
    h = len(allp) * (rh + 8) + 30
    s = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-labelledby="ilc-r-t"><title id="ilc-r-t">{t["ribbon"]}</title>']
    for i, p in enumerate(allp):
        y = 20 + i * (rh + 8); x = lab
        nm = ol(p) + " " + fmtdate(p["date"], L)
        s.append(f'<text x="{X(lab-6)}" y="{y+15}" font-size="11" text-anchor="{anc("end")}" fill="currentColor">{e(nm)}</text>')
        for b in ORDER:
            n = sum(p["values"].get(k, 0) for k in parties if D["parties"][k]["bloc"] == b)
            for j in range(n):
                s.append(f'<rect x="{X(x,cw-1)}" y="{y}" width="{cw-1}" height="{rh}" fill="{COL[b]}" opacity="{0.55 if not p["in_average"] else 1}"/>')
                x += cw
            x += 0
    mx = lab + 60 * cw + (cw - 1) + 0.5
    s.append(f'<line x1="{X(mx)}" x2="{X(mx)}" y1="14" y2="{h-6}" stroke="currentColor" stroke-width="2" stroke-dasharray="3 2"/><text x="{X(mx)}" y="11" text-anchor="middle" font-size="11" fill="currentColor">61</text></svg>')
    out += [f'<h3>{t["ribbon"]} <span class="ilc-tag">{t["avg"] if False else (t["poll"])}</span></h3>', f'<p class="el-note">{t["ribbon_d"]}</p>', "".join(s)]
    # poll table (also the strips' fallback)
    def pollmeta(p):
        bits = [e(POLLSTER_HE.get(p["pollster"], p["pollster"]) if rtl else p["pollster"]), fmtdate(p["date"], L)]
        bits.append(f'{t["n"]} {p["sample"]:,}' if p.get("sample") else f'{t["n"]}: {t["unknown"]}')
        if p.get("moe_pp"): bits.append(f'±{p["moe_pp"]}')
        if p.get("single_source"): bits.append(t["single"])
        if not p["in_average"]: bits.append(t["notavg"])
        return " · ".join(bits)
    head = "".join(f'<th scope="col"><a href="{e(p["source_url"])}" rel="noopener">{e(ol(p))}</a><br><small>{pollmeta(p)}</small></th>' for p in allp)
    body = "".join(f'<tr><th scope="row">{e(pn(k))}</th><td>{f1(avg[k])}</td>' + "".join(f'<td>{p["values"][k] if p["values"].get(k) else "–"}</td>' for p in allp) + "</tr>" for k in parties)
    out.append(f'<div class="ilc-scroll"><table class="el-table ilc-polls"><caption>{t["seats"]} · {t["poll"]} · {t["avg"]}</caption><thead><tr><th scope="col">{t["party"]}</th><th scope="col">{t["avg"]}</th>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    out.append(f'<p class="el-note">– = {t["below"]} / {t["unknown"]}. {t["method"]}{e(METHOD_HE if rtl else D["average"]["method"])}</p>')
    # 3. party bars with poll dots
    rh2 = 24; h = len(parties) * rh2 + 30; lab = 190; sc = (W - lab - 40) / 25
    s = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-labelledby="ilc-b-t"><title id="ilc-b-t">{t["bars"]}</title>']
    for i, k in enumerate(parties):
        y = 10 + i * rh2; b = D["parties"][k]["bloc"]; w = avg[k] * sc
        s.append(f'<text x="{X(lab-8)}" y="{y+14}" font-size="12" text-anchor="{anc("end")}" fill="currentColor">{e(pn(k))}</text>')
        s.append(f'<rect x="{X(lab,w):.1f}" y="{y+3}" width="{w:.1f}" height="14" fill="{COL[b]}" opacity="0.8"/>')
        for p in polls:
            v = p["values"].get(k, 0)
            s.append(f'<circle cx="{X(lab+v*sc):.1f}" cy="{y+10}" r="3.2" fill="var(--bg, #fff)" stroke="currentColor" stroke-width="1.3"/>')
        s.append(f'<text x="{X(lab+max(avg[k],max(p["values"].get(k,0) for p in polls))*sc+8):.1f}" y="{y+14}" font-size="11"{NUM} fill="currentColor">{f1(avg[k])}</text>')
    for v in (4, 10, 20):
        s.append(f'<line x1="{X(lab+v*sc):.1f}" x2="{X(lab+v*sc):.1f}" y1="6" y2="{h-18}" stroke="currentColor" stroke-opacity="0.2"/><text x="{X(lab+v*sc):.1f}" y="{h-5}" font-size="10" text-anchor="middle" fill="currentColor">{v}</text>')
    s.append("</svg>")
    out += [f'<h3>{t["bars"]} <span class="ilc-tag">{t["avg"]}</span></h3>', "".join(s)]
    # 4. 2022
    R = D["results_2022"]; V = R["valid_votes"]; rows = R["rows"]
    rh2 = 22; h = len(rows) * rh2 + 30; lab = 170; sc = (W - lab - 90) / 25
    s = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-labelledby="ilc-l-t"><title id="ilc-l-t">{t["last"]}</title>']
    for i, r in enumerate(rows):
        y = 10 + i * rh2; pc = r["votes"] / V * 100; w = pc * sc
        s.append(f'<text x="{X(lab-8)}" y="{y+14}" font-size="12" text-anchor="{anc("end")}" fill="currentColor">{e(r[L if rtl else "en"])}</text>')
        s.append(f'<rect x="{X(lab,w):.1f}" y="{y+3}" width="{w:.1f}" height="13" fill="{COL[r["bloc"]]}" opacity="{1 if r["seats"] else 0.4}"/>')
        s.append(f'<text x="{X(lab+w+6):.1f}" y="{y+14}" font-size="11"{NUM} fill="currentColor">{pc:.2f}% ({r["seats"]})</text>')
    tx = lab + 3.25 * sc
    s.append(f'<line x1="{X(tx):.1f}" x2="{X(tx):.1f}" y1="4" y2="{h-16}" stroke="currentColor" stroke-dasharray="4 3"/><text x="{X(tx):.1f}" y="{h-3}" font-size="10" text-anchor="middle" fill="currentColor">3.25%</text></svg>')
    out += [f'<h3>{t["last"]}</h3>', f'<p class="el-note">{t["last_d"]}</p>', "".join(s)]
    body = "".join(f'<tr><th scope="row">{e(r[L if rtl else "en"])}</th><td>{r["votes"]:,}</td><td>{r["votes"]/V*100:.2f}</td><td>{r["seats"]}</td><td>{e(R["blocs"][r["bloc"]][L])}</td></tr>' for r in rows)
    out.append(f'<details class="ilc-tbl"><summary>{t["table"]}</summary><table class="el-table"><caption>{t["last"]}</caption><thead><tr><th scope="col">{t["party"]}</th><th scope="col">{t["votes"]}</th><th scope="col">{t["pct"]}</th><th scope="col">{t["seats"]}</th><th scope="col">{t["bloc"]}</th></tr></thead><tbody>{body}</tbody></table></details>')
    out.append(f'<p class="el-note">{t["src"]}: <a href="{R["source_url"]}" rel="noopener">{"ועדת הבחירות המרכזית" if rtl else "Central Elections Committee"}</a>. {"קולות כשרים" if rtl else "Valid votes"}: {V:,}; {"אחוז החסימה" if rtl else "threshold"} 3.25% = {R["threshold_votes"]:,}.</p>')
    # 5. live
    lv = D["live"]
    out.append(f'<h3>{t["live"]}</h3>')
    if not lv["rows"]:
        out.append(f'<p class="el-empty">{t["live_empty"]}</p>')
    out.append(f'<p class="el-note">{"נקבצו לפי הגושים שבהם השתמשו כלי התקשורת המצוטטים; זה תיאור של שיוך מדווח ולא תחזית לקואליציה." if rtl else e(D["bloc_note"])}</p></div>')
    # Wrap each chart so phones can scroll it sideways instead of shrinking the text.
    return re.sub(r"(<svg .*?</svg>)", r'<div class="ilc-chart">\1</div>', "\n".join(out), flags=re.S)

for L, path in (("en", "elections/israel-2026/index.html"), ("he", "he/elections/israel-2026/index.html")):
    p = ROOT / path; txt = p.read_text(encoding="utf-8")
    block = "<!-- ilc:start -->\n" + build(L) + "\n<!-- ilc:end -->"
    if "<!-- ilc:start -->" in txt:
        txt = re.sub(r"<!-- ilc:start -->.*?<!-- ilc:end -->", lambda _: block, txt, flags=re.S)
    else:
        txt = re.sub(r'(<section aria-labelledby="res">\s*<h2 id="res">)[^<]*(</h2>).*?(</section>)',
                     lambda m: m.group(1) + T[L]["h2"] + m.group(2) + "\n" + block + "\n      " + m.group(3), txt, count=1, flags=re.S)
        txt = txt.replace('data-chart="hemicycle"', 'data-chart="none"', 1)
    p.write_text(txt, encoding="utf-8")
print("ok")
