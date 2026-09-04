/* Q4 — §3.1 MI-criticality sweep core. C99, integer-only.
 * Model + decision rule pre-registered in dev-rounds/ROUND-11-Q4-mi-criticality.md
 * BEFORE this was run. Counters emitted as integer CSV; MI computed downstream in
 * fixed-point integer arithmetic (q4_mi_criticality.py). No floats here.
 *
 * Usage: q4_mi_sweep32 [group] [n] [d] [p_num] [seed]
 *   group: 0 = Z_n (cycle, n sites, gens {+1,-1})
 *          1 = D_{n/2} (Cayley{r,s}, n elements, r:(f,k)->(f,k+1), s:(f,k)->(1-f,-k))
 * Emits: group,n,d,p_num,seed, act_permille_num, act_total,
 *        n00,n01,n10,n11 (MI contingency v->nbr, summing BOTH generators for Z;
 *        for D: first row = r-edge table, second = s-edge table),
 *        f00,f01,f10,f11 (floor table: v at t vs v at t (SELF-CANARY pairing)),
 *        x00,x01,x10,x11 (cross-seed floor: same run vs *next* seed's run,
 *        achieved by running an independent second LCG stream in lockstep).
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define TICKS_MEAS 10000
#define BURNIN     1000
#define PNOISE     16

static int32_t fdiv(int32_t a, int32_t b) {
    int32_t q = a / b;
    if ((a % b != 0) && ((a < 0) != (b < 0))) q--;
    return q;
}

static uint32_t lcg_x;
static void lcg_seed(uint32_t seed) { lcg_x = seed & 0x7FFFFFFF; if (!lcg_x) lcg_x = 1; }
static uint32_t lcg_next(void) {
    lcg_x = (uint32_t)((1103515245ULL * lcg_x + 12345ULL) & 0x7FFFFFFFULL);
    return lcg_x;
}
static int32_t lcg_below(int32_t n) { return (int32_t)(lcg_next() % (uint32_t)n); }

typedef struct { int64_t n00, n01, n10, n11; } tab_t;

static void tab_add(tab_t *t, int x, int y) {
    if (!x && !y) t->n00++;
    else if (!x && y) t->n01++;
    else if (x && !y) t->n10++;
    else t->n11++;
}

/* neighbor of element e under generator: kind 0 = first gen (+1 or r), kind 1 = second (-1 or s) */
static int nbr(int group, int n, int e, int kind) {
    if (!group) { /* Z_n: gens +1, -1 */
        if (kind == 0) return (e + 1) % n;
        return (e + n - 1) % n;
    } else {      /* D_{n/2}: element e = f*n2 + k, n2 = n/2; r:(f,k)->(f,k+1); s:(f,k)->(1-f,-k) */
        int n2 = n / 2;
        int f = e / n2, k = e % n2;
        if (kind == 0) return f * n2 + (k + 1) % n2;
        return (1 - f) * n2 + ((n2 - k) % n2);
    }
}

int main(int argc, char **argv) {
    if (argc != 6) { fprintf(stderr, "args: group n d p_num seed\n"); return 2; }
    int group = atoi(argv[1]), n = atoi(argv[2]), d = atoi(argv[3]);
    int p_num = atoi(argv[4]);
    uint32_t seed = (uint32_t)strtoul(argv[5], NULL, 10);

    /* burn-in stream then measurement stream share one LCG (deterministic whole-run);
     * cross-seed floor stream: independent LCG seeded seed+1, same lattice, same rule,
     * its activity bits used for the x-table (v,t) vs (v,t) across the two runs. */
    lcg_seed(seed);
    uint32_t fx = (seed + 1) & 0x7FFFFFFF; if (!fx) fx = 1; /* second LCG inline */

    int32_t *a  = calloc((size_t)n, sizeof(int32_t));
    int32_t *a2 = calloc((size_t)n, sizeof(int32_t));
    uint8_t *act_prev = calloc((size_t)n, 1);
    uint8_t *act_prev2 = calloc((size_t)n, 1);
    if (!a || !a2 || !act_prev || !act_prev2) return 3;

    tab_t r = {0,0,0,0};   /* neighbor via gen0 */
    tab_t s = {0,0,0,0};   /* neighbor via gen1 (== -1 for Z; s for D) */
    tab_t f = {0,0,0,0};   /* SELF-CANARY: v vs v same tick */
    tab_t x = {0,0,0,0};   /* cross-seed floor: v vs v across runs */
    int64_t act_num = 0, act_tot = 0;

    int total_ticks = BURNIN + TICKS_MEAS;
    for (int t = 0; t < total_ticks; t++) {
        /* --- lattice A dynamics (Gauss-Seidel, fixed element order) --- */
        if (t % d == 0) {
            for (int v = 0; v < n; v++) {
                int32_t m = a[v]; if (m > 1 || m < -1) a[v] = m - fdiv(m, 2);
            }
        }
        for (int v = 0; v < n; v++) {
            if (lcg_below(10000) < p_num) a[v] += lcg_below(2*PNOISE+1) - PNOISE;
        }
        for (int v = 0; v < n; v++) {
            if (a[v] > 1 || a[v] < -1) {
                int32_t e = fdiv(a[v], 3); if (e == 0) e = (a[v] > 0) ? 1 : -1;
                a[nbr(group, n, v, 0)] += e;
                a[nbr(group, n, v, 1)] += e;
                a[v] -= 2 * e;
            }
        }
        /* --- lattice B dynamics (independent stream, cross-seed floor) --- */
        if (t % d == 0) {
            for (int v = 0; v < n; v++) {
                int32_t m = a2[v]; if (m > 1 || m < -1) a2[v] = m - fdiv(m, 2);
            }
        }
        for (int v = 0; v < n; v++) {
            fx = (uint32_t)((1103515245ULL * fx + 12345ULL) & 0x7FFFFFFFULL);
            if ((int32_t)(fx % 10000u) < p_num) {
                fx = (uint32_t)((1103515245ULL * fx + 12345ULL) & 0x7FFFFFFFULL);
                a2[v] += (int32_t)(fx % (uint32_t)(2*PNOISE+1)) - PNOISE;
            }
        }
        for (int v = 0; v < n; v++) {
            if (a2[v] != 0) {
                int32_t e = fdiv(a2[v], 3); if (e == 0) e = (a2[v] > 0) ? 1 : -1;
                a2[nbr(group, n, v, 0)] += e;
                a2[nbr(group, n, v, 1)] += e;
                a2[v] -= e;
            }
        }

        if (t >= BURNIN) {
            uint8_t *cur  = malloc((size_t)n);
            uint8_t *cur2 = malloc((size_t)n);
            for (int v = 0; v < n; v++) {
                cur[v]  = (a[v]  != 0);
                cur2[v] = (a2[v] != 0);
                act_num += cur[v];
            }
            act_tot += n;
            if (t > BURNIN) {  /* pair with previous measured tick */
                for (int v = 0; v < n; v++) {
                    tab_add(&r, act_prev[v],  cur[nbr(group, n, v, 0)]);
                    tab_add(&s, act_prev[v],  cur[nbr(group, n, v, 1)]);
                    tab_add(&f, act_prev[v],  cur[v]);            /* self, same lag-1 pairing */
                    tab_add(&x, act_prev[v],  cur2[v]);           /* cross-run floor */
                }
            }
            for (int v = 0; v < n; v++) { act_prev[v] = cur[v]; act_prev2[v] = cur2[v]; }
            free(cur); free(cur2);
        }
    }

    printf("%d,%d,%d,%d,%u,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld\n",
        group, n, d, p_num, seed,
        (long long)act_num, (long long)act_tot,
        r.n00, r.n01, r.n10, r.n11,
        s.n00, s.n01, s.n10, s.n11,
        f.n00, f.n01, f.n10, f.n11,
        x.n00, x.n01, x.n10, x.n11);
    return 0;
}
