#!/usr/bin/env python
# encoding: utf-8

from gazebo_msgs.srv import DeleteModel
import rospy

def delete_model():
    # 删除模型
    rospy.wait_for_service('/gazebo/delete_model')
    try:
        remove_model_proxy = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        remove_model_proxy("ped")
    except rospy.ServiceException, ex:
        print "Service call delete_model failed: %e" % ex

def main():
    rospy.init_node('spawn_models', anonymous=True)
    delete_model()

if __name__ == '__main__':
    main()