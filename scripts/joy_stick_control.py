# redundant node that publishes a drone type message

import rospy
from sensor_msgs.msg import Joy
from offboard_mode.msg import drone
import math 

def joy_callback(msg: Joy):
    input = list(msg.axes)
    joystick = drone()
    joystick.thrust = input[1]
    joystick.yaw = input[0]
    joystick.pitch = input[4]
    joystick.roll = input[3]
    rospy.loginfo(joystick)
    pub.publish(joystick)
    

if __name__ == "__main__":
    rospy.init_node("drone_input_provider",anonymous=True)
    pub = rospy.Publisher("/drone_input",drone,queue_size=10)
    rospy.Subscriber("/joy",Joy,callback=joy_callback)
    rospy.spin()
