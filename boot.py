# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('DJM2.4', 'dkja1234')

webrepl.start()

'''
The problem so far is I am getting an address from DHCP
from my local network because it could change. Then I
would have to take the device and connect to usb.
'''