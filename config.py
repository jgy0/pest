SECRET_KEY = 'Aasdfgssssaaadadsaad'


# 数据库配置
HOSTNAME ="localhost"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MYSQL的用户名，
USERNAME ="root"
#连接MYSQL的密码，
PASSWORD ="root"
# MySQL上创建的数据库名称
DATABASE ="pest_identify"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI=DB_URI


# 邮箱配置
MAIL_SERVER ="smtp.qq.com"
MAIL_USE_SSL = True       # 是否加密
MAIL_PORT = 465
MAIL_USERNAME ="xxxxx@qq.com"          # qq账户
MAIL_PASSWORD ="xxxxxx"           # 授权码
MAIL_DEFAULT_SENDER ="xxxxx"    # qq账户


# flask cache配置
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST ="127.0.0.1"
CACHE_REDIS_PORT =6379
