#!/usr/bin/env python

import rospy
from data_class import Data_class
#from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, DeleteModel, ModelState
from gazebo_msgs.srv import *
from tf.transformations import quaternion_from_euler


#def del_model( modelName ):
#    """ Remove the model with 'modelName' from the Gazebo scene """
#    # delete_model : gazebo_msgs/DeleteModel
#    del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel) # Handle to model spawner
#    # rospy.wait_for_service('gazebo/delete_model') # Wait for the model loader to be ready 
#    # FREEZES EITHER WAY
#    del_model_prox(modelName) # Remove from Gazebo
#    
    
    
def create_ped(modelname, px, py, pz, rr, rp, ry, sx, sy, sz):
    f = open('/home/lab1/gazebo_link_attacher_ws/src/test/worlds/actor.sdf','r')
    ped = f.read()
    # Replace modelname
    ped = ped.replace('actor', str(modelname))

    req = SpawnModelRequest()
    req.model_name = modelname
    req.model_xml = ped
    req.initial_pose.position.x = px
    req.initial_pose.position.y = py
    req.initial_pose.position.z = pz

    q = quaternion_from_euler(rr, rp, ry)
    req.initial_pose.orientation.x = q[0]
    req.initial_pose.orientation.y = q[1]
    req.initial_pose.orientation.z = q[2]
    req.initial_pose.orientation.w = q[3]

    return req
    
    
def pose_update(modelname, px, py):
    pose_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)
    pose_msg = ModelState()
    pose_msg.model_name = 'modelname'
    pose_msg.position.x = px
    pose_msg.position.y = py
    pose_msg.position.z = 0
    pose_pub.publish(pose_msg)
    
#def delete_model(modelname):
#    # Initialise a ROS node with the name service_client
#    rospy.init_node('service_client')
#    # Wait for the service client /gazebo/delete_model to be running
#    rospy.wait_for_service('/gazebo/delete_model')  
#    # Create the connection to the service
#    delete_model_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
#    # Create an object of type DeleteModelRequest
#    delete_model_object = DeleteModelRequest()
#    # Fill the variable model_name of this object with the desired value
#    delete_model_object.model_name = "modelname"
#    # Send through the connection the name of the object to be deleted by the service
#    result = delete_model_service(delete_model_object)
#    # Print the result given by the service called
#    print result
    
def delete_model(namemodel):
    rospy.wait_for_service('/gazebo/delete_sdf_model')
    delete_model = rospy.ServiceProxy('/gazebo/delete_sdf_model', DeleteModel)
    delete_model(namemodel)
    
    


if __name__ == '__main__':
    rospy.init_node('spawn_models', anonymous=True)
    spawn_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    rospy.loginfo("Waiting for /gazebo/spawn_sdf_model service...")
    spawn_srv.wait_for_service()
    rospy.loginfo("Connected to service!")

#    # Spawn ped
#    rospy.loginfo("Spawning Ped")
#    req1 = create_ped("ped",
#                              0.0, 0.0, 0.51,  # position
#                              0.0, 0.0, 0.0,  # rotation
#                              1.0, 1.0, 1.0)  # size
#    spawn_srv.call(req1)
#    rospy.sleep(1.0)
    
    # delete ped 
    
#    # Delete Ped
#    rospy.loginfo("Deleting Ped")
#    req1 = delete_model("ped")
    
    
#    del_model(req1)
    
    
    #load database
    db="/home/lab1/gazebo_link_attacher_ws/src/test/scripts/atc-20121024.db"
    a = Data_class(db)
    
    ped_list = []    
    
    for i in range(0,11):
        data=[]
        data=a.extract_timewin_at(i)
        ped_add=[]
        
        
        # if no one was in ped_list, initially add ped
        if ped_list == []:
            for j in range(len(data)):
                ped_add = create_ped("%d"%data[j][2], data[j][3]/1000-10,data[j][4]/1000+10,0.0, 
                                    0.0, 0.0, 0.0,
                                    1.0, 1.0, 1.0)
                spawn_srv.call(ped_add)
                ped_list.append(data[j][2])
                
        # check whether existed, if new adding not exsit in ped_list, remove them
        check_list=[]
        for k in data:
            check_list.append(k[2])
        for o in ped_list:
            if o not in check_list:
                delete_model(o)
                ped_list.remove(o)
                
        
        # new coming in new time step, add him                
        for t in data:
            if t[2] not in ped_list:
                ped_add = create_ped("%d"%t[2], t[3]/1000-10,t[4]/1000+10,0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
                spawn_srv.call(ped_add)
                ped_list.append(t[2])
            else: # update the new pose for the left
                pose_update(t[2],data[j][3] - 10,data[j][4])
            