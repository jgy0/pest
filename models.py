from datetime import datetime
import pandas as pd
import torch
from PIL import Image
from exts import db
import os
from torch.utils.data import DataLoader, Dataset, TensorDataset

class UserModel(db.Model):
    __tablename__ = 'user'
    id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    join_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


class EmailCacheModel(db.Model):
    __tablename__ = 'email_cache'
    id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False)
    captcha = db.Column(db.String(100),nullable=False,)
    used=db.Column(db.Boolean,default=False)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    creat_time= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    author = db.relationship(UserModel,backref="questions")


class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time= db.Column(db.DateTime,nullable=False,default=datetime.now)

    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship(QuestionModel,backref=db.backref("answers",order_by=create_time.desc(
    )))
    author = db.relationship(UserModel, backref="answers")


#  深度学习模型
class MyDataset(Dataset):
    def __init__(self, img_path, img_labels, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(img_labels, header=None,sep=' ')
        self.img_dir = img_path
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path).convert("RGB")
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


