"""
Raspberry Pi Pico DPI to HDMI Adapter
Note: This implementation provides VGA-level output (640x480) through DPI signals
that can be converted to HDMI with an external adapter board.
"""
from machine import Pin, PWM
import array
import time
import rp2

# Configuration for 640x480 @ 60Hz
WIDTH = 640
HEIGHT = 480
H_SYNC_PULSE = 96
H_FRONT_PORCH = 16
H_BACK_PORCH = 48
V_SYNC_PULSE = 2
V_FRONT_PORCH = 10
V_BACK_PORCH = 33

# Total line and frame timing
H_TOTAL = WIDTH + H_SYNC_PULSE + H_FRONT_PORCH + H_BACK_PORCH
V_TOTAL = HEIGHT + V_SYNC_PULSE + V_FRONT_PORCH + V_BACK_PORCH

# Pixel clock is 25.175 MHz for VGA 640x480@60Hz
# Since the PIO runs at up to 125MHz, we use a divider of 5 approx.
CLOCK_DIV = 5

# Define GPIO pins
# RGB pins - 8 bits total (3 red, 3 green, 2 blue)
RED_PINS = [2, 3, 4]
GREEN_PINS = [5, 6, 7]
BLUE_PINS = [8, 9]
HSYNC_PIN = 10
VSYNC_PIN = 11
CLOCK_PIN = 12

# Create RGB, HSYNC and VSYNC pins
red_pins = [Pin(pin, Pin.OUT) for pin in RED_PINS]
green_pins = [Pin(pin, Pin.OUT) for pin in GREEN_PINS]
blue_pins = [Pin(pin, Pin.OUT) for pin in BLUE_PINS]
hsync = Pin(HSYNC_PIN, Pin.OUT)
vsync = Pin(VSYNC_PIN, Pin.OUT)
pixel_clock = Pin(CLOCK_PIN, Pin.OUT)

# Define PIO program for HSYNC
@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    autopull=True,
    pull_thresh=32,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
)
def hsync_program():
    # Output high for visible area plus front porch
    set(pins, 1)                           # HSYNC high during visible and front porch
    mov(x, osr)                            # Load X with visible + front porch count
    label("hsync_high")
    jmp(x_dec, "hsync_high")               # Stay high for X cycles
    
    # Output low for sync pulse
    set(pins, 0)                           # HSYNC low during sync pulse
    mov(x, isr)                            # Load X with sync pulse count
    label("hsync_low")
    jmp(x_dec, "hsync_low")                # Stay low for X cycles
    
    # Output high for back porch
    set(pins, 1)                           # HSYNC high during back porch
    mov(x, osr)                            # Load X with back porch count
    label("hsync_backporch")
    jmp(x_dec, "hsync_backporch")          # Stay high for X cycles

# Define PIO program for VSYNC
@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    autopull=True,
    pull_thresh=32,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
)
def vsync_program():
    # Output high for visible area plus front porch
    set(pins, 1)                           # VSYNC high during visible and front porch
    mov(x, osr)                            # Load X with visible + front porch count
    label("vsync_high")
    jmp(x_dec, "vsync_high")               # Stay high for X cycles
    
    # Output low for sync pulse
    set(pins, 0)                           # VSYNC low during sync pulse
    mov(x, isr)                            # Load X with sync pulse count
    label("vsync_low")
    jmp(x_dec, "vsync_low")                # Stay low for X cycles
    
    # Output high for back porch
    set(pins, 1)                           # VSYNC high during back porch
    mov(x, osr)                            # Load X with back porch count
    label("vsync_backporch")
    jmp(x_dec, "vsync_backporch")          # Stay high for X cycles

# Define PIO program for RGB pixel data
@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    autopull=True,
    pull_thresh=32,
    out_shiftdir=rp2.PIO.SHIFT_RIGHT,
    fifo_join=rp2.PIO.JOIN_TX,
)
def rgb_program():
    # Output pixel data
    out(pins, 8)                          # Output 8 bits of RGB data

# Initialize pixel clock
pwm = PWM(pixel_clock)
pwm.freq(25_175_000 // CLOCK_DIV)  # Set pixel clock frequency
pwm.duty_u16(32768)               # 50% duty cycle

# Initialize state machines
sm_hsync = rp2.StateMachine(0, hsync_program, freq=25_175_000, set_base=hsync)
sm_vsync = rp2.StateMachine(1, vsync_program, freq=25_175_000 // H_TOTAL, set_base=vsync)
sm_rgb = rp2.StateMachine(2, rgb_program, freq=25_175_000, out_base=red_pins[0])

# HSYNC timing (visible + front porch, sync pulse, back porch)
hsync_visible_front = WIDTH + H_FRONT_PORCH - 1
hsync_sync = H_SYNC_PULSE - 1
hsync_back = H_BACK_PORCH - 1

# VSYNC timing (visible + front porch, sync pulse, back porch)
vsync_visible_front = HEIGHT + V_FRONT_PORCH - 1
vsync_sync = V_SYNC_PULSE - 1
vsync_back = V_BACK_PORCH - 1

# Create frame buffer (for test pattern)
def create_test_pattern():
    """Create a test pattern with color bars"""
    buffer = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Create color bars
            if x < WIDTH // 7:
                # White
                color = 0xFF
            elif x < 2 * WIDTH // 7:
                # Yellow
                color = 0xFC
            elif x < 3 * WIDTH // 7:
                # Cyan
                color = 0xF3
            elif x < 4 * WIDTH // 7:
                # Green
                color = 0xF0
            elif x < 5 * WIDTH // 7:
                # Magenta
                color = 0xCF
            elif x < 6 * WIDTH // 7:
                # Red
                color = 0xCC
            else:
                # Blue
                color = 0x33
            row.append(color)
        buffer.append(row)
    return buffer

# Start state machines
def start_display():
    # Put timing values into TX FIFOs
    sm_hsync.put(hsync_visible_front)
    sm_hsync.put(hsync_sync)
    sm_hsync.put(hsync_back)
    
    sm_vsync.put(vsync_visible_front)
    sm_vsync.put(vsync_sync)
    sm_vsync.put(vsync_back)
    
    # Start state machines
    sm_hsync.active(1)
    sm_vsync.active(1)
    sm_rgb.active(1)
    
    # Create test pattern
    framebuffer = create_test_pattern()
    
    # Send pixel data forever
    while True:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                sm_rgb.put(framebuffer[y][x])
            # Wait for HSYNC to complete before starting next line
            time.sleep_us(10)

# Hardware interface info
def print_connection_instructions():
    print("Raspberry Pi Pico DPI to HDMI Adapter Connection Guide:")
    print("-----------------------------------------------------")
    print("This implementation requires an external DPI to HDMI adapter board.")
    print("Connect the following Pico pins to your adapter board:")
    print()
    print("RGB Data Pins:")
    for i, pin in enumerate(RED_PINS):
        print(f"  R{i}: GPIO{pin}")
    for i, pin in enumerate(GREEN_PINS):
        print(f"  G{i}: GPIO{pin}")
    for i, pin in enumerate(BLUE_PINS):
        print(f"  B{i}: GPIO{pin}")
    print()
    print(f"HSYNC: GPIO{HSYNC_PIN}")
    print(f"VSYNC: GPIO{VSYNC_PIN}")
    print(f"PCLK:  GPIO{CLOCK_PIN}")
    print()
    print("You'll need an adapter board like a DPI-to-HDMI converter.")
    print("Suitable options include:")
    print("  - Adafruit DPI TFT Kippah")
    print("  - Custom DPI to HDMI adapter using chips like TFP410 or ADV7513")
    print()
    print("Starting display with test pattern...")

# Main program
if __name__ == "__main__":
    print_connection_instructions()
    start_display()