from pyniryo import *
import numpy as np
import cv2

# Connecting to robot
robot = NiryoRobot("169.254.200.200")
robot.calibrate_auto()

# Getting calibration param
mtx, dist = robot.get_camera_intrinsics()
# Moving to observation pose
observation = PoseObject(0.164,-0.005,0.144,3.048,1.13,2.968)
default = PoseObject(0.0,0.0,0.0,0.0,0.0,0.0)
place = PoseObject(-0.04, -0.279, 0.13, -0.409, 1.335, -1.937)
robot.move_joints([0.0,0.0,0.0,0.0,0.0,0.0])
robot.move_pose(observation)

while "User do not press Escape neither Q":
    # Getting image
    img_compressed = robot.get_img_compressed()
    
    #Uncompressing image
    img_raw = uncompress_image(img_compressed)
    
    # Undistorting
    img_undistort = undistort_image(img_raw, mtx, dist)
    
    # Trying to find markers
    workspace_found, res_img_markers = debug_markers(img_undistort)
    # Trying to extract workspace if possible
    if workspace_found:
        img_workspace = extract_img_workspace(img_undistort, workspace_ratio=1.0)
    else:
        img_workspace = None

    # --- --------- --- #
    # --- YOUR CODE --- #
    # --- --------- --- #
    '''img_gray = cv2.cvtColor(img_undistort, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_undistort, cv2.COLOR_BGR2RGB)
    img_gray_blur = cv2.GaussianBlur(img_gray, (9, 9), 2)
    edges = cv2.Canny(img_gray_blur, 30, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=80)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img_undistort, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(img_undistort,(x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
'''
   #concat = concat_imgs((imgraw,img_gray,img_rgb))
    #cv2.imshow("Coin Detection", concat)
    

    # - Display
    # Concatenating raw image and undistorted image
    concat_ims = concat_imgs((img_raw, img_undistort))
    # Concatenating extracted workspace with markers annotation
    if img_workspace is not None:
        resized_img_workspace = resize_img(img_workspace, height=res_img_markers.shape[0])
        res_img_markers = concat_imgs((res_img_markers, resized_img_workspace))
    # Showing images
    #show_img("Images raw & undistorted", concat_ims)

    img_gray = cv2.cvtColor(res_img_markers, cv2.COLOR_BGR2GRAY)
    #img_rgb = cv2.cvtColor(img_undistort, cv2.COLOR_BGR2RGB)
    img_gray_blur = cv2.GaussianBlur(img_gray, (9, 9), 2)
    edges = cv2.Canny(img_gray_blur, 30, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=80)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(res_img_markers, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(res_img_markers,(x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    key = show_img("Markers", res_img_markers, wait_ms=30)

    if key in [27, ord("q")]:  # Will break loop if the user press Escape or Q
        break
