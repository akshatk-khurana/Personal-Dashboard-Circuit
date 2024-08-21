print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

from machine import Pin, I2C, ADC, PWM
import ssd1306
from time import sleep

# Define important variables
WIDTH = 128
HEIGHT = 64

notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
}

# Assign all the pins
screen_pin = I2C(0, scl=Pin(22), sda=Pin(21))
screen = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, screen_pin)

slider_pin = Pin(34)
slider = ADC(slider_pin)
slider.width(ADC.WIDTH_12BIT)
slider.atten(ADC.ATTN_11DB)

buzzer_pin = Pin(23)
buzzer_pwm = PWM(buzzer_pin)
buzzer_pwm.duty(0)

LED_bar_pins = [13, 12, 14, 27, 26, 25, 33, 32, 18, 19]
LED_bar_pins.reverse()

print("Pins defined!")

keypad_keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

keypad_row = [15, 2, 0, 4]
keypad_col = [16, 17, 5, 35]

row_pins = [Pin(i, Pin.OUT) for i in keypad_row]
col_pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in keypad_col]

# Define functions
def show_bar_LED(count):
    for index, pin in enumerate(LED_bar_pins):
        led = Pin(pin, Pin.OUT)
        if index < count:
            led.on()
        else:
            led.off()

def clear_bar_LED():
    for pin in LED_bar_pins:
        led = Pin(pin, Pin.OUT)
        led.off()

def convert_volume(volume):
    return int(volume * 1024 / 10)

def clear_screen():
    screen.fill(0)

def convert_reading(reading):
    return int(reading * 10 / 4095)

def check_keypad_input():
    for row_index, row in enumerate(row_pins):
        row.value(0)
        for col_index, col in enumerate(col_pins):
            if col.value() == 0:
                return keypad_keys[row_index][col_index]
        row.value(1)
    return None


def play_note(note, duration, volume):
    buzzer_pwm.freq(int(notes[note]))
    buzzer_pwm.duty(volume)
    time.sleep_ms(duration)
    buzzer_pwm.duty(0)

print("Functions defined!")


# Main code 
vol = 0
while True:
    clear_screen()
    clear_bar_LED()
    show_bar_LED(vol)

    new_vol = convert_reading(slider.read())
    if vol != new_vol:
        vol = new_vol

    pressed_key = check_keypad_input()

    if pressed_key is not None:
        print(f"Key: {pressed_key}")

        if pressed_key == "#":
            print("Quitting dashboard...")

    screen.show()


# Closing code
buzzer_pwm.deinit()