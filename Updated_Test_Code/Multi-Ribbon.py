"""
Raspberry Pi Pico 2 Multi-Ribbon Cable Interface System
Handles keyboard matrix, trackpad I2C, and USB ribbon connections
"""

from machine import Pin, I2C, UART
import time
import json
import sys

class RibbonConfig:
    """Stores configuration for each ribbon connector"""
    def __init__(self, connector_id, device_type, pins, params=None):
        self.connector_id = connector_id
        self.device_type = device_type  # 'keyboard', 'trackpad', 'usb'
        self.pins = pins
        self.params = params or {}

class KeyboardMatrix:
    """Handles keyboard matrix scanning"""
    def __init__(self, row_pins, col_pins):
        self.rows = [Pin(p, Pin.OUT) for p in row_pins]
        self.cols = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in col_pins]
        self.key_state = {}
        
        # Initialize all rows high
        for row in self.rows:
            row.value(1)
    
    def scan(self):
        """Scan keyboard matrix and return pressed keys"""
        pressed = []
        
        for row_idx, row in enumerate(self.rows):
            # Set current row low, others high
            for r in self.rows:
                r.value(1)
            row.value(0)
            
            time.sleep_us(10)  # Settling time
            
            # Check columns
            for col_idx, col in enumerate(self.cols):
                if col.value() == 0:  # Active low when pressed
                    key = (row_idx, col_idx)
                    pressed.append(key)
        
        return pressed
    
    def get_keys(self):
        """Get formatted key presses"""
        keys = self.scan()
        return [f"R{r}C{c}" for r, c in keys]

class TrackpadI2C:
    """Handles I2C trackpad communication"""
    def __init__(self, sda_pin, scl_pin, address=0x2A, freq=400000):
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=freq)
        self.address = address
        self.available = self.check_device()
    
    def check_device(self):
        """Check if trackpad is present"""
        try:
            devices = self.i2c.scan()
            return self.address in devices
        except:
            return False
    
    def read_data(self):
        """Read trackpad data (implementation depends on specific trackpad)"""
        if not self.available:
            return None
        
        try:
            # Example: read 6 bytes (X_low, X_high, Y_low, Y_high, buttons, status)
            data = self.i2c.readfrom(self.address, 6)
            
            x = (data[1] << 8) | data[0]
            y = (data[3] << 8) | data[2]
            buttons = data[4]
            
            return {
                'x': x,
                'y': y,
                'buttons': buttons,
                'left_click': bool(buttons & 0x01),
                'right_click': bool(buttons & 0x02)
            }
        except Exception as e:
            print(f"Trackpad read error: {e}")
            return None

class USBPassthrough:
    """Handles USB data line passthrough"""
    def __init__(self, dp_pin, dm_pin):
        # Note: True USB requires specialized handling
        # This is a simplified example
        self.dp = Pin(dp_pin, Pin.IN)
        self.dm = Pin(dm_pin, Pin.IN)
        self.connected = False
    
    def check_connection(self):
        """Check if USB device is connected"""
        # USB devices pull D+ (or D-) high when connected
        self.connected = self.dp.value() == 1 or self.dm.value() == 1
        return self.connected

class RibbonManager:
    """Main manager for all ribbon connections"""
    def __init__(self):
        self.devices = {}
        self.configs = []
        self.uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    
    def load_config(self, config_json):
        """Load configuration from JSON string"""
        try:
            configs = json.loads(config_json)
            for cfg in configs:
                self.add_device(RibbonConfig(
                    cfg['connector_id'],
                    cfg['device_type'],
                    cfg['pins'],
                    cfg.get('params', {})
                ))
            print(f"Loaded {len(configs)} device configurations")
            return True
        except Exception as e:
            print(f"Config load error: {e}")
            return False
    
    def add_device(self, config):
        """Add a device based on configuration"""
        try:
            if config.device_type == 'keyboard':
                device = KeyboardMatrix(
                    config.pins['rows'],
                    config.pins['cols']
                )
            elif config.device_type == 'trackpad':
                device = TrackpadI2C(
                    config.pins['sda'],
                    config.pins['scl'],
                    config.params.get('address', 0x2A)
                )
            elif config.device_type == 'usb':
                device = USBPassthrough(
                    config.pins['dp'],
                    config.pins['dm']
                )
            else:
                print(f"Unknown device type: {config.device_type}")
                return
            
            self.devices[config.connector_id] = {
                'device': device,
                'config': config
            }
            print(f"Added {config.device_type} on connector {config.connector_id}")
        except Exception as e:
            print(f"Error adding device {config.connector_id}: {e}")
    
    def read_device(self, connector_id):
        """Read data from specific device"""
        if connector_id not in self.devices:
            return None
        
        dev = self.devices[connector_id]
        device_type = dev['config'].device_type
        
        try:
            if device_type == 'keyboard':
                return dev['device'].get_keys()
            elif device_type == 'trackpad':
                return dev['device'].read_data()
            elif device_type == 'usb':
                return {'connected': dev['device'].check_connection()}
        except Exception as e:
            print(f"Error reading {connector_id}: {e}")
            return None
    
    def poll_all(self):
        """Poll all connected devices"""
        results = {}
        for conn_id in self.devices:
            data = self.read_device(conn_id)
            if data:
                results[conn_id] = data
        return results
    
    def send_status(self, data):
        """Send status over UART"""
        try:
            json_str = json.dumps(data) + '\n'
            self.uart.write(json_str)
        except:
            pass
    
    def check_commands(self):
        """Check for incoming configuration commands"""
        if self.uart.any():
            try:
                cmd = self.uart.readline().decode('utf-8').strip()
                if cmd.startswith('{'):
                    return cmd
            except:
                pass
        return None

# Example configuration format
EXAMPLE_CONFIG = """
[
  {
    "connector_id": "CONN1",
    "device_type": "keyboard",
    "pins": {
      "rows": [2, 3, 4, 5],
      "cols": [6, 7, 8, 9, 10, 11]
    }
  },
  {
    "connector_id": "CONN2",
    "device_type": "trackpad",
    "pins": {
      "sda": 16,
      "scl": 17
    },
    "params": {
      "address": 42
    }
  },
  {
    "connector_id": "CONN3",
    "device_type": "usb",
    "pins": {
      "dp": 20,
      "dm": 21
    }
  }
]
"""

def main():
    print("=== Pico 2 Multi-Ribbon Interface ===")
    print("Waiting for configuration...")
    
    manager = RibbonManager()
    
    # Wait for configuration or load default
    config_received = False
    timeout = 10  # 10 seconds to receive config
    start = time.time()
    
    while not config_received and (time.time() - start) < timeout:
        cmd = manager.check_commands()
        if cmd:
            if manager.load_config(cmd):
                config_received = True
                break
        time.sleep(0.1)
    
    if not config_received:
        print("No config received, loading example...")
        manager.load_config(EXAMPLE_CONFIG)
    
    print("Starting main loop...")
    print("Send JSON config via serial to reconfigure")
    print("")
    
    # Main loop
    last_poll = 0
    poll_interval = 0.05  # 50ms polling
    
    while True:
        # Check for new configuration
        cmd = manager.check_commands()
        if cmd:
            print("Reconfiguring...")
            manager.devices.clear()
            manager.load_config(cmd)
        
        # Poll devices
        if time.time() - last_poll >= poll_interval:
            data = manager.poll_all()
            if data:
                # Print to console
                for conn_id, values in data.items():
                    if values:
                        print(f"{conn_id}: {values}")
                
                # Send over UART
                manager.send_status(data)
            
            last_poll = time.time()
        
        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.print_exception(e)
