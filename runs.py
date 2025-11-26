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
def d_settings():
    chassis.settings(300, 500, 150, 750)


def reset():
    hub.imu.reset_heading(0)
    d_settings()


# reflection color
Color.WHITE = Color(h=0, s=0, v=100)
Color.RED = Color(h=352, s=92, v=75)
Color.BLUE = Color(h=217, s=94, v=70)
Color.GREEN = Color(h=96, s=67, v=88)
Color.YELLOW = Color(h=45, s=70, v=100)
Color.BLACK = Color(h=200, s=22, v=17)
Color.ORANGE = Color(h=7, s=86, v=100)
Color.NONE = Color(h=180, s=32, v=7)

run_color.detectable_colors(
    [
        Color.WHITE,
        Color.RED,
        Color.BLUE,
        Color.GREEN,
        Color.YELLOW,
        Color.BLACK,
        Color.ORANGE,
        Color.NONE,
    ]
)


def wheels_cleaning():
    while True:
        chassis.settings(1000, 1000)
        chassis.straight(10000)


def run_1():
    # setup
    chassis.reset()
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


def run_2():
    # setup
    # chassis.setup()
    #
    # chassis.straight(680)
    left_arm.run_angle(500, 80)
    left_arm.run_angle(-500, 80)
    right_arm.run_angle(500, 400)
    right_arm.run_angle(-500, 450)


def run_3():
    # setup
    chassis.settings(500)
    chassis.straight(-600)
    chassis.straight(300)


runs = [
    (Color.WHITE, run_1, 1),
    (Color.YELLOW, run_2, 2),
    (Color.NONE, run_3, 3),
]

ran = False
while not ran:
    for run in runs:
        if run_color.color() == run[0]:
            ran = True
            hub.display.number(run[2])
            hub.light.on(run[0])
            run[1]()
            break
