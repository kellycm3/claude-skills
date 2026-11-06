# electronics-maker

Hobby electronics specialist: platform choice (Arduino / Raspberry Pi / ESP32), circuit basics, soldering, PCB design, sensors, IoT and 3D-printed enclosures — with three calculators that do the arithmetic instead of guessing it.

| Tool | Answers |
|---|---|
| `led_resistor_calculator.py` | Which real resistor, what current results, will the pin and resistor survive? |
| `voltage_divider_calculator.py` | Which pair, how much current wasted, is the output impedance ADC-safe? |
| `battery_life_estimator.py` | How long will it run, and is active or sleep draining it? |

```bash
python skills/electronics-maker/scripts/led_resistor_calculator.py --sample
```

Stdlib only; no network. Use `/cs:electronics-maker` or the `cs-electronics-maker` agent.

## Provenance

The specialist text in `skills/electronics-maker/references/maker_handbook.md` was supplied by the repository maintainer's collaborator and is kept as written. The calculators, sourced references, worksheet, agent and command were added in this package.
