# Warning !!!! rc/override doesent work for px4,
# IT prolly doesn't even work for ardupilot, but it will after some debugging

#!/usr/bin/env python

import rospy
from mavros_msgs.srv import CommandBoolRequest, SetModeRequest, CommandBool, SetMode
from mavros_msgs.msg import OverrideRCIn, Thrust
from geometry_msgs.msg import PoseStamped, Twist

def rc_override():
    rospy.init_node('rc_override', anonymous=True)

    # Wait for the mavros services to become available
    rospy.wait_for_service('mavros/cmd/arming')
    rospy.wait_for_service('mavros/set_mode')
    
    # create publisher for cmd_vel setpoint
    cmd_vel_attitude = rospy.Publisher("mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=10)
    
    # Send a few setpoints before hand
    vel = Twist()
    vel.linear.z = 1

    rate = rospy.Rate(20)
    
    # Send a few setpoints before starting
    for i in range(100):   
        if(rospy.is_shutdown()):
            break
        cmd_vel_attitude.publish(vel)
        rate.sleep()
    
    # Arm the drone
    arm_cmd = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
    arm = CommandBoolRequest()
    arm.value = True
    arm_cmd(arm)
    rospy.loginfo("Armed")


    rospy.loginfo("Sent few initial setpoints")

    # Set the drone mode to "offboard"
    mode_cmd = rospy.ServiceProxy('mavros/set_mode', SetMode)
    offb = SetModeRequest()
    offb.custom_mode = "OFFBOARD"
    mode_cmd(offb)
    rospy.loginfo("Set to offboard mode")

    # rospy.loginfo("Sending stream of setpoints")
    # while True:   
    #     if(rospy.is_shutdown()):
    #         break
    #     # rospy.loginfo(vel)
    #     cmd_vel_attitude.publish(vel)
    #     rate.sleep()
    
    
    # Create a publisher for the RC Override topic
    pub = rospy.Publisher('mavros/rc/override', OverrideRCIn, queue_size=10)

    # Create a RC Override message
    rc_msg = OverrideRCIn()

    # Set the RC channel values
    rc_msg.channels[0] = 1500  # Roll
    rc_msg.channels[1] = 1500  # Pitch
    rc_msg.channels[2] = 1600  # Throttle
    rc_msg.channels[3] = 1500  # Yaw

    # Publish the RC Override message
    while not rospy.is_shutdown():
        pub.publish(rc_msg)
        rospy.sleep(0.01)

if __name__ == '__main__':
    try:
        rc_override()
    except rospy.ROSInterruptException:
        pass
