try:
    from machine import UART,Pin
    uart = UART(1,
                baudrate=9600,
                bits=8,
                parity=None,
                stop=1,
                rx=Pin(5),
                tx=Pin(4))
except:
    import board
    import busio
    import digitalio
    uart = busio.UART(board.GP4, board.GP5,
                      baudrate=9600,
                      bits=8,
                      parity=None,
                      stop=1)
    

from time import sleep
bufr = bytearray(10)  # Pre-allocate a buffer
bufw = bytearray(10)  # Pre-allocate a buffer
for i in range(100):
    msg=input("Write 10 letters ")
    if msg=="":
        break
    bufw[:]=msg.encode()
    uart.write(bufw)
    print('It is going to read')
    rd=uart.readinto(bufr)
    print(rd,bufr)
