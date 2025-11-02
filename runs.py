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
DriveBase.settings(chassis, 200)

# default:
d_settings = chassis.settings(200, 750, 150, 750)

# reflection color
run_white = Color(h=0, s=0, v=100)
run_red = Color(h=352, s=91, v=67)
run_blue = Color(h=218, s=92, v=69)
run_green = Color(h=154, s=82, v=49)
run_yellow = Color(h=51, s=73, v=99)
run_orrange = Color(h=7, s=85, v=98)

chassis.settings(400)

chassis.straight(650)
chassis.straight(-100)
