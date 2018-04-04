#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
This module is for the Point at function from Pepper inside a ROS Environment.
It uses code from https://github.com/suturo16/ros_pepper
"""


from std_srvs.srv import *
from naoqi_bridge_msgs.srv import *
import rospy
import qi
import os

# Mutes the robot if it is unmuted or
# unmute if the robot is muted
def pepper_trigger_mute(req):
    if audiodevice.isAudioOutMuted():
        audiodevice.muteAudioOut(False)
        return TriggerResponse(True,'Unmuted')
    else:
        audiodevice.muteAudioOut(True)
        return TriggerResponse(True,'Muted')

# Sets the mute status to the given bool
def pepper_set_mute(req):
    audiodevice.muteAudioOut(req.data)
    return TriggerResponse(True,'Muted')

# Shows the image of the given url
# by downloading it. Use old version
# of image if it's already downloaded
def pepper_show_image(req):
    tablet.showImage(req.data)
    return SetStringResponse(True)

# Shows the image of the given url
# without caching like in show_image
def pepper_show_image_no_cache(req):
    tablet.showImageNoCache(req.data)
    return SetStringResponse(True)

# Shows the image of the given url
def pepper_hide_image(req):
    tablet.hideImage()
    return TriggerResponse(True,'Hidden')

# Lets pepper say the given string
def pepper_say(req):
    tts.say(req.data)
    return SetStringResponse(True)

# Sets the volume to the given value
def pepper_set_volume(req):
    tts.setVolume(req.data)
    return SetFloatResponse(True,'Volume changed')

# Returns the current volume
def pepper_get_volume(req):
    return GetFloatResponse(tts.getVolume(),'Volume returned')

# Increases the volume by 5%
def pepper_increase_volume(req):
    volume = tts.getVolume()
    if volume >= 0.95:
        tts.setVolume(1.0)
    else:
        tts.setVolume(volume + 0.05)
    return TriggerResponse(True,'Increased volume')

# Increases the volume by 5%
def pepper_decrease_volume(req):
    volume = tts.getVolume()
    if volume <= 0.05:
        tts.setVolume(0.0)
    else:
        tts.setVolume(volume - 0.05)
    return TriggerResponse(True,'Decrease volume')

# Sets the autonomous life state
# Possible states:
# http://doc.aldebaran.com/2-5/ref/life/state_machine_management.html#autonomouslife-states
def pepper_autonomous_life_set_state(req):
    autonomous_life.setState(req.data)
    return SetStringResponse(True)

def pepper_autonomous_life_get_state(req):
    return GetStringResponse(autonomous_life.getState())

# Sets state to interactive if 
def pepper_autonomous_life_trigger_interactivity(req):
    if not autonomous_life.getState() == 'interactive':
        rospy.log('Switch to interactive mode')
        autonomous_life.setState('interactive')
        return TriggerResponse(True,'interactivity enabled')
    else:
        rospy.log('Disable autonomous life')
        autonomous_life.setState('disabled')
        return TriggerResponse(True,'autonomous life disabled')


# The server announces the service to our ROSCORE and stays open until the Core is closed or the Node is manually
# terminated.
def pepper_ros_server():
    rospy.init_node('pepper_ros_server')
    prefix = rospy.get_param("tf_prefix","")
    # initializing our transformer!
    s_mute_trigger = rospy.Service(prefix+'/mute', Trigger, pepper_trigger_mute)
    s_set_mute = rospy.Service(prefix+'/set_mute', SetBool, pepper_set_mute)
    s_tablet_show_image = rospy.Service(prefix+'/show_image', SetString, pepper_show_image)
    s_tablet_show_image_nc = rospy.Service(prefix+'/show_image_no_cache', SetString, pepper_show_image_no_cache)
    s_tablet_hide = rospy.Service(prefix+'/hide_image', Trigger, pepper_hide_image)
    s_say = rospy.Service(prefix+'/say', SetString, pepper_say)
    s_set_volume = rospy.Service(prefix+'/set_volume', SetFloat, pepper_set_volume)
    s_get_volume = rospy.Service(prefix+'/get_volume', GetFloat, pepper_get_volume)
    s_increase_volume = rospy.Service(prefix+'/increase_volume',Trigger,pepper_increase_volume)
    s_decrease_volume = rospy.Service(prefix+'/decrease_volume',Trigger,pepper_decrease_volume)
    s_set_life = rospy.Service(prefix+'/autonomous_life/set_state', SetString, pepper_autonomous_life_set_state)
    s_get_life = rospy.Service(prefix+'/autonomous_life/get_state', GetString, pepper_autonomous_life_get_state)
    s_get_life = rospy.Service(prefix+'/autonomous_life/trigger_interactivity', Trigger, pepper_autonomous_life_trigger_interactivity)
    rospy.spin()


# We are using the NAO API from Aldebaran, we start the session with the given IP address. And save the TTS as
# a global variable in this script. That is the best way of getting it inside the Say Method.
if __name__ == "__main__":

    session = qi.Session()
    try:
        session.connect("tcp://" + str(os.environ['NAO_IP']) + ":" + str(9559))
    # this will give us some light if something breaks while starting the service.
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + str(os.environ['NAO_IP']) + "\" on port " + str(9559)
               + ".\n" + "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    global audiodevice
    global tablet
    global tts
    # Get the different services
    autonomous_life = session.service("ALAutonomousLife")
    audiodevice = session.service("ALAudioDevice")
    tablet = session.service("ALTabletService")
    tts = session.service("ALTextToSpeech")

    pepper_ros_server()