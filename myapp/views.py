# views视图

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from random import sample

from myapp.models import User,XinXi,Comment
from django.contrib.auth.hashers import check_password,make_password
import logging
from django.db import IntegrityError


# 注意：之前网页的ecommerce_products_details的商品精选评论没有评论内容，有两个原因，1是没有设置下面这个Django配置，2是comments.csv没有足够多的评论，1和2缺一不可。
import os


import pandas as pd
import re
import jieba
from collections import Counter

from speculate import Speculate

from django.contrib import messages

# #(方案二，有效，下面改为了from myapp.models import User)
# from django.contrib.auth.models import User
from myapp.models import User



from django.contrib.auth import login as auth_login, authenticate


from django.contrib.auth.decorators import login_required

# # from django.shortcuts import render, redirect
# from .models import User          # 你的用户模型







# #Create your views here.

# # # 登录页面视图(新版本，这里已经把登录流程改走 Django 官方认证体系了。)

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(
            '<script>alert("用户名或密码不正确！");location.href="/login/"</script>'
        )

    if not check_password(password, user_obj.password):
        return HttpResponse(
            '<script>alert("用户名或密码不正确！");location.href="/login/"</script>'
        )

    # 让 Django 认证系统认识此用户
    user_obj.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user_obj)

    return redirect('/index')   # 显式 return



# # # 登录页面视图(原版本)
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     elif request.method == 'POST':
#         res=request.POST
#
#         obj=User.objects.filter(username=res['username'])
#
#         if obj:
#             obj = obj[0]
#             if check_password(res['password'],obj.password):
#                 request.session['user'] = obj.id
#             return HttpResponse('<script>alert("登录成功！");location.href="/index"</script>')
#         return HttpResponse('<script>alert("用户名或密码不正确！");location.href="/login/"</script>')
#     else:
#         return HttpResponse('<script>alert("请求方式不正确")</script>')





# # 退出登录，删除提交的user对象的id，指向登录页面视图（原）
# def logout(request):
#     try:
#         del request.session['user']
#     except:
#         pass
#     return HttpResponse('<script>alert("退出成功！");location.href="/"</script>')


# 退出登录(新)
def logout(request):
    request.session.flush()
    return HttpResponse('<script>alert("退出成功！");location.href="/"</script>')



#添加日志记录以捕获注册过程中的信息和异常

logger = logging.getLogger(__name__)




# # 注册页面视图
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            # 检查用户名或密码是否为空
            if not username or not password:
                logger.info("用户名或密码为空")
                return HttpResponse('<script>alert("用户名和密码不能为空！");location.href="/register/"</script>')

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                logger.info("用户名已存在")
                return HttpResponse('<script>alert("用户名已存在，请选择其他用户名！");location.href="/register/"</script>')

            # 创建用户
            obj = User()
            obj.username = username
            obj.password = make_password(password, None, "pbkdf2_sha256")
            obj.email = email
            obj.phone = phone
            obj.save()

            logger.info("注册成功")
            return HttpResponse('<script>alert("注册成功，跳转登录！");location.href="/"</script>')

        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            return HttpResponse('<script>alert("注册失败，请重新尝试！");location.href="/register/"</script>')

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return HttpResponse('<script>alert("注册失败，请重新尝试！");location.href="/register/"</script>')

    else:
        return HttpResponse('<script>alert("请求方式不正确！");location.href="/register/"</script>')






# 实际的首页的视图，右边的index部分，即index是base首页的一个主页表格部分
# 定义一个视图函数index()：
#    (index它接收一个 request 参数（HTTP 请求对象）)
# 查询商品数据：
#    (使用Django的ORM（对象关系映射）查询数据库中的XinXi模型,
#        order_by('-CommentCountStr')表示按照CommentCountStr字段进行降序排序（从高到低）,
#        [: 5] 表示取排序后的前五个商品)。
# 数据处理
#   (遍历查询到的每个商品对象 product,
#       假设 GoodRate 是一个浮点数或可以转换为浮点数的字符串，表示好评率,
#       将 GoodRate 转换为百分比格式，并赋值给 product.GoodRatePercent 属性。
#       打印, 经过处理后的 GoodRatePercent 值（用于调试）
# 构建上下文并渲染模板
#   (创建一个字典 context，将查询到的商品数据存储在 products 键下)
#   (使用 render 函数，将 request对象、模板文件index.html、上下文context 作为参数，
#       把处理后的数据传递给 index.html 模板进行渲染，生成用户可见的网页内容生成 HTTP 响应并返回给用户)
def index(request):

    products = XinXi.objects.order_by('-CommentCountStr')[:5]

    for product in products:
        product.GoodRatePercent = "{:.0f}%".format(float(product.GoodRate) * 100)
        print(product.GoodRatePercent)

    context = {'products': products}
    return render(request,'index.html',context)







# 实际的首页的视图，左边的ecommerce_products部分
def ecommerce_products(request):
    query = request.GET.get('search', '')
    page_number = request.GET.get('page')  # 获取请求中的页码参数
    if query:
        products = XinXi.objects.filter(product_name__icontains=query).order_by('id')  #按ID排序 # .order_by('id') 属于新添部分
    else:
        products = XinXi.objects.all().order_by('id')  #按ID排序 # .order_by('id') 属于新添部分

    # 创建分页器对象，设置每页显示的数量为 10
    paginator = Paginator(products, 10)

    # 获取请求的页码对应的Page对象
    page_obj = paginator.get_page(page_number)

    # 计算评分星星
    for product in page_obj.object_list:
        product.full_stars = ['bx bxs-star text-warning'] * int(product.AverageScore)
        product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(product.AverageScore))
        product.GoodRatePercent = "{:.0f}%".format(float(product.GoodRate) * 100)


    context = {
        'products': [
            {
            'product': product,
             'full_stars': product.full_stars,
             'empty_stars': product.empty_stars
            }
            for product in page_obj.object_list],

        'page_obj': page_obj,

        'query': query,  # 添加搜索参数到上下文中
    }

    return render(request, 'ecommerce_products.html', context)





# # 获取请求中的商品id参数
# # 使用id查询对应商品对象
# # 为本商品计算评分星星
# # 获取评论数据
# # 获取同一品牌的其他商品
# # 为其他商品计算评分星星
# # 传入请求和文本 渲染模版到html里面
#
# def ecommerce_products_details(request):
#     id = request.GET.get('id')
#     product = get_object_or_404(XinXi, id=id)
#
#     # print(product.product_id)
#     # comments = Comment.objects.filter(product_id=product.product_id).order_by('comment_date')[:5]
#     # print(comments)
#
#     product.full_stars = ['bx bxs-star text-warning'] * int(product.AverageScore)
#     product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(product.AverageScore))
#
#     comments = Comment.objects.filter(product_id=product.id).order_by('comment_date')[:5]
#
#     # 除了本商品外，查询同一品牌的其他商品
#     brand = product.brand
#     other_products = XinXi.objects.filter(brand=brand).exclude(id=id)[:3]
#
#     # 除了本商品外，如果其他商品不足三个商品，则在本商品的全部商品里面随机选取3个商品,并为其他商品计算评分星星
#     if len(other_products) < 3:
#         other_products = XinXi.objects.filter(brand=brand).exclude(id=id)
#         other_products = sample(list(other_products), min(len(other_products), 3))
#
#     for other_product in other_products:
#         other_product.full_stars = ['bx bxs-star text-warning'] * int(other_product.AverageScore)
#         other_product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(other_product.AverageScore))
#
#     # # 除了本商品外，对其他商品计算评分星星
#     # for product in other_products:
#     #     product.full_stars = ['bx bxs-star text-warning'] * int(product.AverageScore)
#     #     product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(product.AverageScore))
#
#     # print(product.product_id)
#     # comments = Comment.objects.filter(product_id=product.product_id).order_by('comment_date')[:5]
#     # print(comments)
#
#     context = {
#         'product': product,
#         'other_products': other_products,
#         'comments': comments,
#     }
#
#     #传入请求和文本 渲染模版到html里面
#     return render(request, 'ecommerce_products_details.html',context)


# 实际的首页的视图，左边的ecommerce_products_details部分
def ecommerce_products_details(request):
    id = request.GET.get('id')
    product = get_object_or_404(XinXi, id=id)

    # 计算评分星星
    product.full_stars = ['bx bxs-star text-warning'] * int(product.AverageScore)
    product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(product.AverageScore))

    # 获取评论数据
    # comments = Comment.objects.filter(product_id=product.id).order_by('-comment_date')[:5]
    # 商品精选评论，分配的规则是随机分配，且每个商品id的评论的数量上限最多是6行评论
    comments = Comment.objects.filter(product_id=product.product_id).order_by('comment_date')[:6]
    # 在视图文件中打印调试信息
    print(comments)
    print(f"Product ID: {product.id}, Comments Count: {len(comments)}")
    # comments = Comment.objects.all()
    for comment in comments:
        print(f"Comment ID: {comment.id}, Comment: {comment.comment}, Date: {comment.comment_date}")


    # 获取同一品牌的其他商品
    brand = product.brand
    other_products = XinXi.objects.filter(brand=brand).exclude(id=id)[:3]

    # 为其他商品计算评分星星
    for other_product in other_products:
        other_product.full_stars = ['bx bxs-star text-warning'] * int(other_product.AverageScore)
        other_product.empty_stars = ['bx bxs-star text-secondary'] * (5 - int(other_product.AverageScore))

    context = {
        'product': product,
        'other_products': other_products,
        'comments': comments,
    }

    return render(request, 'ecommerce_products_details.html', context)



# 实际的首页的视图，左边的ecommerce_comment_list部分
def ecommerce_comment_list(request):
    query = request.GET.get('search', '')
    page_number = request.GET.get('page')  # 获取请求中的页码参数
    if query:
        comments = Comment.objects.filter(comment__contains=query).order_by('id')   # 这里原代码是没有.order_by('id')，所以源代码不能使用搜索栏的功能，但是这里的新代码可以使用搜索栏功能
    else:
        comments = Comment.objects.all().order_by('id')     # # 这里原代码是没有.order_by('id')，所以源代码不能使用搜索栏的功能，但是这里的新代码可以使用搜索栏功能

    # 创建分页器对象，设置每页显示的数量为 10
    paginator = Paginator(comments, 10)

    # 获取请求的页码对应的Page对象
    page_obj = paginator.get_page(page_number)

    context = {
        'comments': page_obj,
        'page_obj': page_obj,
        'query': query,  # 添加搜索参数到上下文中
    }
    return render(request, 'ecommerce_comment_list.html',context)






# 实际的首页的视图，左边的whole_chart部分,数据这里我没传，没写视图函数定义传数据，我是直接写死在html里面
def entirety_chart(request):
    return render(request, 'entirety_chart.html')

# 实际的首页的视图，左边的relativity_chart部分，数据这里我没传，没写视图函数定义传数据，我是直接写死在html里面
def relativity_chart(request):
    return render(request, 'relativity_chart.html')




# preprocess_text函数,清理和处理文本数据，提取出有用的词汇给 comment_chart函数
#   去掉标点符号和特殊字符
#   将文本转换为小写
#   使用jieba分词，将文本分割成单词列表
#   过滤掉单个字符的词
#   返回处理后的单词列表
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    words = jieba.lcut(text)
    filtered_words = [word for word in words if len(word) > 1]
    return filtered_words


# 实际的首页的视图，左边的comment_chart部分
# comment_chart 函数，这个函数是Django视图函数，用于处理评论数据并生成词频统计结果
#   从CSV文件中读取评论数据， 只保留“评论”这一列
#   将所有评论合并成一个长字符串 本文
#   调用preprocess_text函数 处理 文本
#   统计每个单词的出现次数
#   获取出现次数最多的前200个单词
#   将结果格式化为一个列表，每个元素是一个字典，包含单词和对应的出现次数
#   将结果存储到上下文中，以便传递到HTML模板
#   使用Django的render函数渲染HTML模板，并将上下文传递给模板，返回HTTP响应
def comment_chart(request):
    df = pd.read_csv('spiders/comments.csv')
    df = df[['评论']]


    all_text = ' '.join(df.values.flatten().astype(str))

    words = preprocess_text(all_text)
    word_count = Counter(words)
    top_200_words = word_count.most_common(200)

    result = [{'name': word, 'value': count} for word, count in top_200_words]

    context = {
        'result': result,
    }
    return render(request, 'comment_chart.html', context)








# 实际的首页的视图，左边的sale_data_predict部分
    # 新添功能：原来上传：一个变量的上下文数据：result
            # 现在上传：全部变量的上下文数据：result,brand,rating,price,average_score,error_message
    # 新添功能：if not... else...表单验证逻辑，确保所有必填字符都已填写
        # (原版，不填直接提交会返回一个ValueError异常的页面)
        # (一次修改版，不填直接提交会返回当前页面，设置评分范围：字符串类型，浮点数类型)
        # (二次修改版，部分填直接提交会返回当前页面)
        # (三次修改版，部分填直接提交会返回固定的错误消息)
    # 新添功能：设置错误消息(根据不同的输入提交，返回不同的错误消息)

# 定义sale_data_predict函数，用于处理销售数据预测的请求
def sale_data_predict(request):

    result = None  # 初始化结果为 None，表示初始状态下没有预测结果
    brand = None   # 初始化品牌为 None，表示初始状态下没有品牌信息
    rating = None  # 初始化评分率为 None，表示初始状态下没有好评率信息
    price = None   # 初始化价格为 None，表示初始状态下没有价格信息
    average_score = None  # 初始化平均得分为 None，表示初始状态下没有平均分信息
    error_message = None  # 初始化错误消息为 None，表示初始状态下没有错误消息

    if request.method == 'POST':    # 检查请求方法是否为POST，如果是POST请求，则处理表单数据,来源于html的用户请求：即用户输入的brand,rating,price,average_score
        brand = request.POST.get('brand')    # 从POST请求中获取品牌数据，并赋值给变量brand
        rating = request.POST.get('rating', '')      # 从POST请求中获取品牌数据，并赋值给变量brand
        price = request.POST.get('price', '')   # 从POST请求中获取价格数据，并赋值给变量price；如果未获取到，则默认为空字符串''
        average_score = request.POST.get('average_score', '')  # 从POST请求中获取平均分数据，并赋值给变量average_score；如果未获取到，则默认为空字符串''


        if not brand or not rating or not price or not average_score:   # 检查：品牌、评分率、价格和平均分是否都已填写(brand,rating,price,average_score 是否已经填写)
            error_message='请填写所有字段信息'   # 如果有任意一个字段未填写，则设置错误消息为'请填写所有字段信息'
        else:
            try:    # 如果所有字段都已填写，则尝试进行数据转换和验证
                brand_str=str(brand)    # 在html选择的固定的品牌的时候，将品牌数据转换为字符串类型，并赋值给变量brand_str
                price_float=float(price)    # 将价格数据转换为浮点数类型，并赋值给变量price_float，这里只能输入数字或部分符合，如果输入了符号例如---就点击预测，则会该输入框隔壁跳出小提示小窗口【！请输入数字。】
                rating_float=float(rating)  # 将好评率数据转换为浮点数类型，并赋值给变量rating_float，这里只能输入数字或部分符合，如果输入了符号例如---就点击预测，则会该输入框隔壁跳出小提示小窗口【！请输入数字。】
                average_score_float=float(average_score)    # 将评分率数据转换为浮点数类型，并赋值给变量rating_float，这里只能输入数字或部分符合，如果输入了符号例如---就点击预测，则会该输入框隔壁跳出小提示小窗口【！请输入数字。】

                print([''])     #控制台打印 空格字符串 列表

                if not (0<=rating_float<=1):    # 检查好评率是否在0到1的范围内
                    error_message='好评率必须在0到1之间'      # 如果评分率超出范围，则设置错误消息为'好评率必须在0到1之间'
                elif not(0<=average_score_float<=5):    # 检查平均分是否在0到5的范围内
                    error_message='平均分必须在0到5之间'     # 如果平均分超出范围，则设置错误消息为'平均分必须在0到5之间'
                else:           # 如果所有数据都有效，则准备数据并进行预测
                    data=[price_float, brand_str, rating_float, average_score_float]     # 将转换后的数据，组合成一个列表，赋值给变量data
                    result=Speculate(data)   # 调用Speculate函数，对列表变量data，进行随机森林模型的预测，得出预测结果result。

            # 如果数据转换过程中发生ValueError异常
                # （例如无法将字符串转换为浮点数，这里是因为，我在html默认设置的字段为'请选择品牌...'，
                # 但实际上Speculate()函数并没有'请选择品牌'这个字段，因为Speculate()函数包括的字段只有"价格"、"品牌"、"好评率"、"平均分"，
                # 所以Speculate()函数会转换报错，这个函数里面的一个功能是把，品牌列的内容的 字符串转换为数值，然后再预测
                # 正确的做法应该是，选择一个在品牌列 里面 已经存在的字符串，
                # 而不是选择这里默认的字符串，这里默认的字符串是'请选择品牌...'这个字段，这是无法转换为数值的，所以会发生ValueError异常
                # 这里则捕获异常，并设置错误消息为'请选择品牌字段信息'，意思是选择品牌列 里面的 有效的存在的 品牌字段，例如小米、oppo等字段
            except ValueError:
                error_message='请选择品牌字段信息'

    # 准备要传递给模板的上下文数据
    context = {
        'result': result,   #预测结果
        'brand': brand,     #品牌信息
        'rating': rating,   #好评率信息
        'price': price,     #价格信息
        'average_score': average_score,     #平均分信息
        'error_message': error_message      #错误信息
    }

    # 渲染并返回sale_data_predict.html模板，同时传递上下文数据context
    return render(request, 'sale_data_predict.html', context)






# 图表学习样板（用来测试练习html的ApexChart的属性功能）
def ApexCharts_learn_demo(request):
    return render(request,'ApexCharts_learn_demo.html')


# def user_profile_admin(request):
#     return render(request, 'user_profile_admin.html')

#
# def reset_password(request):
#     return render(request, 'reset_password.html')





# # 方法二/版本二：定义user_profile_admin函数，用于处理个人信息(这里已经把登录流程改走 Django 官方认证体系了。可行，且未来扩展功能如权限管理，很方便)


# 导入 Django 自带的login_required装饰器，用于限制未登录用户访问某个视图函数。例如：给视图函数加上@login_required后，未登录用户访问时会自动跳转到登录页。
# 导入 Django 的快捷函数：
    # render：用于渲染模板并返回 HTTP 响应（将数据传递给 HTML 页面）。
    # redirect：用于重定向到其他 URL（如表单提交后跳转到首页）。
    # get_object_or_404：根据条件查询数据库对象，若不存在则返回 404 错误（替代直接使用Model.objects.get()，更友好地处理不存在的情况）。
# 导入 Django 的消息框架，用于在视图和模板之间传递一次性通知（如 “操作成功”“错误提示”），通常配合messages.success(request, "提示内容")使用。
# 导入 从当前应用（.表示当前目录）的models.py文件中导入User模型（数据库表结构定义），用于操作用户相关的数据（如查询、创建用户）。
# 总结：这些导入是 Django 开发中处理用户认证、页面渲染、数据交互的基础工具组合。

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User

@login_required
def user_profile_admin(request):
    # 现在 request.user 就是当前登录用户（Django 官方体系）
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        user.nickname  = request.POST.get('nickname', '').strip()
        # Django 视图函数中处理表单提交数据的常见写法，作用是从 POST 请求中获取 "nickname" 字段的值，并赋值给用户对象的 nickname 属性
            # request.POST是 Django 中处理 POST 请求数据的字典 - like 对象，存储了表单提交的键值对。
            # .get('nickname', '')表示获取，键为nickname的值：
                # 如果表单中存在name="nickname"的字段，则返回其值；
                # 如果不存在该字段，则返回默认值''（空字符串），避免出现KeyError。
            #.strip()对获取到的值调用字符串的strip()方法，去除首尾的空白字符（如空格、换行符等），用于简单的数据清洗，避免用户输入的意外空格影响数据准确性。
            #user.nickname 将处理后的值赋值给user对象的nickname属性，后续会调用user.save()将修改保存到数据库中。
        user.email     = request.POST.get('email', '').strip()
        user.phone     = request.POST.get('phone', '').strip()
        user.username  = request.POST.get('username', '').strip()
        user.address   = request.POST.get('address', '').strip()

        try:
            user.save()
            messages.success(request, "个人信息已更新！")
        except Exception as e:
            messages.error(request, f"保存失败：{e}")
        return redirect('user_profile_admin')

    return render(request, 'user_profile_admin.html', {'user': user})




# # 方法一/版本一：定义user_profile_admin函数，用于处理个人信息(可行，session.get，但未来扩展功能如权限管理，它说不方便)
# # 坚持使用自定义会话存储，移除 @login_required，并在视图中统一 逻辑：
# def user_profile_admin(request):
#     user_id = request.session.get('user')
#     print(f"当前用户ID: {user_id}")  # 调试信息
#     if not user_id:
#         return redirect('/login/')
#
#     # GET：渲染初始页面
#     if request.method == 'GET':
#         user = get_object_or_404(User, id=user_id)
#         return render(request, 'user_profile_admin.html', {'user': user})
#
#     # POST：保存修改
#     elif request.method == 'POST':
#         user = get_object_or_404(User, id=user_id)
#         user.nickname = request.POST.get('nickname', '').strip()
#         user.email = request.POST.get('email', '').strip()
#         user.phone = request.POST.get('phone', '').strip()
#         user.username = request.POST.get('username', '').strip()
#         user.address = request.POST.get('address', '').strip()
#
#         try:
#             user.save()
#             messages.success(request, "个人信息已更新！")
#         except Exception as e:
#             messages.error(request, f"保存失败：{e}")
#
#     return redirect('user_profile_admin')













# # 修改密码（reset_password 在新页面弹窗版本，session.get，版本1的视图，有效）
# # #视图采用 session 中保存的用户 id 来定位当前登录用户，仅修改密码，不做登录态变化。
# #       模板层你已写好了 JS 禁用按钮逻辑，这里只补充 后端校验 + 反馈弹窗。
# # from django.shortcuts import render, redirect
# # from django.contrib import messages
# # from django.contrib.auth.hashers import check_password, make_password
# from django.views.decorators.http import require_http_methods
# # from myapp.models import User
# # import re
#
# PWD_REGEX = re.compile(r'^[A-Za-z0-9]{8,16}$')   # 8-16 位数字或字母
#
# @require_http_methods(["GET", "POST"])
# def reset_password(request):
#     user_id = request.session.get('user')
#     if not user_id:                       # 未登录
#         return redirect('/login/')
#
#     user = User.objects.get(pk=user_id)
#
#     if request.method == 'GET':
#         return render(request, 'reset_password.html')
#
#     # POST
#     old_pwd = request.POST.get('old_password', '').strip()
#     new_pwd = request.POST.get('new_password', '').strip()
#     confirm_pwd = request.POST.get('confirm_password', '').strip()
#
#     # 1. 空值检查
#     if not all([old_pwd, new_pwd, confirm_pwd]):
#         return _popup_resp(request, '所有字段都必须填写！')
#
#     # 2. 格式检查
#     if not PWD_REGEX.match(new_pwd):
#         return _popup_resp(request, '新密码必须为 8-16 位数字或字母！')
#
#     # 3. 两次新密码一致性
#     if new_pwd != confirm_pwd:
#         return _popup_resp(request, '两次新密码输入不一致！')
#
#     # 4. 原密码正确性
#     if not check_password(old_pwd, user.password):
#         return _popup_resp(request, '原密码不正确，请重新填写！')
#
#     # 5. 保存新密码
#     user.password = make_password(new_pwd)
#     user.save()
#     messages.success(request, '密码修改成功，请重新登录！')
#     return redirect('/login/')
#
#
# def _popup_resp(request, msg):
#     """
#     返回一个极简页面，内嵌弹窗提示 + 自动清空表单的 JS
#     """
#     html = f"""
#     <!doctype html>
#     <html>
#     <head>
#       <meta charset="utf-8">
#       <title>提示</title>
#       <style>
#         body{{font-family:Arial;margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#f4f4f4}}
#         .modal{{background:#fff;border:1px solid #ccc;border-radius:6px;padding:30px 40px;box-shadow:0 4px 12px rgba(0,0,0,.15)}}
#         .modal h3{{color:#d9534f;margin-top:0}}
#         .modal a{{float:right;margin-top:10px;text-decoration:none;color:#333;font-size:20px}}
#       </style>
#     </head>
#     <body>
#       <div class="modal">
#         <a href="javascript:window.location.href='{request.path}';" title="关闭">&times;</a>
#         <h3>{msg}</h3>
#         <p>密码错误</p>
#       </div>
#       <script>
#         // 清空 sessionStorage 中可能的缓存值
#         sessionStorage.clear();
#       </script>
#     </body>
#     </html>
#     """
#     from django.http import HttpResponse
#     return HttpResponse(html)





# #下面是版本二 ： 修改密码（reset_password 版本是本页面的框框红色小字提示，这里已经把登录流程改走 Django 官方认证体系了。版本2的视图html，有效）

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import re

from django.contrib.auth import login as django_login
from django.contrib import messages   # ① 新增


PWD_REGEX = re.compile(r'^[A-Za-z0-9]{8,16}$')

@login_required
@require_http_methods(["GET", "POST"])
def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html')

    old_pwd = request.POST.get('old_password', '').strip()
    new_pwd = request.POST.get('new_password', '').strip()
    cf_pwd  = request.POST.get('confirm_password', '').strip()

    errors = {}

    # 空值检查
    if not old_pwd:
        errors['old_error'] = '原密码不能为空'
    if not new_pwd:
        errors['new_error'] = '新密码不能为空'
    if not cf_pwd:
        errors['confirm_error'] = '确认密码不能为空'

    # 格式检查
    if new_pwd and not PWD_REGEX.match(new_pwd):
        errors['new_error'] = '密码必须为8-16位数字或字母'
    if cf_pwd and not PWD_REGEX.match(cf_pwd):
        errors['confirm_error'] = '密码必须为8-16位数字或字母'

    # 密码一致性检查
    if new_pwd != cf_pwd:
        errors['new_error'] = '两次密码不匹配，请重新填写'
        errors['confirm_error'] = '两次密码不匹配，请重新填写'

    # 原密码验证
    if old_pwd and not authenticate(username=request.user.username, password=old_pwd):
        errors['old_error'] = '原密码不匹配，请重新填写'

    if errors:
        return render(request, 'reset_password.html', errors)

    # 保存新密码
    user = request.user
    user.set_password(new_pwd)
    user.save()


    # 保持登录状态 #原
    # login(request, user)

    django_login(request, user)  # 使用别名 #新

    # ② 绿色提示
    messages.success(request, "个人密码已经更新！")
    return render(request, 'reset_password.html', {'success': True})








#
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
# breakpoint()  # Python 3.7+ 支持，会进入交互调试模式
print("到这了吗")
from .models import Article
print("到这了")

# Django后台-编辑组-Article-用户权限

# @permission_required('myapp.can_publish', raise_exception=True)：
# def article_list(request)：
# articles = Article.objects.all()
# return render(request, 'article_list.html', {'articles': articles})
    #   这是权限验证装饰器，指定只有拥有myapp应用中can_publish权限的用户才能访问该视图；raise_exception=True表示当用户无权限时直接返回 403 错误，而非重定向到登录页。
    #   定义了名为article_list的视图函数，接收request请求对象作为参数。
    #   函数内部通过Article.objects.all()查询所有文章数据，
    #   使用render函数将文章数据传递给article_list.html模板并返回渲染后的页面。
# 总结：整体作用，限制只有特定权限的用户才能访问文章列表页面，增强了应用的权限管控。

    # 有Article权限的用户:
        # 无论article_list.html=是True还是False，两种情况都会正常返回页面article_list.html
                            # 即需要涉及：
                            # 下面任何一种"即需要"，这里都能成立，这里都能有效运行
    # 无Article权限的用户:
        # 如果raise_exception=False，会导致Django认为你权限不够所以是登录不完全而重定向，重定向，回到登录页面。（重定向是正常的，原因是"登录不够圆满"）
            # 不同重定向的区别：
                #之前的重新向，例如def reset_password的，例如def user_profile_admin的，原因是从User传输的内容方式错误导致系统认为你登录不够，
                        # 那么User模型类，把全部文件关于User的手动session.get的id 改为 Django系统的AbstractUser和admin.site.register来get的id，来解决重定向的问题。
                #这里的重定向，例如article_list的，原因是admin5有权限，而admin2无权限，系统认为admin2登录不够。
                        # 那么，即使改为 Django系统的AbstractUser和admin.site.register来get的id，还是重定向，
                        # 因为在Django后台的超级用户给的admin2用户没有myapp.can_publish的权限，而这里恰好需要这个权限才能进去Article_Django_test，所以还是登录不够而发生重定向。
                        # 这是 Django 的默认登录保护机制 在起作用：
                        # 你把 raise_exception=False 后，无权限用户会触发 “登录重定向”（/accounts/login/?next=/articles/）。
                        # 你当前登录的是 admin2，而它 确实没有 myapp.can_publish 的用户权限，于是 Django 认为你“还没登录够”，把你送到登录页。
                            # 即需要涉及：
                            # def article_list函数=False + article_list.html + class Article模型类 + admin后台 + base路径 + articles/urls
        # 如果raise_exception=True，会导致Django默认返回403错误
        #    403在Django有三种情况，分别是：
        #       403，情况一：Django默认返回完全空白的页面（F12的网络>页面刷新>会显示403错误）（默认空白页面）
                        # 空响应根因：Django 自带的 403 视图 默认不返回 HTML，只返回空字符串，于是浏览器看到空白。
                        # Django 自带的 django.views.defaults.permission_denied（即没写 handler403 时的默认实现）
                            # 即需要涉及：
                            # def article_list函数=True + article_list.html + class Article模型类 + admin后台 + base路径 + articles/urls
        #       403，情况二：Django返回一个极简的页面（F12的网络>页面刷新>会显示403错误）（官方推荐做法）
                        # 官方做法就是 只放一个名为 403.html 的模板——哪怕是极简一行字也行：
                        # 然后，什么都不用配置（不要写 handler403等）。Django 会自动找到它并返回。
                        # <!-- templates/403.html -->
                        # <h1>403 Forbidden</h1>
                            # 即需要涉及：
                            # def article_list函数=True + article_list.html + class Article模型类 + admin后台 + base路径 + articles/urls + 403.html的情况二
        #       403，情况三：返回一个自定义的页面（F12的网络>页面刷新>会显示403 错误）（官方推荐做法+我的base模版）
                            # 即需要涉及：
                            # def article_list函数=True + article_list.html + class Article模型类 + admin后台 + base路径 + articles/urls + 403.html的情况三 + def handler403函数 + setting的HANDLER403(注意：setting这里的代码可有可无)

@permission_required('myapp.can_publish', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})










# def handler403(request, exception)：
#     return render(request, '403.html', status=403)
    #    这段代码是 Django 中自定义的 403 错误处理视图函数，即定义了处理 403（权限拒绝）错误的视图，接收请求对象request和错误异常exception作为参数，
    #    函数通过render方法渲染自定义的403.html模板，并返回带有 403 状态码的 HTTP 响应。
# 总结：作用是，当用户访问没有权限的资源时，系统会调用该函数，显示自定义的 403 权限错误页面，而不是 Django 默认的错误页面，提升用户体验和系统专业性。

# 函数，调用430 错误 到 403.html
def handler403(request, exception):
    # logger.warning("handler403 被调用")
    return render(request, '403.html', status=403)










# 测试debug
# views.py
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)   # 断点打在这
    print(article.title)                          # 下一步