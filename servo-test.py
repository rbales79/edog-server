from adafruit_servokit import ServoKit
import re

# Initialize the ServoKit instance for 16 channels
kit = ServoKit(channels=16)

def set_servo_angle(servo_id: int, angle: float):
    """Sets the specified servo to the given angle."""
    if 0 <= servo_id < 16 and 0 <= angle <= 180:
        print(f"Setting servo {servo_id} to angle {angle}")
        kit.servo[servo_id].angle = angle
    else:
        print("Invalid servo ID or angle. Servo ID must be between 0-15 and angle between 0-180.")

print("Interactive Servo Control")
print("Enter command in the format servoID:Angle, or 'exit' to quit.")

while True:
    command = input("Enter servoID:Angle > ").strip()
    if command.lower() == 'exit':
        print("Exiting interactive servo control.")
        break

    match = re.match(r"(\d+):(\d+)", command)
    if match:
        servo_id = int(match.group(1))
        angle = int(match.group(2))
        set_servo_angle(servo_id, angle)
    else:
        print("Invalid format. Please use servoID:Angle.")