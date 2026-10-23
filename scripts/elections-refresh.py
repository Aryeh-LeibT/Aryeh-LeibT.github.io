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
    """Every Saturday and every Yom Tov date is a holy day, paused from 12:00 the day
    before until 21:00 on the day. Adjacent holy days overlap, so Shabbat next to
    Yom Tov becomes one continuous block."""
    yt = set(json.loads((D / "yomtov.json").read_text())["dates"])
    today = now.date()
    for d in (today, today + datetime.timedelta(days=1)):
        holy = d.weekday() == 5 or d.isoformat() in yt
        if not holy: continue
        start = datetime.datetime.combine(d - datetime.timedelta(days=1), datetime.time(12), now.tzinfo)
        end = datetime.datetime.combine(d, datetime.time(21), now.tzinfo)
        if start <= now < end:
            return ("Shabbat" if d.weekday() == 5 else "") + (" and " if d.weekday() == 5 and d.isoformat() in yt else "") + ("Yom Tov" if d.isoformat() in yt else "")
    return None

def validate():
    errs = []
    for race in sorted(p for p in D.iterdir() if p.is_dir() and p.name != "input"):  # input/ holds election-night CSVs, not a race
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
