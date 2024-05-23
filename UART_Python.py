
import serial

port = input("port: (like COM11)")

ser = serial.Serial(
    port=port,
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
ser.write(b'\r\n')  
while True:
    n=ser.in_waiting
    rx_uart = ser.read(n).decode()
    print(rx_uart)
        
    tx_uart = input("!")
    if tx_uart == "":
        break
    else:
        tx_uart += '\r\n'
        ser.write(tx_uart.encode('ascii'))  
        
ser.close()   

