# Power and Safety Canon

What `battery_life_estimator.py` models, and the hazards the skill must raise.
🟢 standard result · 🟡 varies by part/vendor · 🔴 folklore.

## 1. Duty-cycled average current 🟢

`I_avg = (I_active · t_active + I_sleep · t_sleep) / period`, life = usable capacity / `I_avg`.
It is a weighted average, so a long period dominated by sleep means **sleep current sets the
life**. The tool prints each phase's share; when sleep exceeds 50% it says to cut sleep
current rather than shorten the active burst.

## 2. Measure the board, not the chip 🟡

A microcontroller's datasheet deep-sleep figure excludes the rest of the board. Linear
regulators with high quiescent current, USB-serial bridge chips, power LEDs and pull-ups can
each draw more than the chip in deep sleep. Espressif's sleep-mode documentation states chip
figures only for the chip. Measure the whole board with a multimeter in µA range or a current
profiler, and use that as `--sleep-ua`.

## 3. Capacity derating 🟡

Nominal mAh is measured under favourable conditions. Cold temperature, ageing, high drain and
the protection circuit's cutoff voltage all reduce what you can use. The tool defaults to
`--derate 0.8`; this is a conservative planning figure, not a measured one.

## 4. When the estimate is fiction 🟡

Batteries self-discharge and age whatever the load. Beyond about five years the tool warns
that the arithmetic stops predicting anything.

## 5. Lithium cells — always raise these 🟢

- Use cells with a protection circuit (over-charge, over-discharge, short-circuit) or add one.
- Charge only with a charger designed for the chemistry and cell count.
- Never puncture, crush, or short a cell; do not charge unattended on a flammable surface.
- Do not mix cells of different age or capacity in a pack.

## 6. Mains voltage 🟢

Do not build mains-connected circuits on a breadboard or unenclosed. Use a certified,
enclosed supply module or switching module; keep mains and low-voltage sides physically
separated; fuse the mains side; if you cannot name each of these, hand the mains part to a
qualified electrician. The skill never advises working on live mains.

## 7. Soldering fumes 🟢

Rosin-based flux fume is a recognised cause of occupational asthma; use a fume extractor or
work in ventilated space. Lead-free solder avoids lead exposure but needs a higher
temperature; wash hands before eating regardless.

## Sources

1. Espressif Systems, *ESP-IDF Programming Guide — Sleep Modes* (power figures are chip-level).
2. Adafruit Learning System, *Li-Ion & LiPoly Batteries* — protection circuits and charging.
3. IEC 62133, *Safety requirements for portable sealed secondary cells and batteries*.
4. Battery University (Cadex Electronics), pages on lithium-ion ageing and self-discharge.
5. UK Health and Safety Executive, *Controlling exposure to rosin-based solder fume* (colophony guidance).
6. Horowitz & Hill, *The Art of Electronics*, 3rd ed. — power supplies and safety notes.
