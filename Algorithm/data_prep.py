import warnings
warnings.filterwarnings('ignore')
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import torch 
import yaml
import os
from os import walk
from pathlib import Path
import cv2
import torchvision
import torchvision.transforms as transforms
import torchvision.transforms.functional as F
from torchvision.utils import draw_bounding_boxes
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from torchvision.io import read_image
import yaml
from tqdm import tqdm
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights


'''
Prep for dataset for training and testing
'''



class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, label_transform=None):
        self.annotations_file = annotations_file    
        self.label_dir = sorted(os.listdir(annotations_file))
        # self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir # sorted(os.listdir(img_dir))
        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        self.transform = weights.transforms()
        # self.target_transform = sefl.label_transform

    def __len__(self):
        return len(self.label_dir)

    def __getitem__(self, idx):
        '''
        For a given index, this function reutrns the image and label corresponding to that index

        '''
        img_path = os.path.join(self.img_dir, self.label_dir[idx].split('txt')[0]+"jpg")
        image = read_image(img_path)
        # image = torchvision.transforms.functional.pil_to_tensor(image)
        label_path = os.path.join(self.annotations_file,self.label_dir[idx])
        # print(label_path)
        column_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
        
        try:
            label = pd.read_csv(label_path, delimiter=' ',header=None,on_bad_lines='error')
        except:
            label = pd.read_csv(label_path, delimiter=' ',header=None,on_bad_lines='warn',names=column_names)
        # print(df.head(0))
        # if self.transform:
        image = self.transform(image)
        # if self.target_transform:
        label = self.label_transform(image.shape,label)
        return image, label
    
    def label_transform(self,image_shape,df):
        '''
        This function convert the labels into the format 
        [class, 'top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_x']
        Currently:
        1.  the labels are normalized to value between 0 to 1
        2. They are of the format cxcywh 

        This function scales the bbox back to the required format 
        AND changes the format from cxcywh to xyxy
        Pytorch normally required the format xyxy
        '''


        if df.shape[1]>5:
            df = df.drop(df.columns[5:], axis=1)
        # print(df.shape)
        column_names = ['labels', 'top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y']
        # this is the required format 
        # the column names have been set according to the required format 
        # although the content inside isn't
        df.columns = column_names
        # df.insert(2, "boxes", np.zeros_like(df['labels']))
        # df['class'] = df['class'].astype(str)
        # the bounding box that we have is normalized and of format x_center,y_center,width,height
        boxes = []
        for i in range(df.shape[0]):
            
            b0 = df['top_left_x'][i]#*image_shape[1]
            b1 = df['top_left_y'][i]#*image_shape[2]
            b2 = df['bottom_right_x'][i]#*image_shape[1]
            b3 = df['bottom_right_y'][i]#*image_shape[2]
            bb = torch.tensor([b0,b1,b2,b3])
            bb =torchvision.ops.box_convert(bb, in_fmt='cxcywh', out_fmt='xyxy').numpy()
            boxes.append(bb)
            # df['boxes'][i] = bb
            # df['top_left_x'][i] = bb[0]
            # df['top_left_y'][i] = bb[1]
            # df['bottom_right_x'][i] = bb[2]
            # df['bottom_right_y'][i] = bb[3]
        boxes = torch.tensor(boxes,dtype=torch.float32)
        # print(boxes.shape)
        target = {"labels":torch.tensor(df['labels'].values,dtype=torch.int64),"boxes":boxes}

        return target
    
    # def transform(self,image):
        # transform = weights.transform()


    def show(self,images,df,save_path = 'None'):
        '''
        Displays the image with the bounding boxes
        '''
        
        bbox = df.drop(['class'],axis=1)
        bbox = bbox.values
        drawn_boxes = draw_bounding_boxes(images, torch.tensor(bbox), colors="red",labels = df['class'].astype(str),width = 2, font_size=100)
        imgs = drawn_boxes
        if not isinstance(imgs, list):
            imgs = [imgs]
        fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
        for i, img in enumerate(imgs):
            img = img.detach()
            img = F.to_pil_image(img)
            axs[0, i].imshow(np.asarray(img))
            axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
        if save_path == 'None':
            plt.savefig('test.png')
        else:
            plt.savefig(save_path)

    def show_after_training(self,images_tuple,df,save_path = 'None',transform_bbox = False):
        '''
        Displays the image with the bounding boxes
        '''
        plt.close()
        # for i in range(len(images_tuple)):
        i = 0
        images = images_tuple[i]
        bbox = df[i]['boxes']
        # bb = torch.tensor([[1,1,10,10]])
        # bbox =torchvision.ops.box_convert(bbox, in_fmt='xyxy', out_fmt='xyxy')#.numpy()
        # images = F.to_pil_image(images)
        # images = self.transform(images)
        images = images*255 #.permute(1,2,0)
        if transform_bbox:
            bbox = [bbox[:,0]*images.shape[1],bbox[:,1]*images.shape[2], bbox[:,2]*images.shape[1], bbox[:,3]*images.shape[2]]
            bbox = torch.stack(bbox,dim=1)
        else: 
            bbox = torchvision.ops.box_convert(bbox, in_fmt='cxcywh', out_fmt='xyxy')
            bbox = bbox*255
            # bbox = [bbox[:,0]*images.shape[1],bbox[:,1]*images.shape[2], bbox[:,2]*images.shape[1], bbox[:,3]*images.shape[2]]
            # bbox = torch.stack(bbox,dim=1)
            # bbox = bbox*255
        
        
        drawn_boxes = draw_bounding_boxes(images.to(torch.uint8),bbox , colors="red", labels = df[i]['labels'].numpy().astype(str),width = 10, font_size=100)
        imgs = drawn_boxes
        imgs = [imgs]

        fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
        for i, img in enumerate(imgs):
            img = img.detach()
            img = F.to_pil_image(img)
            axs[0, i].imshow(np.asarray(img))
            axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

        plt.show()
        if save_path == 'None':
            plt.savefig('test.png')
        else:
            plt.savefig(save_path)

if __name__ == "__main__":
    with open('/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/data.yaml') as f:
        data = yaml.safe_load(f)
    label_names = data['names']
    dd = CustomImageDataset("/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/train/labels","/home/newmatik/PCB Defect/Algorithm/PCB-Components-1495/train/images")
    label_hist = np.zeros(len(label_names))
    # for i in tqdm(range(len(dd))):
    i = 117 # 115 162 279
    # for i in range(115,1162):
    print(i)
    _, labels = dd[i]
    # labels = labels['class'].values
    # for label in labels:
    #     label_hist[label] += 1

    # # print(label_names)
    # # print(label_hist)
    # plt.bar(label_names,label_hist)
    # plt.savefig('label_hist.png')