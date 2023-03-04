import bluetooth
import time
import binascii

loop_prog = True

my_devices = [('a4c1388c3622', 'Desk:       ', 0),
              ('a4c13859da18', 'Thermostat: ', 0),
              ('a4c138133c6c', 'Patio:      ', 0),
              ('a4c1381e4420', 'AC Vent:    ', 0),
              ('a4c138d14b3a', 'Outside:    ', 0),
              ('a4c138c3e807', 'Bathroom:   ', 0)]

ble = bluetooth.BLE()
if ble.active() == False:
    ble.active(True)

def scan_callback(event, addr):
    global my_devices  # Declare my_devices as global
    
    if event == 6:  #because event 6 has no addr returned
        print('SCAN DONE')
        return

    mac_add_hex = binascii.hexlify(addr[1]).decode('utf-8')

    if mac_add_hex in [device[0] for device in my_devices]:
        temp = get_temp(addr)
        updated_devices = []
        for device in my_devices:
            if device[0] == mac_add_hex:
                updated_device = (device[0], device[1], round(temp, 2))
            else:
                #updated_device must have a value, since it has no new data
                #we will just make it what it currently is.
                updated_device = device
            updated_devices.append(updated_device)
        my_devices = updated_devices


def get_temp(addr):
        data = binascii.hexlify(addr[4]).decode('utf-8')
        hex_str = data[52:58]
        decimal_val = int(hex_str, 16)
        celcius = decimal_val/10000
        fahrenheit = celcius * 1.8 + 32
        fahrenheit_rounded = round(fahrenheit, 1)
        return fahrenheit_rounded

ble.irq(scan_callback)
ble.gap_scan(0,500000, 500000)

try:
    while loop_prog:
        time.sleep(6)
        
        for device in my_devices:
            if device[2] == 0:
                continue
            print(device[1], device[2])
        print('\n')

except KeyboardInterrupt:
    print('User stopped the program.')
    ble.irq(None)
    ble.gap_scan(None)


