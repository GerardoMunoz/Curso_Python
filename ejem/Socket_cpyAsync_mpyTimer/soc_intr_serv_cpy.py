#CircuitPython
#https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/concurrent-tasks
#https://learn.adafruit.com/elements/3108525/download?type=zip
import socketpool
import wifi
import asyncio

wifi.radio.connect("Ejemplo","12345678")
pool=socketpool.SocketPool(wifi.radio)

print("IP address", wifi.radio.ipv4_address)
s = pool.socket()
s.bind(('', 80))
s.listen(5)

i=0
async def socket_wr():
  global i
  while True:
    try:
        cl, addr = s.accept()
        msg = "Any text ñ "+str(i)
        i += 1
        cl.send(msg)
        print("Sent: " + str(msg))
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')


async def main():
    print('one')
    task_1 = asyncio.create_task(socket_wr())
    #task_2=...
    print('two')
    await asyncio.gather(task_1)#await asyncio.gather(task_1,task_2)
    print('three')

asyncio.run(main())