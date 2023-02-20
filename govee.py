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
    mac_add_string = addr[1]
    mac_add_hex = binascii.hexlify(mac_add_string).decode('utf-8')
    if mac_add_hex == 'a4c13859da18' or mac_add_hex == 'a4c1388c3622':
        #turns binary into string of hex octets
        data = binascii.hexlify(addr[4]).decode('utf-8')
        #print(mac_add_hex, data[54:60])
        hex_str = data[52:58]
        decimal_val = int(hex_str, 16)
        celcius = decimal_val/10000
        fahrenheit = celcius * 1.8 + 32
        print(mac_add_hex, fahrenheit)

    
ble.irq(scan_callback)
ble.gap_scan(5000, 5000000, 5000000)

time.sleep(6)

ble.gap_scan(None)
ble.irq(None)
