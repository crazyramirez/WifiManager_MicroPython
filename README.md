# WIFI MANAGER (MicroPython)
Simple WIFI MANAGER MicroPython script.
<br><br>
Possibility to connect to the Wi-Fi network saved in the wifi_credentials.json file or create an Access Point to configure the device's Wi-Fi connection from another device.

## INSTALL
In this case I'm using the RPi Pico W board, so you need to download the corresponding Firmware:
<br>
Configure your device using Thonny for example
Copy the script to your device (Raspberry Pi Pico W - ESP32...)

Use the following functions:

## Connect to Wifi
    wifimanager.connect_wifi()

## Create Access Point
    wifimanager.ap_mode()
