#!/usr/bin/env python3
"""Pick two real resistors for a voltage divider and report what the divider costs you.

Vout = Vin * R2 / (R1 + R2). Any ratio is easy on paper; the choices that matter
are which real E24 pair lands closest, how much current the divider wastes
(a problem on batteries), and its output impedance (a problem for ADC inputs,
which want a low-impedance source). Optionally models a load across R2.

Deterministic arithmetic only. Stdlib only. No network.

Exit codes:
    0  divider is sound
    2  divider works but has a warning (error, current, or output impedance)
    3  invalid input
    4  refused: a divider can only step voltage down (0 < Vout < Vin)
"""

import argparse
import json
import sys

E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
DECADES = [1e3, 1e4, 1e5, 1e6]  # 1 kohm .. 9.1 Mohm
VALUES = [round(b * d, 3) for d in DECADES for b in E24]

MAX_ERROR_PCT = 2.0
# Source impedance ADC inputs commonly want at or below (AVR datasheets cite
# 10 kohm); your MCU's datasheet is authoritative.
ADC_SOURCE_LIMIT_OHMS = 10_000.0

SAMPLE = {"vin": 12.0, "vout": 3.3, "max_current_ua": 500.0}


def loaded_vout(vin, r1, r2, load):
    r2_eff = r2 if load is None else (r2 * load) / (r2 + load)
    return vin * r2_eff / (r1 + r2_eff)


# Any pair within this error of the target counts as "close enough"; among those
# we take the lowest total resistance the current budget allows, because lower
# resistance means lower output impedance and less noise pickup.
ACCEPT_ERROR_PCT = 0.5


def search(vin, vout, max_current_ua, load):
    budget_a = max_current_ua / 1e6
    scored = []
    for r1 in VALUES:
        for r2 in VALUES:
            if vin / (r1 + r2) > budget_a:
                continue
            scored.append((abs(loaded_vout(vin, r1, r2, load) - vout), r1, r2))
    if not scored:
        return None
    best_err = min(e for e, _, _ in scored)
    tolerance = max(best_err, vout * ACCEPT_ERROR_PCT / 100.0)
    close = [(r1 + r2, e, r1, r2) for e, r1, r2 in scored if e <= tolerance]
    _, _, r1, r2 = min(close)
    return None, r1, r2


def fmt_ohms(v):
    if v >= 1e6:
        return f"{v/1e6:g} Mohm"
    if v >= 1e3:
        return f"{v/1e3:g} kohm"
    return f"{v:g} ohm"


def design(vin, vout, max_current_ua, load):
    found = search(vin, vout, max_current_ua, load)
    if found is None:
        return {"error": "no E24 pair (1 kohm..9.1 Mohm) fits the current budget"}
    _, r1, r2 = found
    actual = loaded_vout(vin, r1, r2, load)
    current_ua = vin / (r1 + r2) * 1e6
    zout = (r1 * r2) / (r1 + r2)
    err_pct = (actual - vout) / vout * 100.0
    warnings = []
    if abs(err_pct) > MAX_ERROR_PCT:
        warnings.append(f"ERROR: {err_pct:+.1f}% from target; widen the current budget or trim with a pot")
    if zout > ADC_SOURCE_LIMIT_OHMS:
        warnings.append(f"HIGH-IMPEDANCE: {zout/1000:.1f} kohm output; an ADC input may read low. "
                        "Add 0.1 uF at the pin, buffer with an op-amp, or lower both resistors")
    return {
        "inputs": {"vin_v": vin, "vout_target_v": vout, "max_current_ua": max_current_ua,
                   "load_ohms": load},
        "r1_ohms": r1, "r2_ohms": r2,
        "vout_actual_v": round(actual, 4), "error_pct": round(err_pct, 2),
        "divider_current_ua": round(current_ua, 1),
        "output_impedance_ohms": round(zout, 0),
        "warnings": warnings,
    }


def render_text(d):
    lines = [
        f"R1 (top)       : {fmt_ohms(d['r1_ohms'])}",
        f"R2 (bottom)    : {fmt_ohms(d['r2_ohms'])}",
        f"Vout           : {d['vout_actual_v']} V ({d['error_pct']:+}% vs target)",
        f"Divider current: {d['divider_current_ua']} uA",
        f"Output Z       : {fmt_ohms(d['output_impedance_ohms'])}",
    ]
    lines += [f"WARNING        : {w}" for w in d["warnings"]] or ["Warnings       : none"]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--vin", type=float, help="input voltage (V)")
    ap.add_argument("--vout", type=float, help="desired output voltage (V)")
    ap.add_argument("--max-current-ua", type=float, default=100.0,
                    help="current the divider may waste (uA), default 100")
    ap.add_argument("--load-ohms", type=float, default=None,
                    help="resistance across R2 (ohm); omit for an unloaded divider")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example (12 V to 3.3 V)")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    if a.sample:
        a.vin, a.vout, a.max_current_ua = SAMPLE["vin"], SAMPLE["vout"], SAMPLE["max_current_ua"]
    if a.vin is None or a.vout is None:
        ap.error("--vin and --vout are required (or use --sample)")
    if a.vin <= 0 or a.vout <= 0 or a.max_current_ua <= 0 or (a.load_ohms is not None and a.load_ohms <= 0):
        print("error: all values must be positive", file=sys.stderr)
        return 3
    if a.vout >= a.vin:
        print(f"REFUSED: a divider only steps down; {a.vout} V is not below {a.vin} V. "
              "Use a boost converter or level shifter to go up.", file=sys.stderr)
        return 4

    d = design(a.vin, a.vout, a.max_current_ua, a.load_ohms)
    if "error" in d:
        print(f"error: {d['error']}", file=sys.stderr)
        return 3
    print(json.dumps(d, indent=2) if a.output == "json" else render_text(d))
    return 2 if d["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
