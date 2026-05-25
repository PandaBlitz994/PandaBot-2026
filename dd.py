from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import XboxController
# Import required MicroPython libraries.
from usys import stdin
from uselect import poll

hub = PrimeHub()
left_wheel = Motor(Port.A, Direction.COUNTERCLOCKWISE)  # purple
right_wheel = Motor(Port.E, Direction.CLOCKWISE)  # red

left_motor = Motor(Port.F, gears=[20, 28])  # yellow
right_motor = Motor(Port.D, gears=[20, 28])  # blue

sensor = ColorSensor(Port.C)  # green
sensor2 = ColorSensor(Port.B)  # cyan


cutie = DriveBase(left_wheel, right_wheel, wheel_diameter=62.4, axle_track=80)

dd = XboxController()


# Register the standard input so we can read keyboard presses.
keyboard = poll()
keyboard.register(stdin)

while True:
    # Check if a key has been pressed.
    if keyboard.poll(0):

        # Read the key and print it.
        key = stdin.read(1)
        print("You pressed:", key)