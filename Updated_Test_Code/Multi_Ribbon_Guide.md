# Multi-Ribbon Interface Hardware Guide

Complete guide for connecting laptop ribbons to Raspberry Pi Pico 2

---

## Hardware Schematic

### Basic Connection Overview

```
Raspberry Pi Pico 2 Connections:

GP0(TX)  ──► USB Serial (Config)
GP1(RX)  ──► USB Serial (Config)

GP2-5    ──► Keyboard Rows (CONN1)
GP6-11   ──► Keyboard Columns (CONN1)

GP16(SDA)──► Trackpad SDA (CONN2) with 4.7kΩ pull-up
GP17(SCL)──► Trackpad SCL (CONN2) with 4.7kΩ pull-up

GP20     ──► USB D+ (CONN3)
GP21     ──► USB D- (CONN3)

3.3V     ──► Power to Ribbons
GND      ──► Common Ground
```

### Connector Pinouts

**CONNECTOR 1 - Keyboard Matrix (0.5mm pitch, 10-pin)**
- Pins 1-4: Rows → GP2-GP5
- Pin 5: GND
- Pins 6-10: Columns → GP6-GP11

**CONNECTOR 2 - Trackpad I2C (1.0mm pitch, 4-pin)**
- Pin 1: 3.3V
- Pin 2: SDA → GP16 (with 4.7kΩ pull-up)
- Pin 3: SCL → GP17 (with 4.7kΩ pull-up)
- Pin 4: GND

**CONNECTOR 3 - USB Passthrough (0.5mm pitch, 4-pin)**
- Pin 1: VCC (5V - not connected to Pico)
- Pin 2: D- → GP21
- Pin 3: D+ → GP20
- Pin 4: GND

### Power Distribution

```
USB 5V → Pico VSYS (Powers Pico)
      └→ Optional: Buck converter → Ribbon 5V devices

Pico 3.3V Out → Keyboard connector
             └→ Trackpad connector (via pull-ups)
             └→ Level shifters (if needed)
```

---

## Required Components

| Component | Specification | Qty | Purpose |
|-----------|--------------|-----|---------|
| FFC/FPC Connectors | 0.5mm pitch, various pins | 2-5 | Connect ribbon cables |
| FFC/FPC Connectors | 1.0mm pitch, various pins | 1-3 | Trackpad, wider ribbons |
| Pull-up Resistors | 4.7kΩ, 1/4W | 2-4 | I2C lines (SDA/SCL) |
| Logic Level Shifter | Bidirectional, 3.3V ↔ 5V | 1 | For 5V ribbons |
| Capacitors | 0.1µF ceramic | 3-5 | Power decoupling |
| PCB or Breadboard | - | 1 | Mount components |

---

## Critical Safety Notes

**ALWAYS CHECK THESE BEFORE CONNECTING:**

- **Voltage Check**: Verify ribbon voltage BEFORE connecting to Pico (max 3.3V on GPIO)
- **Hot Plugging**: Never connect/disconnect ribbons while powered
- **Short Protection**: Check for shorts with multimeter before powering
- **ESD Protection**: Use anti-static precautions

---

## Ribbon Cable Decoding Guide

### Tools You'll Need

1. **Digital Multimeter** - Continuity tester and voltage measurement
2. **Logic Analyzer** - 8-channel minimum (Saleae or cheap clones)
3. **USB Microscope** - Inspect connector pins and traces
4. **Breakout Boards** - FFC/FPC to pin headers for testing

---

### Step-by-Step Decoding Process

#### STEP 1: Identify Pin Count and Pitch

Count the pins on the ribbon connector and measure spacing with calipers.

Common pitches:
- 0.5mm (most common)
- 1.0mm
- 1.25mm

#### STEP 2: Find Power and Ground Pins

With original laptop powered ON (be careful!):

1. Set multimeter to DC voltage mode
2. Black probe to laptop ground (screw hole or metal chassis)
3. Probe each pin - look for 3.3V, 5V, or 0V (GND)
4. Mark power pins with colored tape/labels

#### STEP 3: Continuity Testing

With laptop powered OFF:

1. Test continuity between each ribbon pin and the device
2. For keyboards: trace to key switches
3. For trackpads: trace to trackpad chip
4. Map which ribbon pin goes where

#### STEP 4: Signal Identification with Logic Analyzer

Connect logic analyzer to unknown signal pins:

1. Power on laptop with ribbon connected
2. For keyboards: press keys and watch for signal changes
3. For I2C: look for clock + data patterns (SCL/SDA)
4. For SPI: look for clock + MOSI + MISO + CS
5. For USB: look for differential pair (D+/D-)

#### STEP 5: Document Your Findings

Create a pinout diagram with:
- Pin numbers (1, 2, 3...)
- Function (GND, VCC, DATA, etc.)
- Voltage levels
- Protocol info (I2C address, SPI mode, etc.)

---

### Pro Tips for Decoding

- **Label everything** - Use a label maker or tape with pin numbers
- **Take photos** - Document before disconnecting anything
- **Search datasheets** - If you find chip numbers, search for datasheets
- **Community help** - Post on forums like BadCaps or EEVBlog with photos

---

## Common Ribbon Types & Protocols

### 1. Keyboard Matrix Ribbons

**Characteristics:**
- 8-30 pins (usually 10-16)
- Organized as rows and columns
- Rows are outputs (driven by controller)
- Columns are inputs (read by controller)
- Usually 3.3V or 5V logic

**How to Identify:**
Press keys while monitoring pins - you'll see row + column combinations change

---

### 2. Trackpad I2C Ribbons

**Characteristics:**
- 4-8 pins
- VCC (3.3V), GND, SDA, SCL minimum
- May include: INT (interrupt), RST (reset)
- Common I2C addresses: 0x2A, 0x2C, 0x15
- Clock speed: 100kHz or 400kHz

**How to Identify:**
Look for two signals showing clock pattern (SCL) and data pattern (SDA). Use logic analyzer with I2C decoder.

---

### 3. USB Ribbons

**Characteristics:**
- 4 pins: VCC (5V), D-, D+, GND
- D+/D- are differential pair
- Often color coded:
  - Red: VCC
  - White: D-
  - Green: D+
  - Black: GND
- 480 Mbps for USB 2.0

**How to Identify:**
Look for tightly coupled pair of traces, measure for ~5V on power pin

---

### 4. Display/LVDS Ribbons

**Characteristics:**
- 20-50+ pins (very high pin count)
- Multiple differential pairs
- High-speed signals (requires specialized hardware)
- Usually NOT compatible with basic GPIO

**WARNING:** Display ribbons require specialized LVDS converters and are beyond basic Pico GPIO capabilities. Not recommended for this project.

---

## PCB Design Tips

### Layout Considerations

- **Keep I2C lines short** - Minimize trace length for SDA/SCL to reduce noise
- **Ground plane** - Use solid ground plane on bottom layer
- **Decoupling caps** - Place 0.1µF caps close to each FFC connector VCC pin
- **Connector spacing** - Leave 5-10mm between connectors for cable routing
- **Test points** - Add test points for all signal lines for debugging

### Recommended PCB Services

- **JLCPCB** - Cheap, fast, good for prototypes ($2 for 5 boards)
- **PCBWay** - Slightly more expensive, better quality control
- **OSH Park** - US-based, higher quality, purple PCBs

### Important: Breadboard Prototype First

Before designing a PCB, prototype on a breadboard using FFC breakout boards. This lets you test pinouts and protocols before committing to a PCB design.

---

## Troubleshooting Common Issues

### Problem: Device Not Detected

**Solutions:**
- Check all connections with continuity tester
- Verify power voltage (should be 3.3V or as specified)
- Check if ribbon is inserted correct way (pin 1 orientation)
- Try adding pull-up resistors to I2C lines
- Verify with oscilloscope/logic analyzer that signals are present

---

### Problem: Intermittent Connection

**Solutions:**
- Clean ribbon contacts with isopropyl alcohol
- Check FFC connector locking mechanism
- Replace ribbon cable if damaged
- Verify solder joints on PCB

---

### Problem: Pico Won't Boot After Connection

**EMERGENCY STEPS:**

1. **IMMEDIATELY DISCONNECT** - You may have a short circuit
2. Check for shorts between VCC and GND with multimeter
3. Verify no pins are shorted together
4. Test Pico alone to ensure it still works
5. Check for reversed polarity on ribbon

---

## Action Plan: Ready to Build?

Follow these steps in order:

1. Identify and decode your ribbon cables using the guide above
2. Order FFC/FPC breakout boards for safe testing
3. Prototype on breadboard first
4. Test with the Python code provided earlier
5. Design custom PCB once everything works
6. Scale up your project!

---

## Additional Resources

### Where to Get Help
- BadCaps Forum
- EEVBlog Forum
- Raspberry Pi Forums
- Reddit: r/raspberry_pi, r/AskElectronics

### Useful Search Terms
- "laptop ribbon pinout"
- "[laptop model] keyboard connector"
- "FFC breakout board [pitch]mm"
- "I2C trackpad protocol"

---

Good luck with your multi-ribbon interface project!
