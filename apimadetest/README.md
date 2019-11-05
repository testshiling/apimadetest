基于Django实现的后端接口，有以下接口：
注册（post）、登录（post、get）、添加房源（post）、创建订单（post）。
目前接口比较粗浅，对参数校验也不严格，现在能跑起来，后续再优化。

玩法：
1、安装Python3环境；
2、安装django环境，版本2以上就可以；
3、安装MySQL数据库；
4、将项目下载到本地；
5、修改apimadetest/settings.py文件中的数据库配置

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apimadetest',   #预先创建一个数据库，utf-8格式
        'USER': 'root',          #您本地数据库的用户名
        'PASSWORD': 'luoshiling',  #您本地数据库的密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


5、运行步骤：
A、 cd apimadetest/
B、 python manage.py makemigrations
C、 python manage.py migrate    #准备数据库环境
D、 python manage.py createsuperuser   #创建超级用户,方便管理
E、 python manage.py runserver   #启动项目

6、apitest/test/test.py 中有一些测试脚本可以运行试试


