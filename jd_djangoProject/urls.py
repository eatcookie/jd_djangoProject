"""
URL configuration for jd_djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

# 项目根路由 urls.py（通常位于 项目同名目录 下）的极简配置
    #   即（通常位于 jd_dangoProject项目 同名目录jd_dangoProject 下）的极简配置
    #       把 /admin/ 路径映射到 Django 自带的 后台管理界面。
    #       把其余所有 URL 转发给 myapp/urls.py 去处理。
# 对应关系
# | 访问地址                           |  实际处理                    |
# | ------------------------------    | ----------------------     |
# | `http://127.0.0.1:8000/admin/`    | Django 管理后台              |
# | `http://127.0.0.1:8000/` 及所有下级 | `myapp/urls.py` 中定义的路由  |

urlpatterns = [
    path("admin/", admin.site.urls),     # 管理员界面
    path('',include('myapp.urls')), # 你的应用
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'myapp.views.handler403'
