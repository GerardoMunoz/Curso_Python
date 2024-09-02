import time
import board
import analogio
import digitalio
import wifi
import socketpool
# import adafruit_requests

# Wi-Fi Configuration
SSID = "Ejemplo"  # Replace with your Wi-Fi SSID
PASSWORD = "12345678"  # Replace with your Wi-Fi password

# Server Configuration
HOST = "192.168.65.237"  # Replace with the IP address of the receiver
PORT = 5000  # Use the same port on the receiver

# Connect to Wi-Fi
wifi.radio.connect(SSID, PASSWORD)
print(f"Connected to {SSID}!")

# Initialize socket
pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
sock.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# Initialize the joystick's analog inputs
x_axis = analogio.AnalogIn(board.A0)  # Connected to ADC0
y_axis = analogio.AnalogIn(board.A1)  # Connected to ADC1

# Initialize the push button digital input
button = digitalio.DigitalInOut(board.GP22)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Assuming the button is connected to GND when pressed

def get_voltage(pin):
    # Convert the raw analog reading to voltage
    return (pin.value * 3.3) / 65536

while True:
    # Read the X and Y positions of the joystick
    x_value = get_voltage(x_axis)
    y_value = get_voltage(y_axis)
    
    # Read the state of the push button (True = not pressed, False = pressed)
    button_state = not button.value
    
    # Create a data string to send
    data = f"{x_value:.2f},{y_value:.2f},{button_state}\n"
    
    # Send the data via socket
    sock.send(data.encode('utf-8'))
    
    # Wait for 1 second
    time.sleep(1)
