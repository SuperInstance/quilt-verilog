/* Q6 — Barbieri integer Lyapunov proxy. C99, integer-only.
 * Pre-registration: dev-rounds/ROUND-13-Q6-barbieri.md PART 1 (frozen before run).
 *
 * Usage: q6_lyapunov [group] [n] [d] [p_num] [seed] [mode] [pert] [T]
 *   group: 0 = Z_n (gens +1,-1)  1 = D_{n/2} (r,s)  2 = Z_{n/2} x Z_2 (r,s prism)
 *   mode : 0 = full dynamics   1 = null (identity coin: no decay, no emission)
 *   pert : 0 = self-canary (no perturbation)  1 = +1 at site n/2 after burn-in
 * Emits CSV: group,n,d,p_num,seed,mode,pert, then rows t,S1,support for
 *   t in {0,1,2,4,8,...,T} (t=0 is immediately after perturbation).
 * Twin copies share ONE LCG stream: every noise draw is applied to BOTH copies,
 * so any separation growth is pure dynamics sensitivity, not noise decorrelation.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define BURNIN 1000
#define PNOISE 16

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

static int nbr(int group, int n, int e, int kind) {
    if (!group) {
        if (kind == 0) return (e + 1) % n;
        return (e + n - 1) % n;
    } else {
        int n2 = n / 2, f = e / n2, k = e % n2;
        if (kind == 0) return f * n2 + (k + 1) % n2;
        if (group == 1) return (1 - f) * n2 + ((n2 - k) % n2);   /* D: s inverts k */
        return (1 - f) * n2 + k;                                  /* prism: s keeps k */
    }
}

int main(int argc, char **argv) {
    if (argc != 9) { fprintf(stderr, "args: group n d p_num seed mode pert T\n"); return 2; }
    int group = atoi(argv[1]), n = atoi(argv[2]), d = atoi(argv[3]);
    int p_num = atoi(argv[4]);
    uint32_t seed = (uint32_t)strtoul(argv[5], NULL, 10);
    int mode = atoi(argv[6]), pert = atoi(argv[7]), T = atoi(argv[8]);

    lcg_seed(seed);
    int32_t *a = calloc((size_t)n, sizeof(int32_t));
    int32_t *b = calloc((size_t)n, sizeof(int32_t));
    int32_t *an = calloc((size_t)n, sizeof(int32_t));
    int32_t *bn = calloc((size_t)n, sizeof(int32_t));
    int32_t *cs = calloc((size_t)n, sizeof(int32_t));   /* snapshot scratch */
    if (!a || !b || !an || !bn || !cs) return 3;

    /* burn-in: evolve copy a alone (same dynamics), then clone to b */
    for (int t = 0; t < BURNIN; t++) {
        if (mode == 0 && t % d == 0)
            for (int v = 0; v < n; v++) { int32_t m = a[v]; if (m > 1 || m < -1) a[v] = m - fdiv(m, 2); }
        for (int v = 0; v < n; v++)
            if (lcg_below(10000) < p_num) a[v] += lcg_below(2*PNOISE+1) - PNOISE;
        if (mode == 0) {
            /* emission into scratch then commit (synchronous update) */
            for (int v = 0; v < n; v++) an[v] = a[v];
            for (int v = 0; v < n; v++)
                if (a[v] != 0) {
                    int32_t e = fdiv(a[v], 3); if (e == 0) e = (a[v] > 0) ? 1 : -1;
                    an[nbr(group, n, v, 0)] += e;
                    an[nbr(group, n, v, 1)] += e;
                    an[v] -= 2 * e;
                }
            int32_t *tmp = a; a = an; an = tmp;
        }
    }
    for (int v = 0; v < n; v++) b[v] = a[v];
    if (pert) b[n / 2] += 1;

    printf("%d,%d,%d,%d,%u,%d,%d\n", group, n, d, p_num, seed, mode, pert);
    for (int t = 0; t <= T; t++) {
        if (t == 0 || t == 1 || (t & (t - 1)) == 0) {
            int64_t s1 = 0; int sup = 0;
            for (int v = 0; v < n; v++) {
                int32_t dd = a[v] - b[v];
                if (dd) { sup++; s1 += (dd > 0) ? dd : -dd; }
            }
            printf("%d,%lld,%d\n", t, (long long)s1, sup);
        }
        if (t == T) break;
        /* one tick, SHARED draws */
        int32_t *noise = calloc((size_t)n, sizeof(int32_t));
        for (int v = 0; v < n; v++) {
            int32_t dv = 0;
            if (lcg_below(10000) < p_num) dv = lcg_below(2*PNOISE+1) - PNOISE;
            noise[v] = dv;
        }
        if (mode == 0) {
            for (int side = 0; side < 2; side++) {
                int32_t *x = side ? b : a, *xn = side ? bn : an;
                /* decay is deterministic, no draws */
                for (int v = 0; v < n; v++) xn[v] = x[v];
                if ((t + BURNIN + 1) % d == 0)
                    for (int v = 0; v < n; v++) { int32_t m = xn[v]; if (m > 1 || m < -1) xn[v] = m - fdiv(m, 2); }
                for (int v = 0; v < n; v++) xn[v] += noise[v];
                for (int v = 0; v < n; v++) cs[v] = xn[v];
                for (int v = 0; v < n; v++)
                    if (cs[v] != 0) {
                        int32_t e = fdiv(cs[v], 3); if (e == 0) e = (cs[v] > 0) ? 1 : -1;
                        xn[nbr(group, n, v, 0)] += e;
                        xn[nbr(group, n, v, 1)] += e;
                        xn[v] -= 2 * e;
                    }
            }
            { int32_t *tmp = a; a = an; an = tmp; }
            { int32_t *tmp = b; b = bn; bn = tmp; }
        } else {
            for (int v = 0; v < n; v++) { a[v] += noise[v]; b[v] += noise[v]; }
        }
        free(noise);
    }
    return 0;
}
