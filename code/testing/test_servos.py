from machine import Pin, PWM
import time

DOWN_A, UP_A = 130, 0 

servo_A = PWM(Pin(8))
servo_A.freq(50)

def set_angle_A(angle):
    min_duty = 1500  # Needs to be tested
    max_duty = 8000  # Needs to be tested
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo_A.duty_u16(duty)
    
set_angle_A(DOWN_A) 
time.sleep(0.5)
set_angle_A(UP_A)
time.sleep(2)
set_angle_A(DOWN_A)
