from ultralytics import YOLO
from roboflow import Roboflow
from pathlib import Path
import os
from os.path import expanduser



# from roboflow import Roboflow
# rf = Roboflow(api_key="VJgpCQH1sZG2V5bCfwQi")
# project = rf.workspace("mohamed-nabil-g0a7y").project("yolo_v4_tiny")
# dataset = project.version(1).download("yolov8")


# f = Path(r'C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\YOLO_V4_TINY-1\data.yaml')
# # print(os.path.exists(f))
# model = YOLO('yolov8n.pt')
# model.train(data=f,epochs=6) 

model=YOLO(r"C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\runs\detect\train2\weights\best.pt") 
#download fron runs/detect/train/weights/best.pt supoose trained in GColab
s = Path(r'C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\YOLO_V4_TINY-1\test\images')
results=model(source=s,save=True,conf=0.4)