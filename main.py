from machine import Pin, I2C, ADC
import ssd1306
import time

# Define important variables
WIDTH = 128
HEIGHT = 64

# Assign all the pins
screen_pin = I2C(0, 
             scl=Pin(22), 
             sda=Pin(21))

slider_pin = Pin(32, Pin.IN)

screen = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, screen_pin)

screen.text('Dashboard', 10, 2)      
screen.show()