from pyniryo import *
import cv2
import numpy as np

ip = "169.254.200.200"

bot = NiryoRobot(ip)

bot.calibrate_auto()

observation = PoseObject(0.164,-0.005,0.144,3.048,1.13,2.968)
default = PoseObject(0.0,0.0,0.0,0.0,0.0,0.0)
place = PoseObject(-0.04, -0.279, 0.13, -0.409, 1.335, -1.937)
bot.move_joints([0.0,0.0,0.0,0.0,0.0,0.0])
bot.move_pose(observation)


cv2.namedWindow("Coin Detection", cv2.WINDOW_NORMAL)

'''def pick_up_coin(x, y, r):
    # Calculate the 3D position of the detected coin relative to the robot's base frame
    coin_pos = bot.get(x, y, mtx, dist)

    # Define the desired pose to reach the coin position (you may need to adjust these values)
    coin_pose = PoseObject(coin_pos[0], coin_pos[1], coin_pos[2] + 0.03, 0.0, 1.57, 0.0)

    # Move the robot's arm to the desired pose
    bot.move_pose(coin_pose)

    # Open the gripper
    bot.open_gripper()

    # Move the robot down to pick up the coin
    bot.move_pose(coin_pose.with_z(coin_pos[2]))

    # Close the gripper to pick up the coin
    bot.close_gripper()

    # Lift the coin
    bot.move_pose(place)
'''
while True:
    mtx, dist = bot.get_camera_intrinsics()
    imgcomp = bot.get_img_compressed()
    imgraw = uncompress_image(imgcomp)
    imgdist = undistort_image(imgraw, mtx, dist)

    img_gray = cv2.cvtColor(imgraw, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(imgraw, cv2.COLOR_BGR2RGB)
    img_gray_blur = cv2.GaussianBlur(img_gray, (9, 9), 2)
    edges = cv2.Canny(img_gray_blur, 30, 150)


    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=80)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(imgraw, (x, y), r, (0, 255, 0), 4)
            cv2.circle(img_gray, (x, y), r, (0, 255, 0), 4)
            cv2.circle(img_rgb, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(imgraw, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            #pick_up_coin(x, y, r)

    concat = concat_imgs((imgraw,img_gray,img_rgb))
    cv2.imshow("Coin Detection", concat)

    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
bot.end()
