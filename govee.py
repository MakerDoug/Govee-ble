import bluetooth
import time
import binascii
import urequests 





loop_prog = True

my_devices = [('a4c1388c3622', 'Desk:       ', 0),
              ('a4c13859da18', 'Thermostat: ', 0),
              ('a4c138133c6c', 'Patio:      ', 0),
              ('a4c1381e4420', 'AC Vent:    ', 0),
              ('a4c138d14b3a', 'Outside:    ', 0),
              ('a4c138c3e807', 'Bathroom:   ', 0),
              ('a4c1380839ae', 'MeliDesk:   ', 0)]

#govee 5074 'e38ec8c2b0ec', 'Front Door:  '

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK = 'http://api.thingspeak.com/update?api_key='
API_KEY = '61I0QNLTPFQHRSY1'

ble = bluetooth.BLE()
if ble.active() == False:
    ble.active(True)


def scan_callback(event, addr):
    global my_devices  # Declare my_devices as global
    
    if event == 6:  #because event 6 has no addr returned
        #print('SCAN DONE')
        return

    mac_add_hex = binascii.hexlify(addr[1]).decode('utf-8')

    for device in my_devices:
      if mac_add_hex == device[0]:
         temp = get_temp(addr)
         device_index = my_devices.index(device)
         my_devices[device_index] = (device[0], device[1], temp)



def get_temp(addr):
    data = binascii.hexlify(addr[4]).decode('utf-8')
    hex_str = data[52:58]
    decimal_val = int(hex_str, 16)
    celcius = decimal_val / 10000
    fahrenheit = celcius * 1.8 + 32
    fahrenheit_rounded = round(fahrenheit, 2)
    
    #fahrenheit_rounded = int(fahrenheit * 10 + 0.5) / 10
    return round(fahrenheit_rounded, 2)


ble.irq(scan_callback)


try:
    while loop_prog:
        ble.gap_scan(4000,2000000,2000000)
        time.sleep(5)
 
        #Every loop loads these with the latest temperature.
        Desk = 			my_devices[0][2]
        Thermostat = 	my_devices[1][2]
        Patio = 		my_devices[2][2]
        AC = 			my_devices[3][2]
        Outside = 		my_devices[4][2]
        Bathroom = 		my_devices[5][2]
        MeliDesk =      my_devices[6][2]
        
        #This is just for debugging, printing to console.
        sent	  = {'Desk':		Desk,
                     'Thermostat':	Thermostat,
                     'Patio':		Patio,
                     'AC':			AC,
                     'Outside':		Outside,
                     'Bathroom':	Bathroom,
                     'MeliDesk':    MeliDesk}
        
        temp_json = {'field1':Desk,
                     'field2':Thermostat,
                     'field3':Patio,
                     'field4':AC,
                     'field5':Outside,
                     'field6':Bathroom,
                     'field7':MeliDesk}

        #request = urequests.post( THINGSPEAK + API_KEY, json = temp_json, headers = HTTP_HEADERS )
        print(sent)

except KeyboardInterrupt:
    print('User stopped the program.')
    ble.irq(None)
    ble.gap_scan(None)
