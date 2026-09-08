"""Finite, exact falsification checks for CANDIDATE.md; not a uniform proof.

Run with: python3 audit_checks.py
Only the standard library is used. No input files or external data are read.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import comb


def mass_count(t, u):
    if abs(u) > t or (t + u) % 2:
        return 0
    return comb(t, (t + u) // 2)


def difference_count(t, u, steps):
    return sum(
        (-1) ** sum(bits)
        * mass_count(t, u - sum(b * h for b, h in zip(bits, steps)))
        for bits in product((0, 1), repeat=len(steps))
    )


def image_count(t, a, b, s, z):
    n = b - a + 2
    bound = (t + abs(z - s) + abs(z + s - 2 * a + 2)) // (2 * n) + 2
    return sum(
        mass_count(t, z - s + 2 * k * n)
        - mass_count(t, z + s - 2 * a + 2 + 2 * k * n)
        for k in range(-bound, bound + 1)
    )


def image_start_difference(t, a, b, z):
    length = b - a
    n = length + 2
    bound = (t + 6) // (2 * length) + 3
    return sum(
        difference_count(t, z + 2 * k * n, (2, 2 * k, 2 * k))
        + difference_count(t, z - 2 * a + 4 + 2 * k * n, (2, 2 * k, 2 * k + 2))
        for k in range(-bound, bound + 1)
    )


counts = defaultdict(int)

# Equation (5), including both parities and both shifted support endpoints.
for t in range(3, 65):
    n = t + 3
    for u in range(-t - 8, t + 15):
        v = u - 3
        left = n * (n - 1) * (n - 2) * difference_count(t, u, (2, 2, 2))
        right = -(v**3 - (3 * n - 2) * v) * mass_count(n, v)
        assert left == right, ("equation_5", t, u, left, right)
        counts["equation_5"] += 1

# Equation (7) against direct killed-walk dynamic programming, including
# singleton intervals and start/endpoint values on either zero boundary.
for length in range(0, 9):
    a, b = -3, length - 3
    for s in range(a - 1, b + 2):
        killed = {s: 1} if a <= s <= b else {}
        for t in range(17):
            for z in range(a - 1, b + 2):
                assert image_count(t, a, b, s, z) == killed.get(z, 0), (
                    "equation_7", t, a, b, s, z
                )
                counts["equation_7"] += 1
            next_killed = defaultdict(int)
            for z, weight in killed.items():
                for nz in (z - 1, z + 1):
                    if a <= nz <= b:
                        next_killed[nz] += weight
            killed = next_killed

# Equations (2), (8), and (9), compared to independent range-triple counts.
walks = {s: {(s, s, s): 1} for s in (0, 2)}
for t in range(21):
    for s in (0, 2):
        assert sum(walks[s].values()) == 2**t
    exceptional_0 = sum(w for (a, b, z), w in walks[0].items() if b < 2)
    exceptional_2 = sum(w for (a, b, z), w in walks[2].items() if a > 0)
    reflected = (mass_count(t, 0) + mass_count(t, 2)) if t % 2 == 0 else 2 * mass_count(t, 1)
    assert exceptional_0 == exceptional_2 == reflected, ("equation_2", t)
    counts["equation_2"] += 1
    for length in range(2, max(3, t + 1)):
        for a in range(2 - length, 1):
            b = a + length
            for z in range(a, b + 1):
                for s in (0, 2):
                    ie = (
                        image_count(t, a, b, s, z)
                        - image_count(t, a + 1, b, s, z)
                        - image_count(t, a, b - 1, s, z)
                        + image_count(t, a + 1, b - 1, s, z)
                    )
                    assert ie == walks[s].get((a, b, z), 0), ("equation_8", t, s, a, b, z)
                    counts["equation_8"] += 1
                expected = walks[0].get((a, b, z), 0) - walks[2].get((a, b, z), 0)
                assert image_start_difference(t, a, b, z) == expected, ("equation_9", t, a, b, z)
                counts["equation_9"] += 1
    for s in (0, 2):
        next_walks = defaultdict(int)
        for (a, b, z), weight in walks[s].items():
            for nz in (z - 1, z + 1):
                next_walks[min(a, nz), max(b, nz), nz] += weight
        walks[s] = next_walks

# Direct switch-walk-switch enumeration verifies the exact small-time TV.
def lamp_step(law):
    result = defaultdict(Fraction)
    for (lit, z), weight in law.items():
        for departure, increment, arrival in product((0, 1), (-1, 1), (0, 1)):
            lamps = set(lit)
            lamps.discard(z)
            if departure:
                lamps.add(z)
            nz = z + increment
            lamps.discard(nz)
            if arrival:
                lamps.add(nz)
            result[frozenset(lamps), nz] += weight / 8
    return result


lamp_laws = [{(frozenset(), s): Fraction(1)} for s in (0, 2)]
for t, expected in ((0, Fraction(1)), (1, Fraction(3, 4))):
    states = lamp_laws[0].keys() | lamp_laws[1].keys()
    tv = sum(abs(lamp_laws[0].get(q, 0) - lamp_laws[1].get(q, 0)) for q in states) / 2
    assert tv == expected, ("small_time_tv", t, tv)
    counts["small_time_tv"] += 1
    lamp_laws = [lamp_step(law) for law in lamp_laws]

for name in sorted(counts):
    print(f"{name}: {counts[name]} exact finite checks; no counterexample")
print("These finite checks do not establish any uniform bound.")
