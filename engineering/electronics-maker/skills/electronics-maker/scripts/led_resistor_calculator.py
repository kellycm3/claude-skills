#!/usr/bin/env python3
"""Size the series resistor for an LED and check the result, not just the formula.

R = (Vs - Vf) / I is the textbook line. The parts that burn boards are what
comes after it: rounding to a real resistor value, the current you actually
get, the power the resistor dissipates, and whether the pin can source it.
This tool does all four and refuses the one case with no answer (supply not
above the LED's forward voltage).

Deterministic arithmetic only. Stdlib only. No network.

Exit codes:
    0  design is sound
    2  design works but has a warning (pin limit, resistor power, dim LED)
    3  invalid input
    4  refused: supply voltage does not exceed forward voltage
"""

import argparse
import json
import sys

# E24 series, 5% tolerance: the values hobbyist resistor kits actually contain.
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

# A 1/4 W resistor run at half rating is the usual conservative hobby rule.
RESISTOR_POWER_LIMIT_W = 0.125
# Below this the LED is usually too dim to read as "on" in daylight.
MIN_VISIBLE_MA = 1.0

SAMPLE = {"vs": 5.0, "vf": 2.0, "current_ma": 10.0, "pin_limit_ma": 20.0}


def next_e24_at_or_above(ohms: float) -> float:
    """Smallest E24 value >= ohms, so the real current never exceeds the target."""
    decade = 1.0
    while ohms >= 10 * decade:
        decade *= 10
    while ohms < decade:
        decade /= 10
    for _ in range(2):  # current decade, then the next
        for base in E24:
            if base * decade >= ohms * (1 - 1e-12):
                return round(base * decade, 6)
        decade *= 10
    return round(E24[0] * decade, 6)


def design(vs, vf, current_ma, pin_limit_ma):
    if vs <= vf:
        return None
    ideal = (vs - vf) / (current_ma / 1000.0)
    r = next_e24_at_or_above(ideal)
    actual_ma = (vs - vf) / r * 1000.0
    r_power = ((vs - vf) / r) ** 2 * r
    warnings = []
    if actual_ma > pin_limit_ma:
        warnings.append(f"PIN-LIMIT: {actual_ma:.1f} mA exceeds the {pin_limit_ma:.0f} mA "
                        "you set for the pin; check the datasheet or switch with a transistor")
    if r_power > RESISTOR_POWER_LIMIT_W:
        warnings.append(f"RESISTOR-POWER: {r_power*1000:.0f} mW; use a higher-wattage part")
    if actual_ma < MIN_VISIBLE_MA:
        warnings.append(f"DIM: {actual_ma:.2f} mA is barely visible; check the LED's rated current")
    return {
        "inputs": {"vs_v": vs, "vf_v": vf, "target_ma": current_ma, "pin_limit_ma": pin_limit_ma},
        "ideal_ohms": round(ideal, 1),
        "resistor_ohms_e24": r,
        "actual_ma": round(actual_ma, 2),
        "resistor_power_mw": round(r_power * 1000, 1),
        "led_power_mw": round(vf * actual_ma, 1),
        "warnings": warnings,
    }


def render_text(d):
    lines = [
        f"Ideal resistor : {d['ideal_ohms']} ohm",
        f"Use (E24, >=)  : {d['resistor_ohms_e24']:g} ohm",
        f"Actual current : {d['actual_ma']} mA",
        f"Resistor power : {d['resistor_power_mw']} mW",
        f"LED power      : {d['led_power_mw']} mW",
    ]
    lines += [f"WARNING        : {w}" for w in d["warnings"]] or ["Warnings       : none"]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--vs", type=float, help="supply/GPIO high voltage (V)")
    ap.add_argument("--vf", type=float, help="LED forward voltage (V); red ~2.0, white/blue ~3.0-3.3")
    ap.add_argument("--current-ma", type=float, default=10.0, help="target LED current (mA), default 10")
    ap.add_argument("--pin-limit-ma", type=float, default=20.0,
                    help="max current you allow from the pin (mA), default 20; confirm in your datasheet")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example (5 V, red LED)")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    if a.sample:
        a.vs, a.vf = SAMPLE["vs"], SAMPLE["vf"]
        a.current_ma, a.pin_limit_ma = SAMPLE["current_ma"], SAMPLE["pin_limit_ma"]
    if a.vs is None or a.vf is None:
        ap.error("--vs and --vf are required (or use --sample)")
    if min(a.vs, a.vf, a.current_ma, a.pin_limit_ma) <= 0:
        print("error: all values must be positive", file=sys.stderr)
        return 3

    d = design(a.vs, a.vf, a.current_ma, a.pin_limit_ma)
    if d is None:
        print(f"REFUSED: supply {a.vs} V does not exceed forward voltage {a.vf} V; the LED will "
              "not light. Raise the supply, use a lower-Vf LED, or add a boost stage.", file=sys.stderr)
        return 4
    print(json.dumps(d, indent=2) if a.output == "json" else render_text(d))
    return 2 if d["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
