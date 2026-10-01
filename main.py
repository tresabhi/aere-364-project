import dynamic_model
import pulseio
import board
import time
import math
import adafruit_bno055
import busio

MIN_INPUT = 1000
MAX_INPUT = 2000
RATE = 60  # Hz


dynamic_model.enable_wind = False

rotation_command = pulseio.PulseIn(board.D5)
i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_bno055.BNO055_I2C(i2c)

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

    x = (dt - MIN_INPUT) / (MAX_INPUT - MIN_INPUT)
    desired_theta = 2 * math.pi * x

    print(imu.euler)
