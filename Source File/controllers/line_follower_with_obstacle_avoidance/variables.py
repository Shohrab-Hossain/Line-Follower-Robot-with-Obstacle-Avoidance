


#-------------------------------------------------------
# Import Libraries                                     |
#-------------------------------------------------------

from controller import Robot, DistanceSensor, Motor



#-------------------------------------------------------
# Initialize variables                                 |
#-------------------------------------------------------

TIME_STEP = 64
MAX_SPEED = 6.28  # rad per second
ANGULAR_VELOCITY = 61  # degrees per second

# # create the Robot instance.
robot = Robot()


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

# set threshold value for ground sensors
gsThreshold = 5.2  # greater than threshold means sensor above black line
gsMaxValue = 1000.0


