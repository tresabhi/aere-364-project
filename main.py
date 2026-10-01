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
LOOP_RATE = 60  # Hz
PWM_MAX = 65536

dynamic_model.enable_wind = False


def to_duty_cycle(input_ms):
    return input_ms * PWM_MAX * FREQUENCY * 1e-3


rotation_command = pulseio.PulseIn(board.D5)
i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_bno055.BNO055_I2C(i2c)
left_motor = pwmio.PWMOut(
    board.D9, frequency=40, duty_cycle=to_duty_cycle(DEFAULT_INPUT)
)
right_motor = pwmio.PWMOut(
    board.D10, frequency=40, duty_cycle=to_duty_cycle(DEFAULT_INPUT)
)


# -1 = max left, 0 = stop, 1 = max right
def power(input):
    left_motor.duty_cycle = to_duty_cycle(1.5 - input / 2)
    right_motor.duty_cycle = to_duty_cycle(1.5 + input / 2)


def to_rad(deg):
    return deg * math.pi / 180


def normalize_angle(rad):
    return (rad + 2 * math.pi) % (2 * math.pi)


print("Waiting for IMU to calibrate...")
while not imu.calibrated:
    time.sleep(0.1)

print("IMU calibrated")

while True:
    time.sleep(1 / LOOP_RATE)

    if len(rotation_command) == 0:
        continue

    dt = rotation_command.popleft() * 1e-3

    # low time
    if dt > MAX_INPUT:
        continue

    x = (dt - MIN_INPUT) / (MAX_INPUT - MIN_INPUT)
    desired_theta = normalize_angle(2 * math.pi * x)

    current_theta = normalize_angle(to_rad(-imu.euler[0]))
    delta_theta = math.pi - normalize_angle(desired_theta + math.pi - current_theta)

    power(delta_theta / math.pi / 10)
