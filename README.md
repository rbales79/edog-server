# TCPServer for Edog Control

This Python script provides a TCP server implementation to control edog's servo motors using the `adafruit_servokit` library. It listens for incoming TCP connections, receives servo angle commands, and adjusts the servo motors accordingly.

## Requirements

- Python 3.6 or higher
- `adafruit-circuitpython-servokit` library

You can install the required library using pip:

```bash
pip3 install adafruit-circuitpython-servokit
```

## Usage

To use the script, you can simply run it using Python:

```bash
python script_name.py
```

By default, the server will bind to `0.0.0.0` on port `5560`, but you can modify these settings by changing the `host` and `port` parameters in the `TCPServer` class constructor.

## TCP Communication Protocol

The server expects incoming messages to be UTF-8 encoded strings. Each message should contain one or more commands to set the angles of the servo motors. Commands should be separated by the pipe `|` character, and each command should have the following format:

```
servo_id:angle1,angle2|servo_id:angle1,angle2|servo_id:angle1,angle2
```

- `servo_id`: An integer representing the ID of the servo motor.
- `angle1`, `angle2`: Float values representing the angles to set for the corresponding servo motors.


---

Feel free to contribute or report issues on the project's GitHub repository.