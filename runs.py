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
    chassis.settings(500, 500, 150, 750)


def reset():
    hub.imu.reset_heading(0)
    d_settings()


reset()


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


def straight_until_black():
    chassis.drive(200, 0)
    while True:
        if floor_color.color() == Color(h=0, s=0, v=-40):
            chassis.stop()
            break


def right_wheel_gyro(gyro):
    while int(hub.imu.heading()) != gyro:
        if hub.imu.heading() > gyro:
            right_wheel.run_angle(500, 1, wait=False)
        elif hub.imu.heading() < -gyro:
            right_wheel.run_angle(-500, 1, wait=False)
        else:
            right_wheel.stop()


def run_1():
    # setup
    reset()
    left_arm.run_time(-700, 1000, wait=None)
    right_arm.run_time(-700, 1000, wait=None)
    # mission 1
    chassis.straight(670)
    chassis.straight(-170)
    chassis.straight(75)
    left_arm.run_time(700, 1500)
    # mission 2
    chassis.turn(30)
    chassis.straight(170)
    chassis.turn(-75)
    chassis.straight(200)
    # mission 3
    right_arm.run_time(speed=700, time=1500, wait=None)
    chassis.straight(-40)
    chassis.curve(radius=-300, angle=45)
    chassis.straight(-230)
    right_arm.run_time(speed=-400, time=1500)
    # return home
    chassis.straight(170, then=Stop.NONE)
    chassis.curve(radius=200, angle=-80, then=Stop.NONE)
    chassis.straight(300, then=Stop.NONE)
    chassis.curve(radius=300, angle=45, then=Stop.NONE)
    chassis.straight(200)


def run_2():
    # setup
    reset()
    # pushing & pulling ship
    right_arm.run_time(750, 1000, wait=None)
    chassis.straight(580)
    right_arm.run_time(-750, 1500)
    chassis.straight(-90)
    right_arm.run_time(750, 1500)
    chassis.straight(250)
    chassis.straight(-50.67)
    # moving to the diging
    chassis.turn(-30)
    chassis.straight(170)
    chassis.turn(30)
    # chassis.straight(4)
    # pulling the diging
    right_arm.run_time(-800, 1500)
    for i in range(0, 4):
        right_wheel.run_angle(480, 70)
        right_wheel_gyro(0)

    right_arm.run_time(750, 1200)
    chassis.turn(-25)
    right_arm.run_time(-790, 800)
    chassis.straight(40)
    # moving
    chassis.turn(23)
    chassis.straight(173)
    right_arm.run_time(-790, 800)


def run_3():
    # setup
    reset()
    # pushing vrum-vrum car
    chassis.straight(-600)
    chassis.straight(300)


def run_4():
    # setup
    reset()
    right_arm.run_time(speed=-500, time=1000, wait=None)
    left_arm.run_time(speed=-700, time=1000, wait=None)

    # mission 1
    chassis.straight(420)
    # 1
    right_arm.run_angle(speed=800, rotation_angle=100)
    right_arm.run_angle(speed=500, rotation_angle=-90)
    # 2
    right_arm.run_angle(speed=800, rotation_angle=100)
    right_arm.run_angle(speed=500, rotation_angle=-90)
    # 3
    right_arm.run_angle(speed=800, rotation_angle=100)
    right_arm.run_angle(speed=500, rotation_angle=-90)
    # 4
    right_arm.run_angle(speed=800, rotation_angle=100)
    right_arm.run_angle(speed=500, rotation_angle=-90)
    # mission 2
    straight_until_black()
    # mission 3
    left_arm.run_time(speed=700, time=1500)
    # mission 4
    chassis.turn(45)
    chassis.straight(-300)


def run_blueHome():
    reset()
    chassis.straight(2500)


runs = [
    (Color.WHITE, run_1, 1),
    (Color.YELLOW, run_2, 2),
    (Color.NONE, run_3, 3),
    (Color.BLUE, run_4, 4),
    (Color.BLACK, run_blueHome, 5),
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
