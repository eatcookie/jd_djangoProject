#设置url

from django.urls import path


from . import views



urlpatterns = [
    path('', views.login, name='root'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    path('index/', views.index, name='index'),


    path('ecommerce_products/', views.ecommerce_products, name='ecommerce_products'),
    path('ecommerce_products_details/', views.ecommerce_products_details, name='ecommerce_products_details'),
    path('ecommerce_comment_list/', views.ecommerce_comment_list, name='ecommerce_comment_list'),

    path('entirety_chart/', views.entirety_chart, name='entirety_chart'),
    path('relativity_chart/', views.relativity_chart, name='relativity_chart'),
    path('comment_chart/', views.comment_chart, name='comment_chart'),

    path('sale_data_predict/', views.sale_data_predict, name='sale_data_predict'),

    path('ApexCharts_learn_demo/', views.ApexCharts_learn_demo, name='ApexCharts_learn_demo'),



    path('user_profile_admin/', views.user_profile_admin, name='user_profile_admin'),
    path('reset_password/', views.reset_password, name='reset_password'),


    path('articles/', views.article_list, name='article-list'),
    #解释在下面。



]


# 解释 path('articles/', views.article_list, name='article-list'),
# 在 Django 的 URL 配置中，你提到的各个部分含义如下：
    #   path 是 Django 提供的一个函数，用于定义 URL 路由规则，它不是路径本身，而是用来创建路由映射的工具。
    #   'articles/' 代表 URL 路径的一部分，当用户访问网站的 http://域名/articles/ 这个网址时，会触发对应的视图处理。
    #   views.article_list 确实代表后端的视图函数（或视图类的方法），当匹配到该 URL 时，Django 会调用这个视图函数来处理请求并生成响应。
    #   name='article-list' 是该 URL 路由的别名，主要用于在模板或代码中反向生成 URL（通过 {% url 'article-list' %} 语法），而不是直接代表前端的 URL 链接。
    #   关于 views.article_list.html：这并不是 Django 的默认约定，视图函数 article_list 通常会通过 render 函数指定要渲染的模板文件，例如 return render(request, 'article_list.html', context)，这里的 article_list.html 才是前端模板文件的名字，它与视图函数名没有强制的命名关联，可以根据实际需求命名。
    #   简单来说，这个配置的作用是：当用户访问 /articles/ 路径时，Django 会调用 views.article_list 视图函数处理请求，并可以通过 article-list 这个别名在其他地方反向生成该 URL。








