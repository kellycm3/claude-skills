# Component Sizing Canon

What `led_resistor_calculator.py` and `voltage_divider_calculator.py` implement, and the
confidence each claim deserves. 🟢 standard textbook/standards result · 🟡 vendor guidance
that varies by part · 🔴 folklore.

## 1. LED current-limiting resistor 🟢

`R = (Vs − Vf) / I`. The formula follows from Ohm's law and Kirchhoff's voltage law; the LED
is not a resistor, so the resistor must absorb the voltage the LED does not. Two consequences
people miss: if `Vs ≤ Vf` there is no answer (the tool refuses rather than returning a
negative resistance), and rounding the resistor **down** raises the current above target, so
the tool rounds **up** to the next E24 value.

Typical forward voltages (≈2 V red, ≈3 V white/blue) are indicative 🟡. The part's datasheet
wins; two LEDs of the same colour differ.

## 2. Preferred-value series 🟢

Resistors are sold in the IEC 60063 E-series. E24 (5% tolerance) has 24 values per decade and
is what hobby kits contain. A computed 312 Ω does not exist; 330 Ω does. Always design to a
real value and recompute the current.

## 3. Pin current limits 🟡

Microcontroller GPIO pins have a recommended and an absolute-maximum source current that
differ by family and by pin group. The calculator's `--pin-limit-ma` defaults to 20 mA as a
conservative placeholder; replace it with your datasheet's figure. Drive anything larger
through a transistor (see the handbook, *Transistors as switches*).

## 4. Voltage dividers 🟢

`Vout = Vin · R2 / (R1 + R2)`, valid only for an **unloaded** output. A load in parallel with
R2 lowers Vout; the tool's `--load-ohms` models this. A divider can only reduce voltage.

Two costs the formula hides:

- **Wasted current** `Vin / (R1 + R2)` flows continuously — material on a battery.
- **Output impedance** `R1 ∥ R2`. ADC inputs sample through a small capacitor and want a
  low-impedance source; AVR ADC documentation recommends roughly 10 kΩ or less 🟡. A 0.1 µF
  capacitor at the pin or an op-amp buffer fixes a high-impedance divider.

The tool trades these two: among pairs within 0.5% of target it picks the lowest total
resistance the current budget allows.

## 5. What this does not cover

Resistor tolerance stacking (two 5% parts can move the ratio by up to ~10%), temperature
drift, and ADC reference accuracy. For a measurement that matters, use 1% parts and
calibrate against a multimeter.

## Sources

1. Horowitz & Hill, *The Art of Electronics*, 3rd ed., Cambridge University Press, 2015 — ch. 1 (LEDs, dividers, source impedance).
2. IEC 60063, *Preferred number series for resistors and capacitors* — E-series definitions.
3. Microchip/Atmel, ATmega328P datasheet — ADC section, recommended source impedance.
4. SparkFun Learn, *Voltage Dividers* tutorial.
5. Adafruit Learning System, *All About LEDs*.
6. Scherz & Monk, *Practical Electronics for Inventors*, 4th ed., McGraw-Hill, 2016.
