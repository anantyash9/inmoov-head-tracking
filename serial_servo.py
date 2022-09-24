from pyfirmata import Arduino ,SERVO,PWM
from time import sleep
port="COM8"
import random
import time
pins={"face_pitch":6,
"face_yaw":2,
"mouth":3,
"eye_pitch":5,
"eye_yaw":4}

mean={"face_pitch":95,
"face_yaw":73,
"mouth":90,
"eye_pitch":30,
"eye_yaw":80}

def angle_to_pwm(angle):
    inMin, inMax, outMin, outMax=0,180,0,256
    return outMin + (float(angle - inMin) / float(inMax - inMin) * (outMax
                  - outMin))

board=Arduino(port)
for k,v in pins.items():
    board.digital[v].mode=SERVO
    board.digital[v].write(angle_to_pwm(mean[k]))
    print(k,angle_to_pwm(mean[k]))
    sleep(1)
def mouth_moov():
    t1=time.time()
    while time.time()-t1<5:
        board.digital[pins["mouth"]].write(angle_to_pwm(random.randrange(80,120)))
        sleep(0.2)
        board.digital[pins["mouth"]].write(angle_to_pwm(80))

def moov(part,angle):
    board.digital[pins[part]].write(angle_to_pwm(int(angle)))
# while True:
#     print("enter part and angle : ")
#     angle=input()
#     if angle=="mouth_moov":
#         mouth_moov()
#     else:
#         vals=angle.split(":")
#         if vals[0] in pins.keys():
#             board.digital[pins[vals[0]]].write(angle_to_pwm(int(vals[1])))      
#         else:
#             print("enter valid part")

# print("start")
# board.digital[pin].write(angle)
# sleep(1)


