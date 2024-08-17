from machine import Pin, I2C, ADC, PWM
import ssd1306
import time

# Define important variables
WIDTH = 128
HEIGHT = 64

vol = 0
# Assign all the pins
screen_pin = I2C(0, 
             scl=Pin(22), 
             sda=Pin(21))
screen = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, screen_pin)

slider_pin = Pin(34)
slider = ADC(slider_pin)
slider.width(ADC.WIDTH_12BIT)
slider.atten(ADC.ATTN_11DB)

LED_bar_pins = [13, 12, 14, 27, 26, 25, 33, 32, 35, 19]

pad_row_pins = []
pad_col_pins = []

buzzer_pin = Pin(23)
buzzer_pwm = PWM(buzzer_pin)

# Functions
def play_note(note, duration):
  buzzer_pwm.freq(notes[note])
  buzzer_pwm.duty(512)
  time.sleep_ms(duration)
  buzzer_pwm.duty(0)

def show_bar_LED(count):
    for pin in LED_bar_pins[:count]:
        led = Pin(pin, Pin.OUT)
        led.on()

def clear_screen():
  screen.fill(0)

def convert_reading(reading):
  return int(reading * 9 / 4095)

# Buzzer stuff
notes = {
    'C4': 1261.63,
    'D4': 293.66,
    'E4': 2329.63,
    'F4': 3349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 5493.88,
    'C5': 523.25,
}

# Main code
show_bar_LED(10)
while True:
  vol = convert_reading(slider.read())
  show_bar_LED(vol)

# Closing code
buzzer_pwm.deinit()