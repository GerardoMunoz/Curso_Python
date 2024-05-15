import machine
import time

green_led = machine.Pin(14, machine.Pin.OUT)
yellow_led = machine.Pin(15, machine.Pin.OUT)
red_led = machine.Pin(16, machine.Pin.OUT)

winner_list = [123, 456, 789]

lost_number = 999


def wait_char():
            return input("One digit and Enter, please ")

def check_number():
    while True:
        
        print('Press three digits')
        try:
            c = int(wait_char())
            d = int(wait_char())
            u = int(wait_char())
        except:
            print('Ups')
            continue
        number = c*100 + d*10 + u
        
        if number in winner_list:
            green_led.on()
            return "win"
        elif number == lost_number:
            red_led.on()
            return "lost"
        else:
            yellow_led.on()
            print('Press * to continue')
            while wait_char() != '*':
                print('Press * to continue')

result = check_number()
print("Game result:", result)

