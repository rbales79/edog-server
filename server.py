import logging
import socket
import time
from adafruit_servokit import ServoKit
from typing import Tuple, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TCPServer:
    kit = ServoKit(channels=16)

    def __init__(self, host: str = '0.0.0.0', port: int = 5560) -> None:
        self.host = host
        self.port = port
        self.socket = None
        self._create_socket()

    def servo_angle(self, servo_id: int, angle: float) -> None:
        """Set the angle of a servo."""
        if 0 <= angle <= 180:
            logging.info(f'Setting servo {servo_id} to angle {angle}')
            self.kit.servo[servo_id].angle = angle
        else:
            logging.warning("Angle out of range: %s", angle)

    def _create_socket(self) -> None:
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

    def _handle_client(self, conn: Tuple[socket.socket, Any]) -> None:
        """Handle incoming client connections."""
        logging.info(f"Connection established with {conn[1]}")
        try:
            while True:
                data = conn[0].recv(4096)
                if not data:
                    break
                data_string = data.decode("utf-8")
                logging.info(f"Received message: {data_string}")

                legs_order = data_string.split("|")
                for leg_order in legs_order:
                    parts = leg_order.split(":")
                    if len(parts) == 2 and parts[1]:
                        leg_id = int(parts[0])
                        angles = list(map(float, parts[1].split(",")))

                        if leg_id in [1, 3]:
                            self.servo_angle(leg_id * 2, 180 - angles[0])
                            self.servo_angle(leg_id * 2 + 1, 180 - angles[1])
                        else:
                            self.servo_angle(leg_id * 2, angles[0])
                            self.servo_angle(leg_id * 2 + 1, angles[1])
                    else:
                        logging.warning("Received malformed data: %s", leg_order)

        except ConnectionError:
            logging.info("Connection lost.")
        finally:
            conn[0].close()

    def start(self) -> None:
        """Start the TCP server."""
        if not self.socket:
            return

        while True:
            try:
                client_conn = self.socket.accept()
                self._handle_client(client_conn)
            except KeyboardInterrupt:
                logging.info("Server shutting down...")
                break
            except Exception as e:
                logging.exception("An unexpected error occurred: %s", e)

        self.socket.close()


if __name__ == "__main__":
    server = TCPServer()
    server.start()
