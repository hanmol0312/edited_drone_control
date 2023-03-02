import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool, CommandBoolRequest
from mavros_msgs.srv import SetMode, SetModeRequest

# arm
# setpoints
# set to offboard
# setpoint as 0,0,5
# increment x +=2, wait till reached
# increment y +=2, wait till reached
# increment x -=2, wait till reached
# increment y -=2, wait till reached
# hold and land

# arm the drone
rospy.init_node("Sample")
rospy.wait_for_service("/mavros/cmd/arming")
try:
    arming = CommandBoolRequest()
    arming.value = True
    client = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    client.call(arming)

except rospy.ServiceException:
    pass

rospy.loginfo("armed")

setpoint_position = PoseStamped()
setpoint_position.pose.position.z=5

local_position=PoseStamped()

def positioncb(msg: PoseStamped):
    global local_position
    local_position=msg

rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=positioncb)
position_pub = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
rospy.loginfo("getting the local position")
count=0
rospy.loginfo("Publishing some initial setpoints")
rate = rospy.Rate(20)
while not rospy.is_shutdown():
    if count < 100:
        position_pub.publish(setpoint_position)
    else :
        break
    count+=1
    rate.sleep()

rospy.loginfo("Setting to offboard mode")

rospy.wait_for_service("/mavros/set_mode")
try :
    offb_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    offb =SetModeRequest()
    offb.custom_mode="OFFBOARD"
    offb_client.call(offb)
except rospy.ServiceException:
    rospy.loginfo("Could not set to offboard")
    pass

rospy.loginfo("Set to offboard mode")
client.call(arming)
while not rospy.is_shutdown():
    if local_position.pose.position.z <= 4.95:
        position_pub.publish(setpoint_position)
    else: 
        break
    rate.sleep()

rospy.loginfo("Target altitude reached")

setpoint_position.pose.position.x += 2
rospy.loginfo("Taking off")
while not rospy.is_shutdown():
    if local_position.pose.position.x<= 1.95:
        position_pub.publish(setpoint_position)
    else: 
        break
    rate.sleep()


setpoint_position.pose.position.y += 2
rospy.loginfo("0/3")
while not rospy.is_shutdown():
    if local_position.pose.position.y <= 1.95:
        position_pub.publish(setpoint_position)
    else: 
        break
    rate.sleep()

setpoint_position.pose.position.x -= 2
rospy.loginfo("1/3")
while not rospy.is_shutdown():
    if local_position.pose.position.x >= 0.05:
        position_pub.publish(setpoint_position)
    else: 
        break
    rate.sleep()

setpoint_position.pose.position.y -= 2
rospy.loginfo("2/3")
while not rospy.is_shutdown():
    position_pub.publish(setpoint_position)
    rate.sleep()

