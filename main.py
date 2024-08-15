from machine import Pin, I2C, ADC
import ssd1306
import time

# Define important variables
WIDTH = 128
HEIGHT = 64

# Assign all the pins
pad_row_pins = []
pad_col_pins = []

slider_pin = Pin(32, Pin.IN)
screen_pin = I2C(0, 
             scl=Pin(22), 
             sda=Pin(21))

buzzer_pin = Pin(12,Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)

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

def play(note, duration):
  buzzer_pwm.freq(notes[note])
  buzzer_pwm.duty(512)
  time.sleep_ms(duration)
  buzzer_pwm.duty(0)

# Main code
screen = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, screen_pin)
play('C4', 100)

screen.text('Dashboard', 10, 2)      
screen.show()

# Closing code
buzzer_pwm.deinit()