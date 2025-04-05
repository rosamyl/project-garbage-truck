from machine import Pin, PWM
from time import sleep

FORWARD, BACKWARD = True, False

# Motor A
in1 = Pin(2, Pin.OUT)
in2 = Pin(3, Pin.OUT)
en12 = PWM(Pin(6))
en12.freq(1000)

# Motor B
in3 = Pin(4, Pin.OUT)
in4 = Pin(5, Pin.OUT)
en34 = PWM(Pin(7))
en34.freq(1000)

def motor_A_direction(forward):
    in1.value(1 if forward else 0)
    in2.value(0 if forward else 1)

def motor_B_direction(forward):
    in3.value(1 if forward else 0)
    in4.value(0 if forward else 1)

def motors_speed(duty):  # duty: 0-65535
    en12.duty_u16(duty)
    en34.duty_u16(duty)

print("Testing motors")

motor_A_direction(FORWARD)
motor_B_direction(FORWARD)
motors_speed(65535)
print("Forward")
sleep(2)

motor_A_direction(BACKWARD)
motor_B_direction(BACKWARD)
print("Backward")
sleep(2)

motor_A_direction(FORWARD)
motor_B_direction(BACKWARD)
print("Turn right")
sleep(2)

motors_speed(0)
print("Stop")
