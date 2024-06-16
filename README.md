# WIFI MANAGER (MicroPython)
Simple WIFI MANAGER MicroPython script for Micro-Controllers (Raspberry Pi Pico W - ESP32...).
<br><br>
Possibility to connect to the Wi-Fi network saved in the wifi_credentials.json file or create an Access Point to configure the device's Wi-Fi connection from another device.
<br><br>
Auto-Reset from AP Mode after 120 seconds
<br><br>
Nice interface using HTML - CSS - JS to establish the connection on your device.
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
