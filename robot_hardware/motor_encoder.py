import threading

import Encoder
import time
import math


class MotorEncoder:

    def __init__(self, pin_1, pin_2, ticks_per_rev, reverse=False, delta_time=0.05, num_samples=10, timeout=10):
        self.reverse = reverse
        self.enc = Encoder.Encoder(pin_1, pin_2)
        self.ticks_per_rev = ticks_per_rev

        self.max_del_t = delta_time
        self.times = []
        self.readings = []
        self.lock = threading.Lock()

        self.target_samples = num_samples
        self.live_thread = False
        self.timeout = timeout
        self.ran = False

    def start_sampling_thread(self):
        self.last_time = time.time()
        if self.live_thread:
            return
        self.live_thread = True
        th = threading.Thread(target=self.sampling_thread)
        th.start()

    def kill_sampling_thread(self):
        self.live_thread = False

    def sampling_thread(self):
        print("Sampling thread is running")
        self.ran = True
        while self.live_thread and time.time() - self.last_time < self.timeout:
            self.record_reading(self.get_reading())
            time.sleep(self.max_del_t/self.target_samples)
        print("Motor encoder thread stopped")

    def set_direction(self, is_forward):
        self.reverse = not is_forward

    def get_reading(self):
        n = self.enc.read()
        dir = 1 - 2*self.reverse
        return n/self.ticks_per_rev * 2*math.pi *dir # returns in radians

    def record_reading(self, reading):
        with self.lock:
            print(self.times, self.readings)
            self.readings.append(reading)
            self.times.append(time.time())
        self.purge_readings()

    def purge_readings(self):
        with self.lock:
            if len(self.times) == 0:
                return
            i = 0
            t = time.time()
            while t - self.times[i] > self.max_del_t:
                self.times.pop(0);
                self.readings.pop(0)

    @property
    def position(self):
        self.last_time = time.time()
        pos = self.get_reading()
        if not self.live_thread:
            self.record_reading(pos)
        return pos

    @property
    def velocity(self):
        self.last_time = time.time()
        self.purge_readings()
        with self.lock:
            if len(self.readings) < 2:
                return 0
            return self.slope(self.times, self.readings)

    @staticmethod
    def slope(x, y):
        xbar = sum(x) / len(x)
        ybar = sum(y) / len(y)

        numerator = sum([(x[i] - xbar)*(y[i] - ybar) for i in range(len(x))])
        denominator = sum([(el - xbar)**2 for el in x])
        return numerator / denominator