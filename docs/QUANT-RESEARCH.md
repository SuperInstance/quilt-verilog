# QUANT-RESEARCH — quantization lane for quilt-verilog v1

2026-08-29, quantization research lane (Flash, extensive). Answers: *which of
GGML's schemes and the 2024-2026 PTQ wave are pure-RTL-friendly (fixed-point,
integer scales only), what the accuracy-per-bit evidence is, what deployed edge
accelerators actually do, and what Q-scheme each v1 primitive should use.*
Companion RTL: `rtl/q_hebb_edge.v`, `rtl/q_dialfile.v`; doctrine in
`docs/DOCTRINE.md` ("quantization IS the algorithm"), formats in
`docs/SYNTHESIS.md`.

`docs/ABSTRACTION-MATH.md` does not exist yet; §6 is the seed for it.

---

## 1 — What v1 already is, quantization-wise

| Primitive | Current form (rtl/) | Quantization status |
|---|---|---|
| Dial | 16-bit Q-format registers, saturate-never-wrap (ETA_F `0x0800` = 0.0625, THRESH `0x6000` = 0.75) | Fixed-point by construction; dials *are* scales |
| Edge base | PW=16 integer, added to readout (`o_w = saturate(base + engine)`) | Exactly representable — zero error |
| Walk-count ladder | K=8 buckets × B=8 bits; bucket *i* carries implied weight `2^-i`; fresh cofire reads 256; proven 2× dyadic envelope | Already a quantization scheme: power-of-two histogram = block-floating-point |
| Cosine accumulator | Not provisioned in v1 (`view(3)` NAKs); `COS_MIN` dial reserved | Open question — this is where the research lands |

The ladder is the pleasant surprise: it is *already* the RTL-native quantizer —
the scale is implicit in the bucket→bit-offset mapping, dequant is a
shift-and-add with zero multiplies, and the state is integers that never drift.
The research below mostly *validates* it and tells us what to add, not what to
replace.

## 2 — GGML/k-quants: what they are, and what translates to RTL

### The block layouts (from ggml source, `src/ggml-common.h`)

- **Legacy family (QK=32 per block):** Q4_0 = fp16 `d` + nibbles (4.5 bpw);
  Q4_1 = fp16 `d` + fp16 `m` (min/offset, 5.5 bpw); Q5_0/Q5_1 add a 4-byte
  high-bit mask (5.5/6.5 bpw); Q8_0 = fp16 `d` + int8 payload (8.5 bpw);
  Q8_1 = fp16 `d` + fp16 `m` + int8. Dequant is `d*q` (+`m`).
- **K-quant family (super-block QK_K=256, hierarchical):**
  - Q2_K: 16 sub-blocks of 16; scales **and mins quantized to 4 bits**; fp16
    super-block `d`/`dmin`; `x = a*q + b`; 2.625 bpw.
  - Q3_K: 16×16; **6-bit scales**, no min; fp16 `d`; 3.4375 bpw.
  - Q4_K: 8 sub-blocks of 32; **6-bit scales+mins** in 12 bytes; fp16 `d`/`dmin`;
    4.5 bpw. Q5_K = Q4_K + high-bit mask, 5.5 bpw.
  - Q6_K: 16×16; **8-bit (int8) scales**, no min; fp16 `d`; 6.5625 bpw.
  - Q8_K: fp32 `d` + int8 + int16 bsums — **intermediate dot-product form
    only, never a file format.**
- **i-quants (importance-matrix quants):** IQ2_XXS/XS/S, IQ3_XXS/XS/S, IQ4_XS,
  IQ4_NL, IQ1_S/M. Sub-4-bpw group codes **4 or 8 weights via E8/D4 lattice
  codebooks** (idea from QuIP#, also AQLM); fp16 `d` per 256-super-block;
  ~2.06–4.56 bpw. IQ4_NL uses a *non-linear* codebook (LUT of 16 int8 values).
- **IQK (ikawrakow's fork, `ik_llama.cpp`):** IQ2_K/IQ3_K/IQ4_K/IQ5_K — k-quant
  *structure* + non-linear per-weight mapping via tiny LUTs (4/8/16/32 int8
  entries) instead of lattice codebooks; SIMD-register-friendly
  (`_mm256_shuffle_epi8`), nearly same speed as linear k-quants.
- **MXFP4 (ggml, OCP microscaling):** one E8M0 exponent byte (power-of-2 scale)
  + 4-bit payloads per 32-block; NVFP4 variant has UE4M3 scales per 16-element
  sub-block. Scale is `2^e` — **a shift, not a multiply.**

### The translation verdict (RTL lens)

Nothing in GGML is *literally* integer-only: every family carries fp16 block
scales. But every scheme decomposes the same way:

> **integer payload + integer/quantized scale metadata + one float per block
> (or super-block).**

The RTL-native move is to replace that last float with an integer power-of-2
exponent — block-floating-point. That is exactly what Gemmini's optional
power-of-2 scaling does, what OCP MX E8M0 standardizes, and what the v1 ladder
already does implicitly. **Q4_0/Q8_0's fp16 `d` is the single reason the legacy
family is not RTL-direct; the payloads themselves are.**

Ranking by translation cost to pure fixed-point RTL:

| Family | Payload | Scale bits | RTL verdict |
|---|---|---|---|
| Q8_0 | int8 | fp16 → replace with `2^k` | Direct after scale swap. The hardware consensus format (§4) |
| Q4_K/Q5_K | nibbles | 6-bit scales/mins + fp16 super-`d` → int exponent | Direct *structurally*: quantized scale metadata is already integer; hierarchical scales are the key idea |
| Q6_K | 4+2-bit | int8 scales + fp16 `d` → int exponent | Direct; int8 scales are already integer |
| Q4_0 legacy | nibbles | fp16 | Superseded; single 32-block scale is the accuracy weak point k-quants fixed |
| IQ* | codebook indices | fp16 + E8/D4 LUT | LUT cost is fine in silicon, wasteful at cell scale; value is sub-4-bpw only |
| IQK (non-linear) | 2-5 bit + tiny LUT | int | The RTL-friendly version of i-quants if we ever go sub-4-bit |
| TQ1_0/TQ2_0 | ternary | fp16 | Too coarse for similarity scoring; reject |
| MXFP4 | 4-bit mantissa | E8M0 shared exponent | Adopt the *shared-exponent* idea; reject the float mantissa (doctrine: no fp escape hatch) |

### Accuracy-per-bit evidence on real workloads

**Origin data, LLaMA-7B, WikiText-2 PPL (llama.cpp PR #1684, ikawrakow 2023):**

| Scheme | bpw | PPL | vs F16 |
|---|---|---|---|
| F16 | 16 | 5.9066 | — |
| Q2_K | 2.625 | 6.7764 | +14.7% |
| Q3_K_S | 3.4375 | 6.4571 | +9.3% |
| Q3_K_M | 3.5 | 6.1503 | +4.1% |
| Q4_K_S | 4.5 | 6.0215 | +1.9% |
| Q5_K_S | 5.5 | 5.9419 | +0.6% |
| Q6_K | 6.5625 | 5.9110 | **+0.074% (≈ lossless)** |

**Canonical KL-divergence table, Mistral-7B (artefact2 gist, 2024-02; imatrix
from wiki.train, KL on wiki.test):**

| Scheme | bpw | KL med | ln(PPL(Q)/PPL(base)) |
|---|---|---|---|
| IQ1_S | 1.78 | 0.5495 | 0.9235 |
| IQ2_XXS | 2.20 | 0.1751 | 0.2988 |
| IQ2_XS | 2.43 | 0.1146 | 0.2046 |
| Q2_K | 3.00 | 0.0588 | 0.1103 |
| IQ3_XXS | 3.21 | 0.0330 | 0.0589 |
| Q3_K_S | 3.50 | 0.0304 | 0.0511 |
| IQ3_S | 3.52 | 0.0205 | 0.0306 |
| Q3_K_M | 3.89 | 0.0171 | 0.0258 |
| IQ4_XS | 4.32 | 0.0088 | 0.0079 |
| IQ4_NL | 4.56 | 0.0085 | 0.0074 |
| Q4_K_S | 4.57 | 0.0083 | 0.0081 |
| Q4_K_M | 4.83 | 0.0075 | 0.0060 |
| Q5_K_S | 5.52 | 0.0045 | 0.0005 |
| Q5_K_M | 5.67 | 0.0043 | 0.0005 |
| Q6_K | 6.57 | 0.0032 | **−0.0008** |

Reads: (a) i-quants win sub-4-bpw by a wide margin (codebook + imatrix), but at
4+ bpw Q4_K ≈ IQ4 — the k-quant structure is the 4-bit sweet spot; (b) Q6_K is
statistically indistinguishable from fp16; (c) KL (an output-distribution
measure, like our similarity scoring) degrades smoothly with bpw — the
accuracy-per-bit curve is monotone in practice, with super-linear gains at
5-6 bpw.

**Modern model, Llama-3.1-8B-Instruct, 5 benchmarks + PPL (arXiv 2601.14277,
Jan 2026):**

| Scheme | bpw | Avg (5 tasks) | Δ vs F16 | PPL |
|---|---|---|---|---|
| F16 | 16 | 69.47 | — | 7.32 |
| Q3_K_S | 3.4 | 65.49 | −5.73% | 8.96 |
| Q3_K_M | 3.5 | 68.07 | −2.02% | 7.96 |
| Q3_K_L | 3.6 | 68.78 | −0.99% | 7.81 |
| Q4_0 | 4.5 | 67.98 | −2.14% | 7.74 |
| Q4_K_S | 4.2 | 69.17 | **−0.43%** | 7.62 |
| Q4_K_M | 4.5 | 69.15 | −0.46% | 7.56 |
| Q5_0 | 5.5 | 69.92 | **+0.65%** (best) | 7.43 |
| Q6_K | 6.5 | 69.23 | −0.35% | 7.35 |
| Q8_0 | 8.5 | 69.41 | −0.09% | 7.33 |

Pareto frontier of the paper: Q5_0 → Q4_K_S → Q3_K_L → Q3_K_M → Q3_K_S
(Q6_K and Q8_0 are *dominated* — more bits, no quality win). GSM8K (multi-step
reasoning) is the most quantization-sensitive task; HellaSwag barely moves at
any bpw. Lesson for us: *task structure matters more than bit width* — a
firing/similarity decision is a "HellaSwag-style" stable readout, whereas
integrating values over time (our ladders) is a "GSM8K-style" accumulation that
wants the good schemes at 4+ bpw.

**LLaMA-3-era difficulty shift (ikawrakow, ik_llama.cpp discussion #8):**
quantization error QError = PPL(Q)/PPL(fp16) − 1. LLaMA-3.1-70B runs ~1 bpw
"ahead" of LLaMA-v2-70B — newer models carry more information per weight, so
every scheme's error roughly doubles at fixed bpw (Q6_K: 0.65% on LLaMA-3.1 vs
0.1–0.15% on LLaMA-v2; Q8_0 still matches fp16). IQ4_K: 2.7× lower QError than
Q4_0, 40% lower than Q4_K_S; IQ5_K: 2.1× vs Q5_0. Takeaway: budget for the
model generation, not the paper's.

### The importance matrix — and why it's free for RTL

The imatrix is a per-element importance weight computed **offline** from
activation statistics over a calibration corpus; quantization-time solvers
(Q4_K/IQ* with `--imatrix`) minimize *weighted* error so bits are spent on
elements that matter at inference. Runtime cost: zero — the weights are already
chosen when the file is written. This is the cheapest possible "AWQ-flavored"
insight and it transfers to our QUF writer (Python reference): *weight the
ladder increments and any cosine scale selection by activation magnitude at
quantization/bind time, not in the fabric.*

## 3 — The 2024-2026 PTQ wave: what transfers to streaming INT similarity in hardware

| Method | Idea | Transfers to our hardware? |
|---|---|---|
| GPTQ (2210.17323) | Layer-wise, Hessian-based second-order error compensation | Not directly (second-order info + iteration is offline); the *spirit* — compensate where error hurts — transfers as imatrix-style weighting. Our ladder's weighted cofire is the streaming analogue |
| AWQ (2306.00978) | Protect ~1% salient *channels* via per-channel scaling; activation-observed, not weight-observed | **Yes, cheaply**: per-dimension scale registers on the cosine engine. Salience is a scale, not a special datapath |
| SmoothQuant (2211.10438) | Migrate activation outliers into weights offline (mathematically equivalent transform); enables W8A8 | **Yes**: normalize embeddings at ingest (RMS→shift) so the streaming dot product never sees outliers. Cost: one shift per vector write |
| QuaRot (2404.00456) | Random Hadamard rotation removes outliers everywhere; W4A4+KV4 end-to-end | Partially: rotation is *the* outlier fix, but a bit-exact fixed-point orthogonal transform must be consistent across cells — real cost. Defer to v3; at 8-bit + per-channel scales the marginal gain is small (below) |
| SpinQuant (2405.16406) | *Learned* rotations (Cayley SGD); random rotations vary by up to 13 accuracy points; closes gap to fp16 by up to 45.1% vs QuaRot (LLaMA-3 8B, 4-bit) | Same deferral; the "rotation choice matters" warning applies if we ever do 4-bit embeddings |
| OCP MX / MXFP4, NVFP4 | Shared E8M0 power-of-2 exponent per block + tiny mantissas | **Adopt the shared-exponent structure** (block-floating-point scale = shift); reject float mantissas (doctrine) |
| i-quant codebooks (E8/D4), IQK non-linear LUTs | Sub-4-bpw fidelity | Only if cosine goes ≤4-bit; IQK's tiny-LUT form is the RTL-friendly one |

What the wave converges on, in one line: **outliers are the entire problem;
you fix them with scales (AWQ, SmoothQuant), rotations (QuaRot, SpinQuant), or
better block structure (k-quants, imatrix) — and in hardware, scales that are
shifts are free while rotations and lookups are not.** For 8-bit-or-below
*streaming* similarity scoring specifically: per-dimension scales + ingest
normalization + wide accumulator buys ~90% of the outlier fix at near-zero RTL
cost; rotations are the v3 tail.

## 4 — Hardware precedent: what deployed edge accelerators do

| Accelerator | Datapath | Accumulator | Scaling | Why |
|---|---|---|---|---|
| VTA (Apache TVM) | INT8×INT8 (`inpBits=8`, `wgtBits=8`) | INT32 (`accBits=32`), output requantized to INT8 | Fixed-point only, no FP in hardware; scale folded by software | Pure fixed-point keeps the datapath tiny; one post-accumulation requantize |
| Gemmini (UC Berkeley, RISC-V) | Configurable int8/int16/fp16/fp32 | INT32 default (`accType`) | Default: fp32 multiply at accumulator readout; **optional power-of-2 scaling** ("scale results down by powers-of-2"); dynamic scaling on move-in | Wide accumulator, single scale after accumulation; power-of-2 path exists precisely because it's a shift |
| NVDLA (NVIDIA, open) | int8/int16/fp16/fp32 selectable | INT32 | Per-tensor fp32 scales from compiler; precision scaling applied in the SDP stage; INT8 ResNet-50 reference config | Same consensus: INT in, wide accumulate, one scale later |
| (context) Edge TPU / EIE | INT8 symmetric (per-tensor), EIE 4-bit sparse | INT32 | Single tensor scale | The commercial version of the same pattern |

The consensus is unanimous and matches §2's decomposition:

> **Low-bit integer inputs, INT32 accumulator, ONE scale per block/tensor
> applied after accumulation — never per-MAC — with the scale owned by
> software/compiler, and power-of-2 scales when the hardware wants to save the
> multiplier.**

For a Verilog-2005 fabric with no floating point, this is the license to do
exactly what we do: integer state everywhere, scale-by-shift, saturating
outputs.

## 5 — Recommended Q-schemes per primitive (v1 decision table)

| Primitive | Scheme | Storage | RTL cost | Error bound | Rationale |
|---|---|---|---|---|---|
| **Dial (saturating)** | 16-bit Q1.15 fixed-point, **as built**; QUF gains per-dial Q-format metadata; optional U8 compressed form in QUF with per-dial scale (k-quant "quantized scales" + E8M0 idea) | 16b (8b compressed) | none | ≤ 2^-15 rounding, saturation bounded by construction | Dials are *scales*, not data; AWQ says scales deserve protection, not precision games. Keep width; make format travel with the state file |
| **Edge base** | 16-bit integer, **as built** | 16b | none | exactly zero (integer) | This is the affine offset (Q4_K's `dmin`/Q4_1's `m`); asymmetric offsets are why Q2_K/Q4_K/Q5_K beat their symmetric siblings. It is already the cheap win |
| **Walk-count ladder** | K=8×B=8 power-of-2 buckets, **as built**; v1.1 addition: hierarchical epoch shift (super-block scale) for range without wider buckets; imatrix-style weighted cofire at train time | 64b/edge | none (dequant = shift-add) | proven 2× dyadic envelope; random-walk noise σ ∝ √(cofires) | The ladder IS block-floating-point quantization with implicit scale — the RTL-native end state that Q6_K/Q8_0 evidence says is ≈lossless at 6-8 "effective bits". Q6_K's int8 scales → our B=8 counters |
| **Cosine accumulator** (v2, `COS_MIN` reserved) | INT8 symmetric inputs, per-16-element power-of-2 block scale (2^k, E8M0-style), INT32 accumulator, one final scale+normalize | 8b+2b/elt | 1 shift per scale, 1 wide adder | affine-arithmetic bound: Σ per-product 2^-7 rounding + accumulator truncation; see §6 | The VTA/Gemmini/NVDLA consensus shape, made integer-only. AWQ per-dim scales + SmoothQuant ingest normalization handle outliers; rotations deferred |

### Why these and not the exotic ones

- **Q6_K-equivalence is the ceiling we already hit.** The ladder's 2× dyadic
  envelope on a real cofire stream is the same guarantee Q6_K gives a real LLM
  (PPL +0.07% — indistinguishable), at pure-integer cost. Nothing in the k-quant
  family would improve an edge weight's readout; the family's actual lessons are
  *structural* (hierarchical scales, quantized scale metadata, offline
  importance) and we take those as v1.1 reservations, not v1 changes.
- **INT8+shift is the only scheme the three open accelerators converge on** for
  streaming dot products — the cosine engine should not innovate where VTA,
  Gemmini, and NVDLA all agree.
- **Everything we recommend is a power of two or an integer** — no fp32 scales,
  no fp16 anywhere, satisfying the doctrine's "no floating-point escape hatch".

## 6 — Error analysis method (seed for docs/ABSTRACTION-MATH.md)

Method: **interval arithmetic (IA) envelopes now; affine arithmetic (AA) for
the cosine accumulator; saturation as a first-class interval event.** This is
the formalization of what the v1 TBs already do — `tb/tb_hebb_edge.v` asserts
the hyperbolic readout inside a `[1,4)×` interval envelope and the ladder inside
the dyadic `[W/2−1, 2W+1]` envelope; `tb/tb_fabric_smoke.v` asserts exact
integer equality on the unshifted ladder. (docs/ABSTRACTION-MATH.md does not
exist; this section is its seed.)

Per primitive:

1. **Dial:** values are constants with a declared Q-format; error = rounding
   ≤ 2^-F (F = fractional bits), saturation events counted as interval
   truncation to the format's max. Envelope is exact and trivial.
2. **Edge base:** integer — identity interval; no error terms.
3. **Ladder:** every event lands in bucket `floor(age/HL)` or
   `floor(age/HL)+1` (phase ambiguity — exactly the ±1 class the dyadic
   envelope allows). The proven 2× envelope IS the IA result; keep it as the
   contract. Add the random-walk term for *noise* (not worst case): after N
   cofires with per-event weight w, readout σ ≈ w·√N (errors are
   zero-mean, variance adds — this is what makes the similarity readout stable
   in practice even though worst case is 2×).
4. **Cosine accumulator (v2):** use **affine arithmetic** — model each product
   as `x0 + Σ c_i·ε_i` with noise terms ε_i ∈ [−2^-7, 2^-7]; AA tracks the
   *correlation* between errors, which plain intervals badly overestimate in a
   sum of N products (IA grows O(N) range; AA grows O(√N) with zero-mean
   rounding, and both are sound). Final bound = accumulator truncation
   (guard bits: 32 = 2×8 + 16 headroom) + one post-scale rounding. Also keep
   the Q3 pattern: an independent golden model in the TB with asserted
   deviation, plus (for the cosine only) a Monte-Carlo pass over rounding modes
   since the operator is small enough to sweep.
5. **Saturation:** every saturating op contributes an interval truncation; the
   sticky `o_ovf` already surfaces it to the fabric top — the analysis method
   is: *each overflow is a declared, bounded, observable error event, not an
   unbounded drift* (zeroclaw rule 6: integer state never drifts).

Stretch (not on the critical path, zero-dep doctrine): Gappa-style
machine-checked bounds or exhaustive search on the 8-bit products — only if a
future lane wants proofs instead of envelopes.

## 7 — Rejected schemes and why

| Scheme | Rejected because |
|---|---|
| fp16 block scales (Q4_0/Q8_0/Q6_K `d`, k-quant super-`d` as float) | Doctrine: no fp escape hatch. The sole reason legacy GGML isn't RTL-direct. Replaced by integer/power-of-2 scales (§2) |
| Q8_K as a stored format | In GGML it is intermediate dot-product form only, never a file format; same here — the INT32 accumulator is our "Q8_K" |
| Lattice codebooks (IQ2/IQ3, E8/D4) | Value is sub-4-bpw; LUT cost at cell scale beats the payoff; sim-reference performance penalty (ikawrakow's own CPU data: i-quants 2-6× slower than IQK on CPU) |
| Rotations (QuaRot/SpinQuant) for v1/v2 cosine | Bit-exact fixed-point orthogonal transform must be consistent across all cells; at INT8 + per-dim scales + ingest normalization the marginal gain is small. Deferred to v3 with the SpinQuant variance warning (13-point spread across random rotations) |
| GPTQ-style Hessian compensation in fabric | Streaming hardware cannot iterate; offline imatrix weighting captures the same spirit at zero runtime cost |
| MXFP4/NVFP4 float mantissas (E2M1) | Tiny floats violate the fixed-point doctrine; only the shared E8M0 exponent structure is adopted |
| TQ1_0/TQ2_0 ternary | 1.5 bpw-class; below the fidelity floor for similarity scoring; no evidence at our precision needs |
| 8-bit dials | THRESH near a firing boundary needs Q1.15 granularity (2^-15); 8-bit (2^-7 ≈ 0.8%) is provably coarse at the decision edge for zero saving |
| Linear fixed-point for the walk-count ladder | Loses the logarithmic dynamic range that makes the ladder's 2× envelope possible; the ladder is already the k-quant lesson applied |

## 8 — Deferred (reserved, not built in v1)

- **v1.1:** hierarchical epoch shift on the ladder (super-block scale, Q4_K-style); imatrix-weighted cofire (weight by activation magnitude at train/bind time); QUF per-dial Q-format + compressed-dial metadata.
- **v2:** cosine engine per §5 (INT8 + 2^k block scales + INT32 accumulator), with AA error contract and golden-model TB.
- **v3:** fixed-point Hadamard rotation at ingest if outlier studies on real embeddings justify it (SpinQuant evidence says the rotation *choice* matters — a fixed random seed is not acceptable, learned/structured rotations are).

## 9 — Sources

- ggml `src/ggml-common.h` (block layouts, QK sizes, static_asserts) and
  `docs/gguf.md` (type enum, incl. TQ/MXFP4), fetched 2026-08-29.
- llama.cpp PR #1684 (ikawrakow, 2023): k-quant introduction, LLaMA-7B PPL
  tables (via agentwikis primary-source summary).
- artefact2 gist "GGUF quantizations overview" (2024-02-27): Mistral-7B
  KL-divergence per scheme, imatrix methodology.
- Kurt, "Which Quantization Should I Use? A Unified Evaluation of llama.cpp
  Quantization on Llama-3.1-8B-Instruct", arXiv:2601.14277 (Jan 2026).
- ikawrakow, ik_llama.cpp discussion #8 "New quantization types IQ2_K, IQ3_K,
  IQ4_K, IQ5_K" (LLaMA-3.1-70B QError data, IQK performance, non-linear quants).
- Frantar et al., GPTQ, arXiv:2210.17323; Lin et al., AWQ, arXiv:2306.00978;
  Xiao et al., SmoothQuant, arXiv:2211.10438; Ashkboos et al., QuaRot,
  arXiv:2404.00456; Liu et al., SpinQuant, arXiv:2405.16406 (abstracts fetched
  via arXiv API).
- VTA: `apache/tvm-vta` `core/Configs.scala` (inpBits=8, wgtBits=8, accBits=32,
  outBits=8) and `core/TensorGemm.scala`.
- Gemmini: `ucb-bar/gemmini` README (inputType/accType, scaling functions,
  power-of-2 scaling, dynamic scaling).
- NVDLA Primer (nvdla.org): data types, precision scaling, INT8 ResNet-50
  reference configuration.
