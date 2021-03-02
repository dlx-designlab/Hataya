import threading
from gpiozero import RotaryEncoder, Servo
from time import sleep

SERVO = Servo(22)
ROTOR = RotaryEncoder(17, 18, max_steps=0)


SERVO.mid()
sleep(3)
ROTOR.steps = 0


def encoder_reader():
  global ROTOR
  encoder_done = threading.Event()  
  print('Turn the encoder!!')
  
  ROTOR.when_rotated = update_rotor
  encoder_done.wait()

def update_rotor():
    global ROTOR
    steps = ROTOR.steps
    print(steps)

def servo_ctrl():
  global SERVO
  # servo_done = threading.Event()
  print("Servo Online!")
  while True:
    SERVO.min()
    print("servo pos min")
    sleep(5)
    SERVO.mid()
    print("servo pos mid")
    sleep(5)
    SERVO.max()
    print("servo pos max")
    sleep(5)

encoder_thread = threading.Thread(target=encoder_reader)
encoder_thread.start()

servo_thread = threading.Thread(target=servo_ctrl)
servo_thread.start()

# run endless thread
# done.wait()

