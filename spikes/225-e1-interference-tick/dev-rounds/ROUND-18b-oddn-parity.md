# ROUND 18b — odd-n parity cell (pre-registered 7231ce0, DEVIL nudge): round 18 scoped to "this trio, even n" — and the odd-n D/P tie genuinely breaks at seed 42

**Verdict: G-FORM FAIL, G-TIE FAIL as pre-registered. Round 18's theorem is now stated "closed for even n, this trio" — both corrections DEVIL asked for, on the theorem's face.**

## What ran

m ∈ {15, 17} (odd; round 18's grid m ∈ {4,6,8,10,12,16} was even-only), groups Z/D/P, ARM A control + ARM B five fleet seeds, round-18 instrument imported verbatim (K_MAX=288, same ρ̂/brackets, same LCG masks).

## Findings

1. **The D/P tie breaks at odd n, seed 42 — the real discovery.** Gap 0.116 (m=15) / 0.090 (m=17), against ≤2e-4 on the entire even grid and a Δ_null of 1/256. The +1.2% estimator bracket bound (ln n / K) cannot explain a 9–12% gap at fixed seed. Whatever forced ρ(D)=ρ(P) on even n (abelianization saturation through the 4-character subring) does **not** operate at odd n, where D_m abelianizes to ℤ₂ (2 characters, since [D_m,D_m]=⟨r²⟩ has index 2). DEVIL's parity mechanism was not just a doc creak — it predicted exactly where the result would live.
2. **The closed forms do not verify at odd n under the pre-registered tolerance.** All mismatches sit within ~0.6% of the forms (e.g. Z seed 1999: ρ̂=2.012 vs form 2.0), which is estimator-resolution-consistent — but "consistent with" is not "verified," and the pre-reg booked it FAIL without a rescue clause. Honest status: forms *plausible* at odd n, *proven* only at even n.
3. ARM A control tied at 7 on all six odd cells — harness comparable, verdict licensable.

## Consequences

- ROUNDS.md headline and round-18 verdict line re-scoped: "for this trio (ℤ_n, D_n, ℤ_n×ℤ₂), at even n." The class-sized "virtually-cyclic" claim is withdrawn — ℤ_n×ℤ₂ was never representative of that class, and the saturation proof does not transfer (no ℤ²-by-finite, no nontrivial ℤ-semidirect products were analyzed).
- The broken seed-42 tie is **the first candidate genuine D-vs-P spectral separation** in the program — on exactly the fabrics where the round-18 theorem said the ρ route was dead. That theorem survives as "dead at even n"; odd n is open. Named next rung: larger-K adjudication of the seed-42 gap (|τ_k| differs by ≈7× at k=288 — subdominant-tail plausible, so this needs exact tail control, e.g. char-poly/rank arguments or K ≥ 1000) plus the odd-n closed-form derivation from the 2-character subring.

Raw: `r18b-oddn-output.txt` (sha256 in stderr capture). Pre-registration verbatim in the script header.
