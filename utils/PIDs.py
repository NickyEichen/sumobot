import json
import time
import threading

class BasePID:

    DEBUG=True

    def __init__(self, name, ID=None, DEBUG=False):
        self.name = name
        self.ID = ID
        self.DEBUG = DEBUG

        with open('json/%s.json'%name) as f:
            parm = json.load(f)

        self.kp = parm.get('kp')
        self.ki = parm.get('ki')
        self.kd = parm.get('kd')
        self.ke = parm.get('ke', 0)
        self.kf = parm.get('kf', 0)

        self.integral = 0

    def update(self, error, derror, feedforward=0, *args):
        val = self.kp*error + self.ki*self.integral + self.kd * derror + self.kf*feedforward
        self.integral = self.integral*self.ke + error

    def debug(self, *args):
        if BasePID.DEBUG and self.DEBUG:
            label = self.name
            if self.ID is not None:
                label += ":" + str(self.ID)
            print(label, *args)


class AutoDerivativePID(BasePID):
    def __init__(self, name, ID=None, DEBUG=False, delta_time=0.050):
        super(AutoDerivativePID, self).__init__( name, ID, DEBUG)

        self.times = []
        self.errors=[]
        self.max_del_t = delta_time

    def update(self, error, feedforward=0, *args):
        i = 0
        t = time.time()
        while t - self.times[i] > self.max_del_t:
            self.times.pop(0);
            self.errors.pop(0)
        if len(self.errors) < 2:
            return 0
        derror = self.slope(self.times, self.errors)

        super(AutoDerivativePID, self).update(error, derror, feedforward)

    @staticmethod
    def slope(x, y):
        xbar = sum(x) / len(x)
        ybar = sum(y) / len(y)

        numerator = sum([(x[i] - xbar) * (y[i] - ybar) for i in range(len(x))])
        denominator = sum([(el - xbar) ** 2 for el in x])
        return numerator / denominator

class PIDThread():

    def __init__(self, PID, fn, frequency, timeout=10):
        self.pid = PID
        self.fn = fn

        self.timeout = timeout

        self.lock = threading.Lock()
        self.target = None
        self.kill = False
        self.frequency = frequency
        self.last_time = 0

    def start_thread(self):
        if not self.kill:
            return
        self.kill = False
        th = threading.Thread(target=self.looper())
        th.start()

    def stop_thread(self):
        self.kill = True

    def looper(self):
        if not self.target:
            while not self.kill and time.time() - self.last_time < self.timeout:
                time.sleep(self.frequency)
        while not self.kill and time.time() - self.last_time < self.timeout:
            with self.lock:
                self.PID.update(self.target)
            time.sleep(self.frequency)
        print("Stopped PID thread: ", self.PID.name, self.PID.ID)

    def update(self, *target):
        self.target = target
