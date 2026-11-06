---
description: Plan, size and debug a hobby electronics project — platform choice, resistor/divider/battery calculations, hazards and documentation.
argument-hint: "[project idea, parts list, or the circuit that is not working]"
---

# /cs:electronics-maker

Run the electronics-maker pass on `$ARGUMENTS`.

Load `engineering/electronics-maker/skills/electronics-maker/SKILL.md` and follow its workflow.

## Pre-flight

1. What must it do, in one sentence? If unknown, walk `assets/maker_project_worksheet.md` one row at a time.
2. What powers it — USB, battery or mains? Mains or lithium → read `references/power_and_safety_canon.md` first.

## Run

```bash
python skills/electronics-maker/scripts/led_resistor_calculator.py --vs <V> --vf <V> --current-ma <mA>
python skills/electronics-maker/scripts/voltage_divider_calculator.py --vin <V> --vout <V>
python skills/electronics-maker/scripts/battery_life_estimator.py --capacity-mah <mAh> --active-ma <mA> \
    --active-seconds <s> --sleep-ua <uA> --period-seconds <s>
```

Report each exit code. Exit 4 is a refusal with the reason on stderr; surface it, do not work around it.
