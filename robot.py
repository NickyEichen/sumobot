import json
import RPi.GPIO as GPIO

class Drivebase:
    def __init__(self, hardware_map, breaking=False):
        A1 = hardware_map.get("MOTOR_PIN_A1")
        A2 = hardware_map.get("MOTOR_PIN_A2")
        B1 = hardware_map.get("MOTOR_PIN_B1")
        B2 = hardware_map.get("MOTOR_PIN_B2")

        EL1 = hardware_map.get("ENCODER_LEFT_A")
        EL2 = hardware_map.get("ENCODER_LEFT_B")
        ER1 = hardware_map.get("ENCODER_RIGHT_A")
        ER2 = hardware_map.get("ENCODER_RIGHT_B")

        left_motor = Motor(A1, A2, breaking, False)
        left_encoder = Encoder(EL1, EL2, False)

        right_motor = Motor(B1, B2, breaking, True)
        right_encoder = EncodeR(ER1, ER2, True)

    def drive_curvature(self, base_power, curvature):
        """Positive curvature indicates to the left (or backwards to the right)
        while negative curvature indicates curving to the right (or backwards to the left).
        Uses a PID to maintain the desired curvature.

        Not Yet Implemented
        """
        raise NotImplementedError

class Robot:

    def __init__(self):
        with open('json/hardware_map.json') as f:
            hardware_map = json.load(f)
        GPIO.setmode(GPIO.BCM)

        drivebase = Drivebase(hardware_map)
