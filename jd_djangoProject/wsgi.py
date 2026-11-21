"""
WSGI config for jd_djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# 入口文件（wsgi.py）
    #    告诉任何 WSGI 服务器（如 Gunicorn、uWSGI、Daphne）怎样启动你的 Django 项目。
    #       1. 指定当前项目使用的 settings 文件
    #       2. 创建 WSGI 应用对象，供服务器调用
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jd_djangoProject.settings")

application = get_wsgi_application()




# wsgi什么时候会用到
    # 开发：python manage.py runserver 会自动加载它。
    # 生产：
    #   gunicorn jd_djangoProject.wsgi:application
    #   uwsgi --module jd_djangoProject.wsgi:application
    #   以上命令都会读取 application = get_wsgi_application()。

# 常见踩坑
    #   1.如果项目改名，记得同步改 jd_djangoProject.settings 中的包名。
    #   2.启动时报 ModuleNotFoundError: No module named 'jd_djangoProject'，说明
    #       说明 当前目录不在 Python 路径，可临时加：
    #       export PYTHONPATH=$PYTHONPATH:$(pwd)

# wsgi当你执行：
    #   django-admin startproject jd_djangoProject
    #   Django 会自动在项目根目录下生成 jd_djangoProject/wsgi.py，内容就是你现在看到的代码，无需手写。
    #   代码 完全由 startproject 自动生成，你确实没写过。
    #   只要目录结构正确，它就会静静地躺在那里，直到你用 runserver 或 gunicorn 启动项目时才被真正用到。

# wsgi和asgi区别：
    #   wsgi.py 面向 WSGI（传统同步）
    #   asgi.py 面向 ASGI（支持异步、WebSocket、HTTP/2 等）

# 总结：不要改动这段代码，除非项目名或 settings 文件路径变了。


