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

WRONG_TYPE = ["hello", "", " ", "1,5", "3.0.1", "0x1f", "NaN", "1e", "--5", "1 2"]
HUGE = [f"1{rnd.randint(0, 9)}{'0' * rnd.randint(15, 21)}",
        "9" * rnd.randint(16, 25),
        "1" + "0" * rnd.randint(15, 18) + "1"]
BOUNDARY_OK = [str(10 ** 15), str(10 ** 15 + 1), str(10 ** 15 - 1),
               "-273.15", "-273.150001", "-272.9"]
DIV_ZERO = ["0", "-0", "0.0", "1e-320"]

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
