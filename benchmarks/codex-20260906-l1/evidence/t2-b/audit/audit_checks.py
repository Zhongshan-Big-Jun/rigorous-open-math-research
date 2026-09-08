"""Bounded exact falsification checks; successful checks are not uniform proofs."""
from collections import Counter
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json

checks = Counter()


def check(name, condition, case):
    if not condition:
        raise AssertionError((name, case))
    checks[name] += 1


@lru_cache(None)
def pcount(t, z):
    return comb(t, (t + z) // 2) if abs(z) <= t and (t + z) % 2 == 0 else 0


def difference(t, steps, v):
    return sum((-1) ** sum(bits) * pcount(t, v - sum(h * bit for h, bit in zip(steps, bits)))
               for bits in product((0, 1), repeat=len(steps)))


def walk_triples(start, limit):
    current = Counter({(start, start, start): 1})
    result = [current]
    for _ in range(limit):
        following = Counter()
        for (a, b, z), count in current.items():
            for arrival in (z - 1, z + 1):
                following[min(a, arrival), max(b, arrival), arrival] += count
        current = following
        result.append(current)
    return result


laws = {s: walk_triples(s, 16) for s in (0, 2)}
for t in range(17):
    for s in (0, 2):
        check('triple_mass', sum(laws[s][t].values()) == 2 ** t, (s, t))
    left = sum(c for (a, b, z), c in laws[0][t].items() if b <= 1)
    right = sum(c for (a, b, z), c in laws[0][t].items() if -2 <= z < 2)
    check('reflection_22', left == right, t)
    cdf_difference = (sum(c for (a, b, z), c in laws[0][t].items() if z <= 0)
                      - sum(c for (a, b, z), c in laws[2][t].items() if z <= 0))
    check('lower_event_4', cdf_difference == comb(t, t // 2), t)
    for a in range(-4, 1):
        for b in range(2, 7):
            length = b - a + 2
            for z in range(a, b + 1):
                images = sum(
                    difference(t, (2*k, 2*k, 2), z + 2*k*length)
                    + difference(t, (2*k, 2*k+2, 2), z - 2*a + 4 + 2*k*length)
                    for k in range(-t-5, t+6))
                actual = laws[0][t][a, b, z] - laws[2][t][a, b, z]
                check('difference_identity_16', images == actual, (t, a, b, z))

for a in range(-3, 3):
    for length in range(2, 10):
        b = a + length - 2
        for s in (0, 2):
            if not a-1 <= s <= b+1:
                continue
            current = Counter({s: 1}) if a <= s <= b else Counter()
            for t in range(17):
                for z in range(a-1, b+2):
                    images = sum(pcount(t, z-s+2*k*length)
                                 - pcount(t, z+s-2*a+2+2*k*length)
                                 for k in range(-t-5, t+6))
                    check('killed_image_9', images == current[z], (t, a, b, s, z))
                following = Counter()
                for z, count in current.items():
                    for arrival in (z-1, z+1):
                        if a <= arrival <= b:
                            following[arrival] += count
                current = following

for t in range(3, 65):
    n = t + 3
    denominator = n * (n-1) * (n-2)
    for w in range(-n-4, n+5, 2):
        lhs = pcount(t, w-3) - 3*pcount(t, w-1) + 3*pcount(t, w+1) - pcount(t, w+3)
        rhs = pcount(n, w) * (w**3 - (3*n-2)*w)
        check('exchangeability_identity_7', lhs * denominator == rhs, (t, w))

for j in range(1, 129):
    square = comb(2*j, j)**2
    check('central_binomial_2', 4*j*square >= 16**j and (j+1)*square <= 16**j, j)
for t in range(1, 257):
    check('lower_constant', 4*t*comb(t, t//2)**2 >= 4**t, t)


def shifts(k):
    return range(k) if k > 0 else range(k, 0)


for length in range(33, 41):
    for m in range(1, 13):
        first_count = 0
        second_count = 0
        for k in (m, -m):
            pairs = list(product(shifts(k), repeat=2))
            first_count += len(pairs)
            for z in (4-length, 0, length-2):
                for r1, r2 in pairs:
                    w = z + 2*k*length - 2*r1 - 2*r2 - 3
                    check('first_distance_17', abs(w) >= (2*m-1)*length-4*m-1
                          and 2*abs(w) >= m*length, (length, m, k, z, r1, r2))
        for k in (m, -m-1):
            pairs = list(product(shifts(k), shifts(k+1)))
            second_count += len(pairs)
            for base in (4, 2*length-2):
                for r1, r2 in pairs:
                    w = base + 2*k*length - 2*r1 - 2*r2 - 3
                    check('second_distance_18', abs(w) >= 2*m*length-4*m-3
                          and 2*abs(w) >= m*length, (length, m, k, base, r1, r2))
        check('image_multiplicities', first_count == 2*m*m
              and second_count == 2*m*(m+1), (length, m))

report = {
    'purpose': 'Bounded exact falsification only; no uniform claim is proved by these checks.',
    'input_sha256': {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                     for name in ('TASK.md', 'CANDIDATE.md')},
    'checks': dict(checks),
    'total_checks': sum(checks.values()),
    'counterexamples_found': 0,
}
Path('audit_checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
