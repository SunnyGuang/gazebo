# gazebo

Current Progress:
Have scene(rebuild, size reduced), models, ped interface, mobile robot with gpu_lidar

Running SDF Model Peds:

Launch file:
roslaunch gazebo_pro mall_reduce_size.launch (run the scene and spawn mobile robot)

Node:
rosrun gazebo_pro new_method_spawn_model.py

Running SDF Actor Peds:

For actor running, the trajectories have already processed by actor_data/ped.py, produced a new world file with the trajectory in sdf world file. Run the launch file with the spawn the robot with gpu based lidar sensor:
roslaunch gazebo_pro mybot_world.launch

I didn't upload dataset to this repo (too big). If you need the dateset, I will try to send to you. It existed some issues, I will talk to you in online meeting.
