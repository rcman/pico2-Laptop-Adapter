"""
Custom Keyboard Layout Editor for Pico
======================================
This tool allows you to create and test custom keyboard layouts interactively.
It runs on the Pico and lets you assign keycodes to each position in your matrix.

Instructions:
1. Connect your laptop keyboard to the Pico using the appropriate pins
2. Run this tool to interactively map each key
3. Save your custom layout
4. Test your layout in real-time
"""

import board
import digitalio
import time
import usb_hid
import usb_cdc
import storage
import json
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Set up serial for interaction
serial = usb_cdc.console

# Key name to keycode mapping
KEYCODE_MAP = {
    # Basic keys
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D,
    'E': Keycode.E, 'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H,
    'I': Keycode.I, 'J': Keycode.J, 'K': Keycode.K, 'L': Keycode.L,
    'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O, 'P': Keycode.P,
    'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X,
    'Y': Keycode.Y, 'Z': Keycode.Z,
    '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE, '4': Keycode.FOUR,
    '5': Keycode.FIVE, '6': Keycode.SIX, '7': Keycode.SEVEN, '8': Keycode.EIGHT,
    '9': Keycode.NINE, '0': Keycode.ZERO,
    'ENTER': Keycode.ENTER, 'ESC': Keycode.ESCAPE, 'BKSP': Keycode.BACKSPACE,
    'TAB': Keycode.TAB, 'SPACE': Keycode.SPACE, 'MINUS': Keycode.MINUS,
    'EQUAL': Keycode.EQUALS, 'LBRACE': Keycode.LEFT_BRACKET,
    'RBRACE': Keycode.RIGHT_BRACKET, 'BSLASH': Keycode.BACKSLASH,
    'SCOLON': Keycode.SEMICOLON, 'QUOTE': Keycode.QUOTE,
    'GRAVE': Keycode.GRAVE_ACCENT, 'COMMA': Keycode.COMMA,
    'DOT': Keycode.PERIOD, 'SLASH': Keycode.FORWARD_SLASH,
    'CAPS': Keycode.CAPS_LOCK,
    
    # Function keys
    'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3, 'F4': Keycode.F4,
    'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7, 'F8': Keycode.F8,
    'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11, 'F12': Keycode.F12,
    
    # Navigation
    'INSERT': Keycode.INSERT, 'HOME': Keycode.HOME, 'PGUP': Keycode.PAGE_UP,
    'DELETE': Keycode.DELETE, 'END': Keycode.END, 'PGDN': Keycode.PAGE_DOWN,
    'RIGHT': Keycode.RIGHT_ARROW, 'LEFT': Keycode.LEFT_ARROW,
    'DOWN': Keycode.DOWN_ARROW, 'UP': Keycode.UP_ARROW,
    
    # Numeric keypad
    'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'KP_SLASH': Keycode.KEYPAD_FORWARD_SLASH,
    'KP_ASTERISK': Keycode.KEYPAD_ASTERISK, 'KP_MINUS': Keycode.KEYPAD_MINUS,
    'KP_PLUS': Keycode.KEYPAD_PLUS, 'KP_ENTER': Keycode.KEYPAD_ENTER,
    'KP_1': Keycode.KEYPAD_ONE, 'KP_2': Keycode.KEYPAD_TWO,
    'KP_3': Keycode.KEYPAD_THREE, 'KP_4': Keycode.KEYPAD_FOUR,
    'KP_5': Keycode.KEYPAD_FIVE, 'KP_6': Keycode.KEYPAD_SIX,
    'KP_7': Keycode.KEYPAD_SEVEN, 'KP_8': Keycode.KEYPAD_EIGHT,
    'KP_9': Keycode.KEYPAD_NINE, 'KP_0': Keycode.KEYPAD_ZERO,
    'KP_DOT': Keycode.KEYPAD_PERIOD,
    
    # Modifiers
    'LCTRL': Keycode.LEFT_CONTROL, 'LSHIFT': Keycode.LEFT_SHIFT,
    'LALT': Keycode.LEFT_ALT, 'LGUI': Keycode.LEFT_GUI,
    'RCTRL': Keycode.RIGHT_CONTROL, 'RSHIFT': Keycode.RIGHT_SHIFT,
    'RALT': Keycode.RIGHT_ALT, 'RGUI': Keycode.RIGHT_GUI,
    
    # Special keys
    'PRTSCR': Keycode.PRINT_SCREEN, 'SCRLOCK': Keycode.SCROLL_LOCK,
    'PAUSE': Keycode.PAUSE, 'MENU': Keycode.APPLICATION,
    
    # International keys
    'INTL_1': Keycode.INTERNATIONAL_1, # Often \ and | on UK/ISO layouts
    'INTL_2': Keycode.INTERNATIONAL_2, # Often ¢ and ¦ on UK/ISO layouts
    'INTL_3': Keycode.INTERNATIONAL_3, # Often ñ and Ñ on ES layouts
}

# Keycode to name for display
KEYCODE_NAMES = {v: k for k, v in KEYCODE_MAP.items()}

# Interactive menu commands
MENU_COMMANDS = {
    'map': 'Map a key on the matrix',
    'test': 'Test the current layout',
    'save': 'Save the current configuration',
    'load': 'Load a layout',
    'export': 'Export to KMK format',
    'create': 'Create a new layout',
    'edit': 'Edit a layout name',
    'delete': 'Delete a layout',
    'list': 'List available layouts',
    'view': 'View current layout',
    'help': 'Show this help menu',
    'exit': 'Exit the layout editor'
}

# Define default config for row and column pins
DEFAULT_CONFIG = {
    "row_pins": [0, 1, 2, 3, 4, 5],  # GP0-GP5
    "col_pins": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # GP6-GP17
    "current_layout": "default",
    "layouts": {
        "default": {
            # (row, col): keycode
            # This will be populated based on matrix testing
        },
        "us_qwerty": {
            # Predefined US QWERTY layout - will be populated in init_default_layouts
        },
        "uk": {
            # Predefined UK layout - will be populated in init_default_layouts
        }
    }
}

def init_default_layouts(config):
    """Initialize predefined layouts if they don't exist"""
    if "us_qwerty" not in config["layouts"] or not config["layouts"]["us_qwerty"]:
        # This is a simplified layout - actual mapping would depend on the physical matrix
        config["layouts"]["us_qwerty"] = {}
    
    if "uk" not in config["layouts"] or not config["layouts"]["uk"]:
        # This is a simplified layout - actual mapping would depend on the physical matrix
        config["layouts"]["uk"] = {}
    
    return config

def load_config():
    """Load the keyboard configuration from file"""
    try:
        with open('/keyboard_config.json', 'r') as f:
            config = json.load(f)
            return init_default_layouts(config)
    except:
        return init_default_layouts(DEFAULT_CONFIG.copy())

def save_config(config):
    """Save the keyboard configuration to file"""
    # Temporarily disable USB drive to allow writing
    storage.disable_usb_drive()
    try:
        with open('/keyboard_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("Configuration saved successfully.")
        
        # Also generate KMK-compatible keymap file
        generate_kmk_layout(config)
    except Exception as e:
        print(f"Error saving configuration: {e}")
    finally:
        # Re-enable USB drive
        storage.enable_usb_drive()

def generate_kmk_layout(config):
    """Generate a KMK-compatible keymap file from the config"""
    try:
        layout_name = "default"
        if "current_layout" in config:
            layout_name = config["current_layout"]
        
        layout = config["layouts"][layout_name]
        
        # Find matrix dimensions
        max_row = max([r for r, _ in layout.keys()]) if layout else 0
        max_col = max([c for _, c in layout.keys()]) if layout else 0
        
        # Create a template matrix filled with KC.NO (no key)
        matrix = [["KC.NO" for _ in range(max_col + 1)] for _ in range(max_row + 1)]
        
        # Fill in the key mapping
        for pos_str, keycode in layout.items():
            # Convert string position "(r,c)" to integers
            pos = eval(pos_str)
            r, c = pos
            
            key_name = KEYCODE_NAMES.get(keycode, "NO")
            matrix[r][c] = f"KC.{key_name}"
        
        # Generate the Python code
        with open('/kmk_keymap.py', 'w') as f:
            f.write("# KMK Keymap - Generated by Custom Layout Editor\n\n")
            f.write("from kmk.keys import KC\n\n")
            f.write(f"# Layout: {layout_name}\n")
            f.write("KEYMAP = [\n")
            
            for row in matrix:
                row_str = ", ".join(row)
                f.write(f"    [{row_str}],\n")
            
            f.write("]\n")
        
        print("KMK keymap file generated successfully.")
    except Exception as e:
        print(f"Error generating KMK layout: {e}")

def setup_matrix(config):
    """Set up the keyboard matrix based on configuration"""
    row_pins = []
    for pin_num in config["row_pins"]:
        pin = getattr(board, f"GP{pin_num}")
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        row_pins.append(io)
    
    col_pins = []
    for pin_num in config["col_pins"]:
        pin = getattr(board, f"GP{pin_num}")
        io = digitalio.DigitalInOut(pin)
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        col_pins.append(io)
    
    return row_pins, col_pins

def cleanup_matrix(row_pins, col_pins):
    """Clean up GPIO pins"""
    for pin in row_pins + col_pins:
        pin.deinit()

def detect_key_press(row_pins, col_pins, prev_pressed=None):
    """Detect a single key press, ignoring already pressed keys"""
    if prev_pressed is None:
        prev_pressed = []
    
    current_pressed = scan_matrix(row_pins, col_pins)
    
    # Find newly pressed keys
    new_keys = [k for k in current_pressed if k not in prev_pressed]
    
    if new_keys:
        return new_keys[0]  # Return the first new key
    return None

def scan_matrix(row_pins, col_pins):
    """Scan the matrix for pressed keys"""
    pressed_keys = []
    
    # Configure each row for testing
    for r, row_pin in enumerate(row_pins):
        # Set this row pin as output low
        orig_dir = row_pin.direction
        orig_pull = row_pin.pull
        row_pin.direction = digitalio.Direction.OUTPUT
        row_pin.value = False
        
        # Check each column for key presses
        for c, col_pin in enumerate(col_pins):
            if not col_pin.value:  # Key is pressed
                pressed_keys.append((r, c))
        
        # Return the row pin to its original state
        row_pin.direction = orig_dir
        row_pin.pull = orig_pull
    
    return pressed_keys
