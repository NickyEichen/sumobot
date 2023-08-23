from sumobot.robot_hardware.motor import RawMotor as Motor
import time

motor1 = Motor(35, 33, True, False)
motor2 = Motor(12, 32, True, False)

motor1.drive_motor_raw(1)
motor2.drive_motor_raw(1)

time.sleep(1)

motor1.drive_motor_raw(-1)
motor2.drive_motor_raw(-1)

time.sleep(1)

motor1.drive_motor_raw(0)
motor2.drive_motor_raw(0)
