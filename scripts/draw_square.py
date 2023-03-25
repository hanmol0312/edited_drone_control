#!/usr/bin/env python3

## makes the drone go in a square. just run the mavros node 
## add hold mode mapped to a button
import rospy
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest, CommandTOL, CommandTOLRequest
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, PoseStamped, Point, TwistStamped
from px4_controller.msg import drone

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
    def __init__(self):
        self.local_pos = PoseStamped()
        self.setpoint_local = PoseStamped()
        
        self.setpoint_local.pose.position.x =0.0
        self.setpoint_local.pose.position.y =0.0
        self.setpoint_local.pose.position.z =2.0
        
    def local_pos_cb(self,msg : PoseStamped):
        self.local_pos = msg
        # rospy.loginfo(self.local_pos)

    def update_setpoint(self):
        self.setpoint_local.pose.position.x = self.local_pos.pose.position.x
        self.setpoint_local.pose.position.y = self.local_pos.pose.position.y

    def neg_x(self):
        self.setpoint_local.pose.position.x -= 2

    def pos_x(self):
        self.setpoint_local.pose.position.x += 2

    def neg_y(self):
        self.setpoint_local.pose.position.y -= 2

    def pos_x(self):
        self.setpoint_local.pose.position.y += 2

    def neg_z(self):
        self.setpoint_local.pose.position.z -= 0.5

    def pos_z(self):
        self.setpoint_local.pose.position.y += 0.5


def main():
    rospy.init_node("drone_ip")
    drone = fcumode()
    joy = joy_input()
    lc = local_control()

    # subscribes to the joy input 
    sub_joy = rospy.Subscriber("/joy",Joy,callback = joy.joycb)
    # subscribes to the local position input
    sub_pos = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=lc.local_pos_cb)
    
    # publishes to the local setpoint
    pub_local_position = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
    
    # send some initial setpoint to position
    rospy.loginfo("Sending a few initial setpoints")
    rate = rospy.Rate(20)
    i=0
    for i in range(100):
        pub_local_position.publish(lc.setpoint_local)
        rate.sleep()

    # Arm the drone
    rospy.logwarn("Arming")
    drone.arm(True)
    # change to offboard mode
    rospy.loginfo("Mode changed to offboard")
    drone.offboard()

    # takeoff
    rospy.loginfo("Takeoff initiated, target altitude is 2m")        

    while not rospy.is_shutdown():
        if lc.local_pos.pose.position.z < 1.90:
            pub_local_position.publish(lc.setpoint_local)
        else:
            rospy.loginfo("Takeoff altitude reached")
            break
        rate.sleep()
    
    lc.setpoint_local.pose.position.x += 5
    now = rospy.get_time()

    while not rospy.is_shutdown():
        if rospy.get_time() - now < 10:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()
        else: 
            break

    lc.setpoint_local.pose.position.y += 5
    now = rospy.get_time()
    while not rospy.is_shutdown():
        if rospy.get_time() - now < 10:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()
        else: 
            break

    lc.setpoint_local.pose.position.x -= 5
    now = rospy.get_time()
    while not rospy.is_shutdown():
        if rospy.get_time() - now < 10:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()

    lc.setpoint_local.pose.position.y -= 5
    while not rospy.is_shutdown():
        now=rospy.get_time()
        if rospy.get_time() - now < 10:
            pub_local_position.publish(lc.setpoint_local)
            rate.sleep()

main()
