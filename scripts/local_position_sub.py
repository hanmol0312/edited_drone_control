#!/usr/bin/env python3
import rospy
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest, CommandTOL, CommandTOLRequest
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, PoseStamped
from px4_controller.msg import drone

local_pos = PoseStamped()

class joy_input:
    def __init__(self):
        self.joy_in = Joy() #will contain the joy values
        self.drone_ip = drone() #will contain the rpty values
    
    def joycb(self,msg: Joy):
        self.joy_in = msg
        self.drone_ip.thrust = self.joy_in.axes[1]
        self.drone_ip.yaw = self.joy_in.axes[0]
        self.drone_ip.roll = self.joy_in.axes[3]
        self.drone_ip.pitch = self.joy_in.axes[4]
        
class fcumode:
    # def __init__():

    def arm(self,truth):
        arming = CommandBoolRequest()
        arming.value =truth
        rospy.wait_for_service("/mavros/cmd/arming")
        try :
            rospy.loginfo("Arm=%s",truth)
            arm_client = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
            arm_client.call(arming)
            rospy.loginfo("Armed")
        except rospy.ServiceException:
            rospy.logdebug("Could not arm")
    
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
    def __init__(self) :
        self.local_pos = PoseStamped()
        self.setpoint_local =PoseStamped()

    def local_pos_cb(self,msg : PoseStamped):
        self.local_pos = msg
        rospy.loginfo(self.local_pos)


def main():
    rospy.init_node("get_local_pos")
    lc = local_control()
    rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=lc.local_pos_cb)
    rospy.spin()

main()