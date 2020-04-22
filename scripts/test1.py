#!/usr/bin/env python
# encoding: utf-8
from gazebo_msgs.srv import DeleteModel
from gazebo_msgs.msg import ModelState
import rospy
import os
from data_class import Data_class

def pose_publish(px,py):
    pose_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
    pose_msg = ModelState()
    pose_msg.model_name = 'actor1'

    # rospy.loginfo('update position: %d,%d'%(px,py))
    
    pose_msg.pose.position.x = px   
    pose_msg.pose.position.y = py
    pose_msg.pose.position.z = 0

    pose_pub.publish(pose_msg)


if __name__ == '__main__':
    rospy.init_node('main', anonymous=True)
    
    px =0
    py =0

    while not rospy.is_shutdown():
        pose_publish(px, py)
        px+=1
        py+=1
        rospy.sleep(0.04)