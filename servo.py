# use this custom pin-factory to fix servo jitter. 
# make sure pigpio deamon is running: 'sudo pigpiod'
from gpiozero.pins.pigpio import PiGPIOFactory

from gpiozero import AngularServo
from time import sleep

# create a custom pin-factory to fix servo jitter
# more info heere: https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# and here: https://gpiozero.readthedocs.io/en/stable/api_pins.html
pigpio_factory = PiGPIOFactory()

servo = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=pigpio_factory)
servo.angle = 0
print("servo mid")
sleep(3)


while True:

  delay = 0.1     #seconds
  servo_step = 2  #angle

  for i in range (servo.min_angle, servo.max_angle, 2):
    servo.angle = i
    print(f"servo pos {i}")
    sleep(delay)


  for i in range (servo.max_angle, servo.min_angle, -2):
    servo.angle = i
    print(f"servo pos {i}")
    sleep(delay)