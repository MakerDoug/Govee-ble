import bluetooth
import time
import binascii
#import lvgl as lv

loop_prog = True
'''
def create_screen(hex_color):
  screen = lv.obj()
  screen.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(hex_color))
  return screen

scr_home = create_screen(0xdddddd)
lv.scr_load(scr_home)
'''
my_devices = {'a4c1388c3622': 'Desk:       ',
              'a4c13859da18': 'Thermostat: ',
              'a4c138133c6c': 'Patio:      ',
              'a4c1381e4420': 'AC Vent:    ',
              'a4c138d14b3a': 'Outside:    '}


ble = bluetooth.BLE()

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

while loop_prog:
    time.sleep(10)
 


ble.gap_scan(None)
ble.irq(None)
