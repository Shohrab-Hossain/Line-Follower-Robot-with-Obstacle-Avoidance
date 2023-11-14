"""line_following_behavior controller."""
# This program implements a state-machine based line-following behavior
# for the e-puck robot. 

# Author: Shohrab Hossain
# Date: 26th April, 2022
# Update: 26th April, 2022



#-------------------------------------------------------
# Import Libraries                                     |
#-------------------------------------------------------

# from controller import Robot, DistanceSensor, Motor
import motor
import sensor
import variables
import line_follower
import object_avoidance


# #-------------------------------------------------------
# # Initialize variables                                 |
# #-------------------------------------------------------

# get  the Robot instance.
robot = variables.robot

# get the time step of the current world.
timestep = variables.timestep   # [ms]

# set threshold value for ground sensors
gsThreshold = variables.gsThreshold  # greater than threshold means sensor above black line
gsMaxValue = variables.gsMaxValue



# #-------------------------------------------------------
# # Initialize devices                                   |
# #-------------------------------------------------------

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


def isObjectDetected ():

    '''
        Detect any obstacle blocking the line using proximity sensors.
        Input : No input required.
        Output : Boolean. Ture if obstacle detected otherwise False. 
    '''
    isRoboOnColoredPath = line_follower.isRoboOnColoredPath
    return ( (psValues['ps0'] > 80) or (psValues['ps7'] > 80) ) and isRoboOnColoredPath


def isGoalReached ():

    '''
        Check whether robot reached the goal or not.
        Input : No input required.
        Output : Boolean. True if goal reached otherwise False.
    '''
    
    # if front sensors : irCL, irCR, and irG value greater than threshold; and
    # their integer values are equal irCL == irCR == irG; and
    # any of the side sensors : irL or irR value greater than threshold; then
    # Goal Reached.


    # defining front sensor
    frontSensor = ['irCL', 'irCR', 'irGL', 'irGR']

    # checking front sensors values are greater than threshold
    for sensorName in frontSensor:
        sensorValue = gsValues[sensorName]
        if sensorValue < gsThreshold or sensorValue > 30:
            # any value less than threshold means goal not reached
            return False

    
    # for sensorValue in list( gsValues.values() ):
    #     if sensorValue < gsThreshold or sensorValue == gsMaxValue:
    #         return False  # goal not reached
    
    
    # checking front sensors integer values are equal
    if int( gsValues['irCL'] ) == int( gsValues['irCR'] ):
        #checking any of the side sensorsvalue greater than threshold
        if (gsValues['irL'] >= gsThreshold) or (gsValues['irR'] >= gsThreshold):
            print(' <---- Goal Reached ----> ')
            return True  # goal reached

    
    return False  # goal not reached
        


def sleep_for (timeInMS):
    time = timeInMS / 1000
    startingTime = robot.getTime()

    while robot.step(timestep) != -1:
        if robot.getTime() >= startingTime + time:
            break
        print('waiting')




#-------------------------------------------------------
# Main loop:                                           |
#-------------------------------------------------------

# sensors required some times to get actiated
# motor.rotate_to('left')
# motor.rotate_to('right')
sleep_for(800)

# perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    print('GHi')
    # Update sensor readings
    updateSensorValue()


    # Implement the line-following state machine
    
    if isGoalReached():  # goal reached, robot is stopping
        motor.stop_robot()
        break
    elif isObjectDetected():
        object_avoidance.maintain_STATE()
    else:
        line_follower.maintain_STATE()
        
    
    # Repeat all steps while the simulation is running.
    
    
