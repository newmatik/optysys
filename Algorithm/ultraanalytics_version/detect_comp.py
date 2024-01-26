from ultralytics import YOLO
from roboflow import Roboflow
from pathlib import Path
import os
from os.path import expanduser

# rf = Roboflow(api_key="VJgpCQH1sZG2V5bCfwQi")
# project = rf.workspace("pcbdata2").project("pda")
# dataset = project.version(2).download("yolov8")



# f = Path(r'C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\pda-2\data.yaml')
# # # print(os.path.exists(f))
# model = YOLO('yolov8n.pt')
# model.train(data=f,epochs=100) 



# model=YOLO(r"C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\runs\detect\train2\weights\best.pt") 
# #download from runs/detect/train/weights/best.pt supoose trained in GColab
# s = Path(r'C:\Users\VishakaSrinivasan\OneDrive - Newmatik\Desktop\PCB defect\Algorithm\pda-2\test\images')
# results=model(source=s,save=True,conf=0.4)

'''
Bigger component dataset
!pip install roboflow
'''

# rf = Roboflow(api_key="VJgpCQH1sZG2V5bCfwQi")
# project = rf.workspace("nchowdarym").project("pcb-components-djhuq")
# dataset = project.version(1495).download("yolov8")

# f = Path(r'/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/data.yaml')
# # # # print(os.path.exists(f))
# model = YOLO('yolov8n.pt')
# model.train(data=f,epochs=100, batch=2)


model=YOLO(r"/home/newmatik/PCB Defect/Algorithm/runs/detect/train2/weights/best.pt") 
#download fron runs/detect/train/weights/best.pt supoose trained in GColab
s = Path(r'/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/test/images')
results=model(source=s,save=True,conf=0.4)

