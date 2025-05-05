from time import sleep, time
from machine import Pin, PWM
from ultrasonic import scan_distances, measure_distance
from servos import lift, DISTANCE_TO_LIFT
from logger import log

FORWARD, BACKWARD = True, False
RIGHT, LEFT = True, False
FASTEST, FAST, SLOW = 65535, 40000, 20000

sleep(1)

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

def motor_speeds(duty_a: int, duty_b: int) -> None:
    """Sets the motor speeds by duty 0-65535."""
    en12.duty_u16(duty_a)
    en34.duty_u16(duty_b)

def motor_directions(dir_a: bool, dir_b: bool) -> None:
    """Sets the motor directions. True = forward, False = backward."""
    dir_a = not dir_a
    in1.value(1 if dir_a else 0)
    in2.value(0 if dir_a else 1)
    in3.value(1 if dir_b else 0)
    in4.value(0 if dir_b else 1)

def stop() -> None:
    """Stops the motors."""
    motor_speeds(0, 0)

def drive(direction: bool, speed: int, drive_time: float) -> None:
    """Drives straight in the given direction for the given time."""
    motor_directions(direction, direction)
    motor_speeds(speed, speed)
    sleep(drive_time)
    stop()

def turn_on_place(direction: bool, speed: int, degree: int, stop_on_distance=None) -> None:
    """Turns on place by rotating the motors in opposite directions.
       If stop_on_distance is given, it stops when the distance is measured."""
    time_to_turn_90_deg = 5 # Needs to be tested
    time_to_turn = degree * (time_to_turn_90_deg / 90)

    dir_a, dir_b = FORWARD, BACKWARD
    if direction == LEFT:
        dir_a, dir_b = dir_b, dir_a

    motor_directions(dir_a, dir_b)
    motor_speeds(speed, speed)

    time_elapsed = 0
    if stop_on_distance is None:
        sleep(time_to_turn)
    else:
        while time_elapsed < time_to_turn:
            time_elapsed += 0.1
            distance = measure_distance()
            if 0 < distance <= stop_on_distance:
                break
            sleep(0.1)
    stop()

def drive_turn(drive_direction: bool, turn_direction: bool, speed: int, drive_time: float) -> list[float]:
    """Turns while driving and returns the measured distances."""
    a_speed, b_speed = speed, speed
    if turn_direction == LEFT:
        a_speed = int(a_speed / 2) - 5000
    else:
        b_speed = int(a_speed / 2) - 5000

    motor_directions(drive_direction, drive_direction)
    motor_speeds(a_speed, b_speed)

    distances = scan_distances(drive_time)

    stop()
    return distances

def drive_to_target(distance: float) -> bool:
    """Drives towards the target and returns true if the target is reached."""
    log("Target found")

    motor_directions(FORWARD, FORWARD)
    motor_speeds(FASTEST, FASTEST)

    start_time = time()

    while True:
        sleep(0.2)
        measured_distance = measure_distance()

        if measured_distance < 0:
            continue

        if measured_distance <= DISTANCE_TO_LIFT:
            sleep(0.1)
            double_check_distance = measure_distance()
            if double_check_distance <= DISTANCE_TO_LIFT:
                stop()
                return True

        if measured_distance <= distance:
            distance = measured_distance
        elif measured_distance > distance + 10:
            log("Target lost, try to find it again")
            stop()
            turn_on_place(LEFT, FAST, 15, stop_on_distance=distance)
            if 0 < measure_distance() <= distance:
                continue
            turn_on_place(RIGHT, FAST, 30, stop_on_distance=distance)
            if measure_distance() > distance:
                stop()
                return False
        if time() - start_time > 7:
            log("Timeout")
            stop()
            return False

def test_motors() -> None:
    """Tests the motors by driving in all directions."""
    drive(FORWARD, FASTEST, 2)
    drive(BACKWARD, FASTEST, 2)
    drive_turn(FORWARD, LEFT, FASTEST, 2)
    drive_turn(FORWARD, RIGHT, FASTEST, 2)
    turn_on_place(LEFT, FASTEST, 180)
    turn_on_place(RIGHT, FASTEST, 90)

if __name__ == "__main__":
    test_motors()
