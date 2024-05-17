import machine
import time

# Initialize GPIO pins for LEDs
green_led = machine.Pin(14, machine.Pin.OUT)
yellow_led = machine.Pin(15, machine.Pin.OUT)
red_led = machine.Pin(16, machine.Pin.OUT)

# Initialize GPIO pin for button
button = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)

# List of winner numbers
winner_list = [123, 456, 789]

# Lost number
lost_number = 999

def wait_char():
            return input("Please, write a digit and press Enter ")

def check_number():
    while True:
        green_led.off()
        red_led.off()
        yellow_led.off()
        print('Press three digits')
        try:
            c = int(wait_char())
            d = int(wait_char())
            u = int(wait_char())
        except ValueError:
            print('Ups')
            continue
        number = c*100 + d*10 + u
        
        if number in winner_list:
            green_led.on()
            #time.sleep(1)
            #green_led.off()
            return "win"
        elif number == lost_number:
            red_led.on()
            #time.sleep(1)
            #red_led.off()
            return "lost"
        else:
            yellow_led.on()
            #time.sleep(1)
            #yellow_led.off()
            print('Press * to continue')
            while wait_char() != '*':
                print('Press * to continue')
            #return check_number()

# Call the function to start the game
result = check_number()
print("Game result:", result)