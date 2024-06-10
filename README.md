1 环境配置

首先安装python，去官网就可以

安装navicat和mysql ，[教程和软件](https://pan.baidu.com/s/1M-1O2UvUzYggcVTYZMl5fA?pwd=gs97 )

安装第三方库

```
pip install flask
pip install flask_migrate
pip install flask_mail
pip install flask_caching
pip install flask-wtf
pip install email_validator
pip install pymysql
pip install redis
pip install flask-caching
```

[模型和文件下载](https://pan.baidu.com/s/1OfNJXHTPuZPRmfvPW-EA8g?pwd=r0wl )

2 新建数据库

 在navicat新建数据库，连接->mysql

<img src="https://s2.loli.net/2024/04/20/vExzbulYoaqXD9I.png" alt="image-20240420094841494" />

连接名随便

<img src="https://s2.loli.net/2024/04/20/9n4DHut2VIEUBpS.png" alt="image-20240420095012738" style="zoom:50%;" />

右键新建数据库

![image-20240420095152182](https://s2.loli.net/2024/04/20/7qba5B2M3XcQ4kJ.png)



<img src="https://s2.loli.net/2024/04/20/OhiyoSc7w8zV2Hs.png" alt="image-20240420095519043" style="zoom:50%;" />



3  修改项目配置

3.1 修改项目配置

用pycharm打开项目

点击右上角向下的小箭头，然后点击Edit Config

<img src="https://s2.loli.net/2024/04/20/KkYNwLqPpJbhBxo.png" alt="image-20240420102707469" style="zoom:50%;" />

添加flask

![image-20240420102831050](https://s2.loli.net/2024/04/20/tvL7KsyogQxrNY3.png)

然后删除项目下的migrations文件夹

![image-20240420100344158](https://s2.loli.net/2024/04/20/clCbPYuMW94kDNh.png)

修改blueprint下的pest.py ,如果你是pc上只有cpu ，修改如下（如果有显卡，只需修改文件路径）

```python
model_ft.load_state_dict(torch.load(r'D:\BaiduNetdiskDownload\resnet50_pro.pkl',map_location='cpu')
                         ,strict=True)  # strict=False
         # 这里load文件路径修改
def predict(image_path):
    image=deal_image(image_path)
    model_ft.eval()
    # model_ft.to(device)
    with torch.no_grad():
        output=model_ft(image)
        # print(output.size(),output)
        _, preds_tensor = torch.max(output, 1)

        preds = np.squeeze(preds_tensor.numpy()) if not train_on_gpu else np.squeeze(preds_tensor.cpu().numpy())
        pre_id=preds+1
        df=pd.read_csv(r'E:\classes.csv')    # 你的文件路径

        pre_result=df.loc[df['id']==pre_id,'name'].values[0]
        print(pre_result)
        return pre_result

```

改为你模型和文件存放路径

3.2修改邮件发送配置

![image-20240420121137428](https://s2.loli.net/2024/04/20/jkDWGcTP57fQylR.png)

下拉 ，开启服务

![image-20240420121235474](https://s2.loli.net/2024/04/20/pyaqUoK6V4FPk9j.png)

手机发送短信后

![img](https://s2.loli.net/2024/04/20/lfIyk3egLPJhRm5.png)

复制这个授权码，在config.py里填入



运行项目

![image-20240420115444292](https://s2.loli.net/2024/04/20/KSHxIpfTFgJal5t.png)

然后 在pycharm的terminal输入下面三行指令

ORM模型映射成表的三步

1 python -m flask db init:这步只需要执行一次

2 python -m flask db migrate: 识别ORM模型的改变，生成迁移脚本

3 python -m flask db upgrade: 运行迁移脚本，同步到数据库中



![image-20240420101909287](https://s2.loli.net/2024/04/20/XVGNPnk9JUuIEHc.png)



然后在浏览器打开http://127.0.0.1:5000就可以体验项目了







