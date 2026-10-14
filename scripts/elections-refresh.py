#!/usr/bin/env python3
"""Election data refresh.
  --gate   exit 0 if a run is allowed now, 78 if it is Shabbat or Yom Tov in Israel.
  (none)   validate every data/elections/<id>/*.json against the schema below.
Fetchers for official open sources (TSE, CEC, state SoS) are added race by race;
any record without a source URL and retrieved_at time fails validation."""
import json, sys, pathlib, datetime
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "data" / "elections"

def blocked(now):
    if now.weekday() == 4 and now.hour >= 12: return "Shabbat (Friday afternoon)"
    if now.weekday() == 5 and now.hour < 21: return "Shabbat"
    days = set(json.loads((D / "yomtov.json").read_text())["dates"])
    today = now.date().isoformat(); tomorrow = (now.date() + datetime.timedelta(days=1)).isoformat()
    if today in days and not (now.hour >= 21 and tomorrow not in days): return "Yom Tov"
    if tomorrow in days and now.hour >= 12: return "Erev Yom Tov"
    return None

def validate():
    errs = []
    for race in sorted(p for p in D.iterdir() if p.is_dir()):
        for f in ("meta", "results", "polls", "seats"):
            p = race / f"{f}.json"
            try: data = json.loads(p.read_text())
            except Exception as e: errs.append(f"{p}: {e}"); continue
            recs = data.get("sources", []) if f == "meta" else data.get("rows", [])
            for i, r in enumerate(recs):
                url = r.get("url") or r.get("source_url")
                if not url or not url.startswith("https://"): errs.append(f"{p} row {i}: missing https source")
                if not r.get("retrieved_at"): errs.append(f"{p} row {i}: missing retrieved_at")
    for e in errs: print(e)
    print(f"{len(errs)} problem(s)"); return 1 if errs else 0

if __name__ == "__main__":
    if "--gate" in sys.argv:
        why = blocked(datetime.datetime.now(ZoneInfo("Asia/Jerusalem")))
        print(f"skip: {why}" if why else "ok to run"); sys.exit(78 if why else 0)
    sys.exit(validate())
