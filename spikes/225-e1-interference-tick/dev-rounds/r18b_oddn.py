#!/usr/bin/env python3
"""ROUND 18b (pre-registration) -- the odd-n parity cell (DEVIL nudge).

DEVIL's two creaks on round 18 (a69bd1c), both verified real:
(1) SCOPE: grid was m in {4,6,8,10,12,16} -- ALL EVEN.  The closed
    forms rho(Z)=|ce|+|cr+cs|, rho(D)=rho(P)=|ce|+|cr|+|cs| were
    verified (90/90) on even n only.
(2) MECHANISM: D_m abelianization is Z2 x Z2 for EVEN m (since
    [D_m,D_m] = <r^2> of index 4) but Z2 x Z_m/<r^2> = Z2 for ODD m
    (<r^2> = <r>, index 2).  The abelianization-saturation argument
    that "aligns any mask signs" rests on the 1-dimensional
    characters; odd D_m has TWO of them, not FOUR.  So odd n is
    outside both the proof and the grid.

This run closes or re-opens the parity cell: m in {15, 17} (odd),
groups Z/D/P, ARM A control (mask 3,2,2, rho must be 7) + ARM B
(five fleet seeds, same LCG masks), same K_MAX/rho_hat/brackets,
imported verbatim from r18_spectra.

Pre-registered decision rule (frozen before any run):
  G-FORM: for every odd-(m,seed) cell, rho_hat(D) and rho_hat(P)
    each match |ce|+|cr|+|cs| within the round-18 bracket tolerance
    (1e-3 relative, same as C4), and rho_hat(Z) matches
    |ce|+|cr+cs| likewise.
  G-TIE: |rho(D) - rho(P)| <= 1/256 (round-18 D_NULL) in every
    odd-(m,seed) cell.
  If G-FORM and G-TIE both hold: the parity cell CLOSES -- the
    round-18 forms and D/P tie extend to odd n, and the headline
    gains "(n odd and even)" with the mechanism note that the
    saturation argument runs on the 2-char subring for odd m.
  If either fails: the round-18 theorem statement gains a parity
    hypothesis ON ITS FACE ("for even n"), the doc's 'closed'
    becomes 'closed for even n', and the failing cells are booked
    as the next rung (odd-n spectra are genuinely different).
  ARM A must tie at 7 on odd m or the harness is non-comparable and
  no verdict is booked.
"""
import hashlib
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from r18_spectra import (cell, rho_hat, circulant_rho, lcg_mask, ARM_A,
                         SEEDS, K_MAX)
import r18_spectra as r18

MS_ODD = (15, 17)
D_NULL = 1 / 256


def main():
    out = []
    w = out.append
    w(f"== ROUND 18b odd-n parity cell: m={MS_ODD} K_MAX={K_MAX} seeds={SEEDS} ==")
    masks = {s: lcg_mask(s) for s in SEEDS}

    okA = True
    for m in MS_ODD:
        for g in ("Z", "D", "P"):
            c = cell(m, g, ARM_A)
            rh, _ = rho_hat(c["sigmas"], c["n"])
            if not (rh / (c["n"] ** (1.0 / (2 * K_MAX))) - 1e-9
                    <= 7.0 <= rh + 1e-9):
                okA = False
            w(f"A {g} m={m} tau_1={c['taus'][0]} U={c['U']} rho_hat={round(rh,6)}")
    w(f"ARM A control (rho=7 all odd cells): {'PASS' if okA else 'FAIL -> no verdict'}")
    if not okA:
        text = "\n".join(out) + "\n"
        sys.stdout.write(text)
        return

    gform = gtie = True
    for m in MS_ODD:
        for s in SEEDS:
            an = {g: None for g in "ZDP"}
            an["Z"] = circulant_rho(m, masks[s])
            ce, cr, cs = masks[s]
            an["D"] = an["P"] = float(abs(ce) + abs(cr) + abs(cs))
            r = {}
            for g in "ZDP":
                c = cell(m, g, masks[s])
                rh, k = rho_hat(c["sigmas"], c["n"])
                r[g] = rh
                tol = 1e-3 * an[g]
                ok = abs(rh - an[g]) <= tol
                if g in "DP" and not ok:
                    gform = False
                if g == "Z" and not ok:
                    gform = False
                w(f"B m={m} seed={s:9d} {g} rho_hat={rh:.6f} form={an[g]:.6f} "
                  f"{'ok' if ok else 'MISMATCH'}")
            if abs(r["D"] - r["P"]) > D_NULL:
                gtie = False
                w(f"  D/P gap {abs(r['D']-r['P']):.6f} > D_NULL -- TIE BROKEN")
            else:
                w(f"  D/P gap {abs(r['D']-r['P']):.6f} <= D_NULL")
    w(f"G-FORM (closed forms hold on odd n): {'PASS' if gform else 'FAIL'}")
    w(f"G-TIE (D/P within 1/256 on odd n): {'PASS' if gtie else 'FAIL'}")
    if gform and gtie:
        w("VERDICT: parity cell CLOSED -- round-18 forms + D/P tie extend to odd n; "
          "headline may say '(n even and odd) for this trio', mechanism note: "
          "saturation runs on the 2-char subring for odd m.")
    else:
        w("VERDICT: round-18 theorem gains a parity hypothesis ON ITS FACE -- "
          "'closed for even n'; failing odd cells are the next rung.")

    text = "\n".join(out) + "\n"
    sys.stdout.write(text)
    with open("r18b-oddn-output.txt", "w") as f:
        f.write(text)
    print(f"[sha256 self] {hashlib.sha256(text.encode()).hexdigest()}", file=sys.stderr)


if __name__ == "__main__":
    main()
