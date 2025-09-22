import network
import socket
import time
import json
import uasyncio as asyncio
from machine import Pin, Timer

# Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
LED_PIN = 25  # Onboard LED
REFRESH_RATE = 5  # seconds

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
status_led = Pin(LED_PIN, Pin.OUT)

# Network statistics storage
network_stats = {
    "rx_bytes": 0,
    "tx_bytes": 0,
    "rx_packets": 0,
    "tx_packets": 0,
    "last_update": 0,
    "history": [],
    "alerts": []
}

# Alert thresholds (adjust as needed)
ALERT_THRESHOLDS = {
    "rx_bytes_per_sec": 500000,  # 500KB/s
    "tx_bytes_per_sec": 500000,  # 500KB/s
}

# HTML Template for the web interface
html = """<!DOCTYPE html>
<html>
<head>
    <title>Pico Network Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { color: #2c3e50; }
        .card { background-color: #f7f9fc; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat { display: flex; justify-content: space-between; margin: 10px 0; }
        .label { font-weight: bold; }
        .value { color: #3498db; }
        .chart-container { height: 200px; margin: 20px 0; position: relative; }
        .alerts { background-color: #fff3cd; }
        .alert-item { color: #856404; margin: 5px 0; }
        button { background-color: #3498db; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #2980b9; }
    </style>
</head>
<body>
    <h1>Pico Network Monitor</h1>
    
    <div class="card">
        <h2>Current Traffic</h2>
        <div class="stat">
            <span class="label">Received:</span>
            <span class="value" id="rx-bytes">0 B</span>
        </div>
        <div class="stat">
            <span class="label">Transmitted:</span>
            <span class="value" id="tx-bytes">0 B</span>
        </div>
        <div class="stat">
            <span class="label">RX Packets:</span>
            <span class="value" id="rx-packets">0</span>
        </div>
        <div class="stat">
            <span class="label">TX Packets:</span>
            <span class="value" id="tx-packets">0</span>
        </div>
        <div class="stat">
            <span class="label">Last Update:</span>
            <span class="value" id="last-update">Never</span>
        </div>
    </div>
    
    <div class="card">
        <h2>Traffic History</h2>
        <div class="chart-container" id="chart">
            <canvas id="traffic-chart" width="700" height="200"></canvas>
        </div>
    </div>
    
    <div class="card alerts">
        <h2>Alerts</h2>
        <div id="alerts-list">No alerts</div>
        <button onclick="clearAlerts()">Clear Alerts</button>
    </div>
    
    <script>
        // Function to format bytes into KB, MB, etc.
        function formatBytes(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
        }
        
        // Function to update the UI with new data
        function updateStats(data) {
            document.getElementById('rx-bytes').textContent = formatBytes(data.rx_bytes);
            document.getElementById('tx-bytes').textContent = formatBytes(data.tx_bytes);
            document.getElementById('rx-packets').textContent = data.rx_packets;
            document.getElementById('tx-packets').textContent = data.tx_packets;
            document.getElementById('last-update').textContent = new Date(data.last_update * 1000).toLocaleTimeString();
            
            // Update alerts
            const alertsContainer = document.getElementById('alerts-list');
            if (data.alerts.length === 0) {
                alertsContainer.innerHTML = 'No alerts';
            } else {
                alertsContainer.innerHTML = '';
                data.alerts.forEach(alert => {
                    const alertElement = document.createElement('div');
                    alertElement.className = 'alert-item';
                    alertElement.textContent = `${new Date(alert.time * 1000).toLocaleTimeString()}: ${alert.message}`;
                    alertsContainer.appendChild(alertElement);
                });
            }
            
            // Update chart (simplified, could be enhanced with a proper charting library)
            const chartCanvas = document.getElementById('traffic-chart');
            const ctx = chartCanvas.getContext('2d');
            
            // Clear canvas
            ctx.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
            
            // Draw chart if we have history data
            if (data.history.length > 0) {
                const maxDataPoints = 10;
                const history = data.history.slice(-maxDataPoints);
                
                // Find max value for scaling
                let maxValue = 0;
                history.forEach(point => {
                    maxValue = Math.max(maxValue, point.rx_bytes_rate, point.tx_bytes_rate);
                });
                
                const width = chartCanvas.width;
                const height = chartCanvas.height;
                const pointWidth = width / maxDataPoints;
                
                // Draw RX line (blue)
                ctx.beginPath();
                ctx.strokeStyle = '#3498db';
                ctx.lineWidth = 2;
                
                history.forEach((point, index) => {
                    const x = index * pointWidth;
                    const y = height - (point.rx_bytes_rate / maxValue * height);
                    if (index === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                ctx.stroke();
                
                // Draw TX line (green)
                ctx.beginPath();
                ctx.strokeStyle = '#2ecc71';
                ctx.lineWidth = 2;
                
                history.forEach((point, index) => {
                    const x = index * pointWidth;
                    const y = height - (point.tx_bytes_rate / maxValue * height);
                    if (index === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                ctx.stroke();
                
                // Add legend
                ctx.font = '12px Arial';
                ctx.fillStyle = '#3498db';
                ctx.fillText('RX', 10, 15);
                ctx.fillStyle = '#2ecc71';
                ctx.fillText('TX', 40, 15);
            }
        }
        
        // Function to fetch new data
        function fetchData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    updateStats(data);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                })
                .finally(() => {
                    // Fetch again after 5 seconds
                    setTimeout(fetchData, 5000);
                });
        }
        
        // Function to clear alerts
        function clearAlerts() {
            fetch('/api/clear-alerts', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('alerts-list').innerHTML = 'No alerts';
                    }
                })
                .catch(error => {
                    console.error('Error clearing alerts:', error);
                });
        }
        
        // Start fetching data when page loads
        document.addEventListener('DOMContentLoaded', fetchData);
    </script>
</body>
</html>
"""

async def connect_wifi():
    """Connect to WiFi network"""
    if not wlan.isconnected():
        print(f"Connecting to WiFi network: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection with timeout
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print("Waiting for connection...")
            await asyncio.sleep(1)
            
        if wlan.status() != 3:
            print(f"Network connection failed with status {wlan.status()}")
            return False
        else:
            print(f"Connected to WiFi. IP: {wlan.ifconfig()[0]}")
            return True
    return True

def update_network_stats():
    """Update network statistics"""
    global network_stats
    
    # Get current statistics
    current_stats = wlan.status('stations')
    current_time = time.time()
    
    if network_stats["last_update"] > 0:
        # Calculate time delta
        time_delta = current_time - network_stats["last_update"]
        
        # Get deltas since last measurement
        rx_delta = current_stats[0] - network_stats["rx_bytes"]
        tx_delta = current_stats[1] - network_stats["tx_bytes"]
        rx_packet_delta = current_stats[2] - network_stats["rx_packets"]
        tx_packet_delta = current_stats[3] - network_stats["tx_packets"]
        
        # Calculate rates
        rx_rate = rx_delta / time_delta if time_delta > 0 else 0
        tx_rate = tx_delta / time_delta if time_delta > 0 else 0
        
        # Add to history (limit to 100 points)
        history_point = {
            "time": current_time,
            "rx_bytes_rate": rx_rate,
            "tx_bytes_rate": tx_rate
        }
        network_stats["history"].append(history_point)
        if len(network_stats["history"]) > 100:
            network_stats["history"].pop(0)
        
        # Check for alerts
        if rx_rate > ALERT_THRESHOLDS["rx_bytes_per_sec"]:
            alert = {
                "time": current_time,
                "message": f"High incoming traffic: {round(rx_rate/1024, 2)} KB/s"
            }
            network_stats["alerts"].append(alert)
        
        if tx_rate > ALERT_THRESHOLDS["tx_bytes_per_sec"]:
            alert = {
                "time": current_time,
                "message": f"High outgoing traffic: {round(tx_rate/1024, 2)} KB/s"
            }
            network_stats["alerts"].append(alert)
            
        # Limit alerts to most recent 50
        if len(network_stats["alerts"]) > 50:
            network_stats["alerts"] = network_stats["alerts"][-50:]
    
    # Update current stats
    network_stats["rx_bytes"] = current_stats[0]
    network_stats["tx_bytes"] = current_stats[1]
    network_stats["rx_packets"] = current_stats[2]
    network_stats["tx_packets"] = current_stats[3]
    network_stats["last_update"] = current_time

async def handle_client(reader, writer):
    """Handle an HTTP client connection"""
    # Read request
    request_line = await reader.readline()
    request = request_line.decode('utf8').strip()
    
    # Read headers
    while await reader.readline() != b'\r\n':
        pass
    
    # Parse request
    method, path, _ = request.split(' ')
    
    # Serve the appropriate content
    if path == '/':
        # Serve the main HTML page
        response = html
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        writer.write(response)
    
    elif path == '/api/stats':
        # Serve JSON stats
        response = json.dumps(network_stats)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        writer.write(response)
    
    elif path == '/api/clear-alerts' and method == 'POST':
        # Clear alerts
        network_stats["alerts"] = []
        response = json.dumps({"success": True})
        writer.write('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        writer.write(response)
    
    else:
        # 404 Not Found
        writer.write('HTTP/1.0 404 Not Found\r\n\r\n')
        writer.write('404 Not Found')
    
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def blink_led():
    """Blink the status LED to indicate the system is running"""
    while True:
        status_led.value(1)
        await asyncio.sleep(0.1)
        status_led.value(0)
        await asyncio.sleep(2.9)  # Total period of 3 seconds

async def stats_collector():
    """Periodically collect network statistics"""
    while True:
        try:
            update_network_stats()
        except Exception as e:
            print(f"Error collecting stats: {e}")
        await asyncio.sleep(REFRESH_RATE)

async def main():
    """Main application entry point"""
    # Connect to WiFi
    if not await connect_wifi():
        while True:
            # Rapid blink to indicate WiFi connection failure
            status_led.value(1)
            await asyncio.sleep(0.1)
            status_led.value(0)
            await asyncio.sleep(0.1)
    
    # Start web server
    print(f"Starting web server on http://{wlan.ifconfig()[0]}")
    asyncio.create_task(asyncio.start_server(handle_client, "0.0.0.0", 80))
    
    # Start background tasks
    asyncio.create_task(blink_led())
    asyncio.create_task(stats_collector())
    
    # Keep the main task running
    while True:
        await asyncio.sleep(60)

# Start the application
try:
    asyncio.run(main())
except Exception as e:
    print(f"Fatal error: {e}")
    # Reset the device after a fatal error
    import machine
    machine.reset()