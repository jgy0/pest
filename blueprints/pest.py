from flask import Blueprint, render_template, redirect,g,url_for,session
from flask import request
import torch
import torch.nn as nn
import os
from PIL import Image
import numpy as np
import pandas as pd
from torchvision import datasets, transforms, models
from torchvision.models import resnet50
from decorators import login_required

transform=transforms.Compose([
                              transforms.Resize((255,255)),
                              transforms.ToTensor(),
                              transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
                              ])

"""加载模型"""
device = torch.device("cuda" if torch.cuda.is_available() else "")
train_on_gpu=torch.cuda.is_available()
model_ft=resnet50()
num_in = model_ft.fc.in_features
model_ft.fc =nn.Linear(num_in, 102)
model_ft.load_state_dict(torch.load(r'D:\code\python\agriculture_pest_identify\code\resnet50_pro.pkl'),strict=True)  # strict=False

"""
测试图像
"""


def deal_image(image_path):
    img=Image.open(image_path).convert("RGB")
    img=transform(img)
    # print(img.size())     # torch.Size([3, 255, 255])
    img=img.unsqueeze(0)
    # print(img.size())     # torch.Size([1, 3, 255, 255])   b c h w
    return img.to(device)

def predict(image_path):
    image=deal_image(image_path)
    model_ft.eval()
    model_ft.cuda()
    with torch.no_grad():
        output=model_ft(image)
        # print(output.size(),output)
        _, preds_tensor = torch.max(output, 1)

        preds = np.squeeze(preds_tensor.numpy()) if not train_on_gpu else np.squeeze(preds_tensor.cpu().numpy())
        # print(preds)
        pre_id=preds+1
        # 处理类名id到类名name的映射
        df=pd.read_csv(r'F:\dataset\classes.csv')
        """
        print(df.dtypes)
        id       int64
        name    object
        """
        pre_result=df.loc[df['id']==pre_id,'name'].values[0]
        print(pre_result)
        return pre_result
        # print(type(pre_result)) # <class 'str'>


#  定义视图函数
pest = Blueprint('pest', __name__, url_prefix='/pest')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@pest.route('/upload', methods=['POST','GET'])

def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(UPLOAD_FOLDER, f.filename)
        session['file'] = upload_path
        f.save(upload_path)
        return redirect(url_for('pest.result'))
    else:
        return render_template('pest.html')


@pest.route('/result', methods=['GET','POST'])
@login_required
def result():
    if request.method == 'GET':
        path=session['file']
        print('预测文件路径:'+path)
        result_ = predict(path)
        return render_template('result.html',result=result_)
    else: return render_template('pest.html')


if __name__ == '__main__':
    image_path = r'F:\dataset\ip102_v1.1\test\75213.jpg'
    predict(image_path)

