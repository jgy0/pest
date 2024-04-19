# pest
农业害虫识别系统
项目启动需要确保pc上有下面三个环境

python

flask

mysql

```
pip install flask
pip install flask-migrate

```





ORM模型映射成表的三步

1 python -m flask db init:这步只需要执行一次

2 python -m flask db migrate: 识别ORM模型的改变，生成迁移脚本

3 python -m flask db upgrade: 运行迁移脚本，同步到数据库中

<img src="https://s2.loli.net/2024/04/19/LBCJk7zw4thMaIy.png" alt="image-20240412214137096" style="zoom:67%;" />

