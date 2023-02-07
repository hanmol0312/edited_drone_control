# takes the input and publishes it to the key topic
import rospy
from pynput.keyboard import Key, Listener
from std_msgs.msg import String
import subprocess

def on(key:Key):
    pub.publish(format(key))


rospy.init_node("Keypub")
pub = rospy.Publisher("/Key",String,queue_size=10)
subprocess.run(["stty -echo"])
rospy.loginfo("Enter the key here please")
listener = Listener(on_press=on)
listener.start()
listener.join()


