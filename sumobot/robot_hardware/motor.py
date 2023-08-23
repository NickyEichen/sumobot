import RPi.GPIO as GPIO
from sumobot.robot_hardware.motor_encoder import MotorEncoder
from enum import Enum
from utils import PIDs

class RawMotor:

    def __init__(self, pin1, pin2, breaking, reversed):
        GPIO.setup(pin1, GPIO.OUT)
        self.pin1 = GPIO.PWM(pin1, 1000)
        self.pin1.start(0)
        GPIO.setup(pin2, GPIO.OUT)
        self.pin2 = GPIO.PWM(pin2, 1000)
        self.pin2.start(0)

        self.breaking = breaking
        self.direction = reversed

    def drive_motor_raw(self, power):
        direction = (power >= 0) != self.direction
        pwm = abs(power)*100
        other = int(self.breaking)

        if direction ^ self.breaking:
            #pin 1 PWM, pin 2 other
            self.pin1.ChangeDutyCycle(pwm)
            self.pin2.ChangeDutyCycle(other)
        else:
            #pin 2 PWM, pin 1 other
            self.pin1.ChangeDutyCycle(other)
            self.pin2.ChangeDutyCycle(pwm)

class Modes(Enum):
    SET_POSITION = 0
    SET_VELOCITY = 1
    SET_POWER = 2
    SET_ANGULAR_VELOCITY = 3 # Not yet implemented
    ACTIVE_BREAKING = 4


class PIDMotor:

    def __init__(self, hwmap, ID):

        m1 = hwmap.get("MOTOR_%s_P1"%ID)
        m2 = hwmap.get("MOTOR_%s_P2"%ID)
        e1 = hwmap.get("ENCODER_%s_A"%ID)
        e2 = hwmap.get("ENCODER_%s_B"%ID)
        e_ticks = hwmap.get("ENCODER_%s_TICKS" %ID)

        self.encoder = MotorEncoder(e1, e2, e_ticks)
        self.motor = RawMotor(m1, m2, True, False)

        self.runmode = Modes.SET_VELOCITY

        pos_pid = PIDs.BasePID("drive_motor_position_pid", ID)
        self.position_pid_threader = PIDs.PIDThread(pos_pid, self.get_state_position_pid, self.motor.drive_motor_raw)

        vel_pid = PIDs.AutoDerivativePID("drive_motor_velocity_pid", ID)
        self.velocity_pid_threader = PIDs.PIDThread(vel_pid, self.get_state_velocity_pid, self.motor.drive_motor_raw)
        self.desired_position = 0
        self.desired_velocity = 0
        self.desired_acceleration = 0

    def get_state_position_pid(self):
        pos_error = self.desired_position - self.encoder.position
        vel_error = self.desired_velocity - self.encoder.velocity
        return pos_error, vel_error, self.desired_velocity

    def get_state_velocity_pid(self):
        vel_error = self.desired_velocity - self.encoder.velocity

        return vel_error, self.desired_acceleration

    def set_velocity(self, vel, accel=0):
        if not self.runmode == Modes.SET_VELOCITY:
            self.position_pid_threader.kill()
            self.velocity_pid_threader.start_thread()
        self.velocity_pid_threader.touch()
        self.desired_velocity = vel
        self.desired_acceleration = accel

    def set_target_position(self, pos, vel=0):
        if not self.runmode == Modes.SET_POSITION:
            self.velocity_pid_threader.kill()
            self.position_pid_threader.start()
        self.position_pid_threader.touch()
        self.desired_position = pos
        self.desired_velocity = vel

    def active_stop(self):
        if not self.runmode == Modes.ACTIVE_BREAKING:
            self.velocity_pid_threader.kill()
            self.position_pid_threader.kill()
        self.motor.breaking(True)
        self.motor.drive_motor_raw(0)

    def coasting_stop(self):
        if not self.runmode == Modes.ACTIVE_BREAKING:
            self.velocity_pid_threader.kill()
            self.position_pid_threader.kill()
        self.motor.breaking(False)
        self.motor.drive_motor_raw(0)
