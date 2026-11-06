# Electronics Maker Handbook

> Domain reference for the `electronics-maker` skill. Platform selection, circuit basics,
> soldering, PCB design, sensors, IoT, enclosures, community and documentation guidance.
> Supplied by the skill's author and kept as written; the cited, checkable sizing and safety
> material lives in `component_sizing_canon.md` and `power_and_safety_canon.md`.

## Microcontroller Platforms

Guide users to the right platform for their project:

### Arduino
- Best for: Beginners, real-time control, sensor projects, robotics, simple automation.
- Ecosystem: Massive library support, extensive tutorials, huge community.
- Key boards: Arduino Uno (learning), Nano (compact), Mega (many pins), Nano Every (modern replacement).
- Programming: C/C++ via Arduino IDE. Simple setup, beginner-friendly functions (digitalRead, analogWrite, Serial.print).
- Limitations: No built-in networking (need shields), limited processing power, no OS.

### Raspberry Pi
- Best for: Projects needing a full OS, networking, cameras, displays, media, machine learning, web servers.
- Key boards: Pi 5 (full power), Pi Zero 2 W (compact and cheap), Pi Pico (microcontroller, not Linux).
- Programming: Python (recommended), but supports any Linux-compatible language.
- Advantages: Full Linux environment, HDMI output, USB, WiFi, Bluetooth, GPIO pins.
- Not ideal for: Real-time control, battery-powered projects (high power consumption), analog input (no built-in ADC).

### ESP32
- Best for: IoT projects, WiFi/Bluetooth connectivity, battery-powered applications, cost-sensitive projects.
- Features: Built-in WiFi and Bluetooth, dual core, low power modes, ADC, DAC, touch sensors.
- Programming: Arduino IDE (with ESP32 board package), MicroPython, ESP-IDF (advanced).
- Variants: ESP32-S3 (USB native, AI acceleration), ESP32-C3 (RISC-V, ultra low cost).
- Excellent for: Home automation, environmental monitoring, connected devices.

## Circuit Design Basics

Teach fundamental electronics concepts practically:

- **Ohm's Law**: V = IR. Use it to calculate resistor values for LEDs, voltage dividers, and current limiting.
- **Power**: P = VI. Calculate power dissipation to avoid burning components.
- **Series vs parallel**: Understand how voltage and current distribute in each configuration.
- **Voltage dividers**: Two resistors to step down voltage. Essential for sensor interfacing.
- **Pull-up/pull-down resistors**: Prevent floating inputs on digital pins. Most microcontrollers have internal pull-ups.
- **Capacitors**: Decoupling (0.1uF near ICs), bulk filtering (10-100uF on power rails), timing circuits.
- **Transistors as switches**: Use MOSFETs (logic level) or BJTs with base resistors to control high-current loads from microcontroller pins.
- **Diodes**: Flyback diodes across relays/motors, reverse polarity protection, voltage regulation (Zener).

Use breadboards for prototyping. Fritzing or Tinkercad Circuits for virtual breadboarding.

## Soldering

Build reliable permanent circuits:

- **Equipment**: Temperature-controlled soldering iron (60W, chisel tip), lead-free solder (0.8mm), flux, solder wick, solder sucker, helping hands, fume extractor.
- **Technique**: Heat the pad and lead simultaneously, apply solder to the joint (not the iron), hold for 1-2 seconds, remove solder then iron. A good joint is shiny and concave.
- **Common mistakes**: Cold joints (grainy, dull), bridges (solder connecting adjacent pins), too much solder, burned pads from excessive heat.
- **Through-hole**: Easier for beginners. Insert component, solder from the back, trim leads.
- **Surface mount (SMD)**: Requires finer tip, magnification, and steady hands. Start with larger packages (0805 resistors, SOT-23 transistors).
- **Practice**: Solder practice kits are inexpensive and build confidence before working on real projects.

## PCB Design

Move from breadboard to professional circuits:

- **Tools**: KiCad (free, powerful, industry-standard), EasyEDA (free, web-based, integrates with JLCPCB), Fritzing (beginner-friendly).
- **Process**: Schematic capture, footprint assignment, board layout, design rule check, Gerber export, fabrication.
- **Design rules**: Maintain clearances (0.2mm minimum for hobby), use ground planes, keep traces short for high-frequency signals, use appropriate trace widths for current (use a trace width calculator).
- **Fabrication**: JLCPCB, PCBWay, OSH Park. Costs as low as $2-5 for 5 boards (plus shipping).
- **Assembly**: Order stencils for SMD, use solder paste and a hot plate or reflow oven for batch assembly.

## Sensors and Actuators

Common components for maker projects:

- **Temperature/humidity**: DHT22, BME280 (also pressure), DS18B20 (waterproof, one-wire).
- **Motion**: PIR sensors, accelerometers (MPU6050), ultrasonic distance (HC-SR04), IR proximity.
- **Light**: Photoresistors (LDR), phototransistors, ambient light sensors (BH1750), color sensors.
- **Sound**: Electret microphones, I2S MEMS microphones, piezo elements.
- **Actuators**: Servo motors (position control), DC motors (with H-bridge driver), stepper motors (precise rotation), solenoids, relays.
- **Displays**: OLED (SSD1306, 0.96"), TFT LCD, e-paper, LED matrices, seven-segment displays.
- **Communication modules**: GPS (NEO-6M), LoRa (SX1276), NFC/RFID (RC522), CAN bus.

Always check voltage levels and current requirements before connecting components.

## IoT Projects

Build connected devices:

- **Protocols**: MQTT (lightweight, perfect for IoT), HTTP/REST (simple, familiar), WebSockets (real-time bidirectional).
- **Platforms**: Home Assistant (local, privacy-focused), MQTT brokers (Mosquitto), Blynk (mobile dashboards), Adafruit IO (beginner-friendly), AWS IoT / Google Cloud IoT (production scale).
- **Security**: Use TLS/SSL for all connections. Never hardcode credentials — use environment variables or secure storage. Change default passwords. Update firmware regularly.
- **Power management**: Deep sleep modes on ESP32 (microamps). Solar panels with LiPo batteries for outdoor deployments. Calculate battery life before deploying.
- **Data handling**: Send only what you need. Buffer data locally in case of connectivity loss. Use JSON for structured messages.

## 3D Printing Enclosures

Design functional housings for electronics:

- Leave clearance (0.3-0.5mm) for components that need to fit snugly.
- Design mounting posts for PCBs with M2.5 or M3 standoffs.
- Include ventilation holes for heat-generating components.
- Add cable routing channels and strain relief for connectors.
- Use snap-fit or screw-boss designs for assembly — avoid glue when possible.
- Export models as STL; design in Fusion 360, OpenSCAD, or FreeCAD.
- Print prototypes in PLA; use PETG or ABS for enclosures near heat sources.

## Maker Community Resources

Connect users with the community:

- **Learning**: Adafruit Learning System, SparkFun tutorials, Arduino project hub, Instructables, Hackaday.
- **Components**: DigiKey, Mouser, Adafruit, SparkFun, AliExpress (budget, slower shipping).
- **Community**: Reddit (r/arduino, r/raspberry_pi, r/electronics), Hackaday.io, maker spaces and fab labs.
- **Events**: Maker Faire, local hack nights, ham radio clubs, robotics competitions.

## Project Documentation

Document projects for yourself and others:

- Include: project goal, parts list with sources, schematic, code (commented), build photos, lessons learned.
- Host code on GitHub with a clear README.
- Share on Hackaday.io, Instructables, or your own blog.
- License your work explicitly (MIT, GPL, CC-BY-SA).
- Include what did not work — failures teach others more than polished successes.

## Anti-Patterns

**Over-engineering for hypothetical requirements.** Building for scenarios that may never materialize adds complexity without value. Solve the problem in front of you first.

**Ignoring the existing ecosystem.** Reinventing functionality that mature libraries already provide wastes time and introduces risk.

**Premature abstraction.** Creating elaborate frameworks before having enough concrete cases to know what the abstraction should look like produces the wrong abstraction.

**Neglecting error handling at system boundaries.** Internal code can trust its inputs, but boundaries with external systems require defensive validation.

**Skipping documentation.** What is obvious to you today will not be obvious to your colleague next month or to you next year.
