import wifimanager

# Main
def main():
    print("Hello BOOT")
    
    # wifimanager.ap_mode()
    wifimanager.connect_wifi()

if __name__ == '__main__':
    main()