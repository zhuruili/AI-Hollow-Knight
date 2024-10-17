"""
基于yolov10的目标检测
"""
import cv2 as cv
import numpy as np
import torch
import pygetwindow
from PIL import ImageGrab
from ultralytics import YOLO

from .init import window_title

def detect(model='backend\\tasks\models\BOSS.pt'):
    """
    目标检测
    :param model: 模型路径
    """
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    if window:
        x, y, w, h = window.left, window.top, window.width, window.height
    yolo = YOLO(model)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    yolo.to(device)

    while True:
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img_src = cv.cvtColor(np.array(img), cv.COLOR_BGR2RGB)
        size_x, size_y = img_src.shape[1], img_src.shape[0]
        img_det = cv.resize(img_src, (640, 640))
        results = yolo.predict(source=img_det, imgsz=640, conf=0.25, save=False)
        boxes = results[0].boxes.xywhn
        for box in boxes:
            cv.rectangle(
                img_src,
                (int((box[0] - box[2]/2)*size_x), int((box[1] - box[3]/2)*size_y)),
                (int((box[0] + box[2]/2)*size_x), int((box[1] + box[3]/2)*size_y)),
                (255, 255, 0),
                thickness=2
            )
        cv.imshow("detect", img_src)
        if cv.waitKey(1) == 27:
            break
        pass

    




