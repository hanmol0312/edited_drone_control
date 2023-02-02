# This node may serve as an intermediate node, but its already 
# bypassed by <drone_control.py> node, it just publishes to the RPTY topic

import rospy
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Joy
from px4_controller.msg import drone

joy_input = Joy()
drone_ip = drone()

# xbox mapping : 
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
    rospy.loginfo(" %s , %s , %s , %s",drone.thrust,drone.yaw,drone.pitch, drone.roll)

def main():
    
    rospy.init_node("joy_stick_control", anonymous=True)
    pub = rospy.Publisher("/RPTY",drone,queue_size=10)
    sub = rospy.Subscriber("/joy",Joy,callback = joycb)
    print(type(joy_input.axes))
    rospy.spin()

main()
