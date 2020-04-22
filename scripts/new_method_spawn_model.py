#!/usr/bin/env python
# encoding: utf-8
from gazebo_msgs.srv import DeleteModel
from gazebo_msgs.msg import ModelState
import rospy
import os
from data_class import Data_class

def add_model(modelname,px,py):
    GAZEBO_MODEL_PATH = "~/.gazebo/models/"
    model_to_add = 'person_walking' # string
    os.system("rosrun gazebo_ros spawn_model -file " + GAZEBO_MODEL_PATH + model_to_add +"/model.sdf -sdf -model " +  "%d -x %d -y %d" %(modelname,px,py))


def pose_publish(modelname,px,py):
    pose_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
    pose_msg = ModelState()
    pose_msg.model_name = '%s'%modelname

    # rospy.loginfo('update position: %d,%d'%(px,py))
    
    pose_msg.pose.position.x = px   
    pose_msg.pose.position.y = py
    pose_msg.pose.position.z = 0

    pose_pub.publish(pose_msg)


def delete_model(modelname):
    rospy.wait_for_service('/gazebo/delete_model')
    try:
        remove_model_proxy = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        remove_model_proxy("%s"%modelname)
    except rospy.ServiceException, ex:
        print "Service call delete_model failed: %e" % ex


def fix_x(x):
    return x * 137.6/140 - 6.94 #7.06

def fix_y(y):
    return y*68.35/60 + 7.315 #6.43


if __name__ == '__main__':
    rospy.init_node('main', anonymous=True)
        
    db="/home/sunny/catkin_ws/src/atc-20121024.db"
    a = Data_class(db)
    ped_list = []

    for i in range(0,5001):
        data=[]
        data=a.extract_timewin_at(i)

        # if no one was in ped_list, initially add the peds
        if ped_list == []:
            for j in range(len(data)):
            #    rospy.loginfo(data[j][2])
                #add_model(data[j][2], data[j][3]/1000-10,data[j][4]/1000+2)
                add_model(data[j][2],fix_x(data[j][3]/1000),fix_y(data[j][4]/1000))
                ped_list.append(data[j][2])
        
        else:
            check_list=[]
            pos_update = []

            # load data to check list & pos_update list , and check for adding new ped
            for k in data:
                check_list.append(k[2])
                # pos_update.append([k[3]/1000-10,k[4]/1000+2])
                pos_update.append([fix_x(k[3]/1000),fix_y(k[4]/1000)])
                if k[2] not in ped_list:
                    # add_model(k[2],k[3]/1000-10,k[4]/1000+2)
                    add_model(k[2],fix_x(k[3]/1000),fix_y(k[4]/1000))
                    ped_list.append(k[2])

            # check for removing old ped
            for o in ped_list:
                if o not in check_list:
                    delete_model('%d'%o)
                    ped_list.remove(o)

            z = 0
            while not rospy.is_shutdown():
                try:
                    if z >=len(ped_list):
                        break
                    else:
                        rospy.sleep(0.001)
                        pose_publish('%s'%check_list[z], pos_update[z][0], pos_update[z][1])
                except rospy.ROSInterruptException:
                    pass
                z += 1
        
        rospy.loginfo('%d'%i)

        rospy.sleep(0.04)
