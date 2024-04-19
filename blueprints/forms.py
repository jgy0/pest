import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, EqualTo, ValidationError,InputRequired
from models import UserModel,EmailCacheModel
from exts import db

# 用来验证前端提交的数据是否符合要求


class RegistrationForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=100,message="请输入3-20位用户名")])
    password = wtforms.StringField(validators=[Length(min=1,max=20,message="请输入6-20位密码")])
    password_confirm = wtforms.StringField(validators=[EqualTo(fieldname="password", message="密码不一致")])
    # 自定义验证邮箱是否注册，
    # 验证验证码是否正确
    def validate_email(self,field):
        email = field.data
        user=UserModel.query.filter_by(email=email).first()
        if user is not None:
            raise wtforms.ValidationError(message="该邮箱已经注册")

    def validate_capcha(self,field):
        captcha = field.data
        print(captcha)
        email=self.email.data
        captcha_model=EmailCacheModel.query.filter_by(email=email,captcha=captcha).first()
        if captcha_model is None:
            raise wtforms.ValidationError(message="验证码不正确")
        else:                 # 定期删除过期验证码
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=1,max=20,message="请输入6-20位密码")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1,max=100,message="请输入小于100字的标题")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容不能小于3个字符")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="内容不能小于3个字符")])
    question_id=wtforms.IntegerField(validators=[InputRequired(message="需要传入问题id")])