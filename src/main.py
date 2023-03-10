#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot port configuration code
left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False)
right_motor_b = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)

drivetrain_inertial = Inertial(Ports.PORT16)
digital_out_a = DigitalOut(brain.three_wire_port.a)
digital_out_b = DigitalOut(brain.three_wire_port.b)
Flywheel_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
Flywheel_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
Flywheel = MotorGroup(Flywheel_motor_a, Flywheel_motor_b)
Intake = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
Indexer = Motor(Ports.PORT21, GearSetting.RATIO_6_1, True)
controller_1 = Controller(PRIMARY)


def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

def curve(left, right):
    #ajustment factors
    t=5
    #dead zone set to zero
    if left <= 5 and left >= -5:
        left = 0
    if right <= 5 and right >= -5:
        right = 0
    #curve to graph: https://www.desmos.com/calculator/roc1otanrb
    new_left =  (math.exp(-(t/10))+math.exp((abs(left)-100)/10)*(1-math.exp(-(t/10))))*left
    new_right = (math.exp(-(t/10))+math.exp((abs(right)-100)/10)*(1-math.exp(-(t/10))))*right
    return(int(new_left),int(new_right))
    
# wait for rotation sensor to fully initialize
wait(30, MSEC)

# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drive_input = curve(controller_1.axis3.position(), controller_1.axis2.position())
            drivetrain_left_side_speed = drive_input[0]
            drivetrain_right_side_speed = drive_input[1]
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:      1/9/23
#	Description:  21D code general
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
#Vars
latch = False
toggle = False
latch2 = False
toggle2 = False
latch3 = False
toggle2 = False
a_toggle = False
shift = False

#Set
Intake.set_velocity(85, PERCENT)
Intake.set_stopping(COAST)
drivetrain.set_drive_velocity(100, PERCENT)
drivetrain.set_stopping(BRAKE)
Flywheel.set_stopping(COAST)
Indexer.set_max_torque(100, PERCENT)
Indexer.set_position(0, DEGREES)
digital_out_a.set(True)


def autonomous():
    controller_1.screen.print("Auton Start")
    drivetrain.drive_for(FORWARD, 200, MM)
    Intake.spin(REVERSE)
    wait(1,SECONDS)
    drivetrain.drive_for(REVERSE, 150, MM)
    wait(1,SECONDS)
    Intake.stop()
    return

def driver_control():
    controller_1.screen.clear_screen()
    controller_1.screen.print("Drive Start")
    return

competition = Competition(driver_control, autonomous)

#loop
while True:
    
    #shift
    if controller_1.buttonR1.pressing():
        shift = True
    else:
        shift = False

    #endgame
    if controller_1.buttonA.pressing() and shift == True:
        digital_out_a.set(False)
    else:
         digital_out_a.set(True)


    #indexer
    if controller_1.buttonL1.pressing() and shift == False:
        Indexer.set_velocity(100, PERCENT)
        Indexer.spin_for(FORWARD, 370, DEGREES, wait=False)
        wait(0.25, SECONDS)
        Indexer.stop()
    elif controller_1.buttonL1.pressing() and shift == True:
        Indexer.set_velocity(100, PERCENT)
        Indexer.spin(FORWARD)
    else:
        Indexer.stop()

    #intake
    if controller_1.buttonL2.pressing() and shift == False:
        Intake.set_velocity(85, PERCENT)
        Intake.spin(FORWARD)
    #outtake
    elif controller_1.buttonL2.pressing() and shift == True:
        Intake.set_velocity(85, PERCENT)
        Intake.spin(REVERSE)
    else:
        Intake.stop()

    #flywheel
    if toggle and not toggle2: #slow
        Flywheel.spin(FORWARD)
        Flywheel.set_velocity(70, PERCENT)
    elif toggle2 and not toggle: #fast
        Flywheel.spin(FORWARD)
        Flywheel.set_velocity(80, PERCENT)
    else:
        Flywheel.stop()

    if controller_1.buttonR2.pressing() and shift == False: #slow
        if not latch:
            #flip the toggle one time and set the latch
            toggle = not toggle
            latch = True
    else: 
        #Once the BumperA is released then then release the latch too
        latch = False

    if controller_1.buttonR2.pressing() and shift == True: #fast
        if not latch2:
            #flip the toggle one time and set the latch
            toggle2 = not toggle2
            latch2 = True
    else: 
        #Once the BumperA is released then then release the latch too
        latch2 = False

    wait(0.2,SECONDS)