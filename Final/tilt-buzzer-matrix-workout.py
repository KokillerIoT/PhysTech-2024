import time, sys, RPi.GPIO as GPIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Buzzer

# setting up the display
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.parallel = 1
options.gpio_slowdown = 3
options.drop_privileges=False

imageWidth = 64
imageHeight = 32

# fonts : "pixelmix.ttf"(proportion - 8:5)
small_font = ImageFont.truetype("pixelmix.ttf", 8)
midium_font = ImageFont.truetype("pixelmix.ttf", 16)
large_font = ImageFont.truetype("pixelmix.ttf", 24)

# RGB colors
black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 0, 255)
yellow_color = (225, 225, 0)
lightblue_color = (0, 255, 255)
orange_color = (255, 140, 0)

# setting up tilt sensor
GPIO.setmode(GPIO.BCM)
tilt_pin = 12
GPIO.setup(tilt_pin, GPIO.IN)

# setting up buzzer
buzzer = Buzzer(5)

# shows how many of what workout
def workout_title(workout, num):
    image = Image.new("RGB", (imageWidth, imageHeight), black_color)
    draw = ImageDraw.Draw(image)
    draw.text((5, 0), workout[0], fill=yellow_color, font=midium_font)
    draw.text((16, 8), workout[1:], fill=yellow_color, font=small_font)
    draw.text((4, 20), "TGT:", fill=white_color, font=small_font)
    draw.text((32, 16), str(num), fill=green_color, font=midium_font)
    return image

# shows how long the break is
def break_title(seconds):
    image = Image.new("RGB", (imageWidth, imageHeight), black_color)
    draw = ImageDraw.Draw(image)
    draw.text((5, 0), "B", fill=lightblue_color, font=midium_font)
    draw.text((16, 8), "REAK", fill=lightblue_color, font=small_font)
    draw.text((4, 20), "TIME:", fill=white_color, font=small_font)
    draw.text((32, 16), str(seconds), fill=green_color, font=midium_font)
    return image

# shows the count or time during each workout
def count_panel(num, text_above):
    image = Image.new("RGB", (imageWidth, imageHeight), black_color)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text_above, fill=white_color, font=small_font)
    if len(str(num)) == 1:
        start_width = 23
        rgb_color = yellow_color
    elif len(str(num)) == 2:
        start_width = 16
        rgb_color = orange_color
    elif len(str(num)) == 3:
        start_width = 10
        rgb_color = red_color
    draw.text((start_width, 8), str(num), fill=rgb_color, font=large_font)
    return image

# counting up for workouts like pushups, crunches, etc.
def count_up(count, text_above):
    counter = 0
    matrix.SetImage(count_panel(counter, text_above))
    sound(1)
    while counter < count:
        tilt_or_not = GPIO.input(tilt_pin)
        if tilt_or_not == 1:
            while True:
                tilt_or_not = GPIO.input(tilt_pin)
                if tilt_or_not == 1:
                    pass
                else:
                    break
            counter += 1
            matrix.SetImage(count_panel(counter, text_above))

# counting down for workouts like plank, as well as counting down during a break and getting ready
def countdown(seconds, text_above):
    for sec in range(seconds):
        if seconds - sec in [1, 2, 3]:
            matrix.SetImage(count_panel(seconds-sec, text_above))
            sound(0.5)
            time.sleep(0.5)
        elif seconds - sec == seconds:
            matrix.SetImage(count_panel(seconds-sec, text_above))
            sound(1)
        else:
            matrix.SetImage(count_panel(seconds-sec, text_above))
            time.sleep(1)

# shows a message when you finish each workout
def workout_done():
    image = Image.new("RGB", (imageWidth, imageHeight), black_color)
    draw = ImageDraw.Draw(image)
    draw.text((8, 8), "DONE!", fill=blue_color, font=midium_font)
    return image

# activates buzzer for specific time
def sound(seconds):
    buzzer.on()
    time.sleep(seconds)
    buzzer.off()

# setting up the display
matrix = RGBMatrix(options = options)

# setting up order and time for each workouts and breaks
workout_list = {"PUSHUPS":25, "PLANK":120, "CRUNCHES":150, "SQUATS":250, "DUMBELLS":60}
workout_name = list(workout_list.keys())
break_time = 60

# Program
for workout in workout_name[:-1]:
    matrix.SetImage(workout_title(workout, workout_list[workout]))
    sound(1)
    time.sleep(4)
    countdown(3, "STARTS IN(S)")
    if workout == "PLANK":
        countdown(workout_list[workout], "REMAINING(S)")
    else:
        count_up(workout_list[workout], "COUNT")
    matrix.SetImage(workout_done())
    sound(1)
    time.sleep(2)
    matrix.SetImage(break_title(break_time))
    time.sleep(4)
    countdown(break_time, "REMAINING(S)")
matrix.SetImage(workout_title(workout_name[-1], workout_list[workout_name[-1]]))
sound(1)
time.sleep(4)
countdown(3, "STARTS IN(S)")
if workout_name[-1] == "PLANK":
    countdown(workout_list[workout_name[-1]], "REMAINING(S)")
else:
    count_up(workout_list[workout_name[-1]], "COUNT")
matrix.SetImage(workout_done())
time.sleep(5)