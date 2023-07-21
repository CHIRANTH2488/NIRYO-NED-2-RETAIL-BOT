from niryo_robot_python_ros_wrapper import *
import rospy

rospy.init_node("niryo_ned")

bot = NiryoRosWrapper()

#
workspace_name = "gazebo_1"

bot.set_learning_mode(True)

bot.calibrate_auto()


#
observation_pose = (0.174, 0., 0.211, 3.137, 1.478, 3.137)
#observation_pose = (0., 0., 0., 0., 1., -1.)
place_pose = (0., 0.25, 0.1, 0., 1.57, 1.57)


#
for i in range(0,5):
bot.move_pose(*observation_pose)
# Trying to pick target using camera
ret = bot.vision_pick(workspace_name,
                              height_offset=0,
                              shape=ObjectShape.ANY,
                              color=ObjectColor.ANY)
obj_found, shape_ret, color_ret = ret
if obj_found:
    bot.place_from_pose(*place_pose)

bot.set_learning_mode(True)
