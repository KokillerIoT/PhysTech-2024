import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the tilt sensor
tilt_pin = 12

# Set up the tilt pin as an input
GPIO.setup(tilt_pin, GPIO.IN)

# Counts how many times tilt happened
counter = 0

def workout_counter(count):
    time.sleep(0.5)
    print("Target number:", count)
    counter = 0
    print("Count:", counter)
    while counter < count:
        tilt_state = GPIO.input(tilt_pin)
        if tilt_state == 1:
            counter += 1
            print("Count:", counter)
            time.sleep(1)
    time.sleep(1)
    print("Finished")
    time.sleep(1)

def workout_timer(seconds):
    print("Target time:", seconds)
    for sec in range(seconds):
        print("Break time remaining:", seconds - sec, "seconds")
        time.sleep(1)
    print("Break time remaining:", 0, "seconds")
    time.sleep(2)

try:
    push_ups = int(input("How many push_ups: "))
    plank = int(input("Plank for how long: "))
    crunches = int(input("How many crunches: "))
    squats = int(input("How many squats: "))
    breaktime = int(input("Break for how long: "))
    
    print("Push ups")
    workout_counter(push_ups)
    print("Break")
    workout_timer(breaktime)
    
    print("Plank")
    time.sleep(1)
    for i in range(3):
        print("Starting in", 3 - i)
        time.sleep(1)
    workout_timer(plank)
    print("Break")
    workout_timer(breaktime)
    
    print("Crunches")
    workout_counter(crunches)
    print("Break")
    workout_timer(breaktime)
    
    print("Squats")
    workout_counter(squats)
    
    print("Workouts done")
    time.sleep(1)
    print("Program finished")
    GPIO.cleanup()

except:
    print("Error")
    print("Program finished")
    GPIO.cleanup()