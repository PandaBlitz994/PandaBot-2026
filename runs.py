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
Color.MAGENTA = Color(h=240, s=100, v=100)#this is floor black not magenta

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
        Color.MAGENTA#this is floor black not magenta
    ]
)


def wheels_cleaning():
    chassis.use_gyro(False)
    while True:
        chassis.settings(1000, 1000)
        chassis.straight(10000)

def till_black(speed, turn_rate):
    chassis.drive(speed, turn_rate)
    while floor_color.reflection() > 11:
        print(floor_color.reflection())
    chassis.stop()

# def straight_until_black(speed):
#     chassis.drive(speed, 0)
#     while True:
#         print(floor_color.color())
#         if floor_color.color() == Color.MAGENTA:#this is floor black not magenta
#             chassis.stop()
#             break


def right_wheel_gyro(speed, gyro):
    current_gyro = int(hub.imu.heading())
    if current_gyro <= gyro:
        right_wheel.run(-speed)
        while True:
            if int(hub.imu.heading()) >= gyro:
                right_wheel.stop()
                break

    elif current_gyro > gyro:
        right_wheel.run(speed)
        while True:
            if int(hub.imu.heading()) <= gyro:
                right_wheel.stop()
                break


def left_wheel_gyro(speed, gyro):
    current_gyro = int(hub.imu.heading())
    if current_gyro <= gyro:
        left_wheel.run(speed)
        while True:
            if int(hub.imu.heading()) >= gyro:
                left_wheel.stop()
                break

    elif current_gyro > gyro:
        left_wheel.run(-speed)
        while True:
            if int(hub.imu.heading()) <= gyro:
                left_wheel.stop()
                break
        
def straight_time(speed, time):
    chassis.drive(speed, 0)
    wait(time)
    chassis.stop

def turn_to(angle, turn_speed):
    chassis.settings(turn_rate=turn_speed)
    start_angle = (hub.imu.heading() + 360) % 360
    deg_to_turn = (angle - start_angle) % 360
    if deg_to_turn >= 180:
        chassis.turn(deg_to_turn - 360)
    else:
        chassis.turn(deg_to_turn)



def run_1():
    # setup
    reset()
    right_arm.run_time(-1000, 1000, wait=None)
    left_arm.run_time(-1000, 1000)
    left_arm.run_angle(speed=700, rotation_angle=150, wait=None)
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
    right_arm.run_time(speed=700, time=1000, wait=None)
    chassis.straight(-40)
    chassis.curve(radius=-300, angle=45)
    chassis.straight(-230)
    right_arm.run_time(-700, 1000)
    # return home
    chassis.straight(170, then=Stop.NONE)
    chassis.curve(radius=200, angle=-80, then=Stop.NONE)
    chassis.straight(300, then=Stop.NONE)
    chassis.curve(radius=300, angle=45, then=Stop.NONE)
    chassis.straight(200)


def run_2():
    # setup
    reset()
    left_arm.run_time(speed=400, time=1000, wait=None)
    right_arm.run_time(speed=1000, time=1500)
    # mission 1
    chassis.straight(560)
    chassis.settings(1000)
    chassis.straight(160)
    d_settings
    # mission 2
    chassis.straight(-70)
    chassis.turn(-30)
    chassis.straight(160)
    chassis.turn(30)
    till_black(speed=100, turn_rate=0)
    chassis.straight(-50)
    right_arm.run_time(speed=-1000, time=1500)
    # right_arm.run_angle(speed=1000, rotation_angle=150)  
    wait(100)
    left_wheel.hold()
    for i in range(4):
        right_wheel.run_angle(speed=1000, rotation_angle=60)
        right_wheel_gyro(speed=100, gyro=0)
        # chassis.straight(-10)
    # mission 3_4
    right_arm.run_time(speed=1000, time=1500)
    # right_arm.run_angle(speed=-1000, rotation_angle=150)
    turn_to(angle=0, turn_speed=50)
    chassis.straight(-30)
    wait(100)
    till_black(speed=100, turn_rate=0)
    wait(100)
    chassis.straight(100)
    # right_arm.run_time(speed=-1000, time=2000, wait=None)
    left_arm.run_time(speed=-400, time=1500)
    left_arm.run_time(speed=400, time=2000)
    left_arm.run_time(speed=500, time=3000, wait=None)
    chassis.straight(90)
    right_wheel.run_angle(speed=500, rotation_angle=40)
    right_arm.run_time(speed=-1000, time=2000)
    right_wheel.run_angle(speed=-500, rotation_angle=40)
    # returning home
    chassis.straight(500, then=Stop.NONE)
    chassis.curve(radius=300, angle=45, then=Stop.NONE)

    # left_arm.run_time(400,1000, wait=None)
    # right_arm.run_time(750,800)
    # right_arm.run_time(-750,1200)
    # moving
    #chassis.turn(26)
    #right_arm.run_time(-790, 800)
    #chassis.straight(20)
    #right_arm.run_time(790, 800)
    

def run_3_4():
    while True:
        pressed = hub.buttons.pressed()
        if Button.RIGHT in pressed or  Button.LEFT in pressed or Button.BLUETOOTH in pressed:
            break
        
    if Button.BLUETOOTH in pressed:
        # run_3
        # pushing vrum-vrum car
        straight_time(-500, 1000)
        chassis.straight(150)
        chassis.use_gyro(False)

    # run switching
    while True:
        pressed = hub.buttons.pressed()
        if Button.RIGHT in pressed or Button.LEFT in pressed:
            chassis.use_gyro(True)
            break

    # run_4
    # setup
    reset()
    right_arm.run_time(speed=-500, time=1000, wait=None)
    left_arm.run_time(speed=-500, time=1000)
    left_arm.run_angle(speed=200, rotation_angle=170, wait=None)
    # mission 1
    chassis.straight(420)
    for i in range(4):
        right_arm.run_time(speed=500, time=1000)
        right_arm.run_time(speed=-800, time=900)
    # mission 2
    till_black(speed=200, turn_rate=0)
    # mission 3
    left_arm.run_time(speed=1000, time=1500)
    # mission 4
    left_arm.run_angle(speed=-1000, rotation_angle=200)
    chassis.turn(90)
    chassis.straight(-420)
    left_arm.run_time(speed=-500, time=1000, wait=None)
    chassis.turn(-135)
    straight_time(speed=-300, time=650)
    # returning home
    chassis.straight(30)
    chassis.curve(radius=-250, angle=45, then=Stop.NONE)
    chassis.straight(-30)
    chassis.turn(90)
    chassis.straight(-400, then=Stop.NONE)
    # right_wheel_gyro(speed=-300, gyro=0)
    # right_arm.run_time(speed=300, time=1500, wait=None)
    # chassis.straight(-300)
    chassis.curve(radius=-300, angle=30, then=Stop.NONE)
    chassis.straight(-300)

def run_5():
    # setup
    reset()
    left_arm.run_time(speed=-1000, time=1000, wait=None)
    right_arm.run_time(speed=-1000, time=1000, wait=None)
    # getting there
    chassis.straight(500, then=Stop.NONE)
    chassis.curve(radius=200, angle=90)
    chassis.straight(20)
    chassis.turn(90)
    # mission 1
    straight_time(speed=-200, time=1500)
    chassis.use_gyro(False)
    hub.imu.reset_heading(180)
    chassis.use_gyro(True)
    chassis.settings(straight_speed=50)
    chassis.straight(30)
    d_settings()
    turn_to(angle=90, turn_speed=50)
    till_black(speed=50, turn_rate=0)
    chassis.straight(20)
    left_arm.run_time(speed=500, time=1500)
    # mission 2
    chassis.straight(-120)
    chassis.turn(45)
    chassis.straight(340)
    chassis.turn(60)
    left_arm.run_until_stalled(-1000)
    # mission 3
    turn_to(angle=90, turn_speed=100)
    right_arm.run_time(speed=1000, time=1000)
    chassis.straight(60)
    chassis.turn(-45)
    right_arm.run_time(speed=-500, time=1000, wait=None)
    chassis.settings(100)
    chassis.straight(100)
    wait(500)
    d_settings()
    # returning home
    turn_to(angle=90, turn_speed=200)
    chassis.straight(-250, then=Stop.NONE)
    chassis.curve(radius=-200, angle=90)
    chassis.straight(-600)



runs = [
    (Color.WHITE, run_1, 1),
    (Color.YELLOW, run_2, 3),
    (Color.BLUE, run_3_4, 34),
    (Color.GREEN, run_5, 2),
    (Color.NONE, wheels_cleaning, 0),
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