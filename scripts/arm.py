import rospy
# from fcu_modes import flight_modes
from mavros_msgs.msg import State
from  mavros_msgs.srv import CommandBool, CommandBoolRequest
from geometry_msgs.msg import PoseStamped
from px4_controller.msg import drone
import threading

drone_state = State()
drone_ip = drone()

def statecb(msg : State):
    rospy.loginfo("State subscription thread")
    global drone_state
    drone_state = msg

def rptycb(msg: drone):
    rospy.loginfo("drone_ip subscription thread")
    global drone_ip
    drone_ip = msg
    rospy.loginfo(msg)

def init_state():
    rospy.loginfo("Subscription thread")
    sub1 = rospy.Subscriber("/mavros/state",State,statecb)
    rospy.spin()

def init_rpty():
    rospy.loginfo("Subscription thread")
    sub2 = rospy.Subscriber("/RPTY",drone,rptycb)
    rospy.spin()

def main():
    rospy.loginfo("main thread")
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        if drone_ip.arm and not drone_state.armed:
            rospy.logwarn("Warning!! Arming the drone.")
            rospy.wait_for_service("/mavros/cmd/arming")
            val = CommandBoolRequest()
            val.value=True

            # pub = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
            # pose = PoseStamped()
            # pose.pose.position.x=0
            # pose.pose.position.y=0
            # pose.pose.position.z=0
            # # sending some setpoints before arming
            # i=0
            # rate = rospy.Rate(20)
            # for i in range(100):
            #     pub.publish(pose)
            #     rate.sleep()
        
            try:
                arming = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
                arming(val)
            except rospy.ServiceException:
                rospy.loginfo("Arming failed")

            rospy.loginfo("Validating arm")
            now = rospy.get_time()
            while not rospy.is_shutdown():
                if(rospy.get_time() - now >=7):
                    rospy.logerr("Arming might have failed")
                    break
                if drone_state.armed:
                    rospy.logwarn("Armed!")
                    break
        else: 
            pass
        rate.sleep()            

rospy.init_node("Arm")
rospy.loginfo("Arming request received")
t1 = threading.Thread(target=init_state, args=())
t1 = threading.Thread(target=init_rpty, args=())
t2 = threading.Thread(target=main, args=())
rospy.loginfo("Starting")
t1.start()
t2.start()
t1.join()
t2.join()
 
