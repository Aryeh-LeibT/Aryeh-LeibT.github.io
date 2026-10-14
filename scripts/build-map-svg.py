#!/usr/bin/env python3
"""One-off builder for the static election maps in images/maps/. Not run in CI.
  US:     us-atlas v3 states-albers-10m.json (ISC; derived from U.S. Census Bureau
          cartographic boundaries, public domain), already projected to 975x610.
  Brazil: Natural Earth 1:50m admin-1 states and provinces (public domain),
          equirectangular projection scaled by cos(latitude).
Usage: build-map-svg.py us <states-albers-10m.json>
       build-map-svg.py br <ne_50m_admin_1_states_provinces (shapefile stem)>
Each state becomes <path id="st-XX" data-st="XX" tabindex="0" role="button">."""
import json, sys, math, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "images" / "maps"
FIPS = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY"}

def dp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]; dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
        d = abs(dy*p[0] - dx*p[1] + b[0]*a[1] - b[1]*a[0]) / L
        if d > dmax: dmax, idx = d, i
    if dmax <= eps: return [a, b]
    return dp(pts[:idx+1], eps)[:-1] + dp(pts[idx:], eps)

def path(rings):
    out = []
    for r in rings:
        if len(r) < 3: continue
        out.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in r) + "Z")
    return "".join(out)

def svg(name, w, h, shapes, label):
    body = "\n".join(f'<path id="st-{k}" data-st="{k}" tabindex="0" role="button" aria-label="{n}" d="{d}"/>' for k, n, d in shapes)
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="em-svg" role="group" aria-label="{label}">\n{body}\n</svg>\n')

def us(src):
    t = json.load(open(src)); sc, tr = t["transform"]["scale"], t["transform"]["translate"]
    arcs = []
    for a in t["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a: x += dx; y += dy; pts.append((x*sc[0]+tr[0], y*sc[1]+tr[1]))
        m = len(pts) // 2
        arcs.append(dp(pts[:m+1], 0.6)[:-1] + dp(pts[m:], 0.6) if len(pts) > 3 else pts)
    def ring(ids):
        pts = []
        for i in ids:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts += seg[1:] if pts else seg
        return pts
    shapes = []
    for g in t["objects"]["states"]["geometries"]:
        k = FIPS.get(g["id"]);
        if not k: continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        shapes.append((k, g["properties"]["name"], path([ring(r) for p in polys for r in p])))
    svg("us-states.svg", 975, 610, sorted(shapes), "Map of US states")

def br(stem):
    import shapefile
    r = shapefile.Reader(stem); shapes = []
    allpts = [p for s in r.iterShapeRecords() if s.record["adm0_a3"] == "BRA" for p in s.shape.points]
    lon0, lat1 = min(p[0] for p in allpts), max(p[1] for p in allpts)
    k = 600 / (max(p[0] for p in allpts) - lon0) * 1
    c = math.cos(math.radians(-14))
    for s in r.iterShapeRecords():
        if s.record["adm0_a3"] != "BRA": continue
        pts, parts = s.shape.points, list(s.shape.parts) + [len(s.shape.points)]
        rings = []
        for i in range(len(parts) - 1):
            ring = [((x - lon0) * k * c + 10, (lat1 - y) * k + 10) for x, y in pts[parts[i]:parts[i+1]]]
            m = len(ring) // 2
            ring = dp(ring[:m+1], 0.5)[:-1] + dp(ring[m:], 0.5)
            if len(ring) >= 4 or s.record["postal"] == "DF": rings.append(ring)
        shapes.append((s.record["postal"], s.record["name"], path(rings)))
    W = round((max(p[0] for p in allpts) - lon0) * k * c + 20); H = round((lat1 - min(p[1] for p in allpts)) * k + 20)
    svg("brazil-states.svg", W, H, sorted(shapes), "Map of Brazilian states")

if __name__ == "__main__":
    {"us": us, "br": br}[sys.argv[1]](sys.argv[2])
