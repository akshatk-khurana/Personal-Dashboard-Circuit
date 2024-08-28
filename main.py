print("_____________________________________________________")

from machine import Pin, I2C, ADC, PWM
import ssd1306
from time import sleep, time

WIDTH = 128
HEIGHT = 64

note_mappings = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
}

note_list = [ "E4", "D4", "E4", "D4", "E4", "B4", "D4", "C5", "A4", "pause",
    "C4", "E4", "A4", "B4", "pause", "E4", "G4", "B4", "C5", "pause",
    "E4", "E4", "D4", "E4", "D4", "E4", "B4", "D4", "C5", "A4", "pause",
    "C4", "E4", "A4", "B4", "pause", "E4", "C5", "B4", "A4", "pause"]

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
    return int(volume * 1023 / 10)

def convert_reading(reading):
    return int(reading * 10 / 4095)

def convert_time(s):
    minutes = s // 60
    seconds = s % 60
    return minutes, seconds

def clear_screen():
    screen.fill(0)

def check_keypad_input():
    key = None
    for row_index, row in enumerate(row_pins):
        for r in row_pins:
            r.value(1)
        row.value(0)
        for col_index, col in enumerate(col_pins):
            if col.value() == 0:
                key = keypad_keys[row_index][col_index]
                sleep(0.1)
                while col.value() == 0:
                    sleep(0.1)
        row.value(1)
        if key:
            break
    return key

def play_note(note, duration, volume):
    frequency = int(note_mappings[note])
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty(volume)
    sleep(duration)
    buzzer_pwm.duty(0)

def home_screen():
    screen.text("Dashboard", 26, 0)
    screen.text("Commands are:", 10, 12)
    screen.text("A for music.", 10, 22)
    screen.text("B for stopwatch.", 10, 32)
    screen.text("C for timer.", 10, 42)
    screen.text("# to quit.", 10, 52)

def music_screen():
    clear_screen()
    screen.text("Playing", 26, 0)
    screen.text("music!", 26, 10)
    screen.text("* for home.", 26, 24)
    screen.show()

def stopwatch_screen(seconds):
    clear_screen()
    minutes, seconds = convert_time(seconds)
    screen.text("Stopwatch", 26, 0)
    screen.text(f"Time: {minutes:02}:{seconds:02}", 15, 22)
    screen.text("* for home.", 26, 42)
    screen.show()

def timer_screen(seconds):
    clear_screen()
    screen.text("Timer", 26, 0)
    minutes, seconds = convert_time(seconds)
    screen.text(f"Time: {minutes:02}:{seconds:02}", 15, 22)
    screen.text("* for home.", 26, 42)
    screen.show()

print("Functions defined!")

vol = 0

timer_seconds = 60
stopwatch_seconds = 0

note_cursor = 0
play_music = False

home_screen()
screen.show()
current_screen = "home"

milliseconds = 0
started = False

while True:
    if started:
        milliseconds += 100

    clear_bar_LED()
    show_bar_LED(vol)

    new_vol = convert_reading(slider.read())
    if vol != new_vol:
        print(vol)
        vol = new_vol

    pressed_key = check_keypad_input()

    if pressed_key is not None:
        print(f"Key: {pressed_key}")

        if pressed_key == "#":
            clear_screen()
            screen.text("Quitting", 10, 8)
            screen.text("dashboard...", 10, 18)
            screen.show()
            break

        elif pressed_key == "*":
            started = False
            play_music = False
            current_screen = "home"
            clear_screen()
            home_screen()
            screen.show()

        if current_screen == "home":
            if pressed_key == "A":
                current_screen = "music"
                clear_screen()
                music_screen()
                screen.show()
                play_music = True

            elif pressed_key == "B":
                current_screen = "stopwatch"
                started = True
                stopwatch_seconds = 0
                clear_screen()
                stopwatch_screen(stopwatch_seconds)
                screen.show()

            elif pressed_key == "C":
                current_screen = "timer"
                started = True
                timer_seconds = 60
                clear_screen()
                timer_screen(timer_seconds)
                screen.show()

        elif current_screen == "music":
            if pressed_key == "A":
                play_music = True
            elif pressed_key == "B":
                play_music = False

    if play_music:
        if note_cursor >= len(note_list):
            note_cursor = 0
        
        if note_list[note_cursor] != "pause":
            play_note(note_list[note_cursor], 0.2, convert_volume(vol))
        note_cursor += 1

    if milliseconds == 1000:
        if current_screen == "timer":
            if timer_seconds > 0:
                timer_seconds -= 1
                timer_screen(timer_seconds)
            elif timer_seconds <= 0:
                clear_screen()
                screen.text("Time's up!", 15, 22)
                screen.show()

        elif current_screen == "stopwatch":
            stopwatch_seconds += 1
            stopwatch_screen(stopwatch_seconds)
        
        milliseconds = 0

    sleep(0.1)