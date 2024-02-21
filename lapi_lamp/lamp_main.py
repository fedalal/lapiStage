#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import paho.mqtt.client as mqtt

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVING_SPEED       = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                 # Dynamixel ID : 1
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyS2'    # Check which port is being used on your controller

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 0           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)

MQTT_BROKER_ADDRESS         = 'lapiStage.local'
MQTT_BROKER_TOPIC           = 'LAPI/lamp/'
MQTT_MIN_MOTOR              = 1
MQTT_MAX_MOTOR              = 7
 
def setMotorTorque(dxl_id, value):
   if value:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, \
         dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
   else:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, \
         dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)

   if dxl_comm_result != COMM_SUCCESS:
      print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
   elif dxl_error != 0:
      print("%s" % packetHandler.getRxPacketError(dxl_error))


def setMotorPosition(dxl_id, position):
   print('Set position for motor', dxl_id, position)
   if position < DXL_MINIMUM_POSITION_VALUE:
      position = DXL_MINIMUM_POSITION_VALUE
   if position > DXL_MAXIMUM_POSITION_VALUE:
      position = DXL_MAXIMUM_POSITION_VALUE
   dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, \
      dxl_id, ADDR_MX_GOAL_POSITION, position)  


def setMotorSpeed(dxl_id, speed):
   print('Set speed for motor', dxl_id ,speed)
   if speed < DXL_MINIMUM_POSITION_VALUE:
      speed = DXL_MINIMUM_POSITION_VALUE
   if speed > DXL_MAXIMUM_POSITION_VALUE:
      speed = DXL_MAXIMUM_POSITION_VALUE
   dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, \
      dxl_id, ADDR_MX_MOVING_SPEED , speed)
 
# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


#---------------------------------------------------

def on_message(client, userdata, message):
    try:
      msg_data = int(message.payload.decode("utf-8"))
      msg_topic = message.topic.rsplit('/', 1)[-1]
     
      #check if topic is 'motor'
      if len(msg_topic) > 5 and msg_topic[0:5] == 'motor':
         msg_motor = int(msg_topic[5:])
         setMotorPosition(msg_motor, msg_data)
       #check if topic is 'speed'
      elif len(msg_topic) > 5 and msg_topic[0:5] == 'speed':
         msg_motor = int(msg_topic[5:])
         setMotorSpeed(msg_motor, msg_data)
 
    except:
      print("Incorrect data:", message.payload.decode("utf-8"))

    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code")

#set motor default speed
for i in range(MQTT_MIN_MOTOR, MQTT_MAX_MOTOR+1):
   setMotorSpeed(i,155)

#connect MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) #create new instance
client.connect(MQTT_BROKER_ADDRESS) #connect to broker
#client.publish(MQTT_BROKER_TOPIC +"motor1","234")#publish

for i in range(MQTT_MIN_MOTOR, MQTT_MAX_MOTOR+1):
   print("Subscribing to topic",MQTT_BROKER_TOPIC +"motor"+str(i))
   client.subscribe(MQTT_BROKER_TOPIC +"motor" +str(i))
for i in range(MQTT_MIN_MOTOR, MQTT_MAX_MOTOR+1):
   print("Subscribing to topic",MQTT_BROKER_TOPIC +"speed"+str(i))
   client.subscribe(MQTT_BROKER_TOPIC +"speed" +str(i))


client.on_connect = on_connect
client.on_message=on_message
client.loop_start()

#---------------------------------------------------
counter = 0
while 1:
  time.sleep(0.1)
  counter += 1
  client.publish(MQTT_BROKER_TOPIC +"live", counter)

# Close port
portHandler.closePort()
