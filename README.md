# Mavros bridge for manual control

Creating a manual control, joystick bridge between user and drone using mavros.
<hr>

### Usage

### Dependencies
Primary :
- Joy package
- mavros package
<hr>

### Supported flight modes 
1. Global velocity Control, joystick.
2. Local position control, keyboard.

### Todo list 
- [x] Create a roslaunch file for velocity control.
- [x] Expand the drone msg to accept more buttons.
- [x] Make local position control flight mode.
- [ ] Add individual function nodes:
  - [ ] Arm node
  - [ ] disarm node
  - [ ] takeoff node
  - [ ] hold node
  - [ ] Joy stick position control node
  - [ ] Keyboard position control contigency node
  - [ ] Drop mode node
- [ ] Make attitude control flight mode.
- [ ] Make acceleration control flight mode.
- [ ] Button activate all the individual nodes, write a master script, Integration.
