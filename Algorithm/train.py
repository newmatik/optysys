import warnings
warnings.filterwarnings('ignore')
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import torch 
import yaml
import os
from pathlib import Path
import cv2
import torchvision
import torchvision.transforms as transforms
import torchvision.transforms.functional as F
from torchvision.utils import draw_bounding_boxes
from data_prep import CustomImageDataset
from tqdm import tqdm
import yaml
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
import time 
from torchmetrics.detection import MeanAveragePrecision
from pprint import pprint 


'''
For training the model.

Vishaka Srinivasan, Newmatik GmBH
'''


def collate_fn(batch):
    return tuple(zip(*batch))



train_dataset = CustomImageDataset("/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/train/labels","/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/train/images")
training_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, num_workers=1, collate_fn=collate_fn)

valid_dataset = CustomImageDataset("/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/valid/labels","/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/valid/images")
valid_loader = DataLoader(valid_dataset, batch_size=2, shuffle=True, num_workers=0, collate_fn=collate_fn)


model = fasterrcnn_resnet50_fpn(weights=None, num_classes=4495, pretrained_backbone=True)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
# model.train()

start = time.process_time()
epoch = 30
check_loss = 10000
# training loop
for e in range(epoch):
    for loader_idx ,data in enumerate(training_loader):
    # data = next(iter(training_loader))
        model.train()
        inputs, target = data


        # Zero your gradients for every batch!
        optimizer.zero_grad()


        train_loss_dict = model(inputs,target)
        train_losses = sum(loss for loss in train_loss_dict.values())
        train_losses.backward()
        optimizer.step()
    
    print(f'{e}/{epoch}  Train loss: {train_losses}')
    if check_loss > train_losses:
        torch.save(model.state_dict(), f'./model_{e}.pth')
        check_loss = train_losses

    # for valid_loader_idx, valid in enumerate(valid_loader):
        
    #         # valid = next(iter(valid_loader))
    #         inputs, target = valid
    #         model.train()
    #         torch.no_grad() 
    #         valid_loss_dict = model(inputs,target)
    #         valid_losses = sum(loss for loss in valid_loss_dict.values())
    #         model.eval()

    #         preds = model(inputs)
    #         metric = MeanAveragePrecision(iou_type="bbox",class_metrics=True)
    #         metric.update(preds, target)



    # metrics = metric.compute()
    # print(f'{e}/{epoch} Training loss:{train_losses} Validation loss: {valid_losses},Validation mAP: {metrics["map"]}, Validation mAP 50: {metrics["map_50"]}')
    # print('time taken: ',(time.process_time() - start)/60,' minutes')
    # if check_loss > valid_losses:
    #     torch.save(model.state_dict(), f'./model_{e}.pth')
    #     check_loss = valid_losses
    
    



##
# model.eval()
# preds = model(inputs)


# metric = MeanAveragePrecision(iou_type="bbox",class_metrics=True)
# metric.update(preds, target)
# # from pprint import pprint
# pprint(metric.compute())


