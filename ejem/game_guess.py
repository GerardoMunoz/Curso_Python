import machine
import time


# List of winner numbers
winner_list = [123, 456, 789]

# Lost number
losing_number = 999

def wait_char(port_ir):
    # temporarily the keyboard is used
    return input("Please, write a digit and press Enter ")

def check_number(port_ir=16,green=15,yellow=14,red=13):
# Initialize GPIO pins for LEDs
    green_led = machine.Pin(green, machine.Pin.OUT)
    yellow_led = machine.Pin(yellow, machine.Pin.OUT)
    red_led = machine.Pin(red, machine.Pin.OUT)
    while True:
        green_led.off()
        red_led.off()
        yellow_led.off()
        print('Press three digits')
        try:
            c = int(wait_char(port_ir))
            d = int(wait_char(port_ir))
            u = int(wait_char(port_ir))
        except ValueError:
            print('Ups')
            continue
        number = c*100 + d*10 + u
        
        if number in winner_list:
            green_led.on()
            return "You won"
        elif number == losing_number:
            red_led.on()
            return "You lost"
        else:
            yellow_led.on()
            print('Press * to continue')
            while wait_char(port_ir) != '*':
                print('Press * to continue')

# Call the function to start the game
result = check_number()
print("Game result:", result)
