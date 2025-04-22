from time import sleep
from motor import test_motors, stop
from servos import lift

stop()

if __name__ == "__main__":
    #test_motors()
    sleep(1)
    lift()
