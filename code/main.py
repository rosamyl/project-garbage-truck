from time import sleep
from random import randint
from motor import drive_turn, turn_on_place, drive_to_target, test_motors, stop, LEFT, RIGHT, FORWARD, BACKWARD, FAST, FASTEST
from servos import lift, DISTANCE_TO_LIFT
from ultrasonic import measure_distance

stop()

def run() -> None:
    """Main loop"""
    while True:
        direction_to_turn = randint(0, 1) == 0
        driving_time = randint(2, 4)

        measured_distances = drive_turn(FORWARD, direction_to_turn, FAST, driving_time)

        process_distances(measured_distances, direction_to_turn)

def process_distances(distances: list[float], previous_direction: bool) -> None:
    """Processes the measured distances and takes actions based on them."""
    close_measurements = sum(1 for distance in distances if distance <= DISTANCE_TO_LIFT)
    object_on_scoop = close_measurements > 1 # To avoid lifting on measurement errors

    if object_on_scoop:
        lift()
        turn_on_place(previous_direction, FAST, 90)
        return

    average_distance = sum(distances) / len(distances)
    min_distance = min(distances)
    max_distance = max(distances)

    if average_distance < 20 and max_distance < 25:
        # Wall in front
        turn_on_place(previous_direction, FAST, 180)
        return

    if average_distance > 300 and min_distance > 200:
        # Far away and too much variance in measurements
        return

    # Check if the lowest distance is significantly lower than
    # measurements before and after it which indicates an object
    min_index = distances.index(min_distance)
    longer_distances_before = False
    longer_distances_after = False

    for i in range(1, 3):
        if min_index - i >= 0 and distances[min_index - i] >= min_distance + 20:
            longer_distances_before = True
        if min_index + i < len(distances) and distances[min_index + i] >= min_distance + 20:
            longer_distances_after = True

    if longer_distances_before and longer_distances_after:
        turn_on_place(not previous_direction, FAST, 30, stop_on_distance=min_distance)
        if 0 < measure_distance() <= min_distance:
            object_on_scoop = drive_to_target(min_distance)
            if object_on_scoop:
                lift()
                turn_on_place(previous_direction, FAST, 90)
            return

    print("No actions taken.")

if __name__ == "__main__":
    sleep(1)
    test_motors()
    sleep(1)
    #lift()
