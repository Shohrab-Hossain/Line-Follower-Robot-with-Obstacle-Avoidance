


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



#-------------------------------------------------------
# User Defined Function                                |
#-------------------------------------------------------



def updateSensorValue ():

    '''
        Update with new sensors value.
        Input : No input required.
        Output : No output. Updates psValues and gsValues variables.
    '''

    psValues = sensor.getPSvalues()
    gsValues = sensor.getGSvalues()


def isLineDetected ():
    # Right sensor hits black line then go to line following state
    return (gsValues['irR'] >= gsThreshold) and (gsValues['irR']    )


def isCenterSensorOnLine ():
    return (gsValues['irCL'] >= gsThreshold) and (gsValues['irCR'] >= gsThreshold)


def align_with_obstacle ():
    while ( robot.step(timestep) != -1 ):  # turning Right until ps5 sensor get closer to obstacle
        # turn right
        motor.setSpeed(MAX_SPEED, -MAX_SPEED)

        # Update sensor readings
        updateSensorValue()

        if psValues['ps5'] >= 100:
            break

    while ( robot.step(timestep) != -1 ):  # going forward to make the sensors free from balck line

        # Update sensor readings
        updateSensorValue()

        if psValues['ps6'] > 100:
            # go forward
            speed = 0.5 * MAX_SPEED
            print('Make distance')
            motor.setSpeed(speed, -speed)
        else:
            # turn right
            motor.setSpeed(0.5*MAX_SPEED, 0.5*MAX_SPEED)
        

        if gsValues['irL'] < gsThreshold and gsValues['irR'] < gsThreshold:
            break
    
    print(f'aligned with obstacle')


def align_with_line ():
    if isCenterSensorOnLine():  # Center sensors are on black line then turn right 90 degree
        motor.rotate_to('right')
    else:  # otherwise keep turning right until center sensors are on black line
        while ( robot.step(timestep) != -1 ):
            # update sensor readings
            updateSensorValue()
            # set motor speed
            motor.setSpeed(MAX_SPEED, -MAX_SPEED)
            # check sensor on line or not
            if isCenterSensorOnLine():
                break
    
    while ( robot.step(timestep) != -1 ):  # going forward to make Left sensor free from black line
        # update sensor readings
        updateSensorValue()
        # set motor speed
        motor.setSpeed(0.4*MAX_SPEED, 0.4*MAX_SPEED)
        # check left sensor out of line or not
        if (gsValues['irL'] < gsThreshold) and (gsValues['irL'] != gsMaxValue):
            break
    
    print(f'aligned with Line')



#-------------------------------------------------------
# Obstacle Avoidance Loop                              |
#-------------------------------------------------------

def maintain_STATE ():
    print(' --< Object Detected >-- ')

    # Update sensor readings
    updateSensorValue()

    
    align_with_obstacle()
    
    counter = 0
    tempEven = 0
    tempOdd = 1
    while ( robot.step(timestep) != -1 ):  # obstacle avoiding loop

        # Update sensor readings
        updateSensorValue()

        if isLineDetected():      
            align_with_line ()
            print(f'going back to line following state') 
            break

        if psValues['ps6'] > 100:  # if obstacle gets too close then turn left to make distance
            # turn right
            speed = 0.3 * MAX_SPEED
            print('Make distance')
            motor.setSpeed(speed, -speed)

            if counter == tempEven:
                counter = 0
                tempEven = 0
            tempEven = counter
            if (counter % 2 == 0):
                counter = counter + 1

            continue

        if psValues['ps5'] > 80 or psValues['ps6'] > 80:  # go straight
            # go forward
            speed = 0.5 * MAX_SPEED
            motor.setSpeed(speed, speed)
        else:  # turn right towards obstacle
            # speed = 0.4 * MAX_SPEED
            # motor.setSpeed(-speed, speed)

            if counter > 4 : 
                speed = 0.3 * MAX_SPEED
                motor.setSpeed(speed, speed)
            else:
                speed = 0.4 * MAX_SPEED
                motor.setSpeed(-speed, speed)

            if counter == tempOdd:
                counter = 0
                tempOdd = 1
            tempOdd = counter
            if (counter % 2 != 0):
                counter = counter + 1



