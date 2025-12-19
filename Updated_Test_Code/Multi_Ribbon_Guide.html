<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ribbon Cable Interface Hardware Guide</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #a0aec0;
            font-size: 1.1em;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        h2 {
            color: #2d3748;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        h3 {
            color: #4a5568;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .schematic-box {
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        
        .component {
            background: white;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .component-title {
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .pin-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.95em;
        }
        
        .pin-table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        .pin-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .pin-table tr:hover {
            background: #f7fafc;
        }
        
        .warning {
            background: #fff5f5;
            border-left: 4px solid #f56565;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .warning-title {
            color: #c53030;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .tip {
            background: #f0fff4;
            border-left: 4px solid #48bb78;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .tip-title {
            color: #2f855a;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .tool-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .tool-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .tool-item strong {
            display: block;
            margin-bottom: 5px;
            font-size: 1.1em;
        }
        
        code {
            background: #edf2f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #c7254e;
        }
        
        .diagram {
            background: white;
            border: 2px solid #cbd5e0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        
        .ascii-art {
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.2;
            color: #2d3748;
            white-space: pre;
            text-align: left;
            overflow-x: auto;
        }
        
        .steps {
            counter-reset: step;
        }
        
        .step {
            counter-increment: step;
            background: #f7fafc;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            position: relative;
            padding-left: 60px;
        }
        
        .step::before {
            content: counter(step);
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: #667eea;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔌 Multi-Ribbon Interface Hardware Guide</h1>
            <p class="subtitle">Complete guide for connecting laptop ribbons to Raspberry Pi Pico 2</p>
        </header>
        
        <div class="content">
            <!-- SCHEMATIC SECTION -->
            <div class="section">
                <h2>Hardware Schematic</h2>
                
                <div class="diagram">
                    <div class="ascii-art">
┌─────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI PICO 2                          │
│                                                                 │
│  GP0(TX) ●────────────────────────────► USB Serial (Config)    │
│  GP1(RX) ●────────────────────────────► USB Serial (Config)    │
│                                                                 │
│  GP2-5   ●──┐                                                   │
│             ├──────────────────► Keyboard Rows (CONN1)          │
│  GP6-11  ●──┘                                                   │
│             └──────────────────► Keyboard Columns (CONN1)       │
│                                                                 │
│  GP16(SDA)●─────┬──────────────► Trackpad SDA (CONN2)          │
│  GP17(SCL)●─────┴──────────────► Trackpad SCL (CONN2)          │
│                 │                                               │
│                 └── 4.7kΩ Pull-ups to 3.3V                     │
│                                                                 │
│  GP20    ●─────────────────────► USB D+ (CONN3)                │
│  GP21    ●─────────────────────► USB D- (CONN3)                │
│                                                                 │
│  3.3V    ●─────────────────────► Power to Ribbons              │
│  GND     ●─────────────────────► Common Ground                 │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│  CONNECTOR 1 (FFC)   │  Keyboard Matrix (0.5mm pitch, 10-pin)
│  ┌────────────────┐  │
│  │ 1  2  3  4  5  │  │  Pins 1-4:  Rows    → GP2-GP5
│  │ 6  7  8  9 10  │  │  Pins 6-10: Columns → GP6-GP11
│  └────────────────┘  │  Pin 5:     GND
└──────────────────────┘

┌──────────────────────┐
│  CONNECTOR 2 (FFC)   │  Trackpad I2C (1.0mm pitch, 4-pin)
│  ┌──────────────┐    │
│  │ 1  2  3  4   │    │  Pin 1: 3.3V
│  └──────────────┘    │  Pin 2: SDA → GP16 (with 4.7kΩ pull-up)
└──────────────────────┘  Pin 3: SCL → GP17 (with 4.7kΩ pull-up)
                          Pin 4: GND

┌──────────────────────┐
│  CONNECTOR 3 (FFC)   │  USB Passthrough (0.5mm pitch, 4-pin)
│  ┌──────────────┐    │
│  │ 1  2  3  4   │    │  Pin 1: VCC (5V - not connected to Pico)
│  └──────────────┘    │  Pin 2: D-  → GP21
└──────────────────────┘  Pin 3: D+  → GP20
                          Pin 4: GND

POWER DISTRIBUTION:
═══════════════════
     USB 5V
        │
        ├──────► Pico VSYS (Powers Pico)
        │
        └──────► Optional: Buck converter → Ribbon 5V devices

     Pico 3.3V Out
        │
        ├──────► Keyboard connector
        ├──────► Trackpad connector (via pull-ups)
        └──────► Level shifters (if needed)
                    </div>
                </div>
                
                <div class="component">
                    <div class="component-title">Required Components</div>
                    <table class="pin-table">
                        <tr>
                            <th>Component</th>
                            <th>Specification</th>
                            <th>Quantity</th>
                            <th>Purpose</th>
                        </tr>
                        <tr>
                            <td>FFC/FPC Connectors</td>
                            <td>0.5mm pitch, various pin counts</td>
                            <td>2-5</td>
                            <td>Connect ribbon cables</td>
                        </tr>
                        <tr>
                            <td>FFC/FPC Connectors</td>
                            <td>1.0mm pitch, various pin counts</td>
                            <td>1-3</td>
                            <td>Trackpad and wider ribbons</td>
                        </tr>
                        <tr>
                            <td>Pull-up Resistors</td>
                            <td>4.7kΩ, 1/4W</td>
                            <td>2-4</td>
                            <td>I2C lines (SDA/SCL)</td>
                        </tr>
                        <tr>
                            <td>Logic Level Shifter</td>
                            <td>Bidirectional, 3.3V ↔ 5V</td>
                            <td>1</td>
                            <td>If ribbons use 5V logic</td>
                        </tr>
                        <tr>
                            <td>Capacitors</td>
                            <td>0.1µF ceramic</td>
                            <td>3-5</td>
                            <td>Power decoupling near connectors</td>
                        </tr>
                        <tr>
                            <td>PCB or Breadboard</td>
                            <td>-</td>
                            <td>1</td>
                            <td>Mount all components</td>
                        </tr>
                    </table>
                </div>

                <div class="warning">
                    <div class="warning-title">⚠️ Critical Safety Notes</div>
                    <ul>
                        <li><strong>Voltage Check:</strong> Always verify ribbon voltage BEFORE connecting to Pico (max 3.3V on GPIO)</li>
                        <li><strong>Hot Plugging:</strong> Never connect/disconnect ribbons while powered - can damage Pico</li>
                        <li><strong>Short Protection:</strong> Check for shorts with multimeter before powering</li>
                        <li><strong>ESD Protection:</strong> Use anti-static precautions when handling ribbons and Pico</li>
                    </ul>
                </div>
            </div>

            <!-- RIBBON DECODING SECTION -->
            <div class="section">
                <h2>Ribbon Cable Decoding Guide</h2>
                
                <h3>Tools You'll Need</h3>
                <div class="tool-list">
                    <div class="tool-item">
                        <strong>Digital Multimeter</strong>
                        Must have continuity tester and voltage measurement
                    </div>
                    <div class="tool-item">
                        <strong>Logic Analyzer</strong>
                        8-channel minimum (Saleae, cheap clones work)
                    </div>
                    <div class="tool-item">
                        <strong>USB Microscope</strong>
                        For inspecting connector pins and traces
                    </div>
                    <div class="tool-item">
                        <strong>Breakout Boards</strong>
                        FFC/FPC to pin headers for safe testing
                    </div>
                </div>

                <h3>Step-by-Step Decoding Process</h3>
                <div class="steps">
                    <div class="step">
                        <strong>Identify Pin Count and Pitch</strong>
                        <p>Count the pins on the ribbon connector and measure the spacing between pins with calipers. Common pitches: 0.5mm (most common), 1.0mm, 1.25mm.</p>
                    </div>
                    
                    <div class="step">
                        <strong>Find Power and Ground Pins</strong>
                        <p>With the original laptop powered ON (be careful!):</p>
                        <ul>
                            <li>Set multimeter to DC voltage mode</li>
                            <li>Black probe to laptop ground (screw hole, metal chassis)</li>
                            <li>Probe each pin - look for 3.3V, 5V, or 0V (GND)</li>
                            <li>Mark power pins with colored tape/labels</li>
                        </ul>
                    </div>
                    
                    <div class="step">
                        <strong>Continuity Testing</strong>
                        <p>With laptop powered OFF:</p>
                        <ul>
                            <li>Test continuity between each ribbon pin and the device it connects to</li>
                            <li>For keyboards: trace to the key switches</li>
                            <li>For trackpads: trace to the trackpad chip</li>
                            <li>Map which ribbon pin goes where</li>
                        </ul>
                    </div>
                    
                    <div class="step">
                        <strong>Signal Identification with Logic Analyzer</strong>
                        <p>Connect logic analyzer to unknown signal pins:</p>
                        <ul>
                            <li>Power on laptop with ribbon connected</li>
                            <li>For keyboards: press keys and watch for signal changes</li>
                            <li>For I2C: look for clock + data patterns (SCL/SDA)</li>
                            <li>For SPI: look for clock + MOSI + MISO + CS</li>
                            <li>USB: look for differential pair (D+/D-)</li>
                        </ul>
                    </div>
                    
                    <div class="step">
                        <strong>Document Your Findings</strong>
                        <p>Create a pinout diagram showing:</p>
                        <ul>
                            <li>Pin numbers (1, 2, 3...)</li>
                            <li>Function (GND, VCC, DATA, etc.)</li>
                            <li>Voltage levels</li>
                            <li>Protocol (I2C addr, SPI mode, etc.)</li>
                        </ul>
                    </div>
                </div>

                <div class="tip">
                    <div class="tip-title">💡 Pro Tips</div>
                    <ul>
                        <li><strong>Label everything:</strong> Use a label maker or tape with pin numbers</li>
                        <li><strong>Take photos:</strong> Document before disconnecting anything</li>
                        <li><strong>Search datasheets:</strong> If you find chip numbers, search for datasheets</li>
                        <li><strong>Community help:</strong> Post on forums like BadCaps, EEVBlog with photos</li>
                    </ul>
                </div>
            </div>

            <!-- SPECIFIC RIBBON TYPES -->
            <div class="section">
                <h2>Common Ribbon Types & Protocols</h2>
                
                <div class="component">
                    <div class="component-title">Keyboard Matrix Ribbons</div>
                    <p><strong>Typical Characteristics:</strong></p>
                    <ul>
                        <li>8-30 pins (usually 10-16)</li>
                        <li>Organized as rows and columns</li>
                        <li>Rows are outputs (driven by controller)</li>
                        <li>Columns are inputs (read by controller)</li>
                        <li>Usually 3.3V or 5V logic</li>
                    </ul>
                    <p><strong>How to Identify:</strong> Press keys while monitoring pins - you'll see row + column combinations change</p>
                </div>

                <div class="component">
                    <div class="component-title">Trackpad I2C Ribbons</div>
                    <p><strong>Typical Characteristics:</strong></p>
                    <ul>
                        <li>4-8 pins</li>
                        <li>VCC (3.3V), GND, SDA, SCL minimum</li>
                        <li>May include: INT (interrupt), RST (reset)</li>
                        <li>Common I2C addresses: 0x2A, 0x2C, 0x15</li>
                        <li>Clock speed: 100kHz or 400kHz</li>
                    </ul>
                    <p><strong>How to Identify:</strong> Look for two signals that show clock-like pattern (SCL) and data pattern (SDA). Use logic analyzer with I2C decoder.</p>
                </div>

                <div class="component">
                    <div class="component-title">USB Ribbons</div>
                    <p><strong>Typical Characteristics:</strong></p>
                    <ul>
                        <li>4 pins: VCC (5V), D-, D+, GND</li>
                        <li>D+/D- are differential pair</li>
                        <li>Often color coded: Red (VCC), White (D-), Green (D+), Black (GND)</li>
                        <li>480 Mbps for USB 2.0</li>
                    </ul>
                    <p><strong>How to Identify:</strong> Look for tightly coupled pair of traces, measure for ~5V on power pin</p>
                </div>

                <div class="component">
                    <div class="component-title">Display/LVDS Ribbons</div>
                    <p><strong>Typical Characteristics:</strong></p>
                    <ul>
                        <li>20-50+ pins (very high pin count)</li>
                        <li>Multiple differential pairs</li>
                        <li>High-speed signals (requires specialized hardware)</li>
                        <li>Usually NOT compatible with basic GPIO</li>
                    </ul>
                    <div class="warning">
                        <div class="warning-title">⚠️ Not Recommended</div>
                        Display ribbons require specialized LVDS converters and are beyond basic Pico GPIO capabilities.
                    </div>
                </div>
            </div>

            <!-- PCB DESIGN TIPS -->
            <div class="section">
                <h2>PCB Design Tips</h2>
                
                <h3>Layout Considerations</h3>
                <ul>
                    <li><strong>Keep I2C lines short:</strong> Minimize trace length for SDA/SCL to reduce noise</li>
                    <li><strong>Ground plane:</strong> Use a solid ground plane on bottom layer</li>
                    <li><strong>Decoupling caps:</strong> Place 0.1µF caps close to each FFC connector's VCC pin</li>
                    <li><strong>Connector spacing:</strong> Leave 5-10mm between connectors for cable routing</li>
                    <li><strong>Test points:</strong> Add test points for all signal lines for debugging</li>
                </ul>

                <h3>Recommended PCB Services</h3>
                <ul>
                    <li><strong>JLCPCB:</strong> Cheap, fast, good for prototypes ($2 for 5 boards)</li>
                    <li><strong>PCBWay:</strong> Slightly more expensive, better quality control</li>
                    <li><strong>OSH Park:</strong> US-based, higher quality, purple PCBs</li>
                </ul>

                <div class="tip">
                    <div class="tip-title">💡 Breadboard Prototype First</div>
                    Before designing a PCB, prototype on a breadboard using FFC breakout boards. This lets you test pinouts and protocols before committing to a PCB design.
                </div>
            </div>

            <!-- TROUBLESHOOTING -->
            <div class="section">
                <h2>Troubleshooting Common Issues</h2>
                
                <div class="component">
                    <div class="component-title">Device Not Detected</div>
                    <ul>
                        <li>Check all connections with continuity tester</li>
                        <li>Verify power voltage (should be 3.3V or as specified)</li>
                        <li>Check if ribbon is inserted correct way (pin 1 orientation)</li>
                        <li>Try adding pull-up resistors to I2C lines</li>
                        <li>Verify with oscilloscope/logic analyzer that signals are present</li>
                    </ul>
                </div>

                <div class="component">
                    <div class="component-title">Intermittent Connection</div>
                    <ul>
                        <li>Clean ribbon contacts with isopropyl alcohol</li>
                        <li>Check FFC connector locking mechanism</li>
                        <li>Replace ribbon cable if damaged</li>
                        <li>Verify solder joints on PCB</li>
                    </ul>
                </div>

                <div class="component">
                    <div class="component-title">Pico Won't Boot After Connection</div>
                    <ul>
                        <li><strong>IMMEDIATELY DISCONNECT:</strong> You may have a short circuit</li>
                        <li>Check for shorts between VCC and GND with multimeter</li>
                        <li>Verify no pins are shorted together</li>
                        <li>Test Pico alone to ensure it still works</li>
                        <li>Check for reversed polarity on ribbon</li>
                    </ul>
                </div>
            </div>

            <!-- NEXT STEPS -->
            <div class="section">
                <h2>Ready to Build?</h2>
                <p>Here's your action plan:</p>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Identify and decode your ribbon cables using the guide above</li>
                    <li>Order FFC/FPC breakout boards for safe testing</li>
                    <li>Prototype on breadboard first</li>
                    <li>Test with the Python code provided earlier</li>
                    <li>Design custom PCB once everything works</li>
                    <li>Scale up your project!</li>
                </ol>
            </div>
        </div>
    </div>
</body>
</html>
