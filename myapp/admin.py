# from django.contrib import admin
#
# # Register your models here.
#
# # Django 自动生成的占位符
#     #   出现在：myapp/admin.py
#     #   告诉 Django 如何把 自定义模型 注册到 管理后台（http://127.0.0.1:8000/admin/）。
#     #   目前为空，需要你 手动 添加注册代码，例如以下代码：
#     #   写完保存后，刷新后台即可看到并管理 User 表数据
#
# from django.contrib import admin
# from .models import User     # 引入模型
#
# @admin.register(User)        # 注册到后台
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'nickname')  # 列表页显示字段
#     search_fields = ('username', 'email')             # 搜索框
#
#
# # 为什么要写admin.py
#     #    不写 admin.py 的唯一后果是：你的模型不会出现在 Django 管理后台。
#     #    除此之外，对网站运行、API、模板、数据库迁移等 没有任何影响。
# # 写了有什么用
#     #   能在 /admin/ 里 增删改查 你的数据（不用自己写页面）。
#     #   可快速 填充测试数据、排查线上问题。
#     #   对非技术人员（运营、客服）提供 可视化后台。
#
# # admin的前提
#     #   假设你的模型叫 `User`，文件 `models.py` 里有：
#     #
#     #   ```python
#     #   from django.contrib.auth.models import AbstractUser
#     #
#     #   class User(AbstractUser):
#     #       phone = models.CharField(max_length=15, blank=True)
#     #     nickname = models.CharField(max_length=50)
#     #   ```
#     #
#     #   然后在 `admin.py` 里 **加三行**：
#     #
#     #   ```python
#     #   from django.contrib import admin
#     #   from .models import User     # 引入模型
#     #
#     #   @admin.register(User)        # 注册到后台
#     #   class UserAdmin(admin.ModelAdmin):
#     #       list_display = ('username', 'email', 'nickname')  # 列表页显示字段
#     #       search_fields = ('username', 'email')             # 搜索框
#
# # 总结：详情onenote笔记Django-admin后台管理








# 上面是新版本，下面是补充后的新版本。(解决问题：要让 Django 管理后台的“修改密码”链接重新出现，让管理后台可以修改密码后并转为哈希密码)







# # # 新方法一(直接继承 UserAdmin（推荐，零代码量）)
# #     #   在 admin.py 里把你自定义的 User 模型 重新注册到 Django 自带的 UserAdmin，它会自动带“修改密码”按钮：
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin   # 关键
# from .models import User
# #
# # # 把自定义模型挂到内置 UserAdmin，就能复用“修改密码”链接
# admin.site.register(User, UserAdmin)
# #
# #
# # # 新方法二(手动在自定义 ModelAdmin 里加“修改密码”按钮)
# # # 参考笔记本onenote笔记Django-admin后台管理






# 上面是补充后的新版本，下面是二次补充后的新版本。(解决问题：用来测试后台用户权限功能)






# # 新方法一的补充（用来测试后台用户权限功能403的页面）
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Article

admin.site.register(User, UserAdmin)   # 让后台带“改密码”按钮
admin.site.register(Article)    # Django后台编辑组模型和用户权限测试



