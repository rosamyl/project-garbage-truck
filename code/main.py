from time import sleep
from motor import test_motors
from servos import lift

if __name__ == "__main__":
    test_motors()
    lift()
    sleep(1)
    lift()
