from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import hub_menu


# Declaring ports
hub = PrimeHub()
left_wheel = Motor(Port.A, Direction.COUNTERCLOCKWISE)  # Cyan cable
right_wheel = Motor(Port.E)  # Red cable
left_arm = Motor(Port.B)  # Rurple cable
right_arm = Motor(Port.F)  # Blue cable
run_color_sensor = ColorSensor(Port.D)  # Yellow cable
floor_color_sensor = ColorSensor(Port.C)  # Green cable

chassis = DriveBase(left_wheel, right_wheel, 62.4, 81)
chassis.use_gyro(True)

def reset_drive_settings():
    """resets to the default speed, acceleration and turn rate"""
    chassis.settings(straight_speed=500, straight_acceleration=500, turn_rate=150, turn_acceleration=750)

def reset():
    """restets the gyro angle, drive settings"""
    hub.imu.reset_heading(0)
    reset_drive_settings()

# reflection color
WHITE = Color(h=0, s=0, v=100)
RED = Color(h=352, s=92, v=75)
BLUE = Color(h=218, s=94, v=72)
GREEN = Color(h=96, s=67, v=88)
YELLOW = Color(h=40, s=70, v=100)
BLACK = Color(h=200, s=20, v=19)
ORANGE = Color(h=7, s=86, v=99) 
NO_COLOR = Color(h=180, s=32, v=7)
FLOOR_BLACK = Color(h=240, s=100, v=100)

run_color_sensor.detectable_colors(
    [
        WHITE,
        RED,
        BLUE,
        GREEN,
        YELLOW,
        BLACK,
        ORANGE,
        NO_COLOR,
        FLOOR_BLACK,  # this is floor black not magenta
    ]
)


def wheels_cleaning():
    chassis.use_gyro(False)
    while True:
        chassis.settings(1000, 1000)
        chassis.straight(10000)


def breakpoint():
    while not Button.BLUETOOTH in hub.buttons.pressed():
        pass
    wait(250)


def drive_untill_black(speed, turn_rate):
    chassis.drive(speed, turn_rate)
    while floor_color_sensor.reflection() > 11:
        print(floor_color_sensor.reflection())
    chassis.stop()


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
        while int(hub.imu.heading()) < gyro:
            pass
        left_wheel.stop()

    elif current_gyro > gyro:
        left_wheel.run(-speed)
        while int(hub.imu.heading()) > gyro:
            pass
        left_wheel.stop()

def straight_time(speed, time):
    """speed: Number, mm/s
    time: Number, ms
    """
    chassis.drive(speed, 0)
    wait(time)
    chassis.stop()


def turn_to(angle, turn_speed):
    chassis.settings(turn_rate=turn_speed)
    start_angle = (hub.imu.heading() + 360) % 360
    deg_to_turn = (angle - start_angle) % 360
    if deg_to_turn >= 180:
        chassis.turn(deg_to_turn - 360)
    else:
        chassis.turn(deg_to_turn)


def white_run():
    # setup
    reset()
    right_arm.run_time(-1000, 1000, wait=None)
    left_arm.run_time(-1000, 1000)
    left_arm.run_angle(speed=700, rotation_angle=150, wait=None)
    # going to the brush
    chassis.straight(670)
    chassis.straight(-170)
    chassis.straight(75)
    left_arm.run_time(700, 1500)# pulling the brush
    # going to MO2
    chassis.turn(30)
    chassis.straight(170)
    chassis.turn(-75)
    chassis.straight(200)#revealing the map
    # going to MO3
    right_arm.run_time(speed=700, time=1000, wait=None)
    chassis.straight(-40)
    chassis.curve(radius=-300, angle=45)
    chassis.straight(-230)
    left_arm.run_time(-1000, 1000, wait=None)#relesing the brush
    right_arm.run_time(-700, 1000)#doing the mission
    # return home
    chassis.straight(170, then=Stop.NONE)
    chassis.curve(radius=200, angle=-80, then=Stop.NONE)
    chassis.straight(300, then=Stop.NONE)
    chassis.curve(radius=300, angle=45, then=Stop.NONE)
    chassis.straight(200)


def black_run():
    # setup
    reset()
    right_arm.run_time(speed=1000, time=1000, wait=None)
    left_arm.run_time(speed=-1000, time=1000, wait=None)
    # getting there
    chassis.straight(500, then=Stop.NONE)
    chassis.curve(radius=200, angle=90)
    chassis.turn(90)
    # straiting on the wall
    straight_time(speed=-200, time=1500)
    chassis.use_gyro(False)
    hub.imu.reset_heading(180)
    chassis.use_gyro(True)
    # taking the trasure out
    chassis.straight(30)
    chassis.turn(-90)
    chassis.straight(70)
    left_arm.run_time(speed=1000, time=1000)
    chassis.straight(70)
    left_arm.run_time(speed=-1000, time=1000)
    # going to the whale and droping the tresure
    chassis.straight(-120)
    chassis.turn(45)
    chassis.straight(280)
    chassis.turn(60)
    left_arm.run_until_stalled(1000)
    # whale
    turn_to(angle=90, turn_speed=100)
    chassis.straight(130)
    right_arm.run_time(speed=-1000, time=1000)
    chassis.straight(30)
    left_wheel_gyro(speed=200, gyro=45)
    # lifting it
    right_arm.run_time(speed=1000, time=1000)
    right_arm.run_time(speed=1000, time=4000, wait=None)
    chassis.straight(-80)
    chassis.straight(80)
    wait(200)
    # reterning home
    left_wheel_gyro(speed=200, gyro=90)
    chassis.straight(-250, then=Stop.NONE)
    chassis.curve(radius=-200, angle=90)
    chassis.straight(-600)


def yellow_run():
    # setup
    reset()
    right_arm.run_time(speed=1000, time=1000, wait=None)
    left_arm.run_until_stalled(-1000)
    right_arm.run_angle(speed=-1000, rotation_angle=150, wait=None)
    # driving to tip the scales
    chassis.settings(1000)
    chassis.straight(-800)
    reset_drive_settings()
    drive_untill_black(speed=-100, turn_rate=0)
    right_arm.run_time(speed=1000, time=500, wait=None)
    chassis.straight(-280)
    # tiping the scales
    right_arm.run_time(speed=-1000, time=2000)
    right_arm.run_time(speed=1000, time=2000)
    # driving to what's on sale
    chassis.straight(-400)
    chassis.turn(45)
    # discovering what's on sale
    right_arm.run_time(speed=-1000, time=1000, wait=None)
    chassis.straight(240)
    right_arm.run_time(speed=1000, time=2000, wait=None)
    left_arm.run_until_stalled(500)
    chassis.straight(-200)
    left_arm.run_time(speed=-500, time=1000, wait=None)
    chassis.straight(80)
    left_arm.run_until_stalled(-1000)
    # returning home and pushing vrum-vrum
    left_wheel_gyro(speed=100, gyro=90)
    straight_time(speed=-500, time=2500)
    right_arm.run_time(speed=-1000, time=2000, wait=None)
    right_wheel_gyro(speed=500, gyro=50)
    straight_time(speed=-500, time=2000)
    chassis.straight(30)
    chassis.straight(-200)

def blue_run():
    # waiting for a button press
    while True:
        pressed = hub.buttons.pressed()
        if pressed:
            break

    # pushing vrum-vrum car
    if Button.BLUETOOTH in pressed:
        straight_time(-500, 1000)
        chassis.straight(100)
        chassis.use_gyro(False)

    else: 
        # setup
        reset()
        right_arm.run_time(speed=-500, time=1000, wait=None)
        left_arm.run_time(speed=-500, time=1000)
        left_arm.run_angle(speed=200, rotation_angle=170, wait=None)
        # mission 1 - mamgora
        chassis.straight(420)
        for i in range(4):
            right_arm.run_time(speed=500, time=1000)
            right_arm.run_time(speed=-800, time=900)
        # mission 2 - napachia
        straight_time(speed=200, time=2500)
        # mission 3 - who lived here?
        left_arm.run_time(speed=1000, time=1500)
        left_arm.run_time(speed=-1000, time=1000)
        # back home
        chassis.settings(straight_speed=-1000)
        chassis.straight(-1000)


def orange_run():
    reset()
    # the juice
    chassis.straight(650)
    chassis.straight(-30)
    right_arm.run(-700)
    left_arm.run_time(speed=1000, time=1600)
    left_arm.run_time(speed=1000, time=1000, wait=None)
    straight_time(speed=500, time=1000)
    wait(2000)
    # returning home
    left_arm.run_time(speed=-1000, time=2000, wait=None)
    chassis.straight(-650)


reset()

runs = [
    (WHITE, white_run, 1),
    (BLACK, black_run, 2),
    (ORANGE, orange_run, 3),
    (YELLOW, yellow_run, 4),
    (BLUE, blue_run, 56),
    (NO_COLOR, wheels_cleaning, 0),
] # for each run: attachment color, run function, run number (for display)

finished = False
while not finished:
    for run in runs:
        if run_color_sensor.color() == run[0]: 
            finished = True
            hub.display.number(run[2]) # Display run number on the matrix (screen)
            hub.light.on(run[0])  # Change the button light color to the run color
            run[1]() # Run the run funciton
            break
