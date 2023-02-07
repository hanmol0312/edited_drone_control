float32 pitch
float32 yaw
float32 thrust
float32 roll
int32 servo
int32 mode 
int32 arm
int32 disarm
int32 hold
int32 camera
int32 kill

# mapping to joy :::
# float32 pitch joy.axes[1] -left stick up and down
# float32 yaw joy.axes[0] - left stick left and right
# float32 thrust joy.axes[4] - right stick up and down
# float32 roll joy.axes[3] - right stick left and right
# float32 servo  
# int32 mode - joy.buttons[2] - X
# int32 arm - joy.buttons[0] - A
# int32 disarm - joy.buttons[3] - Y
# int32 RTL - joy.buttons[1] - B
# int32 camera
# int32 kill