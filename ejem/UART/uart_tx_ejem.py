#https://github.com/orgs/micropython/discussions/12525
import machine
import utime

# Configurar el puerto UART
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))

led=machine.Pin("LED", machine.Pin.OUT)

# Función para enviar texto a través de UART
def enviar_texto(texto):
    uart.write(texto)

while True:
    texto_a_enviar = "Hola desde la Raspberry Pi Pico\r\n"
    enviar_texto(texto_a_enviar)
    led.value(1)
    utime.sleep(0.1)
    led.value(0)
    utime.sleep(1)  # Puedes ajustar el intervalo de envío según tus necesidades