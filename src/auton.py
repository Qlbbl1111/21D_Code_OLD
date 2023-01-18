from vex import *
from main import *

def auton_run():
    #spin roller and back away
    Intake.set_velocity(100, PERCENT)
    Intake.spin(REVERSE)
    drivetrain.drive_for(FORWARD, 200, MM)
    wait(0.5,SECONDS)
    Intake.stop()
    drivetrain.drive_for(REVERSE, 100, MM)
    return