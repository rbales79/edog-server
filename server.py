import logging
import socket
from adafruit_servokit import ServoKit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TCPServer:
    kit = ServoKit(channels=16)

    def __init__(self, host='0.0.0.0', port=5560):
        self.host = host
        self.port = port
        self.socket = None
        self._create_socket()

    def servo_angle(self, servo_id: int, angle: float):
        """Set the angle of a servo."""
        if 0 <= angle <= 180:
            logging.info(f'Setting servo {servo_id} to angle {angle}')
            self.kit.servo[servo_id].angle = angle
            return True
        else:
            logging.warning("Angle out of range: %s", angle)
            return False

    def _create_socket(self):
        """Create and bind the TCP socket."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            logging.info(f"Server started at {self.host}:{self.port} awaiting connections...")
        except socket.error as err:
            logging.error("Error creating socket: %s", err)
            if self.socket:
                self.socket.close()

    def _handle_client(self, conn, addr):
        """Handle incoming client connections and send responses."""
        logging.info(f"Connection established with {addr}")
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data_string = data.decode("utf-8")
                logging.info(f"Received message: {data_string}")

                success = True
                legs_order = data_string.split("|")
                for leg_order in legs_order:
                    parts = leg_order.split(":")
                    if len(parts) == 2 and parts[1]:
                        leg_id, angles_str = int(parts[0]), parts[1].split(",")
                        if len(angles_str) == 2:
                            # Calculate servo IDs based on leg_id
                            femur_servo_id = leg_id * 2
                            tibia_servo_id = leg_id * 2 + 1
                            femur_angle = float(angles_str[0])
                            tibia_angle = float(angles_str[1])
                            # Set angles for both femur and tibia servos
                            success &= self.servo_angle(femur_servo_id, femur_angle)
                            success &= self.servo_angle(tibia_servo_id, tibia_angle)
                        else:
                            success = False
                    else:
                        success = False

                response_message = "Command executed successfully." if success else "Failed to execute command."
                conn.sendall(response_message.encode())
        except ConnectionError:
            logging.info("Connection lost.")
        finally:
            conn.close()

    def start(self):
        """Start the TCP server."""
        if not self.socket:
            return

        while True:
            try:
                client_conn, addr = self.socket.accept()
                self._handle_client(client_conn, addr)
            except KeyboardInterrupt:
                logging.info("Server shutting down...")
                break
            except Exception as e:
                logging.exception("An unexpected error occurred: %s", e)

        self.socket.close()

if __name__ == "__main__":
    server = TCPServer()
    server.start()