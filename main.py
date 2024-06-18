import wifimanager
import time, network

# Main
def main():
    if wifimanager.connect_wifi() == True:
        wlan = network.WLAN(network.STA_IF)
        ssid = wlan.config('essid')
        print(f"---- ----")
        print(f"MAIN - Connected to: {ssid}")
        time.sleep(2)
        print(f"MAIN - After 2 sec. Check Connection: {ssid}")
    else:
        print("False")
        wifimanager.ap_mode()
        
if __name__ == '__main__':
    main()