#  Miniature-AGV-for-material-handling

## **Project Objective**
To build a miniature AGV that can navigate from given starting coordinate to an ending coordinate.

## **System Architecture**
![System Architecture](https://github.com/ashiqrahmana/Miniature-AGV-for-material-handling/blob/main/Architecture.png)

Higher Level Controller: Raspberry Pi 4B

Lower Level Controller: Basic Stamp 2 

## **Onboard Sensors**
1. IR Sensor based Wheel encoders
2. Accelerometer - ADXL 335

## Circuit
![Circuit Diagram](https://github.com/ashiqrahmana/Miniature-AGV-for-material-handling/blob/main/Circuit.png?raw=true)

## **Approach**

### User Input
User Input User input is taken in via GUI built in Python using TKINTER library. 

![GUI Image](https://github.com/ashiqrahmana/Miniature-AGV-for-material-handling/blob/main/GUI_Annotated.png?raw=true)

Once user input is obtained, the data is then sent to lower level controller via serial communication.

### Control and Data Processing
It is always assumed that the robot is placed parallel to X-axis and at (0,0). This serves as the home position for the robot. Once we recieve the start and stop points from user via GUI, we calculate the heading angle using basic geomentry and leverage the differential drive to orient outself with respect to that. The current angular position of the bot is obtained via forward integration of the angular velocity. Once the orientation is matched, we drive forward to the target. The current position is estimated using the IR Wheel encoders and the forward integration of accelerometer data to remove drifts and uncertainities. 

## Folder Structure
|-Code
|----AGV_combined.py  -  Main Python code with GUI and Serial communication 
|----basic_ip_op.bs2  -  Code to read and process all Inputs and Outputs on BS2
|----basicipop.py     -  Serial test code
|----basicipop2.py    -  Serial communicaton code for data transfer
|----niri_code.bs2    -  Basic Drive code on BS2
|----speed_cal.bs2    -  Sensor data extraction
|-Images              -  All images related to the project
|-design              -  All CAD files related to the project


## Assembled Bot
![Bot Image](https://github.com/ashiqrahmana/Miniature-AGV-for-material-handling/blob/main/Bot.jpeg?raw=true)

## Final Result Visualized

![Final Result Viz](https://github.com/ashiqrahmana/Miniature-AGV-for-material-handling/blob/main/boebot-recording.gif)
