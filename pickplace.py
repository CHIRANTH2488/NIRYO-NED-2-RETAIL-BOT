from niryo_robot_python_ros_wrapper import *
import rospy

rospy.init_node("niryo_ned")

bot = NiryoRosWrapper()

#
workspace_name = "conveyorkejriwal"

bot.move_to_sleep_pose()

#bot.set_learning_mode(True)

bot.calibrate_auto()


#
observation_pose = (0.193, -0.002, 0.245, -2.967, 1.301, -2.933)
#observation_pose = (0., 0., 0., 0., 1., -1.)
#place_pose=(0.193, -0.002, 0.245, -2.967, 1.301, -2.933)
place_pose = (-0.003, -0.247, 0.147, -2.912, 1.468, 1.738)


#
for i in range(0,5):
    bot.move_pose(*observation_pose)
    # Trying to pick target using camera
    ret = bot.vision_pick(workspace_name,
                              height_offset=-0.02,
                              shape=ObjectShape.ANY,
                              color=ObjectColor.ANY)
    obj_found, shape_ret, color_ret = ret
    if obj_found:
        #bot.set_pose(0.152,-0.211,0.333,0.009,1.312,-0.806)
        bot.place_from_pose(*place_pose)

#bot.set_learning_mode(True)

zbot.move_to_sleep_pose()
