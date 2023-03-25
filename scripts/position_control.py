#!/usr/bin/env python3

# use this over local_control
# run the mavros, teleop_key node in order to use this node
## subscribe from the /keyboard/arrow to use for teleop
import rospy
from mavros_msgs.srv import  SetMode, SetModeRequest, CommandTOL, CommandTOLRequest
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, PoseStamped, Point, TwistStamped
from px4_controller.msg import drone
from px4_controller.msg import key

class joy_input:
    def __init__(self):
        self.joy_in = Joy() #will contain the joy values
        self.drone_ip = drone() #will contain the rpty values
        
class fcumode:
    # def __init__():

    def takeoff(self, alt):
        position = CommandTOLRequest()
        position.altitude = alt
        rospy.wait_for_service("/mavros/cmd/takeoff")                               
        try :
            rospy.loginfo("Taking off to altitude %s",alt)
            takeoff_client = rospy.ServiceProxy("/mavros/cmd/takeoff",CommandTOL)
            takeoff_client.call(position)
        except rospy.ServiceException:
            rospy.logdebug("Takeoff Unsuccessfull")

    def offboard(self):
        offb = SetModeRequest()
        offb.custom_mode = "OFFBOARD"
        rospy.wait_for_service("/mavros/set_mode")
        rospy.loginfo("offboard=True")
        try:
            offb_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
            offb_client.call(offb)
            rospy.loginfo("Set to offboard")
        except rospy.ServiceException:
            rospy.logdebug("Mode change denied")


class local_control:
    def __init__(self):
        self.local_pos = PoseStamped()
        self.setpoint_local = PoseStamped()
        self.setpoint_local.pose.position.x =0
        self.setpoint_local.pose.position.y =0
        self.setpoint_local.pose.position.z= 2
        
    def local_pos_cb(self,msg : PoseStamped):
        self.local_pos = msg
        rospy.loginfo(msg.pose.position.x)
        rospy.loginfo(msg.pose.position.y)

        # rospy.loginfo(self.local_pos)

arrow_input=key()

def arrow_cb(msg:key):
    global arrow_input
    arrow_input=msg

def main():
    rospy.init_node("drone_ip")
    drone = fcumode()
    joy = joy_input()
    lc = local_control()

    rate =rospy.Rate(20)
    # subscribes to the local position input
    sub_pos = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=lc.local_pos_cb)
    # publishes to the local setpoint
    pub_local_position = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
    rospy.loginfo("Sending a few initial setpoints")
    rate = rospy.Rate(20)
    i=0
    for i in range(100):
        pub_local_position.publish(lc.setpoint_local)
        rate.sleep()

    # change to offboard mode
    rospy.loginfo("Mode changed to offboard")
    drone.offboard()     
    now= rospy.get_time()
    lc.setpoint_local.pose.position.x=5
    lc.setpoint_local.pose.position.y=10
    while not rospy.is_shutdown():
        if lc.setpoint_local.pose.position.x!=4.90:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()
        else:
            break
        if lc.setpoint_local.pose.position.y!=9.90:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()
        else:
            break
        if lc.setpoint_local.pose.position.x!=5.0 and lc.setpoint_local.pose.position.y!=10.0:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()
main()