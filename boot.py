import wifimanager

# Main
def main():
    print("Hello BOOT")
        
    if wifimanager.connect_wifi() == True:
        print("Connected")
    else:
        print("False")
        
    # wifimanager.ap_mode()

if __name__ == '__main__':
    main()