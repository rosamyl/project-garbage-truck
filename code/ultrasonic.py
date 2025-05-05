from time import sleep_us, sleep
from machine import Pin, time_pulse_us
from servos import lift, DISTANCE_TO_LIFT
from logger import log

trigger = Pin(10, Pin.OUT)
echo = Pin(11, Pin.IN)

def measure_distance() -> float:
    """
    Measures the distance using an ultrasonic sensor.
    Returns a negative value if timed out.
    https://wokwi.com/projects/359562059458336769
    """
    # Ensure trigger is low initially
    trigger.low()
    sleep_us(2)

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep_us(10)
    trigger.low()

    # Measure the duration of the echo pulse (in microseconds)
    pulse_duration = time_pulse_us(echo, Pin.high, 30000)

    if pulse_duration < 0:
        print("Timed out")
        return pulse_duration

    # Calculate the distance (in centimeters) using the speed of sound (343 m/s)
    distance = pulse_duration * 0.0343 / 2
    return distance

def scan_distances(time: float) -> list[float]:
    """Measures distances for given time and returns them in a list."""
    measured_distances = []
    elapsed_time = 0

    while elapsed_time < time:
        distance = measure_distance()
        if distance > 0:
            measured_distances.append(distance)
            #print("Distance: {:.2f} cm".format(distance))
            if distance < DISTANCE_TO_LIFT and len(measured_distances) > 1 and measured_distances[-2] < DISTANCE_TO_LIFT:
                return measured_distances
        sleep(0.3)
        elapsed_time += 0.3

    return measured_distances

def test() -> None:
    """Test function to measure distance."""
    while True:
        # Measure the distance and print the value in centimeters
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance))
        if 0 < distance <= 6:
            lift()

        # Wait for 1 second before taking the next measurement
        sleep(1)

if __name__ == "__main__":
    test()
