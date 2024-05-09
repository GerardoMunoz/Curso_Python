from machine import Pin, Timer 
import network
import socket
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect('Ejemplo', '12345678')

max_wait = 10
while max_wait > 0:
  if wlan.status() < 0 or wlan.status() >= 3:
    break
  max_wait -= 1
  print('waiting for connection...')
  time.sleep(1)


if wlan.status() != 3:
   raise RuntimeError('network connection failed')
else:
  print('connected')
  status = wlan.ifconfig()
  ip_addr=input("Please, write IP address: ")


buf = bytearray(1300)

def socket_read(timer):
    ai = socket.getaddrinfo(ip_addr, 80) # Address of Web Server
    addr = ai[0][-1]


    s = socket.socket() 
    s.connect(addr)
    ss=str(s.readinto(buf)) 
    print(ss,buf[:int(ss)])
    s.close()          


tim = Timer()
tim.init(period=4000, callback=socket_read)