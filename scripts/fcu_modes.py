# DO NOT USE
#### TO be used as an include file later, yet to be modified, 

import rospy
from geometry_msgs.msg import Point, PoseStamped
from mavros_msgs.msg import State, PositionTarget
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode, SetModeRequest

class flight_modes():
    def __init__(self) -> None:
        drone_state = State()
        rate = rospy.Rate(20)
        pass

    def setArm(self):
        rospy.wait_for_service("/mavros/cmd/arming")
        try :
            arm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
            arm.call(True)
        except rospy.ServiceException:
            rospy.loginfo("Could not arm")
        

    def setDisArm(self):
        rospy.wait_for_service("/mavros/cmd/arming")
        try : 
            disarm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
            disarm.call(False)
        except rospy.ServiceException:
            rospy.loginfo("unable to disarm")

    def setStabilizedMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', SetMode)
            msg = SetModeRequest
            msg.custom_mode = "STABILIZED"
            flightModeService.call(msg)
        except rospy.ServiceException:
            rospy.loginfo("ServiceException error")

    def setOffboardMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', SetMode)
            msg = SetModeRequest
            msg.custom_mode = "OFFBOARD"
            flightModeService.call(msg)
        except rospy.ServiceException:
            rospy.loginfo("ServiceException")

    def setAltitudeMode(self):
        rospy.wait_for_service("mavros/set_mode")
        try: 
            flightModeService = rospy.ServiceProxy("/mavros/set_mode",SetMode)
            msg = SetModeRequest
            msg.custom_mode = "ALTCTL"
            flightModeService.call(msg)
        except rospy.ServiceException:
            rospy.loginfo("ServiceException")
    
    def setPositionMode(self):
        rospy.wait_for_service("/mavros/set_mode")
        try: 
            flightModeService = rospy.ServiceProxy("/mavros/set_mode",SetMode)
            msg = SetModeRequest
            msg.custom_mode = "POSCTL"
            flightModeService.call(msg)
        except rospy.ServiceException:
            rospy.loginfo("ServiceException")

    def setTakeOff(self):
        rospy.wait_for_service("/mavros/cmd/takeoff")
        try :
            takeoff = rospy.ServiceProxy("/mavros/cmd/takeoff",CommandTOL)

            takeoff(altitude = 3)
        except rospy.ServiceException:
            rospy.loginfo("ServiceException")


# class controller:
#     def __init__(self) -> None:
        
#         self.state = State() # initialing all the main globals for callback
#         self.set_point = PoseStamped()
#         self.local_position = PoseStamped()

#         self.delta = 5 # rate of change

#         # self.set_point.type_mask = int('010111111000', 2) #flag for position setpoint and yaw angle
#         # self.set_point.coordinate_frame = 1 # local ned
#         # initial coordinate frame
#         self.set_point.pose.position.z=3.0 # flying at a constant altitude
#         self.set_point.pose.position.x=0
#         self.set_point.pose.position.y=0

#         # local_position = Point(0.0,0.0,0.0)

#     # callbacks for state and position
#     def position_callback(self, msg: PoseStamped):
#         self.local_position = msg
    
#     def state_callback(self, msg:State):
#         self.state = msg
    
#     # function for hovering
#     def update_set_point(self): 
#         self.set_point = self.local_position


# def main():
#     rospy.init_node("Px4_controller")
    
#     modes = flight_modes()
#     control = controller()
#     rate = rospy.Rate(20)

#     rospy.Subscriber("/mavros/state",State,callback=control.state_callback)
#     rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=control.position_callback)
#     pub = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)

#     while not control.state.armed:
#         modes.setArm()
#         rate.sleep()
    
#     while not rospy.is_shutdown():
#         pub.publish(control.set_point)
#         rate.sleep()

#     modes.setTakeOff()
#     rospy.spin()
        

#     # modes.setOffboardMode()

#     ## hover loop, we can substitute this with anything else
#     # while not rospy.is_shutdown():
#     #     control.update_set_point()
#     #     pub.publish(control.set_point)
#     #     rate.sleep()

