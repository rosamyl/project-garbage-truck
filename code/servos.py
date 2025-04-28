from machine import Pin, PWM
from time import sleep

DOWN_A, UP_A = 110, 0
DOWN_B, UP_B = 50, 160

DISTANCE_TO_LIFT = 6 # cm

servo_A = PWM(Pin(8))
servo_A.freq(50)
servo_B = PWM(Pin(9))
servo_B.freq(50)

def init_servos() -> None:
    """Initializes the servos."""
    global servo_A, servo_B
    servo_A = PWM(Pin(8))
    servo_A.freq(50)
    servo_B = PWM(Pin(9))
    servo_B.freq(50)

def get_duty(angle: int) -> int:
    """Converts the angle to duty cycle for the servo."""
    min_duty = 1500
    max_duty = 8000
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    return duty

def set_angle_a(angle: int) -> None:
    """Sets the angle of servo A."""
    duty = get_duty(angle)
    servo_A.duty_u16(duty)

def set_angle_b(angle: int) -> None:
    """Sets the angle of servo B."""
    duty = get_duty(angle)
    servo_B.duty_u16(duty)

def fast_lift() -> None:
    """Lifts the servos quickly up and down. Not recommended for use."""
    init_servos()
    set_angle_b(UP_B)
    set_angle_a(UP_A)
    sleep(1)
    set_angle_b(DOWN_B)
    set_angle_a(DOWN_A)
    sleep(0.5)
    servo_A.deinit()
    servo_B.deinit()

def lift() -> None:
    """Lifts the servos up and down slowly."""
    init_servos()

    duty_a_down = get_duty(DOWN_A)
    duty_a_up = get_duty(UP_A)
    lift_range_a = range(duty_a_down, duty_a_up, -2)

    duty_b_down = get_duty(DOWN_B)
    duty_b_up = get_duty(UP_B)
    lift_range_b = range(duty_b_down, duty_b_up, 2)

    for a, b in zip(lift_range_a, lift_range_b):
        servo_A.duty_u16(a)
        servo_B.duty_u16(b)
        sleep(0.001)
    sleep(0.5)
    for a, b in zip(reversed(lift_range_a), reversed(lift_range_b)):
        servo_A.duty_u16(a)
        servo_B.duty_u16(b)
        sleep(0.001)
    sleep(0.1)

    servo_A.deinit()
    servo_B.deinit()

if __name__ == "__main__":
    sleep(2)
    lift()
