import dynamic_model
import pulseio
import board
import time
import math

dynamic_model.enable_wind = False

rotation_command = pulseio.PulseIn(board.D5)


MIN_INPUT = 1000
MAX_INPUT = 2000

while True:
    if len(rotation_command) == 0:
        time.sleep(0.1)
        continue

    dt = rotation_command.popleft()

    # low time
    if dt > MAX_INPUT:
        continue

    x = (dt - MIN_INPUT) / (MAX_INPUT - MIN_INPUT)
    theta = 2 * math.pi * x

    print(theta)
