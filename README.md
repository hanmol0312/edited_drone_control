# Manual bridge MAVLINK

Creating a manual control, joystick bridge between user and drone using mavros
<hr>

### Usage
Run the drone_control.launch for the global velocity control of the drone using joysticks. <br>
Yet to create more flight modes and failsafe buttons.
<hr>

### Dependencies
Primary :
- Joy package
- mavros package
<hr>

### Supported flight modes 
1. Global velocity Control.

### Todo list 
- [ ] Create a roslaunch file for velocity control.
- [ ] Expand the drone msg to accept more buttons.
- [ ] Create arm and disarm button.
- [ ] Make local velocity control flight mode.
- [ ] Make local position control flight mode.
- [ ] Make attitude control flight mode.
- [ ] Make acceleration control flight mode.