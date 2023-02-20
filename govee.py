import bluetooth
import time
import binascii

data = None

ble = bluetooth.BLE()

if ble.active() == False:
    ble.active(True)

def scan_callback(event, addr):
    if event == 6:
        print('SCAN DONE')
        return
    global data
    print(event, addr)
    mac_add_string = addr[1]
    mac_add_hex = binascii.hexlify(mac_add_string).decode('utf-8')
    #print(mac_add_hex)
    #if mac_add_hex == 'a4c13859da18' or mac_add_hex == 'a4c1388c3622':
    if mac_add_hex == 'a4c13859da18':
        #turns binary into string of hex octets
        #data = binascii.hexlify(data).decode('utf-8')
        print(mac_add_hex, addr)

    
ble.irq(scan_callback)
ble.gap_scan(5000, 5000000, 5000000)

time.sleep(6)

ble.gap_scan(None)
ble.irq(None)
