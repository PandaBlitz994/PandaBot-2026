from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import hub_menu

# Declaring ports
hub = PrimeHub()
left_wheel = Motor(Port.A, Direction.COUNTERCLOCKWISE)  # Cyan
right_wheel = Motor(Port.E)  # red
left_arm = Motor(Port.B)  # purple
right_arm = Motor(Port.F)  # blue
run_color = ColorSensor(Port.D)  # Yellow
floor_color = ColorSensor(Port.C)  # Green

chassis = DriveBase(left_wheel, right_wheel, 62.4, 81)
chassis.use_gyro(True)


# default:
def default_settings():
    chassis.settings(200, 350, 150, 750)


# reflection color
run_white = Color(h=0, s=0, v=100)
run_red = Color(h=352, s=92, v=75)
run_blue = Color(h=217, s=94, v=70)
run_green = Color(h=96, s=67, v=88)
run_yellow = Color(h=50, s=71, v=100)
run_black = Color(h=200, s=22, v=17)
run_orenge = Color(h=7, s=86, v=100)


def wheels_cleaning():
    while True:
        chassis.settings(1000, 1000)
        chassis.straight(10000)


def run_1():
    # setup
    hub.imu.reset_heading(0)
    chassis.settings(500)
    left_arm.run_time(-700, 1500, wait=None)
    # mission 1
    chassis.straight(700)
    chassis.straight(-200)
    chassis.straight(75)
    left_arm.run_angle(500, 1100)
    # mission 2
    chassis.turn(30)
    chassis.straight(150)
    chassis.turn(-75)
    chassis.straight(200)
    chassis.straight(-230)
    chassis.turn(150)


if run_color.hsv() == run_white:
    hub.display.char("W")
    hub.light.on(Color.WHITE)
    run_1()

# hub.display.char(run_letter)
# hub.light.on(Color.BLUE)
