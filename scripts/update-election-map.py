#!/usr/bin/env python3
"""Election-night map data: writes data/elections/brazil-2026-map.json and us-2026-map.json.
It only writes JSON files. It never commits, pushes, opens PRs or merges.

  init br|us                      write pre-election placeholders (every state 'no results')
  br [--cycle ele2026] [--election 6258] [--fixture-dir DIR]
                                  fetch the TSE public results JSON for all 27 UFs
  us --csv FILE                   build the US file from a hand-checked CSV (see _docs/election-night-plan.md)
  validate                        check both files against the schema and the 'called' rule
  test                            parse the bundled 2026 first-round TSE sample (São Paulo)

Brazil source: https://resultados.tse.jus.br/oficial/<cycle>/<election>/dados/<uf>/<uf>-c0001-e<election:06d>-u.json
  (c0001 = Presidente). Election codes come from /oficial/comum/config/ele-c.json:
  ele2026 6257 = federal 1st round (4 Oct 2026), 6258 = federal 2nd round (25 Oct 2026).
US: no free, unified, licensed live feed exists (AP and similar feeds need a licence and are not used).
  Results are read by hand from each state's official election office and entered in the CSV."""
import csv, json, sys, pathlib, datetime, urllib.request, argparse
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data" / "elections"
BR_FILE, US_FILE = D / "brazil-2026-map.json", D / "us-2026-map.json"
STATUSES = ("no results", "leading", "called")
TSE = "https://resultados.tse.jus.br/oficial/{cycle}/{ele}/dados/{uf}/{uf}-c0001-e{ele:0>6}-u.json"
UFS = {"AC":"Acre","AL":"Alagoas","AM":"Amazonas","AP":"Amapá","BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão","MG":"Minas Gerais","MS":"Mato Grosso do Sul","MT":"Mato Grosso","PA":"Pará","PB":"Paraíba","PE":"Pernambuco","PI":"Piauí","PR":"Paraná","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RO":"Rondônia","RR":"Roraima","RS":"Rio Grande do Sul","SC":"Santa Catarina","SE":"Sergipe","SP":"São Paulo","TO":"Tocantins"}
BR_CANDS = [{"id": "13", "name": "Lula", "name_he": "לולה", "party": "PT"}, {"id": "22", "name": "Flávio Bolsonaro", "name_he": "פלביו בולסונרו", "party": "PL"}]
BR_HE = {c["id"]: c["name_he"] for c in BR_CANDS}
US = {"AL":("Alabama",7),"AK":("Alaska",1),"AZ":("Arizona",9),"AR":("Arkansas",4),"CA":("California",52),"CO":("Colorado",8),"CT":("Connecticut",5),"DE":("Delaware",1),"DC":("District of Columbia",0),"FL":("Florida",28),"GA":("Georgia",14),"HI":("Hawaii",2),"ID":("Idaho",2),"IL":("Illinois",17),"IN":("Indiana",9),"IA":("Iowa",4),"KS":("Kansas",4),"KY":("Kentucky",6),"LA":("Louisiana",6),"ME":("Maine",2),"MD":("Maryland",8),"MA":("Massachusetts",9),"MI":("Michigan",13),"MN":("Minnesota",8),"MS":("Mississippi",4),"MO":("Missouri",8),"MT":("Montana",2),"NE":("Nebraska",3),"NV":("Nevada",4),"NH":("New Hampshire",2),"NJ":("New Jersey",12),"NM":("New Mexico",3),"NY":("New York",26),"NC":("North Carolina",14),"ND":("North Dakota",1),"OH":("Ohio",15),"OK":("Oklahoma",5),"OR":("Oregon",6),"PA":("Pennsylvania",17),"RI":("Rhode Island",2),"SC":("South Carolina",7),"SD":("South Dakota",1),"TN":("Tennessee",9),"TX":("Texas",38),"UT":("Utah",4),"VT":("Vermont",1),"VA":("Virginia",11),"WA":("Washington",10),"WV":("West Virginia",2),"WI":("Wisconsin",8),"WY":("Wyoming",1)}
# Regular Senate class II seats plus the 2026 special elections (Ohio, Florida).
SENATE = "AL AK AR CO DE GA ID IL IA KS KY LA ME MA MI MN MS MT NE NH NJ NM NC OK OR RI SC SD TN TX VA WV WY".split()
SENATE_SPECIAL = ["FL", "OH"]
GOVERNOR = "AL AK AZ AR CA CO CT FL GA HI ID IL IA KS ME MD MA MI MN NE NV NH NM NY OH OK OR PA RI SC SD TN TX VT WI WY".split()
US_PLACEHOLDER_SRC = ("State election office (results not yet reported)", "https://www.usa.gov/state-election-office")

def now_il():
    return datetime.datetime.now(ZoneInfo("Asia/Jerusalem")).replace(microsecond=0).isoformat()

def race(cands, src_name, src_url, updated):
    return {"candidates": cands, "reporting_pct": None, "status": "no results", "called_by": None,
            "source_name": src_name, "source_url": src_url, "updated_at": updated}

def init(which):
    t = now_il()
    if which == "br":
        out = {"id": "brazil-2026-map", "election": "Brazil presidential runoff, 25 October 2026",
               "level": "state", "updated_at": t, "candidates": BR_CANDS,
               "boundaries": {"name": "Natural Earth 1:50m admin-1", "license": "Public domain", "url": "https://www.naturalearthdata.com/"},
               "states": {}}
        for uf, name in UFS.items():
            out["states"][uf] = {"name": name, **race([{**c, "votes": None, "pct": None} for c in BR_CANDS],
                                 "TSE (Tribunal Superior Eleitoral)", TSE.format(cycle="ele2026", ele="6258", uf=uf.lower()), t)}
        write(BR_FILE, out)
    else:
        assert sum(n for _, n in US.values()) == 435
        out = {"id": "us-2026-map", "election": "US midterm elections, 3 November 2026", "level": "state",
               "updated_at": t, "races_available": ["senate", "governor", "house"],
               "boundaries": {"name": "us-atlas v3 (U.S. Census Bureau cartographic boundaries)", "license": "ISC (data: public domain)", "url": "https://github.com/topojson/us-atlas"},
               "states": {}}
        for st, (name, seats) in US.items():
            r = {}
            if st in SENATE: r["senate"] = race([], *US_PLACEHOLDER_SRC, t)
            if st in SENATE_SPECIAL: r["senate_special"] = race([], *US_PLACEHOLDER_SRC, t)
            if st in GOVERNOR: r["governor"] = race([], *US_PLACEHOLDER_SRC, t)
            if seats:
                h = race([], *US_PLACEHOLDER_SRC, t); del h["candidates"]
                h.update({"seats": seats, "tally": {"D": {"won": 0, "leading": 0}, "R": {"won": 0, "leading": 0}, "other": {"won": 0, "leading": 0}},
                          "districts": []})  # districts: reserved for a later per-district map
                r["house"] = h
            out["states"][st] = {"name": name, "races": r}
        write(US_FILE, out)

def write(p, data):
    errs = check(data)
    if errs: sys.exit("refusing to write %s:\n  %s" % (p.name, "\n  ".join(errs)))
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n"); print("wrote", p.relative_to(ROOT))

def check_race(where, r):
    e = []
    if r.get("status") not in STATUSES: e.append(f"{where}: bad status {r.get('status')!r}")
    if r.get("status") == "called" and not r.get("called_by"): e.append(f"{where}: 'called' needs a named called_by source")
    if not str(r.get("source_url", "")).startswith("https://"): e.append(f"{where}: source_url must be https")
    if not r.get("source_name"): e.append(f"{where}: missing source_name")
    try:
        if datetime.datetime.fromisoformat(r["updated_at"]).utcoffset() is None: raise ValueError
    except Exception: e.append(f"{where}: updated_at must be ISO 8601 with an offset")
    rp = r.get("reporting_pct")
    if rp is not None and not (0 <= rp <= 100): e.append(f"{where}: reporting_pct out of range")
    if r.get("status") == "no results" and any(c.get("votes") for c in r.get("candidates", [])): e.append(f"{where}: votes present but status is 'no results'")
    return e

def check(data):
    e = []
    for k, s in data["states"].items():
        if "races" in s:
            for rn, r in s["races"].items(): e += check_race(f"{k}.{rn}", r)
        else: e += check_race(k, s)
    if "won" in json.dumps({k: v.get("status") for k, v in data["states"].items()}): e.append("status may never be 'won'")
    return e

def parse_tse(doc, uf):
    """One UF file from TSE -> our state record."""
    cands = []
    for ag in doc["carg"][0]["agr"]:
        for p in ag["par"]:
            for c in p["cand"]:
                cands.append({"id": c["n"], "name": c["nmu"].title(), "party": p["sg"], "votes": int(c["vap"]),
                              "pct": float(c["pvapn"].replace(",", "."))})
                if str(c["n"]) in BR_HE: cands[-1]["name_he"] = BR_HE[str(c["n"])]
    cands.sort(key=lambda c: -c["votes"])
    rep = float(doc["s"]["pstn"].replace(",", "."))
    d, m, y = doc["dg"].split("/"); hh, mm, ss = doc["hg"].split(":")
    upd = datetime.datetime(int(y), int(m), int(d), int(hh), int(mm), int(ss), tzinfo=datetime.timezone(datetime.timedelta(hours=-3))).isoformat()
    total = sum(c["votes"] for c in cands)
    final = doc.get("tf") == "s" and rep >= 100
    status = "no results" if total == 0 else ("called" if final else "leading")
    return {"name": UFS[uf], "candidates": cands, "reporting_pct": rep, "status": status,
            "called_by": "TSE final tally (totalização finalizada)" if status == "called" else None,
            "source_name": "TSE (Tribunal Superior Eleitoral)", "updated_at": upd}

def br(a):
    out = json.loads(BR_FILE.read_text()); out["states"] = dict(out["states"])
    for uf in UFS:
        url = TSE.format(cycle=a.cycle, ele=a.election, uf=uf.lower())
        if a.fixture_dir: doc = json.loads((pathlib.Path(a.fixture_dir) / url.rsplit("/", 1)[1]).read_text())
        else:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "aryehleibtoren.com election map"}), timeout=30) as r:
                doc = json.load(r)
        rec = parse_tse(doc, uf); rec["source_url"] = url
        out["states"][uf] = rec
    out["updated_at"] = max(s["updated_at"] for s in out["states"].values())
    write(BR_FILE, out)

def us(a):
    """CSV columns: state,race,candidate,candidate_he (optional, Hebrew name for /he/ pages),party,votes,pct,reporting_pct,status,called_by,source_name,source_url,updated_at,won,leading
    race is senate | senate_special | governor | house. For house rows, candidate is blank, party is D/R/other,
    won/leading are seat counts. Rows for one state+race replace that race entirely."""
    out = json.loads(US_FILE.read_text()); seen = {}
    for row in csv.DictReader(open(a.csv, newline="", encoding="utf-8")):
        st, rn = row["state"].strip().upper(), row["race"].strip()
        r = out["states"][st]["races"].get(rn)
        if r is None: sys.exit(f"{st} has no {rn} race in 2026")
        if (st, rn) not in seen:
            seen[(st, rn)] = True
            if rn == "house": r["tally"] = {"D": {"won": 0, "leading": 0}, "R": {"won": 0, "leading": 0}, "other": {"won": 0, "leading": 0}}
            else: r["candidates"] = []
        for k in ("status", "called_by", "source_name", "source_url", "updated_at"):
            r[k] = row.get(k, "").strip() or None
        r["reporting_pct"] = float(row["reporting_pct"]) if row.get("reporting_pct") else None
        if rn == "house":
            r["tally"][row["party"].strip()] = {"won": int(row.get("won") or 0), "leading": int(row.get("leading") or 0)}
        else:
            r["candidates"].append({"name": row["candidate"].strip(), "party": row["party"].strip(),
                                    **({"name_he": row["candidate_he"].strip()} if (row.get("candidate_he") or "").strip() else {}),
                                    "votes": int(row["votes"]) if row.get("votes") else None,
                                    "pct": float(row["pct"]) if row.get("pct") else None})
            r["candidates"].sort(key=lambda c: -(c["votes"] or 0))
    out["updated_at"] = now_il(); write(US_FILE, out)

def test():
    doc = json.loads((ROOT / "scripts/fixtures/tse-ele2026-6257-sp-c0001-u.json").read_text())
    r = parse_tse(doc, "SP")
    assert r["reporting_pct"] == 100 and r["status"] == "called", r
    assert r["candidates"][0]["name"] == "Flavio Bolsonaro" and r["candidates"][0]["votes"] == 12922023
    assert r["updated_at"] == "2026-10-05T12:51:59-03:00"
    print("ok: SP first round,", ", ".join(f"{c['name']} {c['pct']:.2f}%" for c in r["candidates"][:2]))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("which", nargs="?")
    ap.add_argument("--cycle", default="ele2026"); ap.add_argument("--election", default="6258")
    ap.add_argument("--fixture-dir"); ap.add_argument("--csv"); a = ap.parse_args()
    if a.cmd == "init": init(a.which)
    elif a.cmd == "br": br(a)
    elif a.cmd == "us": us(a)
    elif a.cmd == "test": test()
    elif a.cmd == "validate":
        errs = check(json.loads(BR_FILE.read_text())) + check(json.loads(US_FILE.read_text()))
        for x in errs: print(x)
        print(f"{len(errs)} problem(s)"); sys.exit(1 if errs else 0)
