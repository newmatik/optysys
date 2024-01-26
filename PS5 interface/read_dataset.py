import pandas as pd

'''
This script reads the dataset and converts it into a csv file

Vishaka Srinivasan, Newmatik GmBh
'''


# file_path = 'dataset/vishaka-pcbs_commented.txt'  # Replace this with the path to your file
file_path = 'dataset/vish-CAN-0004-01A_commented.txt'

counter = 0
with open(file_path) as f:
    lines = [line.rstrip('\n') for line in f]


df = pd.DataFrame(columns=['Item code', 'Item Description', 'Designator', 'X','Y','Rotation','Layer','Comment'])
item_code = []
item_desc = []
component = []
designator = []
x = []
y = []
rotation = []
layer = []
comment = []
new_pcb_flag = True
counter = 0
FLAG  = 0
NEW = []
for L in lines:
    l = L.split(' ')
    if l[0] == 'F1':
        item_code=l[1]
        
    if l[0] == 'F2':
        item_desc=l[1]
    
    if l[0] == 'F8':
        # print(l)
        x=l[1]
        y=l[2]
        rotation=l[3]
        layer=l[4]
        comment=l[7]
        counter += 1
    
    if l[0] == 'F9':
        designator=l[1]
        counter +=1
    
    if counter == 2:
        NEW.append({'Item code':item_code, 'Item Description':item_desc, 'Designator':designator, 'X':x,'Y':y,'Rotation':rotation,'Layer':layer,'Comment':comment})
        counter = 0
        FLAG += 1

df = pd.concat([df,pd.DataFrame(NEW)])
print(df.head(3))

df.to_csv('dataset/vishaka-CAN004.csv', columns = list(df.columns.values), index=False)

