#!/usr/bin/env python3 -u
"""
E7-EMBED-ROUTE — do embedding-space trajectories between concept pairs decompose
into a small number of cell-like attractor routes, consistent across local models?

Open lane: memory/open-lane-embedding-cells.md (Casey 2026-09-02).

DESIGN
------
Corpus    : 120 single concepts, 4 domains x 30 (NAUTICAL, OBJECT, ABSTRACT, LANDSCAPE).
Cells     : concepts themselves, snapped to integer lattices — embedding v is
            quantized v_int = round(v * S) at severity S in {1000, 250, 100, 40}.
            All distance math is EXACT integer arithmetic (sums of squared diffs in
            Python bigints). Floats exist only inside model inference.
Routes    : for concept pair (A,B): greedy max-progress walk over unvisited corpus
            cells under an integer HOP-RADIUS constraint dist2(cur,c) <= hop2
            (hop2 = median same-domain integer distance, the 'one semantic step';
            sweep at p25/p50/p75). Progress = dist2(cur,B) - dist2(c,B) > 0.
            Tie-break: min hop distance, then lexicographic name. Deterministic.
            Dead-end if no unvisited in-radius cell improves; capped at 20 hops.
Pairs     : 60 total, seeded (20260902): 30 WARM (within-domain), 30 COLD
            (cross-domain incl. concrete<->abstract). Frozen in pairs.json.
Stability : re-quantize at coarser S, optionally integer dither (xorshift PRNG,
            seeds 7/13/42, +-1 per dim w.p. 1/3 each); compare intermediate-cell
            sets/sequences to the fine (S=1000) baseline: Jaccard + LCS fraction.
Cross-model: same corpus+pairs per model; compare intermediate sets BETWEEN models
            (Jaccard), DOMAIN-SEQUENCE LCS (coarse cell class), hub top-10 overlap,
            hub-count rank correlation, and mismatched-pair nulls for chance overlap.
Regime    : WARM vs COLD — hops, top-3 hub funnel share, cross-model consistency.

Output    : stdout log (redirected to run.log) + metrics.json + pairs.json + cache/.
"""

import json, math, os, sys, time, urllib.request, random
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)
OLLAMA = "http://127.0.0.1:11434/api/embed"
PAIR_SEED = 20260902
DITHER_SEEDS = [7, 13, 42]
SEVERITIES = [1000, 250, 100, 40]
FINE = 1000
MAX_HOPS = 30
RADII_Q = [0.25, 0.50, 0.75]  # hop radius = quantile of same-domain integer dist2 (matches run2)
REF_Q = 0.25                   # reference geometry (tight enough for multi-hop)

CORPUS = {
    "NAUTICAL": ["anchor","harbor","lighthouse","foghorn","tide","rudder","keel",
                 "mast","sail","compass","mooring","buoy","wake","hull","chart",
                 "beacon","swell","helm","dockline","shipyard",
                 "bowsprit","capstan","sextant","starboard","ballast","galley",
                 "rigging","prow","stern","wharf"],
    "OBJECT":   ["hammer","chair","ladder","bucket","rope","nail","brick","spoon",
                 "lantern","crate","wrench","blanket","pencil","kettle","shovel",
                 "battery","mirror","needle","hinge","basket",
                 "broom","candle","clamp","drum","fan","hook","jar","pan",
                 "plank","towel"],
    "ABSTRACT": ["justice","memory","rumor","entropy","promise","silence","envy",
                 "patience","truth","doubt","rhythm","origin","limit","chance",
                 "mercy","habit","absence","threshold","paradox","purpose",
                 "anxiety","calm","chaos","certainty","duty","grief","honor",
                 "irony","nostalgia","virtue"],
    "LANDSCAPE":["forest","river","mountain","storm","glacier","meadow","canyon",
                 "iceberg","valley","ridge","cave","delta","marsh","fjord","dune",
                 "geyser","lagoon","tundra","thicket","estuary",
                 "bluff","creek","gorge","inlet","mesa","pond","prairie",
                 "ravine","summit","butte"],
}
DOMAIN_OF = {w: d for d, ws in CORPUS.items() for w in ws}
WORDS = sorted(DOMAIN_OF)  # deterministic order

MODELS = ["nomic-embed-text", "all-minilm:22m", "bge-m3"]  # bge-m3 optional


# ---------------- integer quantization & arithmetic ----------------

def quantize(vec, S):
    return [int(round(x * S)) for x in vec]

def dist2(a, b):
    return sum((x - y) * (x - y) for x, y in zip(a, b))

class XorShift:
    """deterministic integer dither PRNG"""
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF or 1
    def nxt(self):
        x = self.s
        x ^= (x << 13) & 0xFFFFFFFF; x ^= x >> 17; x ^= (x << 5) & 0xFFFFFFFF
        self.s = x
        return x
    def unit(self):
        return (self.nxt() / 0xFFFFFFFF) - 0.5  # [-0.5, 0.5)

def dither(vec_int, seed):
    rng = XorShift(seed * 2654435761)
    return [v + (1 if rng.unit() > 1/6 else (-1 if rng.unit() < -1/6 else 0))
            for v in vec_int]


# ---------------- routes ----------------

def same_domain_dist2s(Q):
    return [dist2(Q[a], Q[b])
            for d, ws in CORPUS.items()
            for a, b in combinations(sorted(ws), 2)]

def quantile(sorted_vals, q):
    i = min(int(q * len(sorted_vals)), len(sorted_vals) - 1)
    return sorted_vals[i]

def route(A, B, Q, words, hop2):
    """greedy max-progress route under integer hop-radius constraint.
    candidates c (incl. B) must satisfy dist2(cur,c) <= hop2 and strict
    progress toward B. Exact integer comparisons only.
    returns (path, dead_end)."""
    if A == B:
        return [A], False
    cur = A
    visited = {A}
    path = [A]
    dead = False
    for _ in range(MAX_HOPS):
        if cur == B:
            break
        d_cur_B = dist2(Q[cur], Q[B])
        best = None  # (-progress, hopdist, name)
        for c in words:
            if c in visited:
                continue
            hd = dist2(Q[cur], Q[c])
            if hd > hop2:
                continue
            prog = d_cur_B - dist2(Q[c], Q[B])
            if prog <= 0:
                continue
            key = (-prog, hd, c)
            if best is None or key < best:
                best = key
        if best is None:
            dead = True
            break
        cur = best[2]
        visited.add(cur)
        path.append(cur)
    return path, dead or path[-1] != B

def intermediates(path):
    return path[1:-1] if len(path) > 2 else []

def jaccard(s1, s2):
    """undefined for empty/empty -> None, excluded from means honestly"""
    s1, s2 = set(s1), set(s2)
    if not s1 and not s2:
        return None
    u = s1 | s2
    return len(s1 & s2) / len(u) if u else None

def mean_ok(vals):
    xs = [v for v in vals if v is not None]
    return (sum(xs) / len(xs)) if xs else None

def lcs(a, b):
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m):
            dp[i+1][j+1] = dp[i][j]+1 if a[i] == b[j] else max(dp[i][j+1], dp[i+1][j])
    return dp[n][m]

def seq_sim(a, b):
    """LCS fraction vs mean length; empty/empty = None (undefined)"""
    if not a and not b:
        return None
    denom = (len(a) + len(b)) / 2
    return lcs(a, b) / denom if denom else None


# ---------------- pairs ----------------

def build_pairs():
    """60 pairs: 30 WARM (within-domain), 30 COLD (cross-domain)."""
    rng = random.Random(PAIR_SEED)
    pairs = []
    # warm: 8/8/7/7 per domain
    warm_quota = {"ABSTRACT": 8, "LANDSCAPE": 8, "NAUTICAL": 7, "OBJECT": 7}
    for d, ws in sorted(CORPUS.items()):
        cands = sorted(combinations(ws, 2))
        rng.shuffle(cands)
        pairs += [{"a": a, "b": b, "regime": "WARM"} for a, b in cands[:warm_quota[d]]]
    # cold: cross-domain mix, incl concrete<->abstract emphasis
    cross = []
    for (d1, w1), (d2, w2) in combinations(sorted(CORPUS.items()), 2):
        for a in w1:
            for b in w2:
                cross.append((a, b))
    rng.shuffle(cross)
    used = set()
    quota = {("ABSTRACT","LANDSCAPE"): 8, ("ABSTRACT","NAUTICAL"): 8,
             ("ABSTRACT","OBJECT"): 8,
             ("NAUTICAL","OBJECT"): 3, ("LANDSCAPE","OBJECT"): 2, ("LANDSCAPE","NAUTICAL"): 1}
    for a, b in cross:
        key = tuple(sorted((DOMAIN_OF[a], DOMAIN_OF[b])))
        if quota.get(key, 0) > 0 and a not in used and b not in used:
            pairs.append({"a": a, "b": b, "regime": "COLD"})
            quota[key] -= 1
            used |= {a, b}
        if len(pairs) == 60:
            break
    return pairs


# ---------------- embeddings ----------------

def embed(model, texts):
    fn = os.path.join(CACHE, model.replace(":", "_").replace("/", "_") + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    out = {}
    for i in range(0, len(texts), 32):
        req = urllib.request.Request(
            OLLAMA, json.dumps({"model": model, "input": texts[i:i+32]}).encode(),
            {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        for t, e in zip(texts[i:i+32], d["embeddings"]):
            out[t] = e
    json.dump(out, open(fn, "w"))
    return out

def probe(model):
    """test embeddability without poisoning the cache"""
    req = urllib.request.Request(
        OLLAMA, json.dumps({"model": model, "input": ["probe"]}).encode(),
        {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        json.load(r)
    return True

def available_models():
    ok = []
    for m in MODELS:
        fn = os.path.join(CACHE, m.replace(":", "_").replace("/", "_") + ".json")
        if os.path.exists(fn):
            ok.append(m); continue
        try:
            probe(m)
            ok.append(m)
        except Exception as e:
            print(f"[skip] {m}: {e}")
    return ok


# ---------------- analysis ----------------

def hub_stats(all_routes):
    counts = {}
    for path, dead in all_routes:
        for c in intermediates(path):
            counts[c] = counts.get(c, 0) + 1
    total = sum(counts.values())
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return counts, top, total

def funnel_share(all_routes, top3_names):
    n = len(all_routes)
    hit = sum(1 for path, _ in all_routes
              if set(intermediates(path)) & set(top3_names))
    return hit / n if n else 0.0

def rank_corr(c1, c2):
    """Spearman over union of hub names (ties: average ranks)."""
    names = sorted(set(c1) | set(c2))
    if len(names) < 3:
        return float("nan")
    def ranks(counts):
        vals = sorted((counts.get(n, 0), n) for n in names)
        pos, out = {}, {}
        for idx, (v, n) in enumerate(vals):
            out.setdefault(v, []).append(idx)
        for v, idxs in out.items():
            avg = sum(idxs)/len(idxs)
            for idx in idxs:
                pos[vals[idx][1]] = avg
        return [pos[n] for n in names]
    r1, r2 = ranks(c1), ranks(c2)
    n = len(names)
    def pearson(x, y):
        mx, my = sum(x)/n, sum(y)/n
        num = sum((a-mx)*(b-my) for a, b in zip(x, y))
        den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
        return num/den if den else float("nan")
    return pearson(r1, r2)

RADII_Q = [0.25, 0.50, 0.75]  # hop radius = quantile of same-domain integer dist2
REF_Q = 0.25                   # reference geometry (tight enough for multi-hop)

def analyze(model, E, pairs):
    print(f"\n=== MODEL {model} ===")
    Qf = {w: quantize(E[w], FINE) for w in WORDS}
    sd = sorted(same_domain_dist2s(Qf))
    rad_report = {}
    base_routes, base_r2, hops = None, None, None
    for rq in RADII_Q:
        r2 = quantile(sd, rq)
        rr = [route(p["a"], p["b"], Qf, WORDS, r2) for p in pairs]
        hh = [len(p0) - 2 for p0, _ in rr]
        dcount = sum(1 for _, d in rr if d)
        rad_report[f"q{int(rq*100)}"] = {
            "hop2": r2, "dead_rate": dcount / len(pairs),
            "mean_hops": sum(hh) / len(hh)}
        print(f"  radius q{int(rq*100):02d} hop2={r2}: dead={dcount/len(pairs):.2f} "
              f"mean_hops={sum(hh)/len(hh):.2f}")
        if rq == REF_Q:
            base_routes, base_r2, hops = rr, r2, hh
    for p, (path, dead) in zip(pairs, base_routes):
        tag = "DEAD" if dead else "ok"
        print(f"  [{p['regime']}] {p['a']} -> {p['b']}: {' > '.join(path)} [{tag}]")

    dead_rate = sum(1 for _, d in base_routes if d) / len(base_routes)
    hops = [len(path)-2 for path, _ in base_routes]
    counts, top, total_cells = hub_stats(base_routes)
    distinct = len(counts)
    top10 = top[:10]
    top10_share = sum(c for _, c in top10) / total_cells if total_cells else 0.0
    top3_names = [n for n, _ in top[:3]]
    deads = [d for _, d in base_routes]
    warm_idx = [i for i, p in enumerate(pairs) if p["regime"] == "WARM"]
    cold_idx = [i for i, p in enumerate(pairs) if p["regime"] == "COLD"]
    def sub(idx): return [base_routes[i] for i in idx]
    reg = {
        "WARM": {"mean_hops": sum(hops[i] for i in warm_idx)/len(warm_idx),
                 "funnel_top3": funnel_share(sub(warm_idx), top3_names)},
        "COLD": {"mean_hops": sum(hops[i] for i in cold_idx)/len(cold_idx),
                 "funnel_top3": funnel_share(sub(cold_idx), top3_names)},
    }
    hub_domains = {}
    for n, c in counts.items():
        hub_domains[DOMAIN_OF[n]] = hub_domains.get(DOMAIN_OF[n], 0) + c
    print(f"  distinct intermediate cells: {distinct}/{total_cells} uses")
    print(f"  top-10 hubs: {top10}  (share={top10_share:.3f})")
    print(f"  hub usage by domain: {sorted(hub_domains.items(), key=lambda kv: -kv[1])}")
    print(f"  dead-end rate: {dead_rate:.3f}  mean hops: {sum(hops)/len(hops):.2f}")
    print(f"  regime: {json.dumps(reg)}")

    # --- quantization stability (reference radius q50, recomputed per lattice) ---
    print("  -- quantization stability vs fine baseline (S=1000) --")
    stab = {}
    for S in SEVERITIES[1:]:
        for seed in [None] + DITHER_SEEDS:
            Qs = {w: quantize(E[w], S) for w in WORDS}
            if seed is not None:
                Qs = {w: dither(v, seed) for w, v in Qs.items()}
            # radius recomputed on the SAME lattice (integer discipline)
            r2s = quantile(sorted(same_domain_dist2s(Qs)), REF_Q)
            rt = [route(p["a"], p["b"], Qs, WORDS, r2s) for p in pairs]
            js = [jaccard(intermediates(a[0]), intermediates(b[0]))
                  for a, b in zip(base_routes, rt)]
            ss = [seq_sim(intermediates(a[0]), intermediates(b[0]))
                  for a, b in zip(base_routes, rt)]
            ident = sum(1 for a, b in zip(base_routes, rt) if a[0] == b[0]) / len(pairs)
            key = f"S{S}" + (f"+d{seed}" if seed else "")
            stab[key] = {"jaccard": mean_ok(js), "lcs": mean_ok(ss),
                         "route_identical": ident,
                         "n_jaccard": sum(1 for v in js if v is not None)}
            print(f"    {key:12s} jaccard={stab[key]['jaccard']:.3f} "
                  f"lcs={stab[key]['lcs']:.3f} identical={ident:.3f} "
                  f"(n={stab[key]['n_jaccard']})")
    return {"base_routes": [(p, d) for p, d in base_routes], "counts": counts,
            "top10": top10, "dead_rate": dead_rate, "mean_hops": sum(hops)/len(hops),
            "distinct": distinct, "top10_share": top10_share, "top3": top3_names,
            "regime": reg, "hub_domains": hub_domains, "stability": stab,
            "radius_sweep": rad_report, "ref_hop2": base_r2}


def dom_seq(path):
    """domain labels of intermediate cells — the coarse cell class"""
    return [DOMAIN_OF[c] for c in intermediates(path)]

def cross_compare(res, pairs):
    print("\n=== CROSS-MODEL COMPARISON ===")
    ms = list(res)
    out = {}
    for m1, m2 in combinations(ms, 2):
        R1, R2 = res[m1]["base_routes"], res[m2]["base_routes"]
        js = [jaccard(intermediates(R1[i][0]), intermediates(R2[i][0]))
              for i in range(len(pairs))]
        ss = [seq_sim(intermediates(R1[i][0]), intermediates(R2[i][0]))
              for i in range(len(pairs))]
        # null: mismatched pairs
        rng = random.Random(PAIR_SEED)
        null = []
        for i in range(len(pairs)):
            j = rng.randrange(len(pairs) - 1)
            if j >= i: j += 1
            null.append(jaccard(intermediates(R1[i][0]), intermediates(R2[j][0])))
        t1 = set(n for n, _ in res[m1]["top10"])
        t2 = set(n for n, _ in res[m2]["top10"])
        rc = rank_corr(res[m1]["counts"], res[m2]["counts"])
        mean_js, n_js = mean_ok(js), sum(1 for v in js if v is not None)
        mean_ss = mean_ok(ss)
        null_m = mean_ok(null)
        # domain-sequence (coarse cell class) comparison + its own null
        djs = [seq_sim(dom_seq(R1[i][0]), dom_seq(R2[i][0]))
               for i in range(len(pairs))]
        rng2 = random.Random(PAIR_SEED + 1)
        dnull = []
        for i in range(len(pairs)):
            j = rng2.randrange(len(pairs) - 1)
            if j >= i: j += 1
            dnull.append(seq_sim(dom_seq(R1[i][0]), dom_seq(R2[j][0])))
        mean_d, null_d = mean_ok(djs), mean_ok(dnull)
        # per-regime
        warm = [js[i] for i, p in enumerate(pairs) if p["regime"] == "WARM"]
        cold = [js[i] for i, p in enumerate(pairs) if p["regime"] == "COLD"]
        out[f"{m1}|{m2}"] = {
            "mean_jaccard": mean_js, "null_jaccard": null_m,
            "lift": (mean_js - null_m) if (mean_js is not None
                                            and null_m is not None) else None,
            "mean_lcs": mean_ss, "n_pairs": n_js,
            "domain_seq_lcs": mean_d, "domain_seq_null": null_d,
            "top10_overlap": len(t1 & t2), "top10_union": len(t1 | t2),
            "rank_corr": rc,
            "warm_jaccard": mean_ok(warm), "cold_jaccard": mean_ok(cold),
            "shared_hubs": sorted(t1 & t2),
        }
        o = out[f"{m1}|{m2}"]
        print(f"  {m1} vs {m2}:")
        print(f"    per-pair intermediate Jaccard {o['mean_jaccard']:.3f} "
              f"(null {o['null_jaccard']:.3f}, lift {o['lift']:+.3f}) "
              f"[n={n_js}/{len(pairs)} both-routed]")
        print(f"    DOMAIN-seq LCS {o['domain_seq_lcs']:.3f} "
              f"(domain null {o['domain_seq_null']:.3f})  <-- coarse-cell convergence")
        print(f"    LCS {o['mean_lcs']:.3f} | warm {o['warm_jaccard']:.3f} "
              f"vs cold {o['cold_jaccard']:.3f}")
        print(f"    hub top-10 overlap {o['top10_overlap']}/{o['top10_union']} "
              f"shared={o['shared_hubs']}")
        print(f"    hub-count Spearman rho={o['rank_corr']:.3f}")
    return out


def main():
    t0 = time.time()
    pairs = build_pairs()
    json.dump(pairs, open(os.path.join(HERE, "pairs.json"), "w"), indent=1)
    print(f"E7-EMBED-ROUTE | {len(pairs)} pairs ({PAIR_SEED}) "
          f"| {len(WORDS)} concepts x 4 domains")
    models = available_models()
    print(f"models: {models}")
    res = {}
    for m in models:
        E = embed(m, WORDS)
        res[m] = analyze(m, E, pairs)
    cross = cross_compare(res, pairs) if len(res) > 1 else {}
    metrics = {
        "config": {"pairs": 40, "pair_seed": PAIR_SEED, "severities": SEVERITIES,
                   "dither_seeds": DITHER_SEEDS, "fine": FINE, "max_hops": MAX_HOPS,
                   "models": models, "corpus": CORPUS},
        "per_model": {m: {k: v for k, v in r.items() if k != "base_routes"}
                      for m, r in res.items()},
        "cross_model": cross,
        "elapsed_s": round(time.time() - t0, 1),
    }
    json.dump(metrics, open(os.path.join(HERE, "metrics.json"), "w"), indent=1)
    # raw routes for later study (the gold)
    raw = {m: [{"pair": p, "regime": pairs[i]["regime"], "path": r[0], "dead": r[1]}
               for i, (r, p) in enumerate(zip(res[m]["base_routes"], pairs))]
           for m in res}
    json.dump(raw, open(os.path.join(HERE, "routes_raw.json"), "w"), indent=1)
    print(f"\ndone in {metrics['elapsed_s']}s -> metrics.json, routes_raw.json")

if __name__ == "__main__":
    main()
