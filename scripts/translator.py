# translator node
# This node may serve as an intermediate node between joystick and drone message, but its already 
# bypassed by <drone_control.py> node, it just publishes to the RPTY topic

import rospy
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Joy
from px4_controller.msg import drone

joy_input = Joy()
drone_ip = drone()

# xbox mapping : a lot more buttons to be added
# axes[0] = H left
# axes[1] = V left
# axes[3] = H right
# axes[4] = V left

def joycb(msg: Joy):
    global joy_input
    joy_input = msg
    global drone_ip
    drone.thrust = joy_input.axes[1]
    drone.yaw = joy_input.axes[0]
    drone.roll = joy_input.axes[3]
    drone.pitch = joy_input.axes[4]
    drone.arm = joy_input.buttons[0]
    drone.disarm = joy_input.buttons[3]
    drone.mode = joy_input.buttons[2]
    drone.hold = joy_input.buttons[1]


def main():
    
    rospy.init_node("translator")
    pub = rospy.Publisher("/RPTY",drone,queue_size=10)
    sub = rospy.Subscriber("/joy",Joy,callback = joycb)
    rospy.loginfo("Translator launched, publishing to RPTY topic")
    rospy.spin()

main()
