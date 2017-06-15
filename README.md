# SmartCap
SmartCap for Blind built with Raspberry Pi 3B

##Components Used:
Raspberry Pi 3B
Pi Camera
HS-2304 Ultrasonic Sensor

##External Dependencies
espeak module for text to speech
Internet connection

##Working:
1. When camera button is pressed, camera takes photo sends to the microsoft cognitive services computer vision API, gets the response back from the API and parses it for description text which is the description of the image uploaded. Then the description is sent to the epeak module which gives the audio output for the blind people.

2. When the Obstacle detection button is pressed, ultrasonic sensor starts and continuosly detects for obstacles. Three condition are pre-programmed:
a) Obstacle <= 80cms - Message: STOP 
b) Obstacle > 80cms <= 120cms - Message: CAUTION
c) Obstacle > 120cms - Message: PROCEED

##Note:
1. Stop the Ultrasonic sensor before image description since the voices may overlap
2. Three shell scripts for boot time execution is provided which should be updated in cron tab so that scripts start automatically on startup