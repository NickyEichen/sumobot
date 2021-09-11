import RPi.GPIO as GPIO

class Motor:

    def __init__(self, pin1, pin2, breaking, reversed, encoder=None):
        self.pin1 = GPIO.PWM(pin1, 1000)
        self.pin1.start(0)
        self.pin2 = GPIO.PWM(pin2, 1000)
        self.pin2.start(0)

        self.breaking = breaking
        self.direction = reversed

    def drive_motor_raw(self, power):
        direction = (power >= 0) != self.direction
        pwm = abs(power)
        other = int(self.breaking)

        if direction ^ self.breaking:
            #pin 1 PWM, pin 2 other
            self.pin1.changeDutyCycle(pwm)
            self.pin2.changeDutyCycle(other)
        else:
            #pin 2 PWM, pin 1 other
            self.pin1.changeDutyCycle(other)
            self.pin2.changeDutyCycle(pwm)

