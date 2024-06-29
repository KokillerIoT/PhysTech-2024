from gpiozero import Buzzer
import time

buzzer = Buzzer(5)

buzzer.on()
time.sleep(1)
buzzer.off()
