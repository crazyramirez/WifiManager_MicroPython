import os
import json
import network
import socket
import time
import machine

# Save Wi-Fi credentials
def save_credentials(ssid, password):
    credentials = {'ssid': ssid, 'password': password}
    with open('wifi_credentials.json', 'w') as f:
        json.dump(credentials, f)

# Load Wi-Fi credentials
def load_credentials():
    try:
        with open('wifi_credentials.json', 'r') as f:
            credentials = json.load(f)
        return credentials['ssid'], credentials['password']
    except OSError:
        return None, None

# Remove Credentials
def remove_credentials():
    try:
        os.remove('wifi_credentials.json')
        print("Wifi Credentials Removed")
    except Exception as e:
        print("Error removing Wifi Credentials file:", e)

# Connect to Wi-Fi
def connect_wifi():
    ssid, password = load_credentials()
    if ssid and password:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        time.sleep(1)
        wlan.active(True)
        wlan.connect(ssid, password)
        max_wait = 10
        while max_wait > 0:
            status = wlan.status()
            if status == network.STAT_GOT_IP:
                print('Connected to WiFi:', wlan.ifconfig())
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
        return True
    else:
        return False
        print("No SSID or Password")

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

# Scan Wifi Networks
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

SSID = "Wifi Config"
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
    ap.config(essid=SSID, authmode=network.AUTH_WPA2_PSK, password=PASSWORD)
    
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
    print(f'Connect to {SSID} Wifi from other Device')
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

def close_existing_connections():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.close()
    except OSError as e:
        print("Closing existing socket connections...")
        s.close()

# Verificación del estado de AP
def verify_ap_mode():
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        print('AP mode is active')
    else:
        print('AP mode is not active')

# Verificación de la conexión Wi-Fi
def print_network_status():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print('Network connected:', wlan.ifconfig())
    else:
        print('Network not connected')

# Main
def main():
    print("INIT Wifi Manager")

if __name__ == '__main__':
    main()

