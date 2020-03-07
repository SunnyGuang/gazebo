# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:16:53 2020

@author: lab1
"""

#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, SpawnModelResponse
from copy import deepcopy
from tf.transformations import quaternion_from_euler

sdf_ped = """<?xml version="1.0" ?>
<sdf version="1.5">
   <world name="default">

      <actor name="actor">
         <skin>
            <filename>walk.dae</filename>
            <scale>1.0</scale>
         </skin>
         
         <pose>0 0 0 0 0 0</pose>
         
         <animation name="walking">
            <filename>walk.dae</filename>
            <scale>1</scale>
            <interpolate_x>true</interpolate_x>
         </animation>
         <script>
            <loop>true</loop>
            <delay_start>0</delay_start>
            <auto_start>true</auto_start>
            <trajectory id="0" type="walking">
            </trajectory>
         </script>
      </actor>

   </world>
</sdf>
"""

def create_ped_request(modelname, px, py):
    """Create a SpawnModelRequest with the parameters of the cube given.
    modelname: name of the model for gazebo
    px py: position of the ped"""
    
    ped = deepcopy(sdf_ped)
    
    # Replace Modelname
    ped = ped.replace('MODELNAME',str(modelname))
    
    req = SpawnModelRequest()
    req.model_name = modelname
    req.model_xml = ped
    req.initial_pose.orientation.x = px
    req.initial_pose.orientation.y = py
    
    return req
    
if __name__ == '__main__':
    rospy.init_node('spawn_ped')
    spawn_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model',SpawnModel)
    rospy.loginfo("Waiting for /gazebo/spawn_sdf_model service...")
    spawn_srv.wait_for_service()
    rospy.loginfo("Connected to service!")
    
    #Spawn Object 1
    rospy.loginfo("Spawning ped")
    req1 = create_ped_request("ped1", 0.0, 0.0)
    spawn_srv.call(req1)
    rospy.sleep(1.0)
