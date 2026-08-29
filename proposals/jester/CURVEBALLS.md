# CURVEBALLS.md - Court Jester Challenge Proposals

## 14 Curveball Challenges (12-15, per task)

### Curveball 1
What if the seed proposal's entire "no multipliers" rule is a classic solution looking for a problem? Modern FPGAs have DSP blocks built exactly for shift-add multiply chains, and wasting 10+ LUTs per cycle of shift-add instead of using one DSP for a single-cycle multiply just bogs down timing and uses more power for the same throughput.
Tag: Target: seed, Unlocks: Quantifiable cost tradeoff between DSP utilization and LUT usage across real FPGA classes, and whether the "zero multipliers" religious rule actually honors the project's "pure Verilog" law.

### Curveball 2
What if a cell lying about its ready signal to starve lower-priority neighbors is not a bug, but a feature? The claude entry's priority arbiter penalizes small cells forever if large cells hog the egress pipe—why not let cells lie about backpressure and let edge latencies enforce fairness instead?
Tag: Target: claude, Unlocks: Bounded starvation model for priority arbiters, and whether voluntary backpressure plus age-based queue dropping is more fabric-efficient than hard priority.

### Curveball 3
The glm entry's wrap-priority flit rule means misaddressed circling flits starve all external traffic forever—what if bridges drop the oldest circling flit instead of blocking ingress entirely? A ring-of-rings fabric can't scale if new packets can't get through because old garbage packets keep looping.
Tag: Target: glm, Unlocks: Deadlock-free flit-dropping policy for ring fabrics, and whether dropping misaddressed flits is more fabric-efficient than infinite TTL queues.

### Curveball 4
Opencode's effect FIFO never drops packets, but what if a cell's refractory period means it can't process incoming effects fast enough, so the FIFO fills forever and backpressures the entire ring? Why not allow dropped effect packets and mark the edge as congested instead of stalling the whole fabric?
Tag: Target: opencode, Unlocks: Congestion-aware edge protocol that trades perfect reliability for scalability, and whether the fleet's "no amnesia" doctrine actually requires guaranteed delivery for bottom-layer stitching.

### Curveball 5
Zeroclaw's dyadic staircase decay for edge weights claims to hit a 1/t law, but what if the bounded 2× error on instantaneous decay rate is enough to break the JEPA doctrine's contrast window requirements? A true logarithmic edge state would let you decay by a fixed percentage per tick, no shifting, no approximation, and avoid the staircase's hard memory horizon limits.
Tag: Target: zeroclaw, Unlocks: True power-law decay implementation that preserves JEPA contrast windows, and whether integer state is actually necessary for drift-free memory.

### Curveball 6
Every proposal's tick scheduler uses a global wall-clock counter, but what if the tick is not time but traffic—each tick fires when a cell processes N flits, not when a counter wraps? A traffic-based tick would adapt to fabric load, so slow fabrics don't waste cycles on idle ticks and fast fabrics don't miss decay deadlines.
Tag: Target: all, Unlocks: Load-adaptive tick protocol that decouples fabric time from wall-clock time, and whether the fleet's "one forgetting doctrine" still holds when decay is tied to traffic instead of time.

### Curveball 7
The glm entry's single shared math tail for sqrt/div means every cosine calculation waits in a queue for hundreds of cycles compared to per-cell cos units—why not split the math tail into per-ring tails instead of forcing all cells to share one? A per-ring tail would scale far better for large multi-ring fabrics.
Tag: Target: glm, Unlocks: Scalable coprocessor arbitration policy for shared math units, and whether the per-fabric tail's cost savings are worth the latency hit for large fabrics.

### Curveball 8
Opencode's cell core FSM prioritizes ingress dispatch over tick processing, but what if a tick is missed because the core is busy handling a flood of effect packets? Why not pre-empt the core for tick processing instead of waiting for idle, even if it means dropping a few effect packets?
Tag: Target: opencode, Unlocks: Pre-emptive scheduler for cell cores that guarantees tick processing deadlines, and whether the tradeoff between packet loss and tick latency is acceptable for bottom-layer learning.

### Curveball 9
Claude's cell FSM uses a cooperative, non-preemptive model where each opcode runs to completion, but what if a long-running cosine calculation blocks all other opcodes for hundreds of cycles? Why not split cosine calculations into micro-operations that yield to the FSM between cycles, so other opcodes can run in parallel?
Tag: Target: claude, Unlocks: Preemptible FSM model for long-running operations, and whether the tradeoff between calculation latency and fabric responsiveness is worth the added complexity.

### Curveball 10
Zeroclaw's view opcode requires a full edge table scan for wsum calculations, which is O(E) per view—what if edge tables use a hash index instead of a linear scan, so views take O(1) time instead of O(E)? A hash index would make view operations fast enough to use in real-time feedback loops.
Tag: Target: zeroclaw, Unlocks: Scalable edge lookup protocol for fast view operations, and whether the added complexity of hash indexes is worth the performance gain for real-time feedback.

### Curveball 11
Seed's universal Q1.14 format claims to be the stability sweet spot, but what if a quilt fabric needs both low-precision dial states and high-precision cosine calculations? A single fixed format wastes space on dial registers that only need 8 bits of fractional precision, and limits cosine accuracy to ±0.005.
Tag: Target: seed, Unlocks: Multi-format fixed-point policy that adapts to different primitive needs, and whether the universal format's simplicity is worth the accuracy and space tradeoffs.

### Curveball 12
Every proposal says "any IO can enter a cell" via thin adapters, but what if the adapter itself becomes a bottleneck? A UART adapter that runs at 1Mbps can't feed a fabric cell that processes 1Gbps of flits—why not let IO adapters have their own internal queues and batch flits instead of processing one per cycle?
Tag: Target: all, Unlocks: Batch-oriented IO adapter protocol that bridges slow external IO with fast fabric cells, and whether the "thin and dumb" adapter rule is actually a bottleneck for real-world use cases.

### Curveball 13
The glm entry's flit TTL is based on hop count, but what if a flit's TTL is based on edge count instead? A edge-count TTL would let flits travel exactly N hops regardless of fabric topology, instead of being tied to the number of cells in the ring.
Tag: Target: glm, Unlocks: Topology-agnostic flit TTL policy, and whether hop-count TTL is actually sufficient for arbitrary fabric topologies.

### Curveball 14
Opencode's effect FIFO journals every forward and inverse action, but what if the journal itself becomes a bottleneck? A FIFO that stores both forward and inverse actions for every effect packet will fill up quickly in large fabrics—why not only journal the forward action and let the inverse action be derived from the opcode?
Tag: Target: opencode, Unlocks: Journaling policy that reduces FIFO size by deriving inverse actions from opcodes, and whether the tradeoff between journal completeness and FIFO utilization is acceptable for bottom-layer stitching.

## Favorite 3 Curveballs
1.  What if a cell lying about its ready signal to starve lower-priority neighbors is not a bug, but a feature? The claude entry's priority arbiter penalizes small cells forever if large cells hog the egress pipe—why not let cells lie about backpressure and let edge latencies enforce fairness instead?
2.  Every proposal's tick scheduler uses a global wall-clock counter, but what if the tick is not time but traffic—each tick fires when a cell processes N flits, not when a counter wraps? A traffic-based tick would adapt to fabric load, so slow fabrics don't waste cycles on idle ticks and fast fabrics don't miss decay deadlines.
3.  Zeroclaw's dyadic staircase decay for edge weights claims to hit a 1/t law, but what if the bounded 2× error on instantaneous decay rate is enough to break the JEPA doctrine's contrast window requirements? A true logarithmic edge state would let you decay by a fixed percentage per tick, no shifting, no approximation, and avoid the staircase's hard memory horizon limits.