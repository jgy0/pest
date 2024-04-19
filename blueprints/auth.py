from flask import Blueprint,render_template,request,jsonify,redirect,url_for,session,flash
from flask_mail import Message
from exts import mail,cache,db
from flask import request
import string
import random
from models import EmailCacheModel,UserModel
from .forms import RegistrationForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login',methods=['GET','POST'])
def login_page():
    if request.method=='GET':
        return render_template('login.html')
    else:
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print('invalid email')
                return redirect(url_for('auth.login_page'))
            if check_password_hash(user.password,password):
                # flask中的session是经过加密后存储在cookie中的
                session['user_id']=user.id
                return redirect('/')
            else:
                print('invalid password')
                return redirect(url_for('auth.login_page'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login_page'))
# GET从服务器上获取数据
# POST 将客户端数据提交给服务器
@auth.route('/register',methods=['POST','GET'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 表单验证 flask-wtf
        form=RegistrationForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user=UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login_page"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register_page"))


@auth.route('logout')
def logout_page():
    session.clear()
    return redirect("/")


@auth.route('/captcha/email')
def captcha_email():
    email = request.args.get('email')
    source=string.digits*4
    cap=random.sample(source,4)
    cap=''.join(cap)
    message = Message(subject='害虫识别系统验证码', recipients=[email]
                      , body=f'您的验证码是:{cap},请勿告诉别人！')
    mail.send(message)
    email_captcha=EmailCacheModel(email=email,captcha=cap)
    db.session.add(email_captcha)
    db.session.commit()
    # cache.set(email,cap,timeout=100)
    return jsonify({"code":200,"message":"","data":None})


@auth.route('/mail/test')
def mail_test():
    message = Message(subject='test message',recipients=['cuncunrouchang1@163.com']
                     , body='这是一条测试邮件')
    mail.send(message)
    return "邮件发送成功"


