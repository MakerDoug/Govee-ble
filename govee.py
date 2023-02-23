import bluetooth
import time
import binascii
import lvgl

ble = bluetooth.BLE()

my_devices = {'a4c1388c3622': 'Office-1: ',
              'a4c13859da18': 'Office-2: ' }


if ble.active() == False:
    ble.active(True)
           
def scan_callback(event, addr):
    if event == 6:
        print('SCAN DONE')
        return
    
    mac_add_string = addr[1]
    mac_add_hex = binascii.hexlify(mac_add_string).decode('utf-8')
    if mac_add_hex in my_devices:
        temp = get_temp(addr)
        print(my_devices[mac_add_hex], round(temp, 2))
        return

def get_temp(addr):
        data = binascii.hexlify(addr[4]).decode('utf-8')
        hex_str = data[52:58]
        decimal_val = int(hex_str, 16)
        celcius = decimal_val/10000
        fahrenheit = celcius * 1.8 + 32
        return fahrenheit
 

ble.irq(scan_callback)
ble.gap_scan(0, 1000000, 1000000)

while True:
    time.sleep(10)
    
    


ble.gap_scan(None)
ble.irq(None)
