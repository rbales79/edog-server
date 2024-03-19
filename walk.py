from adafruit_servokit import ServoKit
import time

# Configuration
kit = ServoKit(channels=16)
delay_between_moves = 0.125  # Seconds

# Servo mappings to legs
leg_servo_mapping = {
    0: {'femur': 0, 'tibia': 1},
    1: {'femur': 2, 'tibia': 3},
    2: {'femur': 4, 'tibia': 5},
    3: {'femur': 6, 'tibia': 7},
}

# Positions by leg: Each leg can have a custom sequence of positions
# Format: leg_id: [[femur_angle, tibia_angle], [femur_angle, tibia_angle], ...]
positions_by_leg = {
    0: [[52, 90], [30, 60], [52, 90]],  # Example positions for leg 0
    1: [[52, 90], [80, 100], [52, 90]],  # customize per leg
    2: [[52, 88], [30, 60], [52, 88]],
    3: [[52, 88], [80, 100], [52, 88]],
}

def move_leg(leg_id, position):
    """Move a leg to a specified position."""
    femur_id = leg_servo_mapping[leg_id]['femur']
    tibia_id = leg_servo_mapping[leg_id]['tibia']
    kit.servo[femur_id].angle = position[0]
    kit.servo[tibia_id].angle = position[1]
    print(f"Moving leg {leg_id} to position {position}")

def iterate_leg_positions():
    """Iterate each leg through its series of positions."""
    while True:
        for leg_id, positions in positions_by_leg.items():
            for position in positions:
                move_leg(leg_id, position)
                time.sleep(delay_between_moves)

if __name__ == "__main__":
    try:
        iterate_leg_positions()
    except KeyboardInterrupt:
        print("Program exited by user")
