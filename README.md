<div align="center">    
    <h2 align="center">TCPServer for Edog Control</h2>
    <p align="center">
        If you wish to control your Edog robot via Wi-Fi, you've come to the right place 😎
    </p>
    <a href="https://github.com/SolidMakers/edog-server">
        <img src="https://i.postimg.cc/tCtShWBv/Repo-illustartion.png" alt="Logo">
     </a>
This Python script provides a TCP server implementation to control edog's servo motors using the `adafruit_servokit` library. It listens for incoming TCP connections, receives servo angle commands, and adjusts the servo motors accordingly.
</div>

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

<div align="center">  
    <img src="https://i.postimg.cc/2SbjKkgW/image.png" alt="Logo">
</div>

```
leg_id:tibia_angle,femur_angle|leg_id:tibia_angle,femur_angle|leg_id:tibia_angle,femur_angle
```

- `leg_id`: An integer representing the ID of the servo motor.
- `angle1`, `angle2`: Float values representing the angles to set for the corresponding servo motors.

## Exemple

In this example, we set the tibia angle of `leg 0` to 52.8° and the femur angle to 90.4° => 0:52.8,90.4
```python
strOrder = "0:52.8,90.4|1:52.8,90.4|2:51.6,87.7|3:51.6,87.7"
self.socket.send(bytes(strOrder, "utf-8"))
```

<div align="center">  
    <img src="https://i.postimg.cc/ydqBD26S/leg-and-servo-id-demo.png" alt="Logo">
</div>

---

Feel free to contribute or report issues on the project's GitHub repository.