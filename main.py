import dynamic_model
import pulseio
import board
import time
import math
import adafruit_bno055
import busio
import pwmio

MIN_INPUT = 1
MAX_INPUT = 2
DEFAULT_INPUT = (MIN_INPUT + MAX_INPUT) / 2
FREQUENCY = 40
RATE = 60  # Hz
PWM_MAX = 65536

dynamic_model.enable_wind = False


def to_duty_cycle(input_s):
    return input_s * PWM_MAX * FREQUENCY * 1e-3


rotation_command = pulseio.PulseIn(board.D5)
i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_bno055.BNO055_I2C(i2c)
left_motor = pwmio.PWMOut(
    board.D9, frequency=40, duty_cycle=to_duty_cycle(DEFAULT_INPUT)
)
right_motor = pwmio.PWMOut(
    board.D10, frequency=40, duty_cycle=to_duty_cycle(DEFAULT_INPUT)
)

print("Waiting for IMU to calibrate...")
while not imu.calibrated:
    time.sleep(0.1)

print("IMU calibrated")

while True:
    time.sleep(1 / RATE)

    if len(rotation_command) == 0:
        continue

    dt = rotation_command.popleft()

    # low time
    if dt > MAX_INPUT:
        continue

    x = (dt / 1000 - MIN_INPUT) / (MAX_INPUT - MIN_INPUT)
    desired_theta = 2 * math.pi * x

    print(imu.euler)
