/**
 * Raspberry Pi Pico Stepper Motor Controller with Web Interface
 * 
 * This program controls a stepper motor using the Raspberry Pi Pico's GPIO pins
 * and provides a web interface for remote control over WiFi.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/gpio.h"
#include "lwip/apps/httpd.h"
#include "pico/time.h"

// WiFi credentials - replace with your own
const char *ssid = "YourWiFiName";
const char *password = "YourWiFiPassword";

// Motor control pins - adjust as needed for your wiring
#define MOTOR_PIN1 2
#define MOTOR_PIN2 3
#define MOTOR_PIN3 4
#define MOTOR_PIN4 5

// Motor control parameters
#define STEPS_PER_REVOLUTION 200  // Typical for 1.8° stepper
#define MIN_STEP_DELAY_MS 2       // Maximum speed (lower value = faster rotation)
#define MAX_STEP_DELAY_MS 20      // Minimum speed (higher value = slower rotation)

// Global variables for motor control
volatile int step_delay_ms = 10;           // Current step delay
volatile bool motor_running = false;       // Motor state
volatile int current_step = 0;             // Current step position
volatile bool direction = true;            // true = clockwise, false = counterclockwise
volatile int target_steps = 0;             // Target steps to move (0 = continuous)

// Step sequences for the motor (4-step sequence)
const int step_sequence[4][4] = {
    {1, 0, 0, 1},
    {1, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 1}
};

// Function prototypes
void initialize_motor();
void step_motor();
void set_motor_pins(int step);
void motor_task();
void start_motor(int steps, bool clockwise, int speed);
void stop_motor();

// Web interface HTML
const char http_html_header[] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n";
const char http_index_html[] = "<!DOCTYPE html><html>"
    "<head><title>Stepper Motor Control</title>"
    "<meta name='viewport' content='width=device-width, initial-scale=1'>"
    "<style>"
    "body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }"
    "h1 { color: #333; }"
    ".control-panel { max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }"
    "button { background-color: #4CAF50; border: none; color: white; padding: 10px 20px; margin: 10px; text-align: center; "
    "text-decoration: none; display: inline-block; font-size: 16px; border-radius: 5px; cursor: pointer; }"
    "button:hover { background-color: #45a049; }"
    "#stop { background-color: #f44336; }"
    "#stop:hover { background-color: #d32f2f; }"
    "input[type=range] { width: 80%; }"
    ".status { margin-top: 20px; padding: 10px; background-color: #f1f1f1; border-radius: 5px; }"
    "</style></head>"
    "<body>"
    "<div class='control-panel'>"
    "<h1>Stepper Motor Control</h1>"
    "<div>"
    "<button id='cw' onclick='rotate(\"cw\")'>Rotate Clockwise</button>"
    "<button id='ccw' onclick='rotate(\"ccw\")'>Rotate Counter-Clockwise</button>"
    "<button id='stop' onclick='stop()'>Stop</button>"
    "</div>"
    "<div>"
    "<p>Speed Control: <span id='speed-value'>50</span>%</p>"
    "<input type='range' min='1' max='100' value='50' id='speed-control' oninput='updateSpeed(this.value)'>"
    "</div>"
    "<div>"
    "<p>Steps: <span id='steps-value'>0</span> (0 = continuous)</p>"
    "<input type='range' min='0' max='1000' value='0' id='steps-control' oninput='updateSteps(this.value)'>"
    "</div>"
    "<div class='status'>"
    "<p>Status: <span id='status'>Stopped</span></p>"
    "<p>Direction: <span id='direction'>-</span></p>"
    "</div>"
    "</div>"
    "<script>"
    "let currentSpeed = 50;"
    "let stepsToMove = 0;"
    ""
    "function updateSpeed(val) {"
    "  document.getElementById('speed-value').textContent = val;"
    "  currentSpeed = val;"
    "}"
    ""
    "function updateSteps(val) {"
    "  document.getElementById('steps-value').textContent = val;"
    "  stepsToMove = val;"
    "}"
    ""
    "function rotate(dir) {"
    "  fetch(`/motor?cmd=${dir}&speed=${currentSpeed}&steps=${stepsToMove}`)"
    "    .then(response => response.text())"
    "    .then(data => {"
    "      document.getElementById('status').textContent = 'Running';"
    "      document.getElementById('direction').textContent = (dir === 'cw') ? 'Clockwise' : 'Counter-Clockwise';"
    "    });"
    "}"
    ""
    "function stop() {"
    "  fetch('/motor?cmd=stop')"
    "    .then(response => response.text())"
    "    .then(data => {"
    "      document.getElementById('status').textContent = 'Stopped';"
    "    });"
    "}"
    "</script>"
    "</body></html>";

// HTTP request handler
err_t http_get_handler(void *arg, struct tcp_pcb *pcb, struct pbuf *p, err_t err) {
    char *data = (char *)p->payload;
    
    // Check if this is a GET request
    if (strncmp(data, "GET ", 4) == 0) {
        // Motor control API
        if (strncmp(data + 4, "/motor", 6) == 0) {
            char *cmd_ptr = strstr(data, "cmd=");
            char *speed_ptr = strstr(data, "speed=");
            char *steps_ptr = strstr(data, "steps=");
            
            // Process command
            if (cmd_ptr) {
                if (strncmp(cmd_ptr + 4, "cw", 2) == 0) {
                    // Calculate speed from percentage (1-100)
                    int speed_percent = 50; // Default
                    if (speed_ptr) {
                        speed_percent = atoi(speed_ptr + 6);
                        if (speed_percent < 1) speed_percent = 1;
                        if (speed_percent > 100) speed_percent = 100;
                    }
                    
                    // Calculate step delay: map speed_percent (1-100) to MAX_STEP_DELAY_MS to MIN_STEP_DELAY_MS
                    int delay = MAX_STEP_DELAY_MS - ((speed_percent - 1) * (MAX_STEP_DELAY_MS - MIN_STEP_DELAY_MS)) / 99;
                    
                    // Get steps if provided
                    int steps = 0; // Default (continuous)
                    if (steps_ptr) {
                        steps = atoi(steps_ptr + 6);
                        if (steps < 0) steps = 0;
                    }
                    
                    // Start motor clockwise
                    start_motor(steps, true, delay);
                } 
                else if (strncmp(cmd_ptr + 4, "ccw", 3) == 0) {
                    // Calculate speed from percentage (1-100)
                    int speed_percent = 50; // Default
                    if (speed_ptr) {
                        speed_percent = atoi(speed_ptr + 6);
                        if (speed_percent < 1) speed_percent = 1;
                        if (speed_percent > 100) speed_percent = 100;
                    }
                    
                    // Calculate step delay
                    int delay = MAX_STEP_DELAY_MS - ((speed_percent - 1) * (MAX_STEP_DELAY_MS - MIN_STEP_DELAY_MS)) / 99;
                    
                    // Get steps if provided
                    int steps = 0; // Default (continuous)
                    if (steps_ptr) {
                        steps = atoi(steps_ptr + 6);
                        if (steps < 0) steps = 0;
                    }
                    
                    // Start motor counter-clockwise
                    start_motor(steps, false, delay);
                } 
                else if (strncmp(cmd_ptr + 4, "stop", 4) == 0) {
                    // Stop motor
                    stop_motor();
                }
            }
            
            // Send response
            tcp_write(pcb, http_html_header, strlen(http_html_header), 1);
            tcp_write(pcb, "{\"status\":\"ok\"}", 15, 1);
            tcp_output(pcb);
        } 
        // Main page
        else {
            tcp_write(pcb, http_html_header, strlen(http_html_header), 1);
            tcp_write(pcb, http_index_html, strlen(http_index_html), 1);
            tcp_output(pcb);
        }
    }
    
    pbuf_free(p);
    tcp_close(pcb);
    return ERR_OK;
}

// Initialize motor GPIO pins
void initialize_motor() {
    gpio_init(MOTOR_PIN1);
    gpio_init(MOTOR_PIN2);
    gpio_init(MOTOR_PIN3);
    gpio_init(MOTOR_PIN4);
    
    gpio_set_dir(MOTOR_PIN1, GPIO_OUT);
    gpio_set_dir(MOTOR_PIN2, GPIO_OUT);
    gpio_set_dir(MOTOR_PIN3, GPIO_OUT);
    gpio_set_dir(MOTOR_PIN4, GPIO_OUT);
    
    // Initialize pins to low
    gpio_put(MOTOR_PIN1, 0);
    gpio_put(MOTOR_PIN2, 0);
    gpio_put(MOTOR_PIN3, 0);
    gpio_put(MOTOR_PIN4, 0);
}

// Set motor pins according to step sequence
void set_motor_pins(int step) {
    gpio_put(MOTOR_PIN1, step_sequence[step][0]);
    gpio_put(MOTOR_PIN2, step_sequence[step][1]);
    gpio_put(MOTOR_PIN3, step_sequence[step][2]);
    gpio_put(MOTOR_PIN4, step_sequence[step][3]);
}

// Move motor one step in current direction
void step_motor() {
    if (direction) {
        // Clockwise
        current_step = (current_step + 1) % 4;
    } else {
        // Counter-clockwise
        current_step = (current_step + 3) % 4;  // +3 is same as -1 with modulo 4
    }
    
    set_motor_pins(current_step);
}

// Start motor with specified parameters
void start_motor(int steps, bool clockwise, int speed) {
    direction = clockwise;
    step_delay_ms = speed;
    target_steps = steps;
    motor_running = true;
}

// Stop motor
void stop_motor() {
    motor_running = false;
    
    // Turn off all motor pins to avoid overheating
    gpio_put(MOTOR_PIN1, 0);
    gpio_put(MOTOR_PIN2, 0);
    gpio_put(MOTOR_PIN3, 0);
    gpio_put(MOTOR_PIN4, 0);
}

// Motor control task (runs in loop)
void motor_task() {
    static int steps_taken = 0;
    
    if (motor_running) {
        step_motor();
        
        // If target_steps is set (not continuous), check if we've reached it
        if (target_steps > 0) {
            steps_taken++;
            if (steps_taken >= target_steps) {
                steps_taken = 0;
                stop_motor();
            }
        }
    }
}

int main() {
    stdio_init_all();
    
    // Initialize motor control
    initialize_motor();
    
    // Initialize WiFi
    if (cyw43_arch_init()) {
        printf("Failed to initialize CYW43 architecture\n");
        return 1;
    }
    
    cyw43_arch_enable_sta_mode();
    
    // Connect to WiFi
    printf("Connecting to WiFi...\n");
    if (cyw43_arch_wifi_connect_timeout_ms(ssid, password, CYW43_AUTH_WPA2_AES_PSK, 10000)) {
        printf("Failed to connect to WiFi\n");
        return 1;
    }
    
    // Print IP address for accessing the web interface
    printf("Connected to WiFi. IP Address: %s\n", ip4addr_ntoa(netif_ip4_addr(netif_list)));
    
    // Initialize HTTP server
    httpd_init();
    
    // Set up HTTP server callback
    tcp_accept(tcp_new(), http_get_handler);
    
    // Main loop
    while (1) {
        // Handle motor control
        motor_task();
        
        // Delay between steps
        if (motor_running) {
            sleep_ms(step_delay_ms);
        } else {
            // If motor is not running, just do a small delay
            sleep_ms(10);
        }
    }
    
    return 0;
}