Features
1. Device Support:

Keyboard Matrix Scanning: Handles row/column matrix keyboards (common in laptops)
I2C Trackpad: Communicates with I2C-based trackpads
USB Passthrough: Basic USB connection detection

2. Configuration System:

JSON-based configuration via USB serial
Dynamically load/reload device configurations
Map any GPIO pins to any ribbon connector

3. Main Components:

KeyboardMatrix: Scans keyboard matrices and reports pressed keys
TrackpadI2C: Reads trackpad position and button data
USBPassthrough: Detects USB device connections
RibbonManager: Coordinates all devices and handles communication

How to Use

Upload to your Pico 2 using Thonny or similar
Send configuration via serial in JSON format (example included)
The Pico will poll all devices and report data over serial

Configuration Example
The code includes an example config showing how to define 3 connectors with different devices. You can modify the pin numbers to match your physical setup.
Next Steps
Hardware-wise, you'll want to:

Design a PCB with multiple FFC connectors (or use breakout boards)
Wire each connector's pins to the GPIO pins specified in your config
Add pull-up/pull-down resistors as needed
Consider level shifters if any ribbons aren't 3.3V

For specific ribbons, you'll need to:

Identify the pinout (use a multimeter/continuity tester)
Determine the protocol (may require oscilloscope analysis)
Adapt the code classes for your specific devices
