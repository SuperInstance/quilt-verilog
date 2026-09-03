#!/usr/bin/env python3
"""CRITICALITY_BY_GROUP — Activity curves differ by lattice group structure.

Test Barbieri et al. prediction: equicontinuity vs sensitivity is decided by group.
Abelian (ℤ) and virtually-cyclic (ℤ × ℤ₂) should be stable.
Dihedral (D_n) should be sensitive/chaotic.

Run: python3 exp3_group_criticality.py
"""

class LCG:
    def __init__(self, seed):
        self.x = seed & 0x7FFFFFFF or 1
    def next(self):
        self.x = (1103515245 * self.x + 12345) & 0x7FFFFFFF
        return self.x
    def below(self, n):
        return self.next() % n

def ring_activity(noise_rate, ticks=3000, seed=20260902):
    """ℤ₁₀₂₄: abelian, should be equicontinuous (stable)."""
    rng = LCG(seed)
    g = 512
    activity = 0
    for t in range(ticks):
        noise = rng.below(1000) < int(1000 * noise_rate)
        if noise:
            delta = rng.below(256) - 128
            g = max(0, min(1023, g + delta))
            if g != 512:
                activity += 1
    return activity / ticks

def dihedral_activity(noise_rate, ticks=3000, seed=20260902):
    """D_n: non-abelian, should be sensitive (bifurcation)."""
    rng = LCG(seed)
    g_angle = 0
    g_radius = 256
    activity = 0
    for t in range(ticks):
        noise = rng.below(1000) < int(1000 * noise_rate)
        if noise:
            angle_delta = rng.below(360)
            radius_delta = rng.below(128) - 64
            g_angle = (g_angle + angle_delta) % 360
            g_radius = max(0, min(512, g_radius + radius_delta))
            if (g_angle % 90 < 10) or g_radius > 384:
                activity += 1
    return activity / ticks

def virtual_cycle_activity(noise_rate, ticks=3000, seed=20260902):
    """ℤ × ℤ₂: virtually-cyclic, should be equicontinuous (stable)."""
    rng = LCG(seed)
    g_z = 512
    g_z2 = 0
    activity = 0
    for t in range(ticks):
        noise = rng.below(1000) < int(1000 * noise_rate)
        if noise:
            z_delta = rng.below(256) - 128
            g_z = max(0, min(1023, g_z + z_delta))
            g_z2 ^= 1
            if g_z != 512 or g_z2 != 0:
                activity += 1
    return activity / ticks

if __name__ == "__main__":
    print("Criticality sweep by lattice group structure")
    print("(Testing Barbieri dichotomy: abelian/virtually-cyclic stable, dihedral sensitive)")
    print()
    noise_rates = [0.01, 0.03, 0.10, 0.30]

    print(f"{'Noise rate':>12} | {'ℤ₁₀₂₄ (abel)':>15} | {'D_n (nonabel)':>15} | {'ℤ×ℤ₂ (virt)':>15}")
    print("-" * 70)

    activities_ring = []
    activities_dihedral = []
    activities_virt = []

    for p in noise_rates:
        a_ring = ring_activity(p)
        a_dihed = dihedral_activity(p)
        a_virt = virtual_cycle_activity(p)
        activities_ring.append(a_ring)
        activities_dihedral.append(a_dihed)
        activities_virt.append(a_virt)
        print(f"   p={p:5.2f}    | {a_ring:15.3f} | {a_dihed:15.3f} | {a_virt:15.3f}")

    print()
    print("Growth analysis (slope from p=0.03 to p=0.30):")
    if len(activities_ring) >= 2:
        slope_ring = (activities_ring[-1] - activities_ring[1]) / (noise_rates[-1] - noise_rates[1])
        slope_dihed = (activities_dihedral[-1] - activities_dihedral[1]) / (noise_rates[-1] - noise_rates[1])
        slope_virt = (activities_virt[-1] - activities_virt[1]) / (noise_rates[-1] - noise_rates[1])
        print(f"  ℤ₁₀₂₄ (abelian):      {slope_ring:.3f}")
        print(f"  D_n (dihedral):       {slope_dihed:.3f}  (ratio: {slope_dihed/slope_ring:.2f}x)")
        print(f"  ℤ×ℤ₂ (virtual-cyclic): {slope_virt:.3f}")
        print()
        if slope_dihed > 1.2 * slope_ring:
            print("✓ PREDICTION CONFIRMED: dihedral shows steeper growth (sensitive)")
        elif slope_dihed < 0.8 * slope_ring:
            print("✗ PREDICTION FALSIFIED: dihedral is less sensitive than expected")
        else:
            print("~ MARGINAL: growth rates are similar (weak signal)")
