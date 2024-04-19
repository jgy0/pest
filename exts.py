from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
db=SQLAlchemy()
mail=Mail()
cache=Cache()
