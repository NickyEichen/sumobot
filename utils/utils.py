
##### PhotoSensors


"""# create an analog input channel on pin 0
light_sensors = [AnalogIn(mcp, x) for x in [MCP.P0, MCP.P1, MCP.P2, MCP.P3]]
light_lows = [0, 0, 0, 0]
light_highs = [3.3, 3.3, 3.3, 3.3]

def read_light_raw(index):
    return float(light_sensors[index].value)

def set_light_low(index):
    light_lows[index] = read_light_raw(index)

def set_light_high(index):
    light_highs[index] = red_light_raw(index)

def read_light(index):
    val = (read_light_raw(index) - light_lows(index)) / (light_highs[index] - light_lows[index])
    return minmax(val)
"""

"""##### MOTORS
# Set Sleep pin high
def drive_motor(power, breaking, pin1, pin2):
    direction = (power >= 0)
    pwm = math.abs(power) * 255
    other = int(breaking)

    if direction ^ breaking:
        #pin 1 PWM, pin 2 other
"""
