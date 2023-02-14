# run the mavros node, joy node
## basic script for joy stick velocity control


#!/usr/bin/env python3
import rospy
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest, CommandTOL, CommandTOLRequest
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from px4_controller.msg import drone


# xbox mapping : 
# axes[0] = H left
# axes[1] = V left
# axes[3] = H right
# axes[4] = V left

# def dronecb():
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



def main():
    rospy.init_node("drone_ip")
    drone = fcumode()
    joy = joy_input()
    cmd_vel = Twist()
    
    sub = rospy.Subscriber("/joy",Joy,callback = joy.joycb)
    pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped",Twist,queue_size=10)
    
    rospy.loginfo("Sending some initial setpoints at 20hz")
    rate = rospy.Rate(20)
    i=0
    for i in range(100):
        pub.publish(cmd_vel)
        rate.sleep()
    
    rospy.loginfo("Trying to arm the drone")
    drone.arm(True)
    rospy.loginfo("Mode changed to offboard")
    drone.offboard()

    rospy.loginfo("Establishing Joy stick control")
    while not rospy.is_shutdown():
        cmd_vel.linear.z=3*joy.drone_ip.thrust
        cmd_vel.angular.z =3*joy.drone_ip.yaw
        cmd_vel.linear.x = 3*joy.drone_ip.pitch
        cmd_vel.linear.y = 3*joy.drone_ip.roll
        pub.publish(cmd_vel)
        rate.sleep()

    # drone.takeoff(3)

    # i=0
    # for i in range(100):
    #     pub.publish(cmd_vel)
    #     rate.sleep()


main()
