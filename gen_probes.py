#!/usr/bin/env python3
"""Generate a per-student, in-class attack probe file.

Run at the start of the U1 L13 partner-attack block. Each student runs this
with their own seat number; nobody else can predict their probe set, and
publishing the probes would defeat the point.

The seed is printed so the file can be regenerated if lost -- but students
should not post their seed or their probe file.
"""
import random
import sys

SEAT = sys.argv[1] if len(sys.argv) > 1 else "?"
# Salt mixes the seat with a per-term value so a shared seed list cannot be
# precomputed across terms.
SALT = "U1L13-2026FA"
rnd = random.Random(f"{SALT}:{SEAT}")


# Every group below is randomised from the seed, so no two seats get the same
# probe set. The per-seat variation is the whole point: it is what makes
# reading a classmate's repo worthless.
_NON_NUMERIC = ["hello", "", " ", "1,5", "3.0.1", "0x1f", "NaN", "1e",
                "--5", "1 2", "twelve", "1/2", "٣", "12abc", "1.2.3",
                "None", "True", "+", "e5", "0b101", "$5"]
WRONG_TYPE = rnd.sample(_NON_NUMERIC, 6)

HUGE = [f"1{rnd.randint(0, 9)}{'0' * rnd.randint(15, 21)}",
        "9" * rnd.randint(16, 25),
        "1" + "0" * rnd.randint(15, 18) + "1"]

# Straddle the two boundaries the labs care about, with per-seat jitter so the
# interesting cases are not always the same exact values.
_pow = rnd.randint(14, 16)
BOUNDARY_OK = [str(10 ** 15), str(10 ** 15 + 1), str(10 ** 15 - 1),
               "-273.15",
               str(round(-273.15 - rnd.choice([1e-6, 1e-5, 1e-4]), 6)),
               str(round(-273.15 + rnd.choice([1e-6, 1e-4, 1e-2]), 6))]

# "Near zero" values -- a guard testing == 0 misses all of these.
_NEAR_ZERO = ["0", "-0", "0.0", "-0.0", "1e-320", "5e-324", "1e-309",
              "0.0000000001", "1e-16", "2**-1074"]
DIV_ZERO = rnd.sample(_NEAR_ZERO, 4)

print(f"""# ATTACK PROBES -- generated for seat {SEAT}
# Do not commit this file. Do not post your seed.
# Run:  python3 attack_probes.py
# Every one of these SHOULD be handled gracefully. A traceback, a hang, or a
# wrong number is a finding.

SEAT = "{SEAT}"
SEED = "{SALT}:{SEAT}"

WRONG_TYPE = {WRONG_TYPE!r}
HUGE = {HUGE!r}
BOUNDARY = {BOUNDARY_OK!r}
DIV_ZERO = {DIV_ZERO!r}
""")
