from time import sleep
import threading
from gpiozero import RotaryEncoder, AngularServo

# use custom pin-factory to fix servo jitter, make sure pigpio deamon is running: 'sudo pigpiod'
from gpiozero.pins.pigpio import PiGPIOFactory
pigpio_factory = PiGPIOFactory()


ENCODER = RotaryEncoder(17, 18, max_steps=0)
SERVO = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=pigpio_factory)
ENC_SRV_RATIO = 2 # How many encoder steps is one servo angle
TAKEOVER_OFFSET = 40 #The difference (in angles) between the Encoder and the Servo posiotn to trigger manual override
IS_AV_MODE = True


SERVO.angle = 0
print("Servo set to mid. Move hande to center position.")
sleep(5)

print("Resetting encoder")
ENCODER.steps = 0


def encoder_reader():
  global ENCODER
  encoder_done = threading.Event()  
  print('Turn the encoder!!')

  ENCODER.when_rotated = get_encoder_step
  encoder_done.wait()

def get_encoder_step():
    global ENCODER, SERVO, IS_AV_MODE, ENC_SRV_RATIO, TAKEOVER_OFFSET
    enc_pos = ENCODER.steps

    if IS_AV_MODE:
      srv_pos = SERVO.angle
      offset = (srv_pos * ENC_SRV_RATIO) - enc_pos
      print(offset)
      if abs(offset) > TAKEOVER_OFFSET:
        IS_AV_MODE = False
    else:
      print(enc_pos)

def servo_ctrl():
  global SERVO, IS_AV_MODE, ENCODER, ENC_SRV_RATIO
  # servo_done = threading.Event()
  delay = 0.1     #seconds
  servo_step = 2  #angle

  SERVO.max()
  print("Moving to Max position")
  sleep(2)
  max_encoder = ENCODER.steps

  print("Servo Online!")
  SERVO.min()
  print("Moving to Min position")
  sleep(2)
  min_encoder = ENCODER.steps

  ENC_SRV_RATIO = (max_encoder - min_encoder) / (SERVO.max_angle - SERVO.min_angle)
  print(f"Servo rng: {SERVO.min_angle}-{SERVO.max_angle} // Encoder rng: {min_encoder}-{max_encoder}")
  print(f"Ratio: {ENC_SRV_RATIO}")
  
  SERVO.mid()
  sleep(2)
  IS_AV_MODE = True
  while IS_AV_MODE == True:
    
    if SERVO.angle < (SERVO.min_angle - servo_step):
      servo_step = 2
      sleep(2)      
    elif SERVO.angle > (SERVO.max_angle - servo_step):
      servo_step = -2
      sleep(2)
    
    SERVO.angle += servo_step
    # print(SERVO.angle)
    sleep(delay)

# Start Threads!
encoder_thread = threading.Thread(target=encoder_reader)
encoder_thread.start()

servo_thread = threading.Thread(target=servo_ctrl)
servo_thread.start()

# run endless thread
# done.wait()