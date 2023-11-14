


#-------------------------------------------------------
# Import Libraries                                     |
#-------------------------------------------------------

import variables



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



#-------------------------------------------------------
# Initialize devices                                   |
#-------------------------------------------------------

# proximity sensors : Infrared-Sensors
ps = {}
psNames = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
psValues = {}

for i in range( len(psNames) ):
    sensorName = psNames[i]
    ps[sensorName] = (robot.getDevice( sensorName ))
    ps[sensorName].enable(timestep)


# ground sensors : Infrared-Sensors
gs = {}
gsNames = ['irL', 'irCL', 'irCR', 'irR', 'irGL', 'irGR']
gsValues = {}

for i in range( len(gsNames) ):
    sensorName = gsNames[i]
    gs[sensorName] = (robot.getDevice( sensorName ))
    gs[sensorName].enable(timestep)



#-------------------------------------------------------
# User Defined Function                                |
#-------------------------------------------------------

def getPSvalues ():
    
    ''' 
        Read all the proximity sensors value.
        Input : No input required.
        Output : Dictionary. Sensors values are returned as key value pairs - {sensorName : sensorValue}.
    '''

    # Reading Proximity Sensors Value
    for i in range( len(psNames) ):
        sensorName = psNames[i]
        psValues[sensorName] = ps[sensorName].getValue()

    return psValues
    
    
def getGSvalues ():
    
    ''' 
        Read all the ground sensors value.
        Input : No input required.
        Output : Dictionary. Sensors values are returned as key value pairs - {sensorName : sensorValue}.
    '''

    # Reading Ground Sensors Value
    for i in range( len(gsNames) ):
        sensorName = gsNames[i]
        gsValues[sensorName] = gs[sensorName].getValue()
        print(f'{sensorName} : {gsValues[sensorName]}')

        # if gsValues[sensorName] == 1000.0:
        #     stop_robot()

        #     print(f'{sensorName} : {gsValues[sensorName]}')
        #     startingTime = robot.getTime()

        #     while ( robot.step(timestep) != -1 ):
        #         if robot.getTime() > startingTime + 0.2:
        #             break
            
        #     getSensorValues()
        #     break
    
    return gsValues
    

