#!/usr/bin/env python3
"""NQ-1 fabric-twin v0 — harvest published wheel tables, fit numpy-only models.

Replay-only: reads COMMITTED published outputs under wheel/ (no fabric runs).
Sources (all 5-seed mean true-residency %, interference arm unless noted):
  - spin9-output.txt  EXP1 (m_s,K) grid: 80 cells, N=6, delta=12, sigma=8/5, pd=3
  - spin5-output.txt  EXP2 grammar sweep s in {15,30}: 7 grammars x K in {1,2}
  - spin4-output.txt  MAIN ladder (spread 0..30 x K{1,2,8} x {ladder,cohort}) + CONTROL N in {2,3}
  - spin11-output.txt EXP1 pd x N uncomp grid (K=1, ladder over [0,30], true12% == true-residency, anchors exact)
Dedupe key: (sorted lats, K, N, pd). Grammar-lats construction rules verified against
published lats columns (spin4 ladder(s)=[0,s/5..s] vs spin5 [0,3,6,9,12,15]; cohort=[0,0,0,s,s,s]).
"""
import re, sys, json, csv
import numpy as np

WHEEL = "/home/eileen/projects/quilt-verilog/spikes/225-e1-interference-tick/wheel"
OUT = WHEEL + "/nq1-fabric-twin"
DELTA = 12
SIGMA = 8.0 / 5.0  # R0 sustained slope (knee-meta REPORT)
ARMD = "interference"

rows = []  # dicts: lats,K,N,pd,y,src,verbatim,grammar

def add(lats, K, N, pd, y, src, verbatim, grammar):
    lats = sorted(lats)
    rows.append(dict(lats=lats, K=K, N=N, pd=pd, y=y, src=src,
                     verbatim=verbatim, grammar=grammar))

def num(s):
    s = s.strip().rstrip("D")
    return float(s)

# ---- spin9 EXP1 -------------------------------------------------------------
txt = open(f"{WHEEL}/spin9-output.txt").read()
blk = txt.split("== EXP 1b")[0]
for ln in blk.splitlines():
    if "|" in ln and "/144" in ln:
        f = [x.strip() for x in ln.split("|")]
        # f: m_s | grammar | lats | K | s1..s5 | mean% | evMean | debtMean
        lats = [int(v) for v in f[2].strip("[]").split(",")]
        add(lats, int(f[3]), 6, 3, float(f[9]), "spin9-output.txt", ln.strip(), f[1])

# ---- spin5 EXP2 -------------------------------------------------------------
txt5 = open(f"{WHEEL}/spin5-output.txt").read()
blk5 = txt5.split("== EXP 2b")[0].split("== EXP 2:")[1]
for ln in blk5.splitlines():
    if "|" in ln and "[" in ln:
        f = [x.strip() for x in ln.split("|")]
        lats = [int(v) for v in f[2].strip("[]").split(",")]
        add(lats, int(f[3]), 6, 3, float(f[9]), "spin5-output.txt", ln.strip(), f[1])

# ---- spin4 MAIN + CONTROL ---------------------------------------------------
txt4 = open(f"{WHEEL}/spin4-output.txt").read()
main4 = txt4.split("== MAIN")[1].split("== CONTROL")[0]
for ln in main4.splitlines():
    if "|" in ln and ("ladder" in ln or "cohort" in ln):
        f = [x.strip() for x in ln.split("|")]
        s, K, var = int(f[0]), int(f[1]), f[2]
        lats = [round(s * i / 5) for i in range(6)] if var == "ladder" else [0]*3 + [s]*3
        add(lats, K, 6, 3, float(f[8]), "spin4-output.txt", ln.strip(), f"{var}@{s}")
ctrl4 = txt4.split("== CONTROL")[1].split("== REFERENCE")[0]
for ln in ctrl4.splitlines():
    if "|" in ln and "[" in ln:
        f = [x.strip() for x in ln.split("|")]
        lats = [int(v) for v in f[2].strip("[]").split(",")]
        add(lats, int(f[1]), int(f[0]), 3, float(f[3]), "spin4-output.txt", ln.strip(), "ladder@30")

# ---- spin11 EXP1 pd x N grid (K=1) -----------------------------------------
txt11 = open(f"{WHEEL}/spin11-output.txt").read()
g11 = txt11.split("== EXP 1: pd x N sweep")[1].split("wall edge location")[0]
NS = [2, 3, 4, 5, 6, 7, 8, 12, 13, 24, 25]
grid11 = {}
for ln in g11.splitlines():
    m = re.match(r"\s+(\d+) \|\s*(.+)", ln)
    if m and ln.count("|") >= 10:
        pd = int(m.group(1))
        cells = [c for c in ln.split("|")[1:]]
        if len(cells) >= 11:
            for N, c in zip(NS, cells):
                grid11[(pd, N)] = num(c)
# ladder lats over [0,30] with N points, round-half-up (verified: pd2/N5 -> [0,8,15,22,30])
def ladder30(N):
    out = [round(30 * i / (N - 1)) for i in range(N)]  # banker's rounding (pd2/N5: 7.5->8, 22.5->22)
    out[-1] = 30
    return out
VERIF = {  # published lats (spin11 canary section) — construction must match
    (1, 2): [0, 30], (1, 3): [0, 15, 30], (2, 4): [0, 10, 20, 30],
    (2, 5): [0, 8, 15, 22, 30], (3, 6): [0, 6, 12, 18, 24, 30],
    (3, 7): [0, 5, 10, 15, 20, 25, 30],
}
for k, v in VERIF.items():
    assert ladder30(k[1]) == v, (k, ladder30(k[1]), v)
for (pd, N), y in sorted(grid11.items()):
    ver = "published-lats" if (pd, N) in VERIF else "constructed-lats(verified-rule)"
    add(ladder30(N), 1, N, pd, y, "spin11-output.txt",
        f"pd={pd} N={N} true12={y}", f"ladder30@pd{pd}")
print(f"raw rows: {len(rows)}; spin11 cells: {len(grid11)}", file=sys.stderr)

# ---- dedupe -----------------------------------------------------------------
seen, dedup = {}, []
for r in rows:
    key = (tuple(r["lats"]), r["K"], r["N"], r["pd"])
    if key in seen:
        seen[key]["src"] += ";" + r["src"]
        # cross-source agreement check
        assert abs(seen[key]["y"] - r["y"]) < 0.051, (key, seen[key]["y"], r["y"])
    else:
        seen[key] = r
        dedup.append(r)
rows = dedup
print(f"deduped rows: {len(rows)}", file=sys.stderr)

# ---- features ---------------------------------------------------------------
def feats(r):
    lats, N, K, pd = r["lats"], r["N"], r["K"], r["pd"]
    span = lats[-1] - lats[0]
    thr = DELTA / 2.0
    m_s = sum(max(0, x - thr) for x in lats) / (N * (30 - thr))
    fresh = sum(1 for x in lats if x <= thr)
    mean_l = sum(lats) / N
    var_l = sum((x - mean_l) ** 2 for x in lats) / N
    rcoord = span * SIGMA / (2 * DELTA)
    mcoord = N / (2 * pd + 1)
    return dict(span=span, N=N, K=K, log2K=np.log2(K), pd=pd, m_s=m_s,
                fresh=fresh, mean_lag=mean_l, std_lag=var_l ** 0.5,
                max_lag=lats[-1], min_lag=lats[0],
                r=rcoord, m=mcoord)

FEATS_BASE = ["span", "N", "K", "log2K", "pd", "m_s", "fresh", "mean_lag",
              "std_lag", "max_lag", "min_lag"]

hdr = ["row_id", "grammar", "lats", "K", "N", "pd", "true_pct", "src", "verbatim"] + \
      FEATS_BASE + ["r", "m"]
with open(f"{OUT}/dataset.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(hdr)
    for i, r in enumerate(rows):
        f = feats(r)
        w.writerow([i, r["grammar"], str(r["lats"]), r["K"], r["N"], r["pd"],
                    r["y"], r["src"], r["verbatim"]] +
                   [round(f[k], 6) for k in FEATS_BASE + ["r", "m"]])

# ---- models (numpy only) ----------------------------------------------------
y = np.array([r["y"] for r in rows])
F = {k: np.array([feats(r)[k] for r in rows]) for k in FEATS_BASE + ["r", "m"]}

def law_X(idx):
    """Two-constant-law design: thresholds FIXED at r=1, m=1; levels fitted (OLS).
    Law content = knee locations; 3 fitted plateau levels are scale calibration."""
    return np.column_stack([np.ones(len(idx)),
                            (F["r"][idx] >= 1.0).astype(float),
                            (F["m"][idx] >= 1.0).astype(float)])

def ridge_X(names, idx):
    M = np.column_stack([F[k][idx] for k in names])
    mu, sd = M.mean(0), M.std(0) + 1e-12
    return (M - mu) / sd, mu, sd

def fit_ridge(Z, yv, lam):
    A = Z.T @ Z + lam * np.eye(Z.shape[1])
    return np.linalg.solve(A, Z.T @ yv)

def quad(Z):
    n = Z.shape[1]
    cols = [Z]
    for i in range(n):
        for j in range(i, n):
            cols.append((Z[:, i] * Z[:, j])[:, None])
    return np.hstack(cols)

MODELS = {
    "median": None,
    "law(r=1,m=1)": "LAW",
    "ridge-linear": FEATS_BASE,
    "ridge-linear+rm (NQ-2)": FEATS_BASE + ["r", "m"],
    "ridge-quad": "QUAD:" + ",".join(FEATS_BASE),
}
LAM = 10.0  # booked; sensitivity at 1/100 reported

rng = np.random.default_rng(1)
perm = rng.permutation(len(rows))
# stratified deal: shuffle, sort by y within shuffled order, deal round-robin ->
# each fold spans the outcome range (regime balance; unstratified folds were pathological)
srt = sorted(perm, key=lambda i: y[i])
folds = [srt[i::5] for i in range(5)]

res = {k: {"err": [], "sq": [], "raw": []} for k in MODELS}
order = np.concatenate(folds)
per_fold = []
for fi, te in enumerate(folds):
    tr = np.setdiff1d(order, te)
    Xl = law_X(tr); wl, *_ = np.linalg.lstsq(Xl, y[tr], rcond=None)
    preds = {"median": np.full(len(te), np.median(y[tr])),
             "law(r=1,m=1)": law_X(te) @ wl}
    Ztr, mu, sd = ridge_X(FEATS_BASE, tr)
    Zte = (np.column_stack([F[k][te] for k in FEATS_BASE]) - mu) / sd
    preds["ridge-linear"] = Zte @ fit_ridge(Ztr, y[tr], LAM)
    names2 = FEATS_BASE + ["r", "m"]
    Z2tr, mu2, sd2 = ridge_X(names2, tr)
    Z2te = (np.column_stack([F[k][te] for k in names2]) - mu2) / sd2
    preds["ridge-linear+rm (NQ-2)"] = Z2te @ fit_ridge(Z2tr, y[tr], LAM)
    Qtr, Qmu = quad(Ztr), None
    qcoef = fit_ridge(quad(Ztr), y[tr], LAM)
    preds["ridge-quad"] = quad(Zte) @ qcoef
    fold = {}
    for k, p in preds.items():
        e = y[te] - p
        res[k]["err"].extend(np.abs(e)); res[k]["sq"].extend(e ** 2)
        res[k]["raw"].extend(zip([int(t) for t in te], np.abs(e).tolist()))
        fold[k] = (float(np.mean(np.abs(e))), float(np.sqrt(np.mean(e ** 2))))
    per_fold.append(fold)

lines = []
lines.append("NQ-1 fabric-twin — 5-fold CV (seed 1, rows shuffled once), metric = |error| in pp")
lines.append(f"n rows = {len(rows)}   folds = 5   lambda = {LAM} (ridge)")
lines.append("")
lines.append(f"{'model':26s} {'MAE pp':>8s} {'RMSE pp':>8s} {'R2':>7s}")
ss = float(np.mean((y - y.mean()) ** 2))
summary = {}
for k in MODELS:
    e = np.array(res[k]["err"]); q = np.array(res[k]["sq"])
    r2 = 1 - q.mean() / ss
    summary[k] = (e.mean(), np.sqrt(q.mean()), r2)
    lines.append(f"{k:26s} {e.mean():8.2f} {np.sqrt(q.mean()):8.2f} {r2:7.3f}")
law_mae = summary["law(r=1,m=1)"][0]
lin_mae = summary["ridge-linear"][0]
quad_mae = summary["ridge-quad"][0]
lines.append("")
lines.append(f"PASS check (pre-reg: learned beats law by >2pp on held-out): "
             f"linear margin = {law_mae - lin_mae:+.2f}pp, quad margin = {law_mae - quad_mae:+.2f}pp")
# per-config wins: held-out configs where quad beats law, and by >2pp each
raw_law = dict(res["law(r=1,m=1)"]["raw"]); raw_q = dict(res["ridge-quad"]["raw"])
wins = sum(1 for i in raw_law if raw_q[i] < raw_law[i])
wins2 = sum(1 for i in raw_law if raw_q[i] < raw_law[i] - 2.0)
lines.append(f"per-config: quad beats law on {wins}/{len(raw_law)} held-out configs; "
             f"by >2pp each on {wins2}")
for fi, f in enumerate(per_fold):
    lines.append(f"  fold {fi}: law MAE {f['law(r=1,m=1)'][0]:.2f}  quad MAE {f['ridge-quad'][0]:.2f}  "
                 f"linear MAE {f['ridge-linear'][0]:.2f}")

# NQ-2: residual variance collapse when r,m added
rssA = np.mean(np.array(res["ridge-linear"]["sq"]))
rssB = np.mean(np.array(res["ridge-linear+rm (NQ-2)"]["sq"]))
drop = 1 - rssB / rssA
lines.append("")
lines.append(f"NQ-2 rider: RSS drop adding r,m to ridge-linear = {drop*100:.1f}% "
             f"(pass bar >50%) -> {'PASS' if drop > 0.5 else 'FAIL'}")
lines.append(f"(collinearity note: in this corpus sigma, delta constant -> r == span/15 exactly; "
             f"corr(span, r) = {np.corrcoef(F['span'], F['r'])[0,1]:.4f}; "
             f"m = N/(2pd+1) is a genuine interaction)")
# sensitivity: lambda 1 and 100 for the linear twin
for lam2 in (1.0, 100.0):
    es = []
    for te in folds:
        tr = np.setdiff1d(order, te)
        Ztr, mu, sd = ridge_X(FEATS_BASE, tr)
        Zte = (np.column_stack([F[k][te] for k in FEATS_BASE]) - mu) / sd
        p = Zte @ fit_ridge(Ztr, y[tr], lam2)
        es.extend(np.abs(y[te] - p))
    lines.append(f"sensitivity lambda={lam2:g}: ridge-linear MAE = {np.mean(es):.2f}pp")

# ---- D2: knee-position mini-test (spin21 knee relocation, n=7) --------------
# rows: (sigma, published knee, law prediction 2*delta/sigma or None)
k21 = [(1.6, 14, 15), (1.6, 20, 15), (1.6, 14, 15), (0.0, 27, None),
       (1.0, 27, 24), (2.0, 10, 12), (1.6, 14, 15)]
sub = [(s, k, p) for s, k, p in k21 if p is not None]
law_err = [abs(k - p) for s, k, p in sub]
# LOO linear knee ~ a + b*sigma (numpy OLS)
loo = []
pts = [(s, k) for s, k, p in sub]
for i in range(len(pts)):
    trp = [q for j, q in enumerate(pts) if j != i]
    X = np.array([[1, s] for s, k in trp]); yy = np.array([k for s, k in trp])
    w, *_ = np.linalg.lstsq(X, yy, rcond=None)
    loo.append(abs(pts[i][1] - (w[0] + w[1] * pts[i][0])))
lines.append("")
lines.append("D2 knee mini-test (SPIN-21 knee relocation, n=7, R3 sigma=0 law n/a excluded):")
lines.append(f"  law (knee=2D/sigma) MAE = {np.mean(law_err):.2f} ticks; "
             f"LOO linear twin MAE = {np.mean(loo):.2f} ticks (n=6, below trainable bar)")

open(f"{OUT}/results.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
# also dump per-fold table
with open(f"{OUT}/per-fold.txt", "w") as fh:
    for i, f in enumerate(per_fold):
        fh.write(f"fold {i}: " + "  ".join(f"{k}={v[0]:.2f}" for k, v in f.items()) + "\n")
print("\nDONE", file=sys.stderr)
