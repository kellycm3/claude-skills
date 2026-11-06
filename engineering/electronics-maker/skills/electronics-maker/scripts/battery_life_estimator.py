#!/usr/bin/env python3
"""Estimate battery life for a duty-cycled device before you deploy it.

Average current = (I_active * t_active + I_sleep * t_sleep) / period. The result
is usually surprising in one direction: people optimise the active burst and
discover the sleep current was the whole budget. This tool reports each phase's
share of consumption so you fix the right one, derates the nominal capacity,
and says when the estimate stops meaning anything (battery self-discharge).

Deterministic arithmetic only. Stdlib only. No network.

Exit codes:
    0  estimate produced, no warning
    2  estimate produced with a warning (sleep-dominated, or beyond shelf life)
    3  invalid input
"""

import argparse
import json
import sys

# Past this, self-discharge and ageing dominate and the arithmetic is fiction.
SHELF_LIFE_YEARS = 5.0
SLEEP_DOMINATED_SHARE = 0.5

SAMPLE = {"capacity_mah": 2000.0, "active_ma": 120.0, "active_seconds": 3.0,
          "sleep_ua": 150.0, "period_seconds": 600.0, "derate": 0.8}


def estimate(capacity_mah, active_ma, active_s, sleep_ua, period_s, derate):
    sleep_s = period_s - active_s
    sleep_ma = sleep_ua / 1000.0
    charge_active = active_ma * active_s       # mA*s per period
    charge_sleep = sleep_ma * sleep_s
    avg_ma = (charge_active + charge_sleep) / period_s
    usable_mah = capacity_mah * derate
    hours = usable_mah / avg_ma
    sleep_share = charge_sleep / (charge_active + charge_sleep)
    warnings = []
    if sleep_share > SLEEP_DOMINATED_SHARE:
        warnings.append(f"SLEEP-DOMINATED: sleep draws {sleep_share*100:.0f}% of the budget; "
                        "shortening the active burst barely helps, so cut sleep current "
                        "(regulator quiescent current, pull-ups, always-on peripherals)")
    if hours / 8766.0 > SHELF_LIFE_YEARS:
        warnings.append(f"BEYOND-SHELF-LIFE: {hours/8766.0:.1f} years exceeds {SHELF_LIFE_YEARS:.0f}; "
                        "self-discharge and ageing will end the battery first")
    return {
        "inputs": {"capacity_mah": capacity_mah, "derate": derate, "active_ma": active_ma,
                   "active_seconds": active_s, "sleep_ua": sleep_ua, "period_seconds": period_s},
        "average_current_ma": round(avg_ma, 4),
        "usable_mah": round(usable_mah, 1),
        "life_hours": round(hours, 1),
        "life_days": round(hours / 24.0, 1),
        "active_share_pct": round((1 - sleep_share) * 100, 1),
        "sleep_share_pct": round(sleep_share * 100, 1),
        "warnings": warnings,
    }


def render_text(d):
    lines = [
        f"Average current: {d['average_current_ma']} mA",
        f"Usable capacity: {d['usable_mah']} mAh",
        f"Estimated life : {d['life_days']} days ({d['life_hours']} h)",
        f"Budget split   : active {d['active_share_pct']}% / sleep {d['sleep_share_pct']}%",
    ]
    lines += [f"WARNING        : {w}" for w in d["warnings"]] or ["Warnings       : none"]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--capacity-mah", type=float, help="battery nominal capacity (mAh)")
    ap.add_argument("--active-ma", type=float, help="current while awake (mA)")
    ap.add_argument("--active-seconds", type=float, help="seconds awake per cycle")
    ap.add_argument("--sleep-ua", type=float, help="whole-board current while asleep (uA), measured, not the chip's datasheet figure")
    ap.add_argument("--period-seconds", type=float, help="seconds per full wake/sleep cycle")
    ap.add_argument("--derate", type=float, default=0.8,
                    help="usable fraction of nominal capacity, default 0.8 (cold, ageing, cutoff voltage)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example (ESP32 sensor node)")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    if a.sample:
        a.capacity_mah, a.active_ma = SAMPLE["capacity_mah"], SAMPLE["active_ma"]
        a.active_seconds, a.sleep_ua = SAMPLE["active_seconds"], SAMPLE["sleep_ua"]
        a.period_seconds, a.derate = SAMPLE["period_seconds"], SAMPLE["derate"]
    req = [a.capacity_mah, a.active_ma, a.active_seconds, a.sleep_ua, a.period_seconds]
    if any(v is None for v in req):
        ap.error("--capacity-mah, --active-ma, --active-seconds, --sleep-ua and "
                 "--period-seconds are required (or use --sample)")
    if min(a.capacity_mah, a.active_ma, a.active_seconds, a.period_seconds) <= 0 or a.sleep_ua < 0:
        print("error: capacity, active current and times must be positive; sleep current >= 0", file=sys.stderr)
        return 3
    if not 0 < a.derate <= 1:
        print("error: --derate must be in (0, 1]", file=sys.stderr)
        return 3
    if a.active_seconds >= a.period_seconds:
        print("error: active time must be shorter than the period (the device never sleeps)", file=sys.stderr)
        return 3

    d = estimate(a.capacity_mah, a.active_ma, a.active_seconds, a.sleep_ua, a.period_seconds, a.derate)
    print(json.dumps(d, indent=2) if a.output == "json" else render_text(d))
    return 2 if d["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
