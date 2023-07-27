from pyniryo import *
import cv2


ip = "169.254.200.200"

bot = NiryoRobot(ip)

bot.calibrate_auto()

observation = PoseObject(0.164,-0.005,0.144,3.048,1.13,2.968)
default = PoseObject(0.0,0.0,0.0,0.0,0.0,0.0)
place = PoseObject(-0.04, -0.279, 0.13, -0.409, 1.335, -1.937)
bot.move_joints([0.0,0.0,0.0,0.0,0.0,0.0])
bot.move_pose(observation)
mtx, dist = bot.get_camera_intrinsics()
'''
while(True):
    bot.move_pose(observation)
    found, shape, color = bot.vision_pick('conveyorkejriwal',-0.015, ObjectShape.ANY, ObjectColor.ANY)
    mtx, dist = bot.get_camera_intrinsics()
    if(found):
        bot.place_from_pose(place)
'''
while(True):
    mtx, dist = bot.get_camera_intrinsics()
    imgcomp = bot.get_img_compressed()
    imgraw = uncompress_image(imgcomp)
    imgdist = undistort_image(imgraw, mtx, dist)
    

    #concat = concat_imgs((imgraw, imgdist))

    img_gray = cv2.cvtColor(imgraw, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(imgraw, cv2.COLOR_BGR2RGB)
    concat = concat_imgs((imgraw,img_gray,img_rgb))
    key = show_img("",concat, wait_ms=30)


bot.end()
