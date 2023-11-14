


#-------------------------------------------------------
# Import Libraries                                     |
#-------------------------------------------------------

import variables
import sensor
import motor



#-------------------------------------------------------
# Initialize variables                                 |
#-------------------------------------------------------

TIME_STEP = variables.TIME_STEP
MAX_SPEED = variables.MAX_SPEED  # rad per second
ANGULAR_VELOCITY = variables.ANGULAR_VELOCITY  # degrees per second

# create the Robot instance.
robot = variables.robot


# get the time step of the current world.
timestep = variables.timestep   # [ms]

# set threshold value for ground sensors
gsThreshold = variables.gsThreshold  # greater than threshold means sensor above black line
gsMaxValue = variables.gsMaxValue


# proximity sensors : Infrared-Sensors
psValues = sensor.getPSvalues()

# ground sensors : Infrared-Sensors
gsValues = sensor.getGSvalues()

camera = robot.getDevice('camera')
camera.enable(timestep)

# ---------------------------------------
isPathSelected = False
isRoboOnColoredPath = False
pathNumber = 0
pathCounter = 0



#-------------------------------------------------------
# User Defined Function                                |
#-------------------------------------------------------


def updateSensorValue ():

    '''
        Update with new sensors value.
        Input : No input required.
        Output : No output. Updates psValues and gsValues variables.
    '''
    starting_time = robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime() > starting_time + (5/1000):
            break

    psValues = sensor.getPSvalues()
    gsValues = sensor.getGSvalues()


def align_to_path ():

    '''
        Align the robot with the black line.
        Input : No input required.
        Output : No output.
    '''

    leftSpeed = 0
    rightSpeed = 0
    # less then threshold means not on line
    isLeftNotAlign = gsValues['irCL'] < gsThreshold
    isRightNotAlign = gsValues['irCR'] < gsThreshold

    if isRightNotAlign:  # then turn Left
        leftSpeed = 0.0
        rightSpeed = 0.5 * MAX_SPEED
        print(' Robot Aligning : > Right ')
    elif isLeftNotAlign:  # then turn Right
        leftSpeed = 0.5 * MAX_SPEED
        rightSpeed = 0.0
        print(' Robot Aligning : < LEFT ')
    
    # update motor speed
    motor.setSpeed(leftSpeed, rightSpeed)
    

def crossAnyTurn ():

    while (robot.step(timestep) != -1):  # robot.step() is required for while loop

        # go forward
        motor.setSpeed(0.4*MAX_SPEED, 0.4*MAX_SPEED)
        
        # Update sensor readings
        updateSensorValue()

        # Process sensor data
        isRobotAligned = (gsValues['irCL'] > gsThreshold) and (gsValues['irCR'] > gsThreshold)  # robot is on line

        if not isRobotAligned:
            align_to_path()
        
        if (gsValues['irL'] < gsThreshold) and (gsValues['irR'] < gsThreshold):
            break


def pathDetectionUsingColor ():
    image = camera.getImage()
    if image:
        blue  = image[0]
        green = image[1]
        red   = image[2]

        if (red > green) and (red > blue):
            print('---- Detected Red ----')
            return 1
        elif (green > red) and (green > blue):
            print('---- Detected Green ----')
            return 2
        else:
            print('---- Detected Blue ----')
            return 3
    
    return 1



#-------------------------------------------------------
# Line Following Loop                                  |
#-------------------------------------------------------

def maintain_STATE ():
    global isPathSelected, isRoboOnColoredPath, pathCounter, pathNumber
    
    # Update sensor readings
    updateSensorValue()

    # Process sensor data
    isRobotAligned = (gsValues['irCL'] > gsThreshold) and (gsValues['irCR'] > gsThreshold)  # robot is on line

    isLeftPath = gsValues['irL'] > gsThreshold   # there is a left path available
    isRightPath = gsValues['irR'] > gsThreshold  # there is a right path available

    isJunctionAvailable = isLeftPath and isRightPath

    
    if not isPathSelected and isRightPath:
        motor.stop_robot()
        pathNumber = pathDetectionUsingColor()
        isPathSelected = True
        motor.rotate_to('right')
        

    if isPathSelected and not isRoboOnColoredPath:
        if isLeftPath or isRightPath:
            if pathCounter == pathNumber:
                isRoboOnColoredPath = True
            else:
                crossAnyTurn()
                pathCounter = pathCounter + 1



    if isJunctionAvailable:  # crossing a junction
        # crossJunction()
        print('found junction')
        motor.go_forward()
    elif isLeftPath and isRoboOnColoredPath:   # found a left path
        motor.rotate_to('left')
    elif isRightPath and isRoboOnColoredPath:  # found a right path
        motor.rotate_to('right')
    elif not isRobotAligned:  # maintianing alignment
        align_to_path()
    else:  # no path available
        motor.go_forward()




