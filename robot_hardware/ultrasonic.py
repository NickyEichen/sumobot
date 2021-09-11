import RPi.GPIO as GPIO
import time
import threading



class Ultrasonic:
    def __init__(self, echo_pin, trigger_pin, max_dist, update_frequency=0.050, timeout=10):
        self.echo = echo_pin
        self.trig = trigger_pin
        self.max_dist = max_dist

        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trig, GPIO.OUT)

        self.last_reading = float('Inf')
        self.kill = True
        self.speed_sound = 34300 # cm/s

        self.update_freq = update_frequency

        self.thread = threading.Thread(target=self.get_reading)

        self.timeout = self.timeout
        self.last_write = time.time()
        self.last_read = time.time()

    def update_cycle(self):
        while (not self.kill) and time.time() - self.last_read < self.timeout:
            self.last_reading = self.get_reading()
            self.last_reading = time.time()
            time.sleep(self.update_freq)

    def start_collection(self):
        if self.kill == False: # Prevent from starting two collection threads
            return
        self.kill = False
        self.thread.start()

    def stop_collection(self):
        self.kill = True

    @property
    def distance(self):
        self.last_read = time.time()
        return self.last_reading

    def get_reading(self):
        GPIO.output(self.trig, 0)
        time.sleep(0.000002)
        GPIO.output(self.trig, 1)
        time.sleep(0.000010)
        GPIO.output(self.trig, 0)
        time.sleep(0.000002)

        # wait for echo reading
        if GPIO.input(self.echo):
            GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=self.update_freq/2-3)
        if GPIO.input(self.echo):
            # It was timed out - failed reading
            return float("Inf")
        start = time.time()
        GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=self.update_freq/2-3)
        if not GPIO.input(self.echo):
            # It was timed out - failed reading
            return float("Inf")

        feedback = time.time()

        if feedback == start:
            return float("Inf")
        else:
            return (feedback - start) * self.speed_sound / 2