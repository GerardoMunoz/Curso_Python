#https://github.com/pi3g/pico-w/tree/main/MicroPython/I%20Pico%20W%20LED%20web%20server
#https://youtu.be/Or-UVgiMQsU

import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

# Set country to avoid possible errors
#rp2.country('DE')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed ',wlan_status)
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        led_quit = r.find('?led=quit')
        print('led_on = ', led_on)
        print('led_off = ', led_off)
        print('led_quit = ', led_quit)
        if led_on > -1:
            print('LED ON')
            led.value(1)
            
        if led_off > -1:
            print('LED OFF')
            led.value(0)

        if led_quit > -1:
            print('QUIT')
            cl.close()
            #print('Connection closed')
            s.close()
            wlan.active(False)
            wlan.disconnect()
            print('Bye')
            break
            
        response = get_html('web_server_cube.html')
        cl.send("HTTP/1.1 200 OK\r\n")
        cl.send("Content-Type: text/html\r\n")
        cl.send("Connection: close\r\n\r\n")
        chunk_size=1000
        for i in range(0, len(response), chunk_size):
            chunk = response[i:i + chunk_size]
            cl.send(chunk)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()
