# WIFI MANAGER (MicroPython)
Simple WIFI MANAGER MicroPython script for Micro-Controllers (Raspberry Pi Pico W - ESP32...).
<br><br>
Possibility to connect to the Wi-Fi network saved in the wifi_credentials.json file or create an Access Point to configure the device's Wi-Fi connection from another device.
<br><br>
Stores the last 5 Wi-Fi connections
<br><br>
In the "connect_wifi" function, it scans the available networks and checks the signal quality to connect to the best option previously stored
<br><br>
Auto-Reset from AP Mode after 120 seconds
<br><br>
Nice and clen interface using HTML - CSS - JS to establish the connection on your device.
<br>
Modify the config_page.html file to adapt it to your needs
<br><br>
<img src="./images/wifi_config.jpg" alt="CRYPTO DASHBOARD Demo 1" width="100%"/>

## INSTALL
Configure your device using Thonny for example.
<br>
Copy the script to your device (Raspberry Pi Pico W - ESP32...)

Use the following functions:

## Import WifiManager
    import wifimanager
    
## Connect to Wifi
    wifimanager.connect_wifi()

## Create Access Point
    wifimanager.ap_mode()

You can use these methods in different ways.
<br>
For example, as you can see in the **boot.py** file, you can boot your device and try to connect to the previously stored Wifi network (wifi_credentials.json), if the connection fails it will open the ap mode automatically.
<br><br>
Look at the Log and you will see the different configuration states.
<br><br>
If you have a TFT screen or similar (IE.- ili9341), you can display the connection status on the screen using the corresponding drivers from the manufacturer.
