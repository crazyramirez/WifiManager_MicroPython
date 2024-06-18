import os
import json
import network
import socket
import time
import machine

# Declaramos networks como global
networks = []

# Save Wi-Fi credentials
def save_credentials(ssid, password):
    try:
        with open('wifi_credentials.json', 'r') as f:
            credentials = json.load(f)
    except (OSError, ValueError):
        credentials = []
    new_cred = {'ssid': ssid, 'password': password}
    credentials = [new_cred] + [cred for cred in credentials if cred['ssid'] != ssid]
    if len(credentials) > 5:
        credentials = credentials[:5]
    with open('wifi_credentials.json', 'w') as f:
        json.dump(credentials, f)

# Load Wi-Fi credentials
def load_all_credentials():
    try:
        with open('wifi_credentials.json', 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return []

def load_credentials():
    credentials = load_all_credentials()
    if credentials:
        return credentials[0]['ssid'], credentials[0]['password']
    return None, None

# Remove Credentials
def remove_credentials():
    try:
        os.remove('wifi_credentials.json')
        print("WiFi Credentials Removed")
    except Exception as e:
        print("Error removing WiFi Credentials file:", e)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
        
    if not networks:
        print('No WiFi networks found')
        return False

    best_network = max(networks, key=lambda x: x[3])  # Signal strength is at index 3
    ssid = best_network[0].decode('utf-8')
    credentials = load_all_credentials()
    password = None
    for cred in credentials:
        if cred['ssid'] == ssid:
            password = cred['password']
            break
    if not password:
        print('No password found for the best network')
        return False
    wlan.connect(ssid, password)
    max_wait = 10
    while max_wait > 0:
        status = wlan.status()
        if status == network.STAT_GOT_IP:
            print('Connected to WiFi:', wlan.ifconfig())
            save_credentials(ssid, password)
            return True
        elif status == network.STAT_WRONG_PASSWORD:
            print('Wrong WiFi password')
            return False
        elif status == network.STAT_NO_AP_FOUND:
            print('WiFi SSID not found')
            return False
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    print('Failed to connect to WiFi: Timeout')
    return False

# Disable STA mode
def disable_sta_mode():
    wlan = network.WLAN(network.STA_IF)
    if wlan.active():
        wlan.active(False)
        time.sleep(2)
    print('STA mode disabled')

# Handle Wi-Fi configuration request
def handle_configure(request):
    headers, body = request.split('\r\n\r\n', 1)
    print(f'Headers: {headers}')
    print(f'Body: {body}')
    
    if 'POST /configure' in headers:
        try:
            data = json.loads(body)
            print('Received JSON data:', data)
            ssid = data.get('ssid', '')
            password = data.get('password', '')
            return ssid, password
        except ValueError as e:
            print('Error decoding JSON:', e)
            return None, None
    return None, None

# Scan Wi-Fi Networks
def scan_wifi_networks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    return [network[0].decode('utf-8') for network in networks]

# Read an HTML file
def read_html_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except OSError as e:
        print("Error reading HTML file:", e)
        return "<html><body><h1>Error: HTML file not found</h1></body></html>"

SSID = "WiFi Config"
PASSWORD = "123456789"
# Enter AP mode
AUTO_RESET_TIME = 120
def ap_mode():
    print("---- ----")
    print("Starting AP mode...")
    # Ensure STA Mode is disabled
    disable_sta_mode()
    
    # Reset the AP mode interface
    ap = network.WLAN(network.AP_IF)

    # Config AP Mode
    ap.active(True)
    ap.config(essid=SSID, authmode=network.AUTH_W2_PSK, password=PASSWORD)
    
    close_existing_connections()

    # Check AP 
    for _ in range(10):
        if ap.active():
            break
        time.sleep(1)
    else:
        print("Error: AP mode not activated")
        return
    
    print('AP mode activated successfully')
    print("---- ----")
    print(f'Connect to {SSID} WiFi from other Device')
    print(f'PASSWORD: {PASSWORD}')
    print(f'Open your Browser and Enter')
    print(f'URL: http://{ap.ifconfig()[0]}')
    print("---- ----")

    # Read HTML File
    config_page = read_html_file('config_page.html')

    # Setup Auto Reset Timer     
    start_time = time.time()
    
    # Create Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
        
    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)
            
            request = b""
            while True:
                part = cl.recv(1024)
                request += part
                if len(part) < 1024:
                    break
            
            request = request.decode('utf-8')
            print('Request:', request)
            
            response = ""
            
            if 'GET / ' in request or 'GET / HTTP/1.1' in request:
                print('Serving config_page.html')
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + config_page
            elif 'GET /wifi-networks' in request:
                networks = scan_wifi_networks()
                response = f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{json.dumps(networks)}'
            elif 'POST /configure' in request:
                ssid, password = handle_configure(request)
                response_body = f"Request received: {request}\n"
                if ssid and password:
                    save_credentials(ssid, password)
                    response_body += "Configuration saved. Restarting..."
                response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}'
                cl.send(response)
                cl.close()
                time.sleep(2)
                machine.reset()
            else:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nPage not found'
            
            cl.send(response)
            cl.close()
        
        except OSError as e:
            if e.args[0] == 104:  # ECONNRESET error number in MicroPython
                print("Connection reset by peer")
                machine.reset()
                continue
            elif e.args[0] == 116:  # ETIMEDOUT error number in MicroPython
                continue
            print(f"OSError: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
        if time.time() - start_time > AUTO_RESET_TIME:
            print("120 seconds have passed, resetting...")
            machine.reset()

# Close Existing Connection
def close_existing_connections():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.close()
    except OSError as e:
        print("Closing existing socket connections...")
        s.close()

# Verify Wi-Fi connection status
def print_network_status():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print('Network connected:', wlan.ifconfig())
    else:
        print('Network not connected')

# Periodic Wifi Check        
def periodic_wifi_check(timer):
    print('-- Timer Checking WiFi --')
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    # Check if AP mode is active
    if ap_if.active():
        print('AP mode is active, skipping WiFi check')
        return
    if sta_if.isconnected():
        ssid = sta_if.config('essid')
        print(f'WiFi Connected to: {ssid}')
    else:
        print('WiFi not connected, attempting to connect...')
        if not connect_wifi():
            print('Failed to connect to WiFi')

# Configure timer to check WiFi connection every 20 seconds
timer = machine.Timer(-1)
timer.init(period=20000, mode=machine.Timer.PERIODIC, callback=periodic_wifi_check)

# Main
def main():
    print("INIT WiFi Manager")

if __name__ == '__main__':
    main()

