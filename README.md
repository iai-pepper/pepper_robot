# pepper_robot
Meta-package for Pepper Basic Configuration.
This guide was firstly developed and tested on Ubuntu 14.04 and ROS-indigo, and has now moved to Ubuntu 16.04 and ROS-kinetic. Other versions have not been tested yet and the indigo one might be not up to date anymore.
NOTE: This guide is still under construction/verification and this is currently the first draft. If you encounter any issues while using it, or if something does not work, please create an issue and let us know.

## Installation of pepper-packages

First we need to install die NAOQI Api. Follow the instructions at

- http://doc.aldebaran.com/2-5/dev/python/install_guide.html

## Moving Pepper using a controller
We want to use Teleop on Pepper, luckily every package needed is already available for ROS Kinetic.

### Preparation
You will of course need a controller, we recommend the PS4 Controller.

- Set a system variable NAO\_IP to the IP of Pepper.

Since we adjusted some of the Packages for our scenario, we forked the ones we have altered. All of our packages are within a git-hub organization called iai-pepper. The ones needed are: 
- https://github.com/iai-pepper/nao_extras (contains teleop, adjusted to be used with a ps4 controller)
- https://github.com/iai-pepper/ps4-ros (contains the ps4 driver for ros.)
- The Pepper Robot Repositories: https://github.com/iai-pepper/pepper_robot


And the packages needed are:

- Pepper Meshes: (sudo apt-get install ros-kinetic-pepper-robot ros-kinetic-pepper-meshes)
- And the NaoQi Drivers, in Python or C++: http://wiki.ros.org/naoqi\_driver
- The joy package: http://wiki.ros.org/joy?distro=kinetic

And for other Gamepads than the XBox one:

- jstest-gtk and joystick

(with jstest-gtk test to see if the controller is working and which port it is on)

If the wireless ps4 Controller should be used, please follow the instructions of this repo:
- https://github.com/iai-pepper/ps4-ros

For Navigation you should clone:
- https://github.com/iai-pepper/pepper_plymouth_ros.git

#### Other ros dependencies:
Other dependencies one might need to install while setting up Pepper for the first time: 
- sudo apt-get install ros-kinetic-move-base-msgs 

### On Pepper

First you will want to disable "`Life"'. It is very annoying to try to control a robot that move around when it wants to. So connect to the Pepper via SSH.

```sh
ssh nao@$NAO_IP
```

In ssh:

```sh
nao stop
naoqi-bin --disable-life
```

Now open another shell and connect again to the Pepper via SSH.
Type:

```sh
qicli call ALMotion.wakeUp
```

This will wake up the robot.

If you want to restart the slight background movement of Pepper (which is used to let Pepper seem more lifelike), execute the following command:

```sh
qicli call ALBackgroundMovement.setEnabled 1
```

### Starting everything up!

Now just start the Pepper bringup and Nao teleop:

```sh
roslaunch pepper_bringup pepper_full.launch
```

or

```sh
roslaunch pepper_bringup pepper_full_py.launch
```
     
and in another shell launch the Teleop, and the ps4 joystick driver:

```sh
roslaunch ps4_ros ps4.launch 
```

Hold the "share" and "playstation" button for a few seconds until the controller is flashing white in order to put it into pairing mode. It should connect to your laptop after a few seconds and glow constantly blue. 

Everything is ready! Use the button 9 (options) to enable or disable gamepad control.

### Controlling the Robot

9 (options) to enable or disable gamepad control.
Left Joystick: forwards, backwards, sideways (omni)
Right Joystick: turn in place
Hold L1: move head instead of body.
L1 + right joystick: move head left right, up down. 

Rectangle: Show the choosen default logo (see the pepper_bringup_py.launch file)
O: Switch between "disable autonomous life" and "enable autonomous life" 
X: Switch between "mute" and "unmute"

L2: Trigger smile newsletter

## Localization
For localizazion one needs a map and the amcl node. 
#### Map
If a map is published by another robot in the network, you can ignore this step. Otherwise launch: 

```sh
roslaunch pepper_plymouth_ros map_server.launch 
```
This will launch the map server with a map of the lab. 
#### Localization (amcl)
Launch the amcl node. It will allow you to localize the robot and will also publish the map->odom transform.
```sh
roslaunch pepper_plymouth_ros amcl.launch 
```
Once this is launched, you can go to rviz, set the global-frame to "map". Click the "2D Pose Estimate" button and click and drag on the map, depending on where your robot currently is. The robot model should jump to that location and the particle array should show many red arrows around the robot. 
If this didn't work, check if you have set the "/pepper_robot" prefix in the "2D Pose Estimate" by right clicking on that button and selecting "Tool Properties". The topic name of "2D Pose Estimate" should be:

    "pepper_robot/initialpose"

you can also adjust the one below for move_base already.
The red arrows should start to group around the robot more and will be less spread out once you move the robot a bit. 
So do so, to get a proper localization.

## Navigation
For navigation, launch: 
```sh
roslaunch pepper_plymouth_ros move_base.launch 
```
Similar to Localization, one can use the rviz button "navigate to" to set a point on the map to which the robot will then attempt to go. Make sure global fixed frame is set to map for this. 


## Multi Sensor Localization and Navigation
It's possible to use all three of Pepper's laser sensors for Localization and navigation. However, this is currently still being tested and fine tuned. (amcl and move_base do not support multiple sensors at this point)
For this to be possible in the first place, one needs an extra package, which would stitch the 3 sensors together, so that their data will be published on one topic instead. 

https://github.com/iai-pepper/ira_laser_tools

launch:
```sh
roslaunch ira_laser_tools laserscan_multi_merger.launch
```
There are also the configutations for amcl and move_base available, which have already been adapted to this. So launch the following instead of the above:
```sh
roslaunch pepper_plymouth_ros amcl_multi.launch 
roslaunch pepper_plymouth_ros move_base_multi.launch 
```



## knowrob_pepper_openease

At https://github.com/sasjonge/knowrob_pepper_openease you can find a package to use pepper as a guide for openEASE. The package depends on the [NaoQI Python SDK](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)

1. Start your local openEASE instance with the known start-webrob script (for further information have a look at the [openEASE documentation](http://www.knowrob.org/doc/docker))
2. Run the following command to start the server to control pepper and your local knowrob (including the ) that will be used by openEASE: `roslaunch knowrob_pepper_openease knowrob_pepper_full.launch`
3. First log in to your local openEASE instance at [https://localhost/user/sign-in](https://localhost/user/sign-in). After this go to [https://localhost/remote](https://localhost/remote) to use the knowrob you started in step 2.

You can now use the following predicates in openEASE:

```pepper_say(+TextToSay)```
Pepper says the given text. 

```pepper_point_at(+Translation,+FrameID,+TextToSay)```
To use this command localisation is necessary. Lets Pepper points at the point given by the Translation and the FrameID. After finishing the pointing action Pepper will say the Text given by TextToSay.


### Shutting down the Robot
To prevent the robot from moving weirdly when shutting down all your nodes, call (on the robot): 

    qicli call ALMotion.rest 
    
And if you want to turn it off completly via command line: 
    
    sudo shutdown -h now

One does not require a password for this. 

### Troubleshooting
Your jsX port might change, depending on how many devices are connected to your computer. If so, don't forget to adjust the $JOY_DEV variable in the .bashrc!

<!---
This might not  be needed anymore since it's an env. Variable!

It may happen the your controller is not on the JS0 port, in this case just go into the joy package

```sh
roscd joy
cd src
EDITOR_OF_CHOICE joy_node.cpp
```

In line 95 just change the "`/dev/input/js1"' to the right port.
-->
## Mapping

To capture a map you additionally need the following package:

https://github.com/humanrobotinteraction-plymouth/pepper_plymouth_ros
