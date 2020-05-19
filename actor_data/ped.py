#!/usr/bin/env python
# encoding: utf-8
import os
from data_class import Data_class
import numpy as np

db="/home/sunny/catkin_ws/src/atc-20121024.db"
a = Data_class(db)

actor_array = np.empty([91,1])
actor_list = actor_array.tolist()
#print(actor_array,actor_list)

def ad_x(x):
    return (x/1000)* 137.6/140 - 7.06 #7.06 6.94

def ad_y(y):
    return (y/1000)*68.35/60 + 7.815 #6.43 7.315

# initial setup
# list [ actor_order [ time_step [ data  ]  ] ]
#

actor_list[0][0] = [9190600, ad_x(-36668.0), ad_y(-3155.0),-3.073]
actor_list[1][0] = [9190700, ad_x(26636.0), ad_y(-15107.0),3.095]
actor_list[2][0] = [9190802, ad_x(-22342.0), ad_y(1687.0),-1.358]
actor_list[3][0] = [9194800, ad_x(3658.0), ad_y(-320.0),-0.401]
actor_list[4][0] = [9200100, ad_x(42021.0), ad_y(-17560.0),-0.914]
actor_list[5][0] = [9201900, ad_x(46605.0), ad_y(-22013.0),1.644]

#initial used_list and unused_list
used_list = []
used_list_ped = []
for i in range(6):
    used_list.append([i, actor_list[i][0][0]]) 
    # used_list [ actor_order, actor_ID_number]
    #
    used_list_ped.append(actor_list[i][0][0])

# print(np.shape(used_list))

unused_list = []
for i in range(85):
    unused_list.append(i+6)
    actor_list[i+6][0]=([200, 200, 200,200])

for i in range(1, 100):
    data = []
    data = a.extract_timewin_at(i)

    # initial and insert check_list
    check_list = []
    for k in range(len(data)):
        check_list.append(data[k][2])
        if check_list[k] not in used_list_ped:
            used_list.append([unused_list[0],data[k][2]])
            used_list_ped.append(data[k][2])
            unused_list.remove(unused_list[0])

    # check used list
#    for j in used_list:
#        print(j[1],used_list)
#        print(check_list)
#        if j[1] not in check_list:
#            unused_list.append(j[0])
#            unused_list.sort()
#            used_list_ped.remove(j[1])
#            used_list.remove(j)
#            print(used_list)

    #check used list
#   for j in range(len(used_list)):
#        if used_list[j][1] not in check_list:
#            print(used_list[j][1])
#            unused_list.append(used_list[j][0])
#            unused_list.sort()
#            used_list_ped.remove(used_list[j][1])
#            used_list.remove(used_list[j])
#            print(used_list)
#            print(check_list)

    z = []
    # check used_list
    for j in used_list:
        if j[1] in check_list:
            z.append(j)
        else:
            used_list_ped.remove(j[1])
            unused_list.append(j[0])
            unused_list.sort()

    used_list = z      

    #print(used_list_ped)
    #print(used_list)
    #print(check_list)

    #print(len(check_list),len(unused_list),len(data),len(used_list))

    for k in range(len(used_list)):
        actor_list[used_list[k][0]].append([data[k][2], ad_x(data[k][3]), ad_y(data[k][4]), data[k][8]])
    
    for k in range(len(unused_list)):
        actor_list[unused_list[k]].append([200, 200, 200,200])

#print(len(actor_list))
#print(len(actor_list[0][0]))

#for i in actor_list:
#    print(i)

f = open("ped.world","a")
f.write('<?xml version="1.0" ?>')
f.write('\n<sdf version="1.5">')
f.write('\n  <world name="default">')
f.write('\n    <include>')
f.write('\n      <uri>model://ground_plane</uri>')
f.write('\n    </include>')
f.write('\n    <include>')
f.write('\n      <uri>model://sun</uri>')
f.write('\n    </include>')
f.write('\n    <include>')
f.write('\n      <uri>model://mall_new_reduce_size</uri>')
f.write('\n    </include>\n')
f.close()

# redo the new actor list
#new_actor = []
#for i in range(50):
#    for j in actor_list[i]:
#        new_actor.append(j)



for j in range(10):
    f = open("ped.world","a")
    c = '\n    <actor name="actor%d">'%(j+1)
    f.write(c)
#    c1 ='\n      <pose>%g %g 0 0 0 0</pose>'%(actor_list[j][3][1],actor_list[j][3][2])
#    f.write(c1)
    f.write('\n      <pose>200 200 0 0 0 0</pose>')
    f.write('\n      <skin>')
    f.write('\n        <filename>moonwalk.dae</filename>')
    f.write('\n        <scale>1.0</scale>')
    f.write('\n      </skin>')
    f.write('\n      <animation name="walking">')
    f.write('\n        <filename>walk.dae</filename>')
    f.write('\n        <scale>1.000000</scale>')
    f.write('\n        <interpolate_x>true</interpolate_x>')
    f.write('\n      </animation>')
    f.write('\n      <script>')
    f.write('\n        <loop>false</loop>')
    f.write('\n        <delay_start>0</delay_start>')
    f.write('\n        <auto_start>true</auto_start>')
    f.write('\n        <trajectory id="0" type="walking">\n')
    f.close()

    #initial state:
    if actor_list[j][1][1] == 200:
        c1="\n          <waypoint>"
        c2="\n              <time>0.04</time>"
        c3="\n              <pose>200 200 0 0 0 0</pose>"
        c4="\n          </waypoint>\n"
        c = c1 + c2 + c3 + c4
        f = open("ped.world","a")
        f.write(c)
        f.close()

    #print('actor%d'%(j+1))

    for i in range(len(actor_list[j])-1):

        # case appear actor:
        if (actor_list[j][i][1] == 200) and (actor_list[j][i+1][1]!=200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%(i/5)
            c3="\n              <pose>200 200 0 0 0 0</pose>"
            c4="\n          </waypoint>\n"
            c = c1 + c2 + c3 + c4

            b1="\n          <waypoint>"
            b2="\n              <time>%g</time>"%((i)/5+0.2)
            b3="\n              <pose>%g %g 0 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            b4="\n          </waypoint>\n"
            b = b1 + b2 + b3 + b4

            f = open("ped.world","a")
            f.write(c)
            f.write(b)
            f.close()

        #case disappear actor:
        if (actor_list[j][i][1] != 200) and (actor_list[j][i+1][1]==200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%(i/5 + 0.2)
            c3="\n              <pose>200 200 0 0 0 0</pose>"
            c4="\n          </waypoint>\n"
            c = c1 + c2 + c3 + c4
            f = open("ped.world","a")
            f.write(c)
            f.close()

        if (actor_list[j][i][1]!=200) and (actor_list[j][i+1][1]!=200):
            c1="\n          <waypoint>"
            c2="\n              <time>%g</time>"%((i)/5+0.2)
            c3="\n              <pose>%g %g 0 0 0 %g</pose>"%(actor_list[j][i+1][1],actor_list[j][i+1][2], actor_list[j][i+1][3])
            c4="\n          </waypoint>\n"
            c = c1 + c2 + c3 + c4
            f = open("ped.world","a")
            f.write(c)
            f.close()     

    # final state:
    if actor_list[j][1][1] == 200:
        c1="\n          <waypoint>"
        c2="\n              <time>%g</time>"%(100/5+0.2)
        c3="\n              <pose>200 200 0 0 0 0</pose>"
        c4="\n          </waypoint>\n"
        c = c1 + c2 + c3 + c4
        f = open("ped.world","a")
        f.write(c)
        f.close()

    
    f = open("ped.world","a")
    f.write('\n        </trajectory>')
    f.write('\n      </script>')
    f.write('\n    </actor>\n')
    f.close()

f = open("ped.world","a")
f.write('  </world>')
f.write('\n</sdf>')
f.close()


#####
#for j in range(1):
#    for i in range(len(actor_list[j])-3):
#        print("            <waypoint>")
#        print("                <time>%g</time>"%((i)/25+0.04))
#        print("                <pose>%g %g 0 0 0 0</pose>"%(actor_list[j][i+3][1],actor_list[j][i+3][2]))
#        print("            </waypoint>")
#        print("")