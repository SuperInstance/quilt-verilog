# WORLD-CLASS-SURVEY BRIEF — quilt-verilog gap analysis

You are the CUTTING-EDGE SURVEY lane. Casey's directive: "study the cutting edge verilog papers and repos in related and unrelated topics and let's make our system world-class. we are close."

Repo: /home/eileen/projects/quilt-verilog. Branch `world-class-survey` (exists — review `git log world-class-survey` first; commit your doc there, no merge/push). DeepSeek/DeepInfra REVOKED. Use web_search + web_fetch heavily.

## Read first (know the gap, not the known)
docs/INDEX.md, docs/CUTTING-EDGE-rtl.md, docs/FORMAL-PROOFS.md, docs/CHIP-MATRIX.md.

## Our system (baseline for comparison)
Verilog-2005 cellular fabric: N cells on a ring interconnect, flit-based messaging, 5+1 opcodes (bind/link/effect/view/tick + fire), conserved cellular state, formal proofs (PDR closed UNBOUNDED conservation, k-induction depth-130, 854-clause machine-derived invariant committed), fabric-level Python-vs-RTL cosim bit-exact (NCELL=2 done; 4/8 parameterization in progress on branch cosim-scaleup), coherence-protocol arena with adjudicated synthesis verdict (docs/coherence-arena/VERDICT.md — read it). Fold any mid-survey dockings into the doc.

## Survey rings
(a) DIRECT: NoC ring topologies, flit-based flow control, deadlock-free routing theory (Duato), formal verification of NoCs (k-induction, PDR/IC3 on protocols), open-source NoC RTL (OpenSMART, Ariane NoC, Litex, AXI meshes).
(b) ADJACENT: cellular automata hardware, amorphous computing, CRDTs in hardware, token-based coherence (IEEE), transactional NoC.
(c) UNRELATED-but-transferable: local rules + global guarantees proven — self-stabilizing systems (Dijkstra/Schneider), population protocols (Angluin), swarm consensus.
Old foundational theory is fair game (Duato 1997, Dijkstra 1974, Angluin 2004); prefer 2023–2026 for the rest. Cite EVERY claim (URL or paper ref).

## Internal prior art (captain's order)
Check our own back catalog via `gh repo view SuperInstance/<name>` (read-only): quilt-mhs (federation messaging), MerkleMesh (merkle proofs over cell-ledger journals), quilt-fleet (quorum/migration), cuda-constraint-engine (1B+ constraints/sec oracles). A gap we close by PORTING our own proven code is a CHEAPER difficulty class than building new — mark those distinctly.

## Deliverable — docs/WORLD-CLASS-GAP.md
1. Ranked 10 things that would make quilt-verilog world-class: field's best vs ours, the gap, concrete path in OUR architecture (Verilog-2005, conservation, ring), difficulty S/M/L (or PORT where internal prior art applies).
2. The 3 things we do that the field does NOT — honestly sorted: genuinely novel vs re-derivation. Evidence verbatim.
3. The single highest-leverage next move.
Tapestry doctrine: undersell in the summary, evidence in the body.

## Report back
Top-3 gaps, our top-3 genuine novelties, the highest-leverage move.
