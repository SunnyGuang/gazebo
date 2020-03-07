import rospy
from data_class import Data_class
#from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, DeleteModel, ModelState
from gazebo_msgs.srv import *
from tf.transformations import quaternion_from_euler

def create_ped(modelname, px, py, pz, rr, rp, ry, sx, sy, sz):
    f = open('/home/lab1/gazebo_link_attacher_ws/src/test/worlds/actor.sdf','r')
    ped = f.read()
    # Replace modelname
    ped = ped.replace('MODELNAME', str(modelname))

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


if __name__ == '__main__':
    rospy.init_node('spawn_models', anonymous=True)
    spawn_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    rospy.loginfo("Waiting for /gazebo/spawn_sdf_model service...")
    spawn_srv.wait_for_service()
    rospy.loginfo("Connected to service!")

    db="/home/lab1/gazebo_link_attacher_ws/src/test/scripts/atc-20121024.db"
    a = Data_class(db)
    
    ped_list = []

    for i in range(0,1):
        data=[]
        data=a.extract_timewin_at(i)

        # if no one was in ped_list, initially add ped
        if ped_list == []:
            for j in range(len(data)):
                ped_add = create_ped("%d"%data[j][2], data[j][3]/1000-10,data[j][4]/1000+10,0.0, 
                                    0.0, 0.0, 0.0,
                                    1.0, 1.0, 1.0)
                spawn_srv.call(ped_add)
                ped_list.append(data[j][2])
                print(ped_list)
                