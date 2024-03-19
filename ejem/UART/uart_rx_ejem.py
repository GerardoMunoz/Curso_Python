#https://github.com/orgs/micropython/discussions/12525
from machine import Pin, I2C, UART
import utime

# Configurar la conexión UART (TX: Pin 0, RX: Pin 1)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Configurar el pin 16 como salida
led = Pin("LED", Pin.OUT)

while True:
    try:
        datos_recibidos = uart.read(1)  # Leer un byte de datos
        if datos_recibidos:
            texto = datos_recibidos.decode('utf-8','replace')
            print(texto)

             # Encender el LED al recibir datos
            led.value(1)

            # Esperar un momento antes de apagar el LED
            utime.sleep(0.1)
            led.value(0)
    except KeyboardInterrupt:
        break

# Cerrar la conexión UART al salir
uart.deinit()