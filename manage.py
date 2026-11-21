    #   类 Unix 系统的 shebang，告诉操作系统用当前环境变量里找到的 python 解释器来执行此文件，Windows 会忽略这一行。
    #   文档字符串，说明这是 Django 的 命令行工具。
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# 这段代码是 Django 项目根目录下的 manage.py 文件，它是 整个 Django 项目的“启动器”。
    #   无论你执行 python manage.py runserver、python manage.py migrate 等任何命令，最终都会由这个脚本把参数交给 Django 内核处理。
# 当你执行：django-admin startproject jd_djangoProject
    #   Django 会在项目根目录下自动创建 manage.py，内容就是你现在看到的这段模板代码，无需手动编写。




# 引入 Python 标准库：
    #   os 用来操作环境变量、文件系统等；
    #   sys 用来获取命令行参数 sys.argv

# 把真正的逻辑封装在 main() 函数里，方便测试或复用。
    #   设置默认的环境变量 DJANGO_SETTINGS_MODULE 指向项目配置文件jd_djangoProject.settings。 这样 Django 才能找到 jd_djangoProject/settings.py。
    #   捕获 Django 未安装的异常，给出友好提示。如果你没激活虚拟环境或没装 Django，会在这里抛出错误。
    #   把命令行参数交给 Django 内核sys.argv。
        # 例如：
        # sys.argv = ['manage.py', 'runserver'] → 启动开发服务器
        # sys.argv = ['manage.py', 'migrate'] → 执行数据库迁移
# 入口检查：
    # 只有在直接 运行文件 时才触发 main()；
    # 被其它模块 import 时不执行。
# 总结：manage.py 就是 Django 的“命令中转站”，负责设置环境、检查依赖、把你在终端敲的命令转发给 Django 内核去执行。





import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jd_djangoProject.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
