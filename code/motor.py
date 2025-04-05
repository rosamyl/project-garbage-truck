from machine import Pin, PWM
from time import sleep

FORWARD, BACKWARD = True, False
RIGHT, LEFT = True, False
FASTEST, FAST, SLOW = 65535, 40000, 20000

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

def motor_speeds(duty_a, duty_b):  # duty: 0-65535
    en12.duty_u16(duty_a)
    en34.duty_u16(duty_b)

def motor_directions(dir_a, dir_b):
    in1.value(1 if dir_a else 0)
    in2.value(0 if dir_a else 1)
    in3.value(1 if dir_b else 0)
    in4.value(0 if dir_b else 1)
 
def stop():
    motor_speeds(0, 0)

def drive(direction, speed, time):
    motor_directions(direction, direction)
    motor_speeds(speed, speed)
    sleep(time)
    stop()

def turn(direction, speed, degree):
    time_to_turn_90_deg = 1 # Needs to be tested
    time_to_turn = degree * (time_to_turn_90_deg / 90)

    dir_a, dir_b = FORWARD, BACKWARD
    if direction == LEFT:
        dir_a, dir_b = dir_b, dir_a
    motor_directions(dir_a, dir_b)
    motor_speeds(speed, speed)
    sleep(time_to_turn)
    stop()

def test_motors():
    drive(FORWARD, FASTEST, 2)
    drive(BACKWARD, FAST, 2)
    turn(LEFT, FAST, 180)
    turn(RIGHT, FASTEST, 90)
