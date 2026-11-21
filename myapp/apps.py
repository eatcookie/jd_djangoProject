

# Django 应用的“应用配置类”，用于告诉 Django 如何加载和管理你的应用（myapp）
    #   在运行代码之后 python manage.py startapp myapp
    #   Django 自动在 myapp/apps.py 中创建这个文件和代码




# 从 Django 框架中导入 AppConfig 基类，所有自定义应用配置类都要继承它。
from django.apps import AppConfig

    #   定义一个名为 MyappConfig 的配置类，继承自 AppConfig，类名可以任意，但官方推荐用“应用名 + Config”的格式。
    #   为所有新建模型指定默认主键类型，在 Django 3.2 及以后，默认主键从 AutoField（32 位）升级为 BigAutoField（64 位），确保你的模型 自动生成 bigint 类型的主键，避免未来迁移问题。
    #   告诉 Django 这个配置类对应的是哪个应用目录,必须与setting.py的 INSTALLED_APPS 中的应用名一致（即 myapp）。
        #   使用场景，在setting.py的 INSTALLED_APPS 中，你可以用两种方式注册应用：
            #   | 写法                         | 效果                                            |
            #   | -------------------------- | --------------------------------------------- |
            #   | `'myapp'`                  | Django 会默认加载 `myapp/apps.py` 中的 `MyappConfig` |
            #   | `'myapp.apps.MyappConfig'` | 显式指定加载这个配置类                                   |
    #   总结：MyappConfig 是 Django 识别并初始化 myapp 应用的“身份证”，用来指定应用名、主键类型等全局设置。
class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
















