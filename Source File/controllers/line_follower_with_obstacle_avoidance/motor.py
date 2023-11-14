


#-------------------------------------------------------
# Import Libraries                                     |
#-------------------------------------------------------

import variables
import sensor



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
# Initialize devices                                   |
#-------------------------------------------------------

# initial motor kinematics
leftSpeed = 0
rightSpeed = 0

# initial motors definition    
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

# initial motor position 
leftMotor.setPosition( float('inf') )
rightMotor.setPosition( float('inf') )

# initial motor speed
leftMotor.setVelocity( leftSpeed )
rightMotor.setVelocity( rightSpeed )



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


def setSpeed (leftMotorSpeed=0.0 , rightMototrSpeed=0.0):
    
    '''
        Set the velocity of the robot motor.
        Input : leftMotorSpeed and rightMotorSpeed as Number. Default value is 0.
        Output : No output.
    '''
    
    leftMotor.setVelocity( leftMotorSpeed )
    rightMotor.setVelocity( rightMototrSpeed )


def rotate_to (direction):

    '''
        Rotate to a direction about 90 or 180 degrees. 
        Input : String. Direction of rotaion : left, right, or flip
        Output : No output
    '''

    # left  - rotates 90 degree Counter Clock Wise.
    # right - rotates 90 degree Clock Wise.
    # flip  - rotates 180 degree Clock Wise.

    
    # converting the argument to lower case
    direction = direction.lower()


    # calculating the time required to complete a rotation
    degree = 180 if direction == 'flip' else 90  # degree of rotation
    rotational_time = degree / ANGULAR_VELOCITY  # required rotation time
    
    # reading present time
    time_now = starting_time = robot.getTime()   # present time
    

    # set speed according to required rotation
    if direction == 'left':
        leftSpeed = - MAX_SPEED
        rightSpeed = MAX_SPEED
        print(' Robot rotating : < LEFT ')
    
    elif direction == 'right' or direction == 'flip':
        leftSpeed = MAX_SPEED
        rightSpeed = - MAX_SPEED
        print(' Robot rotating : RIGHT > ')


    # keep rotating for the required time
    while (rotational_time > (time_now - starting_time)) and (robot.step(timestep) != -1):  # robot.step() is required for while loop
        
        # Set motor speeds with the values defined by direction
        setSpeed(leftSpeed, rightSpeed)

        # read present time
        time_now = robot.getTime()
    

    # after a 90 degree rotation, Left or Right IR sensor can be on balck line.
    # so, the robot need to go forward little bit to make the IR sensors free from black line. 
    isForwardRequired = True and direction != 'flip'
    while (isForwardRequired) and (robot.step(timestep) != -1):  # robot.step() is required for while loop
        # Go Forward
        setSpeed(0.3*MAX_SPEED, 0.3*MAX_SPEED)

        # get new values of sensors 
        updateSensorValue()

        # if sensor value greater than threshold then go forward else exit the loop
        # if direction == 'left':
        #     isForwardRequired = (gsValues['irL'] > gsThreshold-1)
        # elif direction == 'right':
        #     isForwardRequired = (gsValues['irR'] > gsThreshold-1)
        # else:
        #     isForwardRequired = False
        isForwardRequired = (gsValues['irL'] > gsThreshold-1) or (gsValues['irR'] > gsThreshold-1)

    print('<---- Rotation complete ----> ')


def go_forward ():
    
    '''
        Move robot to Forward.
        Input : No input required.
        Output : No output. 
    '''
    
    print(' Robot going : ^ Forward ')

    # Set speeds
    setSpeed( MAX_SPEED, MAX_SPEED )


def stop_robot ():

    '''
        Stop robot motor.
        Input : No input required.
        Output : No output.
    '''

    # Set motor speeds zero
    setSpeed()  # default value is 0  




