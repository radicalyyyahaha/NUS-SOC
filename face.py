import cv2

from sklearn.metrics.pairwise import cosine_similarity

from tools import print1


def get_rotate_fast():
    count_rotate_threshold = 4  # TODO
    return count_rotate_threshold


def get_rotate_medium():
    count_rotate_threshold = 8  # TODO
    return count_rotate_threshold


def start_face(frame_width, frame_height, cap, your_face_encoding, app):
    # 检测标志
    flag_detect = False
    face_similarity_threshold = 0.6  # TODO

    # 界限
    left_line_x = frame_width // 3  # TODO
    right_line_x = frame_width // 3 * 2  # TODO
    bottom_line_y = frame_height // 4  # TODO

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
    count_left_right_threshold = 7  # TODO
    count_forward = 0
    count_forward_threshold_fast = 2  # TODO
    count_forward_threshold_slow = 3  # TODO
    count_forward_threshold = count_forward_threshold_fast

    # 摄像头
    camera_cam = 120
    camera_cam_threshold = 175  # TODO：调整至检测到人脸的最佳角度
    forward_slow_camera_cam_threshold = 135
    count_camera_up = 0
    count_camera_up_threshold = 3  # TODO

    # 停止
    count_stop = 0
    count_stop_threshold = 10  # TODO

    # 初始化摄像头
    camera_cam = print1("B")
    for i in range(12):
        camera_cam = print1("U")

    out = False
    while not out:
        ret, frame = cap.read()

        if not ret:
            break

        results = app.get(frame)

        # 绘制边界
        cv2.line(frame, (left_line_x, 0), (left_line_x, frame_height), (255, 0, 0), 2)
        cv2.line(frame, (right_line_x, 0), (right_line_x, frame_height), (255, 0, 0), 2)
        cv2.line(frame, (0, bottom_line_y), (frame_width, bottom_line_y), (255, 0, 0), 2)

        if not results:
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
            for face in results:
                encoding = face.embedding.reshape(1, -1)
                similarity = cosine_similarity(encoding, your_face_encoding)[0][0]
                if similarity > face_similarity_threshold:
                    if not flag_detect:
                        print1('X')
                        flag_detect = True

                    # 绘制框
                    bbox = face.bbox.astype(int)
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                    xc = (bbox[0] + bbox[2]) // 2
                    yc = (bbox[1] + bbox[3]) // 2

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
                        if yc > bottom_line_y:
                            count_forward += 1

                            # update_forward_speed
                            if camera_cam < forward_slow_camera_cam_threshold:
                                count_forward_threshold = count_forward_threshold_slow
                            else:
                                count_forward_threshold = count_forward_threshold_fast

                            if count_forward > count_forward_threshold:
                                print1('W')
                                count_forward = 0
                        elif camera_cam < camera_cam_threshold:
                            count_camera_up += 1
                            if count_camera_up > count_camera_up_threshold:
                                camera_cam = print1('U')
                                count_camera_up = 0
                        else:
                            count_stop += 1
                            if count_stop > count_stop_threshold:
                                print1('X')
                                print1('B')
                                print1('R')
                                out = True
                                cv2.destroyAllWindows()
                                break

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
