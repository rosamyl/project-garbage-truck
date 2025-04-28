from machine import Pin, time_pulse_us
from time import sleep_us, sleep
from servos import lift

trigger = Pin(10, Pin.OUT)
echo = Pin(11, Pin.IN)

def measure_distance() -> float:
    """https://wokwi.com/projects/359562059458336769"""
    # Ensure trigger is low initially
    trigger.low()
    sleep_us(2)

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep_us(10)
    trigger.low()

    # Measure the duration of the echo pulse (in microseconds)
    pulse_duration = time_pulse_us(echo, Pin.high)

    # Calculate the distance (in centimeters) using the speed of sound (343 m/s)
    distance = pulse_duration * 0.0343 / 2
    return distance

def scan_distances(time: float) -> list[float]:
    """Measures distances for given time and returns them in a list."""
    measured_distances = []
    elapsed_time = 0

    while elapsed_time < time:
        distance = measure_distance()
        measured_distances.append(distance)
        print("Distance: {:.2f} cm".format(distance))
        sleep(0.15)
        elapsed_time += 0.15

        # TODO:
        # It could be checked if there is a distance lower than others, which could be a object
        # and return early. Either using moving average or comparing min value to the average.
        # If there are multiple similarly low distances, it could be a wall or a bigger obstacle.

    return measured_distances

def test() -> None:
    """Test function to measure distance."""
    while True:
        # Measure the distance and print the value in centimeters
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance))
        if distance <= 6:
            lift()

        # Wait for 1 second before taking the next measurement
        sleep(1)

if __name__ == "__main__":
    test()
