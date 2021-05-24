# Use this custom pin-factory to fix servo jitter. 
# !!! Make sure pigpio deamon is running: 'sudo pigpiod' !!!
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo, Button, RotaryEncoder
from signal import pause
from time import sleep
import threading

IS_AV_MODE = False

# create a custom pin-factory to fix servo jitter
# more info heere: https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# and here: https://gpiozero.readthedocs.io/en/stable/api_pins.html
pigpio_factory = PiGPIOFactory()
servo = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=pigpio_factory)

ENCODER = RotaryEncoder(17, 18, max_steps=0) # Rotary encoder 
ENC_SRV_RATIO = 2 # How many encoder steps is one servo angle

# Create a limit switch senseor which detects system misalignment 
button = Button(27)

def servo_control(delay, servo_step):
  # global IS_AV_MODE
  while IS_AV_MODE:
    if servo.angle + servo_step > servo.min_angle and servo.angle + servo_step < servo.max_angle:
      servo.angle += servo_step
      sleep(delay)
    else:
      servo_step *= -1
      sleep(delay)
    
    # print(f"servo pos: {servo.angle}")

def encoder_reader():
  global ENCODER
  # encoder_done = threading.Event()  
  ENCODER.when_rotated = get_encoder_step
  print('encoder online!')  
  # encoder_done.wait()


def get_encoder_step():
    global ENCODER #, SERVO, IS_AV_MODE, ENC_SRV_RATIO
    enc_pos = ENCODER.steps
    print(enc_pos)


def av_steering_init():
  servo.angle = 0
  print("Calibration - Servo set to mid position. Align handle position with servo (limit sensor LED off) ")
  while IS_AV_MODE == False:
    sleep(1)
  print("Ready!")    
  sleep(1)
  ENCODER.steps = 0
  print("Resetting encoder")
  sleep(1)


def senseor_on():
    global IS_AV_MODE
    IS_AV_MODE = True
    print("engaged!")


def senseor_off():
  global IS_AV_MODE  
  IS_AV_MODE = False
  print("disengaged!")


if __name__ == "__main__":
  
  # Define sensor triggers - missalignment is equal to a "button released" state
  button.when_pressed = senseor_off
  button.when_released = senseor_on
  
  # init encoder listener
  encoder_reader()
  
  # Initial callibration
  av_steering_init()

  while True:
    if IS_AV_MODE:
      print("AV MODE")
      servo_control(0.1, 2)    

    sleep(2)

    # start manual mode
    # print("MANUAL MODE!")
