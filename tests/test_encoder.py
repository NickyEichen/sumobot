from sumobot.robot_hardware.motor_encoder import MotorEncoder
from time import sleep


pin1 = 31
pin2 = 29
my_encoder = MotorEncoder(pin1, pin2, 1, reverse=False, delta_time=0.050, num_samples=10)

my_encoder.start_sampling_thread()

try:
    while True:
        print(my_encoder.position, my_encoder.velocity, my_encoder.ran)
        sleep(0.1)
finally:
    my_encoder.kill_sampling_thread()
