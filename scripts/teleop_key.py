# publishes the arrow key values to /keyboard/arrow
# can detect multiple keys at a time
# get a dictionary that contains the current state of the up, down, side and left keys

import rospy
from pynput.keyboard import Key, Listener
import subprocess
import sys
import threading
from px4_controller.msg import key

key_values = key()

key_state={
    "key_up":0,
    "key_down":0,
    "key_left":0,
    "key_right":0
}

def printdict():
    rate = rospy.Rate(20)
    while True:
        # print(key_state)
        key_values.key_up=key_state["key_up"]
        key_values.key_down=key_state["key_down"]
        key_values.key_left=key_state["key_left"]
        key_values.key_right=key_state["key_right"]
        pub.publish(key_values)
        rate.sleep()

def on(key:Key):
    if(key==Key.esc):
        print("Exiting")
        subprocess.run(["stty","echo"]) # password mode
        sys.exit() # to the parent thread
    if(key==Key.up):
        key_state["key_up"]=1
    if(key==Key.down):
        key_state["key_down"]=1
    if(key==Key.left):
        key_state["key_left"]=1
    if(key==Key.right):
        key_state["key_right"]=1

def off(key:Key):
    if(key==Key.up):
        key_state["key_up"]=0
    if(key==Key.down):
        key_state["key_down"]=0
    if(key==Key.left):
        key_state["key_left"]=0
    if(key==Key.right):
        key_state["key_right"]=0

rospy.init_node("Keypub")  
pub=rospy.Publisher("/keyboard/arrow",key,queue_size=10)
print("Enter the key here, use ctrl c to exit,press esc to exit")
subprocess.run(["stty","-echo"])
listener = Listener(on_press=on,on_release=off)
listener.start()
thread1=threading.Thread(target=printdict)
thread1.start()
thread1.join()
listener.join()


