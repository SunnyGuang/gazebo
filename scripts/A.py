#!/usr/bin/env python
# encoding: utf-8
from gazebo_msgs.srv import DeleteModel
from gazebo_msgs.msg import ModelState
import rospy
import os

def pose_publish(modelname):
    pose_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
    pose_msg = ModelState()
    pose_msg.model_name = '%s'%modelname

    pose_msg.pose.position.x = 2
    pose_msg.pose.position.y = 8
    pose_msg.pose.position.z = 0

    # rospy.loginfo('update position: %d,%d'%(px,py))
    while not rospy.is_shutdown():
        #rospy.loginfo(pose_msg.pose.position.x,pose_msg.pose.position.y)
        if pose_msg.pose.position.x <= 10:
            pose_msg.pose.position.x +=0.028284
            pose_msg.pose.position.y -=0.028284

        elif pose_msg.pose.position.x <= 15:
            pose_msg.pose.position.x +=0.028284
            pose_msg.pose.position.y -=0.028284

        elif pose_msg.pose.position.x <= 20:
            pose_msg.pose.position.x +=0.0343
            pose_msg.pose.position.y -=0.02058

        elif pose_msg.pose.position.x <= 25:
            pose_msg.pose.position.x +=0.03714
            pose_msg.pose.position.y -=0.014856 

        elif pose_msg.pose.position.x <= 30:
            pose_msg.pose.position.x +=0.038313
            pose_msg.pose.position.y -=0.011494              

        elif pose_msg.pose.position.x <=35:
            pose_msg.pose.position.x +=0.039223
            pose_msg.pose.position.y -= 0.0078446

        elif pose_msg.pose.position.x <=40:
            pose_msg.pose.position.x +=0.038313
            pose_msg.pose.position.y -= 0.011494

        elif pose_msg.pose.position.x <= 50:
            pose_msg.pose.position.x +=0.039223
            pose_msg.pose.position.y -=0.0078446 

        else:
            break

        pose_msg.pose.position.z = 0
        pose_pub.publish(pose_msg)
        rospy.sleep(0.04)


if __name__ == '__main__':
    rospy.init_node('main', anonymous=True)
    pose_publish('mybot')