# Line Follower with Obstacle Avoidance


<br>
<br>

<p align='center'>
  <img src="readme-lib\world.png" alt="Logo" width="80%"/>
</p>


<br>
<br>


## 1. Introduction

In this experiment, a single robot is programmed with line-following and obstacle avoidance behaviour. The robot must first arrive at a point where it can use camera to detect the color of an object. The path to the goal is chosen based on the color. The robot then continues to move until it reaches the start point of the predetermined course, from which point it continues to follow the track until it reaches the goal. If an object is spotted in the path, the robot overcomes the obstacle by going out of the line and returning.

The robot's drive system is a differential drive motor. IR sensors fitted in the ground sensor slot allow the robot to follow the black line. The closed loop control system provides feedback on the robot's trajectory tracking and adjusts the velocity of each motor accordingly, ensuring that the robot stays on track. The proximity sensors track any obstacle approaching the robot as it follows the line. If an obstacle is spotted, the robot turns right and begins to follow the obstacle's wall. The obstacle avoidance closed loop control system maintains the robot following the obstacle's wall, and when the ground sensor detects a black line, the state switches to line following. Until the go-to-goal behaviour is satisfied, the line following state is maintained.

One of the most common uses for this type of line follower is in warehouses, where goods must be moved from one location to another. Another application is in industry, where products can be transferred to a different location based on factors such as color. LFR is also being used in restaurants, where food is transported from the kitchen to the table by line follower robots that recognise different tables by their different colors.

<br>
<br>
<br>

## 2. Finite State Machine

There are five states in the robot system:

**a. Sense color using camera:** The robot will first arrive at a predetermined point in this stage (first right). It uses a mounted camera to view the object in order to determine its color. It's possible that the detected color is Red, Green, or Blue. The course to the goal is chosen based on the color. After that, the 'Go to selected path' state is activated.

**b. Go to selected path:** In this state, the robot travels to the beginning of the path chosen in the previous state. To achieve this, the robot turns right after sensing color from the object and then continues forward. If it detects a left or right turn, it either takes it or skips it, based on the course chosen (red, green, or blue). When it takes the turn, it comes to the course's beginning point, when the 'Line follow' state is triggered.

**c. Line follow:** The ground sensors are continuously monitoring the black line, while the proximity sensors are scanning for any incoming obstacles in this state. When it detects a change, it performs the previously determined action.

When ground sensors detect that the robot is not aligned with the line, the align-to-line task is triggered. When either the left or right sensor detects a line, the robot rotates in that direction; if both sensors detect a line, the robot is at a junction, and it continues forward to cross the junction. While aligning with the line, spinning, or crossing a junction, the left or right sensor may come into contact with the black line, causing the robot to make an error. As a response, in this case, the robot goes ahead slowly until the sensors are no longer in contact with the line.

The ‘Avoid obstacle’ state is triggered when proximity sensors detect any obstacle.

<br>
<br>

<p align='center'>
  <img src="readme-lib\FSM.png" alt="Finite Sate Machine Architecture" width="70%"/>
</p>

<br>

> Figure: Finite Sate Machine Architecture


<br>
<br>

**d. Avoid obstacle:** The robot keeps track of the obstacle while following the obstacle's wall in this state. If the robot goes too far away from the obstacle, it will turn to face it in order to maintain a safe distance. When the robot detects the edge of a wall, it slowly rotates to the next wall. The ground sensors continue to scan for black lines while following the obstacle, and if any are detected, the robot rotates right and the state switches to ‘Line follow’.

**f. Goal Reached:** The robot reaches the goal in this state. Ground sensors are utilized to detect the goal. When all of the ground sensors detect black, it's possible that the goal has been reached. As a result, all of the sensor results are analyzed to determine whether or not there is a goal. If the robot is in a goal state, it will turn off its motor; otherwise, the 'Line follow' state will be activated.

<br>
<br>
<br>

## 3. Control Architecture
The control architecture is reactive and sequential. There are two feedback loops that must be implemented: one for line following and the other for obstacle avoidance. For both states, the perception-action loop is closed loop.

<br>
<br>

<p align='center'>
  <img src="readme-lib\Sensor.png" alt="Ground Sensors Orientation" width="60%"/>
</p>

<br>

> Figure: Ground Sensors Orientation

<br>
<br>


There are six IR sensors in ground sensor slot. The front sensors ‘irGL’ and ‘irGR’ are used to detect goal. The central sensor ‘irCL’ and ‘irCR’ are used to maintain alignment with line. The left and right sensors ‘irL’ and ‘irR’are used to detect left or right path. 

In a closed loop line follower perception-action system, the central sensors are first checked to see if they are on line or not. The robot is aligned with the line if these sensors are on line; else, it will align itself. If the robot is aligned, it will go forward and check whether the left or right sensors detect any lines. If both sensors register a line, the robot is approaching a junction and will continue onward to cross it. If only one of the sensors detects a line, it rotates accordingly. The proximity sensors continue to monitor whether or not an obstacle is approaching. If an obstacle is spotted, the state is changed to 'avoid obstacle'; otherwise, the central sensor alignment is resumed. A feedback loop can also help you avoid making the wrong decision. Any sensor that comes over the black line when rotating or crossing a junction should not register any turn or rotate commands because it is already executing the prior command. Thus, new registers should be avoided until the rotation or crossover is complete. As a result, before launching a new command, the feedback loop checks whether the left or right sensors are free of line.


<br>
<br>

<p align='center'>
  <img src="readme-lib\Line Follower Perception-Action Loop.png" alt="Line Following Perception-Action Loop" width="70%"/>
</p>

<br>

> Figure: Line Following Perception-Action Loop

<br>
<br>

The proximity sensors are utilized to track the obstacle in an obstacle avoidance perception-action closed loop. The ps5 proximity sensor is the robot's rightmost sensor. First, align the robot with the obstacle by turning right until the ps5 value exceeds 80. The robot will be aligned with the obstacle as a result of this. Then the PS5 and PS6 levels are continuously monitored. If both of these sensor values are greater than 110, the robot is too far away from the obstacle, thus it turns right to get closer. If any of these values exceed 80, the robot continues to go forward. If the PS5 sensor value falls below 80, the obstacle wall comes to an end, and the robot rotates right to align with the next wall. These states are maintained in a closed loop. The ground sensor irR, on the other hand, keeps note of any line detection. If a line is detected by the sensor, the robots will rotate 90 degrees right and the state will change to ‘Line following’.

<br>
<br>

<p align='center'>
  <img src="readme-lib\Obstacle Avoidance Perception-Action Loop.png" alt="Obstacle Avoidance Perception-Action Loop" width="70%"/>
</p>

<br>

> Figure: Obstacle Avoidance Perception-Action Loop

<br>
<br>


The drive system of the robot is a differential dive motor. The robot has a DOM of 3 and a DOM of 2 in terms of degrees of freedom and movement. The robot's mobility is non-holonomic because DOF is greater than DOM.

<br>
<br>
<br>

## 4. Challenges, Limitations and Future Works
The calibration of the sensor threshold value, as well as the alignment and position of each ground sensor, was the initial barrier. Second, maintaining the robot aligned with the track line while driving at maximum speed was tricky. Improving the robot's behaviour, such as sharp rotation, junction recognition, obstacle alignment, and wall tracking, was a major challenge. 

The position of the sensors in respect to the width of the black line is an important aspect of the line follower. The robot occasionally receives incorrect values as a consequence of sensor placement. As a solution, the position and alignment of sensors can be fine-tuned for improved performance.
The robot navigates by making sharp 90-degree turns to the left or right. The estimated angular velocity defines the amount of time needed to complete the rotation. Because of the angular velocity, the robot cannot rotate completely in some situations. The rotation will be more perfect if the angular velocity can be determined properly.

The robot encounters a blank spot while detecting obstacles. Especially when the robot rotates 90 degrees to the left or right, the robot is unable to identify obstacles properly and makes incorrect decisions. This may be remedied by making the rotation more precise and crisper, as well as making the obstacle detection process more dynamic.

Occasionally, while crossing a junction, the robot messes up in motor speed, resulting in unintended rotation. This can be rectified by upgrading the junction detection algorithm as well as the decision-making process for crossing the junction. 

Implementing a more precise algorithm and improving the coding logic can improve overall line following and obstacle avoidance behaviour.

<br>
<br>
<br>


---

<br>
<br>

## Important Links

<br>

a. Simulation Software: [Webots](https://cyberbotics.com)
<br>
b. Video: [YouTube Link](https://www.youtube.com/watch?v=aPlNaNd6j_o) 

<br>
<br>
<br>
<br>
