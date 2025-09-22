"""
Keyboard Matrix Mapper for Laptop Keyboards
===========================================
This tool helps you identify the row/column matrix of your laptop keyboard.
Connect each pin from the ribbon cable to a GPIO pin on your Pico, then run this
code to see which connections are made when you press keys.
"""

import board
import digitalio
import time
import usb_cdc

# Define all available GPIO pins on the Pico
ALL_PINS = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, 
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, 
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP26, 
    board.GP27, board.GP28
]

# Pin names for reporting
PIN_NAMES = [
    "GP0", "GP1", "GP2", "GP3", "GP4", "GP5", 
    "GP6", "GP7", "GP8", "GP9", "GP10", "GP11", 
    "GP12", "GP13", "GP14", "GP15", "GP16", "GP17",
    "GP18", "GP19", "GP20", "GP21", "GP22", "GP26", 
    "GP27", "GP28"
]

# Set up serial port for output
serial = usb_cdc.console

def setup_pins():
    """Set up all pins as inputs with pull-ups"""
    pin_ios = []
    for pin in ALL_PINS:
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        pin_ios.append(io)
    return pin_ios

def test_direct_connections():
    """
    First test: Find direct connections between pins.
    This helps identify if the keyboard uses a matrix or direct connections.
    """
    print("Testing for direct connections between pins...")
    pin_ios = setup_pins()
    
    # To store connection information
    connections = {}
    
    for i, output_pin in enumerate(ALL_PINS):
        # Configure this pin as output, low
        pin_ios[i].direction = digitalio.Direction.OUTPUT
        pin_ios[i].value = False
        
        # Check all other pins to see if they're pulled low
        for j, input_pin in enumerate(ALL_PINS):
            if i != j:  # Don't check pin against itself
                if not pin_ios[j].value:  # Connection found
                    if i not in connections:
                        connections[i] = []
                    connections[i].append(j)
                    print(f"Direct connection: {PIN_NAMES[i]} -> {PIN_NAMES[j]}")
        
        # Reset to input with pull-up
        pin_ios[i].direction = digitalio.Direction.INPUT
        pin_ios[i].pull = digitalio.Pull.UP
    
    if not connections:
        print("No direct connections found. This likely uses a matrix.")
    else:
        print(f"Found {len(connections)} direct connections.")
    
    return connections

def find_matrix():
    """
    Find the keyboard matrix by testing all pins as rows and columns.
    Press keys when prompted and the tool will detect connections.
    """
    print("\nKeyboard Matrix Mapping")
    print("======================")
    print("Press keys on your laptop keyboard to see row-column connections.")
    print("Press each key to find out which row and column pins are connected.")
    print("Press Ctrl+C to exit when done.\n")
    
    pin_ios = setup_pins()
    key_map = {}
    
    try:
        while True:
            # Check all possible row-column combinations
            for row_idx in range(len(ALL_PINS)):
                # Set this pin as output low (potential row pin)
                pin_ios[row_idx].direction = digitalio.Direction.OUTPUT
                pin_ios[row_idx].value = False
                
                # Check all other pins as potential column pins
                for col_idx in range(len(ALL_PINS)):
                    if row_idx != col_idx and not pin_ios[col_idx].value:
                        # Connection detected - key is pressed
                        connection = (row_idx, col_idx)
                        if connection not in key_map:
                            print(f"Key detected: Row={PIN_NAMES[row_idx]}, Column={PIN_NAMES[col_idx]}")
                            key_map[connection] = True
                
                # Reset to input with pull-up
                pin_ios[row_idx].direction = digitalio.Direction.INPUT
                pin_ios[row_idx].pull = digitalio.Pull.UP
            
            time.sleep(0.01)  # Small delay to avoid flooding the console
    
    except KeyboardInterrupt:
        # User pressed Ctrl+C to end the mapping
        pass
    
    finally:
        # Clean up - reset all pins
        for io in pin_ios:
            io.deinit()
    
    return key_map

def analyze_results(key_map):
    """Analyze the results to determine the actual matrix size"""
    if not key_map:
        print("No keys detected. Check your connections and try again.")
        return
    
    # Find all unique row and column pins used
    rows = set()
    cols = set()
    for row, col in key_map.keys():
        rows.add(row)
        cols.add(col)
    
    print("\nAnalysis Results:")
    print(f"Found {len(rows)} possible row pins: {', '.join(PIN_NAMES[r] for r in sorted(rows))}")
    print(f"Found {len(cols)} possible column pins: {', '.join(PIN_NAMES[c] for c in sorted(cols))}")
    print(f"Total keys detected: {len(key_map)}")
    
    print("\nSuggested matrix definition for your code:")
    print(f"ROW_PINS = [{', '.join('board.' + PIN_NAMES[r] for r in sorted(rows))}]")
    print(f"COL_PINS = [{', '.join('board.' + PIN_NAMES[c] for c in sorted(cols))}]")

def save_matrix_to_file(key_map):
    """Save the detected matrix to a file for later use"""
    if not key_map:
        return
    
    # Find all unique row and column pins used
    rows = sorted(list(set(row for row, _ in key_map.keys())))
    cols = sorted(list(set(col for _, col in key_map.keys())))
    
    try:
        with open('/matrix_config.py', 'w') as f:
            f.write("# Keyboard Matrix Configuration\n")
            f.write("# Generated by Keyboard Matrix Mapper\n\n")
            f.write("# Row pins\n")
            f.write(f"ROW_PINS = [{', '.join('board.' + PIN_NAMES[r] for r in rows)}]\n\n")
            f.write("# Column pins\n")
            f.write(f"COL_PINS = [{', '.join('board.' + PIN_NAMES[c] for c in cols)}]\n\n")
            f.write("# Key matrix mapping\n")
            f.write("KEY_MATRIX = {\n")
            for row_idx, row in enumerate(rows):
                for col_idx, col in enumerate(cols):
                    if (row, col) in key_map:
                        f.write(f"    ({row_idx}, {col_idx}): 'KEY',  # {PIN_NAMES[row]} - {PIN_NAMES[col]}\n")
            f.write("}\n")
        print("\nMatrix configuration saved to 'matrix_config.py'")
    except:
        print("\nFailed to save configuration file.")

def main():
    print("Laptop Keyboard Matrix Mapper")
    print("=============================")
    print("This tool helps map the matrix of your laptop keyboard")
    print("Connect each ribbon cable pin to a GPIO pin on your Pico.\n")
    
    # First test for direct connections
    connections = test_direct_connections()
    
    input("\nPress Enter to start matrix mapping...")
    
    # Find the matrix by having the user press keys
    key_map = find_matrix()
    
    # Analyze and display results
    analyze_results(key_map)
    
    # Save the matrix to a file
    save_matrix_to_file(key_map)
    
    print("\nMapping complete!")

if __name__ == "__main__":
    main()
