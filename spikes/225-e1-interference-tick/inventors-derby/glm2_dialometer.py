#!/usr/bin/env python3
"""INVENTION 1 — TWIN-RUNOUT DIALOMETER (glm-2 derby entry, 2026-09-02)

Charter §9 (dialometer / feeler-gauge bank / snap points), testable miniature.

Two codings of one channel: C1 native, C2 the E1 late twin (latency 10).
The dial lam in [0,255] advances the late twin to re-align the coupling.
The TRUE runout wave W(lam) = sum_t |C1(t) - C2(t+lam)| is NEVER read
continuously. The only readout is a feeler-gauge bank: boolean blade pulls
"does blade q fit the gap?" implemented as integer accumulation with
early-exit the moment the running sum exceeds q (a tripped blade never pays
for the rest of the wave). The runout profile is RECONSTRUCTED from the
boolean seating log alone.

Bug arm: the twin's sensor sits on a 2x-coarse grid (reports s rounded down
to even). No dial setting can re-align a scale joint with a rotation — the
instrument must show a nonzero runout FLOOR across the whole dial.

Integer-only. Fixed channel (deterministic walk). No floats.
"""
PERIOD = 240

def reality(t):
    phase = t % PERIOD
    if phase < 96:
        return 400 + phase * 8 // 5
    if phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5

LAT = 10
N = 1440                      # 6 channel periods of measurement window
BLADES = [0, 32, 128, 512, 2048, 8192, 32768, 131072]   # geometric blade bank
DIAL = range(0, 256)

class Meter:
    def __init__(self):
        self.adds = 0     # integer additions actually paid
        self.pulls = 0    # blade pulls

    def blade(self, lam, q, bug=False):
        """Boolean fit test, early-exit: sum |C1 - C2_shifted|, trip at > q."""
        self.pulls += 1
        acc = 0
        for t in range(N):
            a = reality(t)
            raw = reality(t - LAT + lam)
            b = (raw // 2) * 2 if bug else raw   # bug arm: 2x-coarse sensor grid
            d = a - b
            if d < 0:
                d = -d
            acc += d
            self.adds += 1
            if acc > q:
                return False
        return True

def true_wave(lam, bug=False):
    """Reference W(lam) — computed ONLY afterwards, to audit the boolean log."""
    acc = 0
    for t in range(N):
        a = reality(t)
        raw = reality(t - LAT + lam)
        b = (raw // 2) * 2 if bug else raw
        d = a - b
        acc += d if d >= 0 else -d
    return acc

def survey_naive(bug, label):
    """Every dial step gets the full blade ladder (the naive boolean bank)."""
    m = Meter()
    profile = []
    zero_seats = []
    for lam in DIAL:
        seated = None
        for q in BLADES:
            if m.blade(lam, q, bug):
                seated = q
                break
        if seated is None:
            seated = BLADES[-1]
        profile.append(seated)
        if seated == 0:
            zero_seats.append(lam)
    wave_cost = len(DIAL) * N
    print(f"== {label} (naive: full ladder at every dial step) ==")
    print(f" blade pulls: {m.pulls}   adds paid: {m.adds}   ({100 * m.adds // wave_cost}% of wave cost)")
    print(f" zero-seatings: {zero_seats}")
    return m.adds, zero_seats

def survey(bug, label):
    """Machinist order: one coarse blade across the dial, fine blades only
    where the coarse blade seats. You pay for landings, not for the wave."""
    m = Meter()
    QC = 2048
    candidates = []
    for lam in DIAL:                       # stage A: coarse blade sweep
        if m.blade(lam, QC, bug):
            candidates.append(lam)
    adds_a, pulls_a = m.adds, m.pulls
    fine = list(reversed(BLADES[:BLADES.index(QC)]))   # [512, 128, 32, 0]
    seated = {}
    zero_seats = []
    for lam in candidates:                  # stage B: descend only at seatings
        s = QC
        for q in fine:                      # descend while blades still fit
            if m.blade(lam, q, bug):
                s = q                       # seated; try the next finer blade
            else:
                break                       # gap too tight below — this is the seat
        seated[lam] = s
        if s == 0:
            zero_seats.append(lam)
    wave_cost = len(DIAL) * N
    # audit the boolean log against the true wave (verification only)
    true = {lam: true_wave(lam, bug) for lam in candidates}
    bracket_ok = all((BLADES[BLADES.index(seated[lam]) - 1] if BLADES.index(seated[lam]) > 0 else -1)
                     < true[lam] <= seated[lam] for lam in candidates)
    floor = min(true_wave(lam, bug) for lam in DIAL)
    print(f"== {label} (two-stage: coarse sweep + fine descent at seatings) ==")
    print(f" stage A: {pulls_a} pulls, {adds_a} adds ({100 * adds_a // wave_cost}% of wave)")
    print(f" stage B: +{m.pulls - pulls_a} pulls, +{m.adds - adds_a} adds -> total {m.adds} adds "
          f"({100 * m.adds // wave_cost}% of wave cost {wave_cost})")
    print(f" coarse seatings: {sorted(candidates)}")
    print(f" zero-seatings (blade 0 logs): {zero_seats}"
          f"   spacing: {[zero_seats[i+1]-zero_seats[i] for i in range(len(zero_seats)-1)]}")
    print(f" true runout floor (verification): {floor}")
    print(f" boolean bracket audit at seatings (lower < W <= seated): {bracket_ok}")
    print()
    return m.adds, zero_seats, floor

if __name__ == "__main__":
    print("TWIN-RUNOUT DIALOMETER — boolean blades only, channel period", PERIOD)
    print("blade bank:", BLADES, " dial 0..255, window N =", N, "ticks\n")
    survey_naive(False, "GOOD COUPLING — naive bank (honest cost lesson)")
    print()
    _, zs1, _ = survey(False, "GOOD COUPLING (native twin): rotation joint")
    _, zs2, floor2 = survey(True,  "BUG ARM (2x-coarse sensor grid): scale joint")
    period = zs1[1] - zs1[0] if len(zs1) > 1 else None
    print(f"VERDICT: zero-seatings at lam={zs1} (twin latency {LAT} + channel period {period})")
    print(f"         bug arm zero-seatings: {zs2 or 'NONE'} — rotation cannot seat a scale joint "
          f"(floor {floor2}, exactly the odd-value count in the window)")
