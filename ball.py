import cv2

from tools import print1


def get_box_coordinates(results):
    for result in results:
        for box in result.boxes:
            if box.cls == 32:
                return box.xyxy[0].tolist()
    return None


def is_sportball_detected(results):
    for result in results:
        for box in result.boxes:
            if box.cls == 32:
                return True
    return False


def get_rotate_fast():
    count_rotate_threshold = 4  # TODO
    return count_rotate_threshold


def get_rotate_medium():
    count_rotate_threshold = 8  # TODO
    return count_rotate_threshold


def start_ball(frame_width, frame_height, cap, model):
    # 检测标志
    flag_detect = False

    # 界限
    left_line_x = frame_width // 3  # TODO
    right_line_x = frame_width // 3 * 2  # TODO
    top_line_y = frame_height // 3 * 2  # TODO

    # 左右信息记忆
    center_line_x = frame_width // 2
    left_right_info_count = 0
    left_right_info_threshold = 1  # TODO
    left_right_disappear = 'none'

    # 旋转
    count_rotate = 0
    count_rotate_threshold = get_rotate_fast()

    # 前进
    count_left = 0
    count_right = 0
    count_left_right_threshold = 10  # TODO
    count_forward = 0
    count_forward_threshold_fast = 2  # TODO
    count_forward_threshold_slow = 8  # TODO
    count_forward_threshold = count_forward_threshold_fast

    # 摄像头
    camera_cam = 120
    camera_cam_threshold = 70  # TODO：调整至检测到球的最佳角度
    forward_slow_camera_cam_threshold = 90
    count_camera_down = 0
    count_camera_down_threshold = 3  # TODO

    # 停止
    count_stop = 0
    count_stop_threshold = 15  # TODO

    # 初始化摄像头和手臂
    camera_cam = print1('B')
    print1('R')

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model.predict(frame, device='cuda:0', classes=[32])

        # 绘制边界
        cv2.line(frame, (left_line_x, 0), (left_line_x, frame_height), (255, 0, 0), 2)
        cv2.line(frame, (right_line_x, 0), (right_line_x, frame_height), (255, 0, 0), 2)
        cv2.line(frame, (0, top_line_y), (frame_width, top_line_y), (255, 0, 0), 2)

        if not is_sportball_detected(results):
            count_rotate += 1

            if not flag_detect:
                # 未找到前快速旋转
                count_rotate_threshold = get_rotate_fast()
            else:
                # 找到之后丢失中速旋转
                count_rotate_threshold = get_rotate_medium()

            if count_rotate > count_rotate_threshold:
                if left_right_info_count > left_right_info_threshold and left_right_disappear == 'right':
                    print1('D')
                else:
                    print1('A')
                count_rotate = 0
        else:
            if not flag_detect:
                print1('X')
                flag_detect = True

            # 绘制框
            box_coords = get_box_coordinates(results)
            x1, y1, x2, y2 = map(int, box_coords)
            xc = (x1 + x2) // 2
            yc = (y1 + y2) // 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 记录左右信息
            if xc < center_line_x:
                if left_right_disappear != 'right':
                    left_right_info_count += 1
                left_right_disappear = 'left'
            elif xc > center_line_x:
                if left_right_disappear != 'left':
                    left_right_info_count += 1
                left_right_disappear = 'right'
            else:
                left_right_info_count += 1

            # x值不满足
            if xc < left_line_x:
                count_left += 1
                if count_left > count_left_right_threshold:
                    print1('A')
                    count_left = 0
            elif xc > right_line_x:
                count_right += 1
                if count_right > count_left_right_threshold:
                    print1('D')
                    count_right = 0
            # x值满足
            else:
                if yc < top_line_y:
                    count_forward += 1

                    # update_forward_speed
                    if camera_cam < forward_slow_camera_cam_threshold:
                        count_forward_threshold = count_forward_threshold_slow
                    else:
                        count_forward_threshold = count_forward_threshold_fast

                    if count_forward > count_forward_threshold:
                        print1('W')
                        count_forward = 0
                elif camera_cam > camera_cam_threshold:
                    count_camera_down += 1
                    if count_camera_down > count_camera_down_threshold:
                        camera_cam = print1('N')
                        count_camera_down = 0
                else:
                    count_stop += 1
                    if count_stop > count_stop_threshold:
                        print1('X')
                        print1('F')
                        print1('W')
                        cv2.destroyAllWindows()
                        break

        cv2.imshow('YOLOv9 Human Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
