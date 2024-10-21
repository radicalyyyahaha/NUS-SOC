import warnings
from time import sleep

import cv2
import requests
import torch
from insightface.app import FaceAnalysis
from ultralytics import YOLO

import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning, module="insightface.utils.transform")

url = 'http://172.25.106.228'

camera_cam = 120

cap = cv2.VideoCapture(f'{url}:5001/video_feed')

sleep(3)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


def print1(direction):
    try:
        response = requests.post(f'{url}:5000/control', data={'command': direction})
        if response.status_code == 200:
            print(f"Command {direction} sent successfully")
        else:
            print(f"Failed to send command {direction}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    if direction == 'W':
        print("Direction: Forward")
    elif direction == 'A':
        print("Direction: Left")
    elif direction == 'D':
        print("Direction: Right")
    elif direction == 'S':
        print("Direction: Backward")
    elif direction == 'X':
        print("Direction: Stop")
    elif direction == 'U':
        print("Direction: Camera Up")
    elif direction == 'N':
        print("Direction: Camera Down")
    elif direction == 'B':
        print("Direction: Camera Reset")
    elif direction == 'F':
        print("Direction: Fetch ball")
        sleep(1)
    elif direction == 'R':
        print("Direction: Release ball")
        sleep(1)
    elif direction == 'C':
        print("Action: Circle")
    elif direction == 'P':
        print("Action: Arm up and down")

    update_camera_cam(direction)
    return camera_cam


def update_camera_cam(direction):
    global camera_cam

    if direction == 'U':
        camera_cam = camera_cam + 3
    elif direction == 'N':
        camera_cam = camera_cam - 3
    elif direction == 'B':
        camera_cam = 120

    if camera_cam > 180:
        camera_cam = 180
    elif camera_cam < 68:
        camera_cam = 68


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

if torch.cuda.is_available():
    cuda_version = torch.version.cuda
    print(f"CUDA version: {cuda_version}")
else:
    print("CUDA is not available.")


model = YOLO('yolov9e.pt').to(device)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

app = FaceAnalysis(providers=['CUDAExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

your_face_encoding = np.load('your_face_encoding_zyq.npy').reshape(1, -1)
