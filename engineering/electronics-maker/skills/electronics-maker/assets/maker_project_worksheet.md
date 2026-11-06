# Maker Project Worksheet

Fill this in before buying parts. One answer per line; if you cannot answer, that is the next thing to work out.

| Question | Your answer | Recommended default |
|---|---|---|
| What must it do? (one sentence, testable) | | Write the pass/fail test first |
| Experience level / tools on hand | | Start with the simplest tool that works |
| Power source: USB, battery, mains | | USB or a sealed supply module |
| Needs WiFi/Bluetooth? | | Yes → ESP32; no → Arduino |
| Run time unattended | | Run `battery_life_estimator.py` first |
| Voltage levels in the circuit (3.3 / 5 / 12 V) | | Check every connection pair |
| Highest current any part draws | | Over the pin limit → use a transistor |
| Any mains or lithium cell involved? | | Read `power_and_safety_canon.md` §5–6 |
| Where does it live? (enclosure, heat, water) | | Prototype in PLA; PETG/ABS near heat |
| Where will you document it? | | GitHub README + one photo set |
