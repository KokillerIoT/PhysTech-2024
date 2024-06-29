import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the tilt sensor
tilt_pin = 12

# Set up the tilt pin as an input
GPIO.setup(tilt_pin, GPIO.IN)

try:
    while True:
        # Read the state of the tilt sensor
        tilt_state = GPIO.input(tilt_pin) # 
        if tilt_state == 1:
            print("Tilt detected.")
        # Print the state (1 for tilted, 0 for not tilted)
        # print("Tilt sensor state:", tilt_state)
        # Wait a short time before checking again
        time.sleep(2)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    GPIO.cleanup()
