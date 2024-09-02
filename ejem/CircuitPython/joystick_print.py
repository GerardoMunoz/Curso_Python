import time
import board
import analogio
import digitalio

# Initialize the joystick's analog inputs
x_axis = analogio.AnalogIn(board.A0)  # Connected to ADC0
y_axis = analogio.AnalogIn(board.A1)  # Connected to ADC1

# Initialize the push button digital input
button = digitalio.DigitalInOut(board.GP22)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Assuming the button is connected to GND when pressed

while True:
    # Read the X and Y positions of the joystick
    x_value = (x_axis.value * 3.3) / 65536
    y_value = (y_axis.value * 3.3) / 65536
    
    # Read the state of the push button (True = not pressed, False = pressed)
    button_state = not button.value
    
    # Print the values
    print(f"Joystick X: {x_value:.2f} V, Joystick Y: {y_value:.2f} V, Button Pressed: {button_state}")
    
    # Wait for 1 second
    time.sleep(1)
