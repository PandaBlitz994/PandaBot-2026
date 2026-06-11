from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon
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
timer = StopWatch()
chassis = DriveBase(left_wheel, right_wheel, 62.4, 81)
chassis.use_gyro(True)


def get_time():
    """Returns the time since the timer was last reset in seconds."""
    return timer.time() / 1000  # Return time in seconds


def reset_drive_settings():
    """resets to the default speed, acceleration and turn rate"""
    chassis.settings(
        straight_speed=500,
        straight_acceleration=500,
        turn_rate=150,
        turn_acceleration=750,
    )


def reset():
    """restets the gyro angle, drive settings"""
    hub.imu.reset_heading(0)
    reset_drive_settings()


# reflection color
WHITE = Color(h=0, s=0, v=100)
RED = Color(h=352, s=92, v=75)
BLUE = Color(h=218, s=94, v=72)
GREEN = Color(h=155, s=78, v=48)
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


def brakepoint():
    while True:
        if Button.BLUETOOTH in hub.buttons.pressed():
            break
        pass
    wait(500)

def check_battery_percent():
    v = hub.battery.voltage()  # Read battery voltage (mV)
    percent = int((v - 7000) * 100 // 1200)  # Convert voltage to percentage
    return percent


def check_run_color():
    print(
        "run sensor hsv:",
        run_color_sensor.hsv(),
        "run sensor color:",
        run_color_sensor.color(),
        "run sensor reflection:",
        run_color_sensor.reflection(),
    )


def wheels_cleaning():
    chassis.use_gyro(False)
    chassis.drive(speed=1000, turn_rate=0)
    while True:
        hub.display.number(check_battery_percent())
        wait(500)

# TODO: rewrite breakpoint function


def drive_untill_black(speed, turn_rate):
    chassis.drive(speed, turn_rate)
    while floor_color_sensor.reflection() > 13:
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


def straight_time(speed, time, turn_rate=0):
    """speed: Number, mm/s
    time: Number, ms
    """
    chassis.use_gyro(False)
    chassis.drive(speed, turn_rate)
    wait(time)
    chassis.stop()
    chassis.use_gyro(True)


def turn_to(angle):
    start_angle = (hub.imu.heading() + 360) % 360
    deg_to_turn = (angle - start_angle) % 360
    if deg_to_turn >= 180:
        chassis.turn(deg_to_turn - 360)
    else:
        chassis.turn(deg_to_turn)


def white_run():
    # setup
    reset()
    right_arm.run_time(speed=1000, time=1000, wait=None)  # making shure the arm is down
    left_arm.run_until_stalled(-1000)  # reseting the arm
    left_arm.run_angle(speed=700, rotation_angle=150, wait=None)
    # going to the brush
    chassis.straight(670)
    chassis.straight(-170)
    chassis.straight(75)
    left_arm.run_time(700, 1500)  # pulling the brush
    # going to MO2
    chassis.turn(30)
    chassis.straight(150.003864)
    turn_to(-35)
    chassis.use_gyro(False)
    straight_time(speed=400, time=3000)  # revealing the map
    chassis.use_gyro(True)
    # returning home and placing a flag
    chassis.straight(-125)
    turn_to(0)
    right_arm.run_time(speed=-1000, time=2000)  # placing the flag
    chassis.straight(-500, then=Stop.NONE)
    chassis.curve(radius=-300, angle=-45)


def black_run():
    # setup
    reset()
    chassis.settings(straight_acceleration=1000)
    left_arm.run_time(speed=1000, time=1000, wait=None)  # reseting elevator
    right_arm.run_time(speed=-1000, time=1000, wait=None)  # reseting the other arm

    # getting there
    chassis.straight(500, then=Stop.NONE)
    chassis.curve(radius=450, angle=45)
    right_arm.run_time(speed=1000, time=1000, wait=None)  # lowering the arm
    right_wheel_gyro(speed=150, gyro=0)
    straight_time(speed=500, time=1000)  # making shur we are at the right place

    # doing the missions
    right_arm.run_time(speed=-1000, time=5000, wait=None)  # transferring the minecart
    left_arm.run_time(speed=-500, time=2000)
    hub.display.icon(Icon.TRUE)
    left_arm.run_time(speed=300, time=2500, wait=None)  # collecting the high vlue item
    hub.display.icon(Icon.TRUE)
    wait(1000)
    hub.display.icon(Icon.HAPPY)
    wait(1500)

    # returning home
    chassis.straight(-50, then=Stop.NONE)
    chassis.curve(radius=-100, angle=-45)
    chassis.curve(radius=-300, angle=45, then=Stop.NONE)
    chassis.curve(radius=-300, angle=-70, then=Stop.NONE)
    chassis.straight(-200)


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
    chassis.straight(-270)
    # tiping the scales
    right_arm.run_time(speed=-1000, time=2000)
    right_arm.run_time(speed=1000, time=2000)
    # driving to what's on sale
    chassis.straight(-410)
    chassis.turn(45)
    # discovering what's on sale
    right_arm.run_time(speed=-1000, time=1000, wait=None)
    chassis.settings(300)
    chassis.straight(260)
    right_arm.run_time(speed=1000, time=3000, wait=None)
    left_arm.run_until_stalled(500)
    chassis.settings(100)
    chassis.straight(-30, then=Stop.NONE)
    reset_drive_settings()
    chassis.straight(-200)
    chassis.straight(80)
    left_arm.run_time(speed=-1000, time=2000, wait=None)
    # returning home and pushing vrum-vrum
    turn_to(90)
    straight_time(speed=-500, time=2500)
    right_arm.run_time(speed=-1000, time=2000, wait=None)
    right_wheel_gyro(speed=500, gyro=50)
    straight_time(speed=-500, time=2000)
    chassis.straight(30)
    right_arm.run_time(speed=1000, time=2000, wait=None)
    right_wheel.run_angle(speed=-500, rotation_angle=500)


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
        straight_time(speed=250, time=2500)
        # mission 3 - who lived here?
        left_arm.run_time(speed=1200, time=1500)
        left_arm.run_time(speed=-1200, time=1000)
        # back home
        chassis.settings(straight_speed=1000)
        chassis.straight(-1000)


def orange_run():
    # setup
    reset()
    right_arm.run_time(speed=-1000, time=500, wait=None)  # reseting the arm
    left_arm.run_time(speed=1000, time=500, wait=None)  # reseting the arm

    # driving to the missions
    straight_time(speed=300, time=2500, turn_rate=5)
    wait(500)

    right_arm.run_time(speed=500, time=1800, wait=None)  # lowering the arm
    left_arm.run_time(speed=-500, time=1800, wait=None)  # lowering the arm
    chassis.straight(-30)
    wait(500)
    # fishing stuff
    # right_arm.run_time(speed=500, time=1500, wait=None)  # lowering the arm
    # left_arm.run_time(speed=-500, time=1500)  # lowering the arm

    right_arm.run_time(speed=-1000, time=2500, wait=None)  # spining the arm
    left_arm.run_time(speed=-1000, time=2500, wait=None)  # spinning the arm

    straight_time(speed=500, time=2000)

    right_arm.run_time(speed=-1000, time=1200, wait=None)  # spining the arm
    left_arm.run_time(speed=-1000, time=1200)  # spinning the arm

    # returning home
    right_arm.run_time(speed=-1000, time=6000, wait=None)  # lifting the arm
    left_arm.run_time(speed=1000, time=6000, wait=None)  # lifting the arm
    chassis.straight(-650)


def green_run(): #matcha
    # setup
    reset()
    left_arm.run_time(speed=-500, time=1500, wait=None)
    right_arm.run_time(speed=500, time=1500, wait=None)
    # drive to flag
    chassis.straight(distance=130, then=Stop.NONE)
    chassis.curve(radius=200, angle=-30)
    chassis.straight(distance=340, then=Stop.NONE)
    chassis.curve(radius=300, angle=-60)
    #drop flag
    chassis.straight(distance=150)
    right_arm.run_time(speed=-100, time=3000)
    chassis.straight(distance=100) 
    right_arm.run_time(speed=200, time=3000,wait=None)
    wait(1500)

    # go to forum
    chassis.straight(distance=400) 
    chassis.turn(-48)
    chassis.straight(distance=140)
    left_arm.run_time(speed=500, time=1500) # lowering the whale
    chassis.straight(distance=50)
    left_arm.run_time(speed=1000, time=1200, wait=None) # lifting the whale
    chassis.straight(distance=-130)
    left_arm.run_time(speed=-800, time=2500) # lifting the whale
    chassis.turn(-10)
    chassis.straight(distance=200)
    chassis.straight(distance=-300)
    



    # party time!!!
    

def run_none():
    while True:
        pressed = hub.buttons.pressed()
        if pressed:
            break

    if Button.BLUETOOTH in pressed:
        right_wheel.stop(Stop.COAST)
        left_wheel.stop(Stop.COAST)
        while True:            
            pass

    else:
        wheels_cleaning()


runs = [
    (BLACK, black_run, 1, "black run"),
    (WHITE, white_run, 2, "white run"),
    (ORANGE, orange_run, 3, "orange run"),
    (YELLOW, yellow_run, 4, "yellow run"),
    (BLUE, blue_run, 56, "blue+vroom vroom contingency"),
    (GREEN, green_run, 7, "matcha run"),
    (NO_COLOR, run_none, 0, "run straight"),
]  # for each run: attachment color, run function, run number (for display)

finished = False
while not finished:
    for run in runs:
        if run_color_sensor.color() == run[0]:
            finished = True
            hub.display.number(run[2])  # Display run number on the matrix (screen)
            hub.light.on(run[0])  # Change the button light color to the run color
            print("BAT_percent:", f"{check_battery_percent()}%")
            timer.reset()
            run[1]()  # Run the run funciton
            break
