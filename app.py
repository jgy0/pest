from flask import Flask,session,g,render_template
import config
from models import UserModel
from exts import db,mail,cache
from blueprints.auth import auth
from blueprints.qa import bp
from blueprints.pest import pest
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)               # db和app绑定
mail.init_app(app)             # mail和app绑定
cache.init_app(app)

migrate=Migrate(app,db)        # ORM映射

app.register_blueprint(auth)   # app 和蓝图绑定
app.register_blueprint(bp)
app.register_blueprint(pest)

# 钩子函数
# before_request ,before_first_request,after_request


@app.before_request
def my_before_request():
    user_id=session.get("user_id")
    if user_id :
        user=UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)


@app.context_processor
def my_context_processor():
    return {"user":g.user}


if __name__ == '__main__':
    app.run()
