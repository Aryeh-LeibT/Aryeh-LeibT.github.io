# Election-night plan: state maps

Pages: `/elections/brazil-2026/map/`, `/elections/us-2026/map/` and the Hebrew versions under `/he/`.
Data: `data/elections/brazil-2026-map.json`, `data/elections/us-2026-map.json`.
Updater: `scripts/update-election-map.py` (writes JSON only; never commits, pushes or merges).
Workflow: `.github/workflows/election-night.yml` (opens or updates ONE data PR per race).

## Schema (per state, or per state race for the US)
`candidates[{name, party, votes, pct}]`, `reporting_pct`, `status` (`no results` | `leading` | `called`),
`called_by`, `source_name`, `source_url` (https), `updated_at` (ISO 8601 with offset).
US House: `seats`, `tally{D,R,other:{won,leading}}`, `districts: []` (reserved for a later district map).
The validator refuses to write a file where `called` has no `called_by`, a source is not https, or a time has no offset.
The page says **Leading** unless `status == "called"` and `called_by` is set. It never says "won".

## Sources
- **Brazil (25 Oct 2026 runoff, confirmed in the TSE 2026 calendar):** TSE public results JSON,
  `https://resultados.tse.jus.br/oficial/ele2026/6258/dados/<uf>/<uf>-c0001-e006258-u.json`.
  Election codes are listed in `/oficial/comum/config/ele-c.json` (6257 = first round, 6258 = runoff).
  The parser is tested against the real first-round São Paulo file (`scripts/fixtures/`), and a full 27-UF
  first-round fetch worked on 14 Oct 2026. A state becomes `called` only when TSE marks the tally final
  (`tf = s`) at 100% of sections; `called_by` = "TSE final tally". Polls close 17:00 Brasília = 22:00 Israel time.
- **US (3 Nov 2026):** there is no free, unified, licensed live feed. AP and similar feeds need a licence, so we do
  not use or scrape them. Results are read by hand from each state's official election office and entered in
  `data/elections/input/us-2026-results.csv` (columns in `us-2026-results.example.csv`). A race is `called` only
  with a named source in `called_by` (e.g. the state's certified result, or a named outlet's public call).
  Expect US updates to be slower and less frequent than Brazil's; the page says so.

## Cadence
- Brazil: cron every 20 minutes, 25 Oct 20:00 UTC to 26 Oct 03:40 UTC (22:00–05:40 Israel time),
  plus `workflow_dispatch` (race = brazil) at any time.
- US: `workflow_dispatch` (race = us) after each CSV update lands, roughly every 20–30 minutes while
  counting (3 Nov 23:00 UTC onward). The CSV itself goes in through the same data PR.
- Each run updates the branch `election-night/<race>` with a normal push (no force-push) and keeps one open PR.

## The human gate
- **Data-only updates** to these tracker pages fall under Aryeh's standing yes for checked election-tracker pages:
  merge once someone has checked the numbers against the source and CI is green; never on Shabbat or Yom Tov;
  tell Aryeh after it is live.
- **Any code, design or wording change** needs Aryeh's explicit yes in the GitHub agent's chat.
- **`called`** needs a named calling source in `called_by`. No source, no call.
- PRs opened by the workflow's GITHUB_TOKEN do not trigger the Site rules workflow, so the workflow runs
  `lint-site.py`, `check-links.py` and the map validator itself before pushing. The merger re-runs them locally too.

## Shabbat and Yom Tov
The workflow uses `scripts/elections-refresh.py --gate` (paused from 12:00 the day before to 21:00 on the day).
Checked 14 Oct 2026: 25 Oct 22:00, 26 Oct 05:00, 3 Nov 23:00 and 4 Nov 14:00 Israel time are all open;
24 Oct 20:00 is blocked (Shabbat). US counting that runs past Friday 6 Nov 12:00 pauses until Saturday 21:00.

## Rollback
- Bad data PR not merged yet: close it; the next run reopens a fresh one.
- Bad data already live: `git revert <merge sha>` on a new branch, open a PR, merge under the same data-only rule,
  and verify the Pages build. Never force-push main.
- Feed broken (TSE format change or outage): stop the cron by disabling the workflow in the Actions tab, keep the
  last good data live, and add a short note on the page via a normal PR (needs Aryeh's yes).

## Rebuilding the map SVGs
`scripts/build-map-svg.py us states-albers-10m.json` (us-atlas v3, ISC) and
`scripts/build-map-svg.py br ne_50m_admin_1_states_provinces` (Natural Earth, public domain; needs pyshp).
