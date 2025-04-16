from machine import Pin, time_pulse_us
from time import sleep_us, sleep
from servos import lift

trigger = Pin(10, Pin.OUT)
echo = Pin(11, Pin.IN)

def measure_distance():
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

def test():
    while True:
        # Measure the distance and print the value in centimeters
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance))
        if distance <= 5:
            lift()

        # Wait for 1 second before taking the next measurement
        sleep(1)

if __name__ == "__main__":
    test()
