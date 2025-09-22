"""
Raspberry Pi Pico Laptop Keyboard Controller
============================================
This code uses CircuitPython and KMK firmware to create a configurable 
laptop keyboard controller that can handle multiple keyboard layouts.
"""

import board
import digitalio
import storage
import supervisor
import usb_hid
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.extensions.media_keys import MediaKeys

# --- Configuration ---
# Set LAYOUT_SELECT_MODE to choose how to select layouts:
# 'button' - Use a button connected to a specific pin
# 'key_combo' - Use a key combination to cycle layouts
# 'config_file' - Read from a config.txt file
LAYOUT_SELECT_MODE = 'key_combo'

# --- Hardware setup ---
# Define pins for row and column connections
# Adjust these pins based on your specific wiring
# This is for a typical matrix; you may need to adjust based on your ribbon cable mapping
ROW_PINS = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5]
COL_PINS = [board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, 
           board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17]

# Optional: Define a pin for a layout selection button
LAYOUT_SELECT_PIN = board.GP28

# --- Keyboard Setup ---
keyboard = KMKKeyboard()
keyboard.modules.append(Layers())
keyboard.modules.append(ModTap())
keyboard.extensions.append(MediaKeys())

# Set up the matrix
keyboard.col_pins = COL_PINS
keyboard.row_pins = ROW_PINS
keyboard.diode_orientation = DiodeOrientation.COL2ROW  # Adjust if needed

# --- Available layouts ---
# These layouts map matrix positions to key codes
# Format: Each list represents a row, each entry in the list represents a key in that position

# US QWERTY layout
LAYOUT_US_QWERTY = [
    [KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12],
    [KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC],
    [KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS],
    [KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENT],
    [KC.LSFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT],
    [KC.LCTL, KC.LGUI, KC.LALT, KC.SPC, KC.RALT, KC.RGUI, KC.APP, KC.RCTL]
]

# UK layout
LAYOUT_UK = [
    [KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12],
    [KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC],
    [KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.NUHS],  # NUHS is UK # key
    [KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENT],
    [KC.LSFT, KC.NUBS, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT],  # NUBS is UK \ key
    [KC.LCTL, KC.LGUI, KC.LALT, KC.SPC, KC.RALT, KC.RGUI, KC.APP, KC.RCTL]
]

# ISO layout (common in Europe)
LAYOUT_ISO = [
    [KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12],
    [KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC],
    [KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.ENT],
    [KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.NUHS],  # NUHS is ISO # key
    [KC.LSFT, KC.NUBS, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, KC.RSFT],  # NUBS is ISO \ key
    [KC.LCTL, KC.LGUI, KC.LALT, KC.SPC, KC.RALT, KC.RGUI, KC.APP, KC.RCTL]
]

# List of all available layouts
LAYOUTS = [LAYOUT_US_QWERTY, LAYOUT_UK, LAYOUT_ISO]
LAYOUT_NAMES = ["US QWERTY", "UK", "ISO"]
current_layout_index = 0

# --- Layout selection and switching logic ---
def setup_layout_selection():
    global current_layout_index
    
    if LAYOUT_SELECT_MODE == 'button':
        # Setup button for layout switching
        layout_button = digitalio.DigitalInOut(LAYOUT_SELECT_PIN)
        layout_button.direction = digitalio.Direction.INPUT
        layout_button.pull = digitalio.Pull.UP
        
        # Check button state at startup
        if not layout_button.value:  # Button is pressed during startup
            current_layout_index = (current_layout_index + 1) % len(LAYOUTS)
            # Blink LED to indicate layout change
            blink_onboard_led(current_layout_index + 1)
            
    elif LAYOUT_SELECT_MODE == 'config_file':
        try:
            with open('/config.txt', 'r') as f:
                saved_layout = f.read().strip()
                if saved_layout in LAYOUT_NAMES:
                    current_layout_index = LAYOUT_NAMES.index(saved_layout)
        except:
            # If file doesn't exist or has invalid content, use default
            pass

def save_layout_preference():
    if LAYOUT_SELECT_MODE == 'config_file':
        # Temporarily disable USB drive to allow file writing
        storage.disable_usb_drive()
        try:
            with open('/config.txt', 'w') as f:
                f.write(LAYOUT_NAMES[current_layout_index])
        except:
            pass
        # Re-enable USB drive
        storage.enable_usb_drive()

def blink_onboard_led(times):
    """Blink the onboard LED to indicate layout selection"""
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    
    for _ in range(times):
        led.value = True
        time.sleep(0.2)
        led.value = False
        time.sleep(0.2)

# --- Define a key combination to switch layouts ---
def cycle_layout():
    global current_layout_index
    current_layout_index = (current_layout_index + 1) % len(LAYOUTS)
    save_layout_preference()
    blink_onboard_led(current_layout_index + 1)
    keyboard.keymap = LAYOUTS[current_layout_index]
    return []  # Return empty sequence to not output any keys

# Define the layout cycle key (Fn+L in this example)
# In your actual implementation, you'd need to define the Fn key somewhere in your layout
LAYOUT_CYCLE = simple_key_sequence(cycle_layout)

# --- Matrix debugging helper ---
def debug_matrix():
    """Function to help map out an unknown keyboard matrix"""
    print("Matrix Debugging Mode")
    
    # Set all row pins as inputs with pull-ups
    rows = []
    for pin in ROW_PINS:
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        rows.append(io)
    
    # Set all column pins as inputs with pull-ups
    cols = []
    for pin in COL_PINS:
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        cols.append(io)
    
    print("Press keys to see which pins are connected...")
    last_states = [True] * (len(rows) + len(cols))
    
    while True:
        states = []
        for io in rows + cols:
            states.append(io.value)
        
        if states != last_states:
            print("Pin states:", end=" ")
            for i, (pin, state) in enumerate(zip(ROW_PINS + COL_PINS, states)):
                if not state:  # active low due to pull-ups
                    if i < len(rows):
                        print(f"Row {i}", end=" ")
                    else:
                        print(f"Col {i - len(rows)}", end=" ")
            print()
            
            last_states = states.copy()
        
        time.sleep(0.01)

# --- Main code ---
def main():
    # Uncomment to enable matrix debugging mode
    # This helps identify which pins are connected to which key positions
    # debug_matrix()
    
    # Setup layout selection 
    setup_layout_selection()
    
    # Set the initial keyboard layout
    keyboard.keymap = LAYOUTS[current_layout_index]
    
    # If using key combo for layout switching, add it to a specific key position
    # For example, replace a rarely used key with the LAYOUT_CYCLE function
    # In this example, we replace the right GUI key
    if LAYOUT_SELECT_MODE == 'key_combo':
        for layout in LAYOUTS:
            # Find the right GUI key and replace it
            row_idx = 5  # Bottom row in our layouts
            key_idx = 5  # Assuming this is the right GUI position
            if row_idx < len(layout) and key_idx < len(layout[row_idx]):
                layout[row_idx][key_idx] = LAYOUT_CYCLE
    
    # Start the keyboard
    keyboard.go()

if __name__ == '__main__':
    main()
