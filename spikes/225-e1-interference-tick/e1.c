/* E1-C — interference tick, C99 port of e1.py (paper 225 / E6 software half).
 * Integer-only. Static allocation. ESP32-ready.
 *
 * CROSS-SUBSTRATE CONTRACT: this must produce byte-identical metrics to
 * e1.py for the same seed and parameters. The one semantic trap is
 * division: Python floors toward -inf, C truncates toward zero. All
 * divisions below go through fdiv() to pin the Python floor semantics
 * as THE contract (the language is the optimization, not the semantics).
 */
#include <stdio.h>
#include <stdint.h>

#define MAX_PULSES 64
#define TICKS 4800

static int32_t fdiv(int32_t a, int32_t b) {
    /* floor division, Python semantics */
    int32_t q = a / b;
    if ((a % b != 0) && ((a < 0) != (b < 0))) q--;
    return q;
}

static int32_t lcg_x;

static void lcg_seed(int32_t seed) { lcg_x = seed & 0x7FFFFFFF; if (lcg_x == 0) lcg_x = 1; }
static int32_t lcg_next(void) {
    lcg_x = (int32_t)((1103515245LL * lcg_x + 12345LL) & 0x7FFFFFFFLL);
    return lcg_x;
}
static int32_t lcg_below(int32_t n) { return lcg_next() % n; }

static int32_t reality(int32_t t) {
    const int32_t period = 240;
    int32_t phase = t % period;
    if (phase < 96)  return 400 + (int32_t)((int64_t)phase * 8 / 5);
    if (phase < 144) return 400 + 96 * 8 / 5 - (phase - 96);
    return 400 + 96 * 8 / 5 - 48 - (int32_t)((int64_t)(phase - 144) * 8 / 5);
}

typedef struct { int32_t mag, life; } pulse_t;

static pulse_t pulses[MAX_PULSES];
static int n_pulses;

typedef struct {
    int32_t events, debt, constructive, cancellations, chatter, max_err;
    int32_t settles;
} result_t;

static result_t run(int interference, int32_t seed, int32_t K, int32_t pulse_div,
                    int32_t delta, int32_t drift, int32_t lat2) {
    result_t r = {0, 0, 0, 0, 0, 0, 0};
    int32_t g, last_snap = -10, t, i;
    n_pulses = 0;
    lcg_seed(seed);
    g = reality(0);

    for (t = 0; t < TICKS; t++) {
        int32_t s1 = reality(t);
        int32_t s2t = (t - lat2 > 0) ? t - lat2 : 0;
        int32_t s2 = reality(s2t);
        int32_t e1, e2, trig1 = 0, trig2 = 0, max_trig = 0, err;

        g += lcg_below(2 * drift + 1) - drift;

        /* expire dead pulses (head = OLDEST, matching e1.py appendleft geometry:
         * py newest at front, oldest at tail, tail-pop = oldest; C appends at
         * tail, so the oldest live here — remove from the front) */
        while (n_pulses > 0 && pulses[0].life == 0) {
            for (i = 1; i < n_pulses; i++) pulses[i - 1] = pulses[i];
            n_pulses--;
        }

        e1 = s1 - g;
        e2 = s2 - g;
        if (e1 < 0) e1 = -e1;
        if (e2 < 0) e2 = -e2;
        if (e1 > delta) trig1 = (s1 - g);
        if (e2 > delta) trig2 = (s2 - g);
        if (e1 > max_trig) max_trig = e1;
        if (e2 > max_trig) max_trig = e2;

        if (!interference) {
            int32_t e = trig1 ? trig1 : trig2;
            if (e) {
                g += e;
                r.events++;
                r.debt += (e < 0) ? -e : e;
                if (t - last_snap == 1) r.chatter++;
                last_snap = t;
                err = s1 - g; if (err < 0) err = -err;
                { int32_t err2 = s2 - g; if (err2 < 0) err2 = -err2; if (err2 > err) err = err2; }
                if (err > max_trig) r.constructive++;
            }
        } else {
            int32_t net = 0;
            if (trig1) {
                int32_t m = fdiv(trig1 < 0 ? -trig1 : trig1, pulse_div);
                if (m < 1) m = 1;
                if (n_pulses < MAX_PULSES) {
                    pulses[n_pulses].mag = (trig1 > 0) ? m : -m;
                    pulses[n_pulses].life = K;
                    n_pulses++;
                }
                r.events++;
                r.debt += (trig1 < 0) ? -trig1 : trig1;
            }
            if (trig2) {
                int32_t m = fdiv(trig2 < 0 ? -trig2 : trig2, pulse_div);
                if (m < 1) m = 1;
                if (n_pulses < MAX_PULSES) {
                    pulses[n_pulses].mag = (trig2 > 0) ? m : -m;
                    pulses[n_pulses].life = K;
                    n_pulses++;
                }
                r.events++;
                r.debt += (trig2 < 0) ? -trig2 : trig2;
            }
            if (n_pulses > 0) {
                int opp = 0, pos = 0, neg = 0;
                for (i = 0; i < n_pulses; i++) net += pulses[i].mag;
                for (i = 0; i < n_pulses; i++) {
                    if (pulses[i].mag > 0) pos = 1;
                    if (pulses[i].mag < 0) neg = 1;
                }
                opp = pos && neg;
                if (net == 0 && opp && n_pulses >= 2) r.cancellations++;
                /* integer halving decay, floor semantics */
                for (i = 0; i < n_pulses; i++) {
                    int32_t mag = pulses[i].mag;
                    if (mag > 1 || mag < -1) mag = mag - fdiv(mag, 2);
                    pulses[i].mag = mag;
                    pulses[i].life--;
                }
                g += net;
                if ((trig1 || trig2)) {
                    err = s1 - g; if (err < 0) err = -err;
                    { int32_t err2 = s2 - g; if (err2 < 0) err2 = -err2; if (err2 > err) err = err2; }
                    if (err > max_trig) r.constructive++;
                    if (t - last_snap == 1) r.chatter++;
                    last_snap = t;
                }
            }
        }

        err = s1 - g; if (err < 0) err = -err;
        { int32_t err2 = s2 - g; if (err2 < 0) err2 = -err2; if (err2 > err) err = err2; }
        if (err > r.max_err) r.max_err = err;
        if (s1 - g <= delta && g - s1 <= delta && s2 - g <= delta && g - s2 <= delta)
            r.settles++;
    }
    return r;
}

int main(void) {
    static const int32_t seeds[5] = {1, 7, 42, 1999, 20260902};
    int si;
    printf("seed,sweep:mode,events,debt,constr,cancel,chatter,maxErr,pctW\n");
    for (si = 0; si < 5; si++) {
        result_t s = run(0, seeds[si], 4, 3, 12, 6, 10);
        result_t q = run(1, seeds[si], 4, 3, 12, 6, 10);
        printf("%d,seq,%d,%d,%d,%d,%d,%d,%d\n", seeds[si], s.events, s.debt,
               s.constructive, s.cancellations, s.chatter, s.max_err,
               (s.settles * 1000) / TICKS);
        printf("%d,int,%d,%d,%d,%d,%d,%d,%d\n", seeds[si], q.events, q.debt,
               q.constructive, q.cancellations, q.chatter, q.max_err,
               (q.settles * 1000) / TICKS);
    }
    return 0;
}
