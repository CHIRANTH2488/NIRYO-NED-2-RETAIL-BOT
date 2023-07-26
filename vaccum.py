from niryo_robot_python_ros_wrapper import *
import rospy

rospy.init_node("niryo_ned")

bot = NiryoRosWrapper()

#
workspace_name = "conveyorkejriwal"

#bot.set_learning_mode(True)

bot.calibrate_auto()
bot.move_to_sleep_pose()

#
observation_pose = (0.193, -0.002, 0.245, -2.967, 1.301, -2.933)
#observation_pose = (0., 0., 0., 0., 1., -1.)
placingPose = (-0.022, -0.247, 0.334, -2.617, 1.269, 2.08)


#
bot.move_to_sleep_pose()
#bot.setup_electromagnet()

while(True):

	bot.move_pose(*observation_pose)

	ret = bot.move_to_object(workspace_name, -0.01, ObjectShape.ANY, ObjectColor.ANY)
	obj_found, obj_shape, obj_col = ret

	#x,y,z,r,p,y = obj_pose
	#objPose = [x,y,z,r,p,y]
	objPose = bot.get_pose_as_list()

	#bot.move_pose(*observation_pose)
	if obj_found:
		#bot.pick_from_pose(objPose[0],objPose[1],objPose[2],objPose[3],objPose[4],objPose[5])
		#bot.place_from_pose(placingPose[0],placingPose[1],placingPose[2],placingPose[3],placingPose[4],placingPose[5])

		#bot.activate_electromagnet('''pin id here''')
                bot.pull_air_vacuum_pump()
		bot.move_pose(*placingPose)
		bot.push_air_vacuum_pump()
		#bot.deactivate_electromagnet('''pin id here''')
	else:
                break


#bot.end()
bot.move_to_sleep_pose()
