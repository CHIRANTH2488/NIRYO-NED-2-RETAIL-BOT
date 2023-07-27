from pyniryo import *

# -- MUST Change these variables
simulation_mode = True
robot_ip_address, workspace_name = "169.254.200.200", "conveyorkejriwal"

#Can Change these variables
grid_dimension = (3, 3)  # conditioning grid dimension
vision_process_on_robot = False  # boolean to indicate if the image processing append on the Robot
display_stream = True  # Only used if vision on computer

# -- Should Change these variables
# The pose from where the image processing happens
observation_pose = PoseObject(0.164,-0.005,0.144,3.048,1.13,2.968)

# Center of the conditioning area
center_conditioning_pose = PoseObject(-0.04, -0.279, 0.13, -0.409, 1.335, -1.937)

# -- MAIN PROGRAM

def process(niryo_robot):
    """

    :type niryo_robot: NiryoRobot
    :rtype: None
    """
    # Initializing variables
    obj_pose = None
    try_without_success = 0
    count = 0
    if not vision_process_on_robot:
        mtx, dist = niryo_robot.get_camera_intrinsics()
    else:
        mtx = dist = None
    # Loop
    while try_without_success < 5:
        # Moving to observation pose
        niryo_robot.move_pose(observation_pose)

        if vision_process_on_robot:
            ret = niryo_robot.get_target_pose_from_cam(workspace_name,
                                                       height_offset=0.0,
                                                       shape=ObjectShape.ANY,
                                                       color=ObjectColor.ANY)
            obj_found, obj_pose, shape, color = ret

        else:  # Home made image processing
            img_compressed = niryo_robot.get_img_compressed()
            img = uncompress_image(img_compressed)
            img = undistort_image(img, mtx, dist)
            # extracting working area
            im_work = extract_img_workspace(img, workspace_ratio=1.0)
            if im_work is None:
                print("Unable to find markers")
                try_without_success += 1
                if display_stream:
                    cv2.imshow("Last image saw", img)
                    cv2.waitKey(25)
                continue

            # Applying Threshold on ObjectColor
            color_hsv_setting = ColorHSV.ANY.value
            img_thresh = threshold_hsv(im_work, *color_hsv_setting)

            if display_stream:
                show_img("Last image saw", img, wait_ms=100)
                show_img("Image thresh", img_thresh, wait_ms=100)
            # Getting biggest contour/blob from threshold image
            contour = biggest_contour_finder(img_thresh)
            if contour is None or len(contour) == 0:
                print("No blob found")
                obj_found = False
            else:
                img_thresh_rgb_w_contour = draw_contours(img_thresh, [contour])

                # Getting contour/blob center and angle
                cx, cy = get_contour_barycenter(contour)
                img_thresh_rgb_w_contour = draw_barycenter(img_thresh_rgb_w_contour, cx, cy)
                cx_rel, cy_rel = relative_pos_from_pixels(im_work, cx, cy)

                angle = get_contour_angle(contour)
                img_thresh_rgb_w_contour = draw_angle(img_thresh_rgb_w_contour, cx, cy, angle)

                show_img("Image thresh", img_thresh_rgb_w_contour, wait_ms=30)

                # Getting object world pose from relative pose
                obj_pose = niryo_robot.get_target_pose_from_rel(workspace_name,
                                                                height_offset=0.0,
                                                                x_rel=cx_rel, y_rel=cy_rel,
                                                                yaw_rel=angle)
                obj_found = True
        if not obj_found:
            try_without_success += 1
            continue
        # Everything is good, so we going to object
        niryo_robot.pick_from_pose(obj_pose)

        # Computing new place pose
        offset_x = count % grid_dimension[0] - grid_dimension[0] // 2
        offset_y = (count // grid_dimension[1]) % 3 - grid_dimension[1] // 2
        offset_z = count // (grid_dimension[0] * grid_dimension[1])
        place_pose = center_conditioning_pose.copy_with_offsets(0.05 * offset_x, 0.05 * offset_y, 0.025 * offset_z)

        # Placing
        niryo_robot.place_from_pose(place_pose)

        try_without_success = 0
        count += 1


if __name__ == '__main__':
    # Connect to robot
    robot = NiryoRobot(robot_ip_address)
    # Changing tool
    robot.update_tool()
    # Calibrate robot if robot needs calibration
    robot.calibrate_auto()
    # Launching main process
    process(robot)
    # Ending
    robot.go_to_sleep()
    # Releasing connection
    robot.close_connection()
