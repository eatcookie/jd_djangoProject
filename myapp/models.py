# 定义导入的模块User、XinXi、Comment、


#(从 Django 的数据库模块中导入 models，它是定义模型类的基础，模型类用于和数据库进行交互，通过定义模型类可以创建与之对应的数据库表)
from django.db import models



# Create your models here.


# 旧，方案一，有效
# # User 模型类（用户表）(models的User原代码)，这是自定义一个 User 的模型类。
# class User(models.Model):
#
#     # 登录账号
#     # (定义一个名为 username 的字符型字段，最大长度为 50，verbose_name 用于在 Django 管理后台等界面显示为 “登录账号”，unique=True 表示该字段的值必须唯一，即每个用户的登录账号不能重复)
#     username = models.CharField(max_length=50, verbose_name='登录账号',unique=True)
#
#     # 密码
#     #(定义密码字段，字符型，最大长度 255，在管理后台显示为 “密码”)
#     password = models.CharField(max_length=255, verbose_name='密码')
#
#     # 昵称
#     #(定义昵称字段，字符型，最大长度 50，显示名称为 “昵称”)
#     nickname = models.CharField(max_length=50, verbose_name='昵称')
#
#     # 邮箱
#     #(定义邮箱字段，使用 EmailField 可以确保输入的是有效邮箱格式，最大长度 100，值唯一，显示名称为 “邮箱”)
#     email = models.EmailField(max_length=100, unique=True,verbose_name='邮箱')
#
#     # 电话/手机
#     #(定义手机字段，字符型，最大长度 15，blank=True 表示在表单中可以为空，null=True 表示在数据库中该字段可以为空，显示名称为 “手机”)
#     phone = models.CharField(max_length=15, blank=True, null=True,verbose_name='手机')
#
#     # 地址
#     #(定义地址字段，字符型，最大长度 255，显示名称为 “地址”)
#     address = models.CharField(max_length=255, verbose_name='地址')
#
#     # 用户类型
#     #(定义用户类型字段，字符型，最大长度 20。choices 参数提供了可选值及对应的显示名称，这里是 “normal” 对应 “普通用户”，“admin” 对应 “管理员”，default='normal' 表示默认值为 “normal”，即普通用户，显示名称为 “用户类型”)
#     user_type = models.CharField(max_length=20,choices=[('normal','普通用户'),('admin','管理员')],default='normal',verbose_name='用户类型')

#     # 头像(这里我在前端的base设置为固定的头像，因为原代码是admin.jpg太丑了，所有我改为了avatar-admin-portrait3.png，后面有需要可用改回去)
#     #(定义头像字段，使用 ImageField 专门用于存储图片，upload_to='avatars/' 指定上传的头像文件保存到名为 avatars 的子目录中，null=True 允许该字段为空，显示名称为 “头像”)
#     avatar = models.ImageField(upload_to='avatars/', null=True, verbose_name='头像')
#
#     # 注册时间
#     #(定义注册时间字段，使用 DateTimeField 存储日期时间，auto_now_add=True 表示当对象第一次被创建时，该字段会自动设置为当前日期和时间，显示名称为 “注册时间”)
#     addtime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
#
#
#     #方法
#     # (定义模型对象的字符串表示方法，当打印或显示该模型对象时，会返回用户的登录账号，方便在 Django 管理后台等地方直观地看到对象的信息)
#     def __str__(self):
#         return self.username
#
#     #元数据
#     # (定义模型的元数据，verbose_name 指定模型在 Django 管理后台等界面显示的名称为 “用户表”，verbose_name_plural 表示复数形式的显示名称，这里将其设置为和 verbose_name 相同，因为在 Django 中有些地方会自动在复数形式后加 “s”，这里避免这种情况，统一显示为 “用户表”。)
#     class Meta:
#         verbose_name = verbose_name_plural = "用户表"




# 新，方案二，有效
# User模型继承了Django 的 AbstractUser， 这是Django 的认证系统
#       （粘贴以下代码，将 User 改为继承 AbstractUser 并设置 AUTH_USER_MODEL）
#       （需在setting.py添加  AUTH_USER_MODEL = 'myapp.User'  ）
#       （需在views.py 把 from django.contrib.auth.models import User 修改为 from myapp.models import User ）
#       （需在pycharm>工具>运行manage.py任务>在控制台的manage.py@jd_djangoProject>先运行命令makemigrations，再运行命令migrate，再重启项目）
# 这意味着：
# 可以使用 authenticate()、login() 等 Django 认证系统功能。
# 可以使用 @login_required 装饰器。
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机')
    address = models.CharField(max_length=255, verbose_name='地址')
    user_type = models.CharField(max_length=20, choices=[('normal', '普通用户'), ('admin', '管理员')], default='normal')
    avatar = models.ImageField(upload_to='avatars/', null=True, verbose_name='头像')



# #(要将你的自定义 User 模型与 Django 自带的认证系统集成，同时保留你的自定义字段，你可以创建一个继承自 AbstractUser 的模型)
# #from django.contrib.auth.models import AbstractUser


# 注意：下面这段缩进代码并未被注释！Python中注释不会结束缩进块，
# 因此以下字段(username/password/nickname/email/addtime/__str__/Meta)
# 实际属于上方的 class User(AbstractUser)，覆盖了AbstractUser的部分默认字段。
# 当前与迁移历史一致，可正常运行；如需精简，请连同迁移一起调整，勿直接删除。

    # 登录账号
    # (定义一个名为 username 的字符型字段，最大长度为 50，verbose_name 用于在 Django 管理后台等界面显示为 “登录账号”，unique=True 表示该字段的值必须唯一，即每个用户的登录账号不能重复)

    username = models.CharField(max_length=50, verbose_name='登录账号',unique=True)

    # 密码
    #(定义密码字段，字符型，最大长度 255，在管理后台显示为 “密码”)
    password = models.CharField(max_length=255, verbose_name='密码')

    # 昵称
    #(定义昵称字段，字符型，最大长度 50，显示名称为 “昵称”)
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    # nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')

    # 邮箱
    #(定义邮箱字段，使用 EmailField 可以确保输入的是有效邮箱格式，最大长度 100，值唯一，显示名称为 “邮箱”)
    email = models.EmailField(max_length=100, unique=True,verbose_name='邮箱')

    # 电话/手机
    #(定义手机字段，字符型，最大长度 15，blank=True 表示在表单中可以为空，null=True 表示在数据库中该字段可以为空，显示名称为 “手机”)
    # phone = models.CharField(max_length=15, blank=True, null=True,verbose_name='手机')
    # phone = models.CharField(max_length=20, blank=True, verbose_name='手机')

    # 地址
    #(定义地址字段，字符型，最大长度 255，显示名称为 “地址”)
    # address = models.CharField(max_length=255, verbose_name='地址')
    # address = models.CharField(max_length=200, blank=True, verbose_name='地址')

    # 用户类型
    #(定义用户类型字段，字符型，最大长度 20。choices 参数提供了可选值及对应的显示名称，这里是 “normal” 对应 “普通用户”，“admin” 对应 “管理员”，default='normal' 表示默认值为 “normal”，即普通用户，显示名称为 “用户类型”)
    # user_type = models.CharField(max_length=20,choices=[('normal','普通用户'),('admin','管理员')],default='normal',verbose_name='用户类型')
    # 头像(这里我在前端的base设置为固定的头像，因为原代码是admin.jpg太丑了，所有我改为了avatar-admin-portrait3.png，后面有需要可用改回去)
    #(定义头像字段，使用 ImageField 专门用于存储图片，upload_to='avatars/' 指定上传的头像文件保存到名为 avatars 的子目录中，null=True 允许该字段为空，显示名称为 “头像”)
    # avatar = models.ImageField(upload_to='avatars/', null=True, verbose_name='头像')

    # 注册时间
    #(定义注册时间字段，使用 DateTimeField 存储日期时间，auto_now_add=True 表示当对象第一次被创建时，该字段会自动设置为当前日期和时间，显示名称为 “注册时间”)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')


    #方法
    # (定义模型对象的字符串表示方法，当打印或显示该模型对象时，会返回用户的登录账号，方便在 Django 管理后台等地方直观地看到对象的信息)
    def __str__(self):
        return self.username

    #元数据
    # (定义模型的元数据，verbose_name 指定模型在 Django 管理后台等界面显示的名称为 “用户表”，verbose_name_plural 表示复数形式的显示名称，这里将其设置为和 verbose_name 相同，因为在 Django 中有些地方会自动在复数形式后加 “s”，这里避免这种情况，统一显示为 “用户表”。)
    class Meta:
        verbose_name = verbose_name_plural = "用户表"






#
# from django import forms
#
# class PasswordResetForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '请输入原密码'}))
#     new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '请设置新密码'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '请再次输入新密码'}))
#
#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get('new_password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if new_password and confirm_password and new_password != confirm_password:
#             self.add_error('confirm_password', '新密码和确认密码不一致')






# XinXi 模型类（商品信息表）
# (定义商品信息模型类，对应数据库中存储商品相关信息的表)
class XinXi(models.Model):
    #主键id
    # (定义主键字段 id，使用 BigIntegerField 可以存储大范围的整数值，primary_key=True 表示该字段是该模型的主键，用于唯一标识表中的每一行记录)
    id = models.BigIntegerField(primary_key=True)

    #商品id
    #(定义商品 id 字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “商品 id”)
    # product_id = models.CharField(verbose_name='商品id',default='',max_length=255)
    product_id = models.BigIntegerField(verbose_name='商品id', default=0)

    #商品名
    #(定义商品名称字段，字符型，最大长度 255，显示名称为 “商品名”)
    product_name = models.CharField(verbose_name='标题/商品名称',max_length=255)

    #价格
    #(定义价格字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “价格”)
    price = models.CharField(verbose_name='价格',default='',max_length=255)

    #店铺
    #(定义店铺字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “店铺”)
    shop = models.CharField(verbose_name='店铺',default='',max_length=255)

    #品牌
    #(定义品牌字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “品牌”)
    brand = models.CharField(verbose_name='品牌',default='',max_length=255)

    #图片
    #(定义图片链接字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “图片”)
    img_url = models.CharField(verbose_name='图片',default='',max_length=255)

    #总评数
    #(定义总评数字段，整数型，默认值为 0，最大长度 255（不过 IntegerField 通常不会用 max_length，可能这里可以优化），显示名称为 “总评数”)
    # CommentCountStr = models.IntegerField(verbose_name='总评数',default=0,max_length=255)
    CommentCountStr = models.IntegerField(verbose_name='总评数',default=0)

    #平均分
    #(定义平均分字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “平均分”)
    AverageScore = models.CharField(verbose_name='平均分',default='',max_length=255)

    #好评数
    #(定义好评数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “好评数”)
    GoodCountStr = models.CharField(verbose_name='好评数',default='',max_length=255)

    #默认好评
    #(定义默认好评数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “默认好评”)
    DefaultGoodCountStr = models.CharField(verbose_name='默认好评',default='',max_length=255)

    #好评率
    #(定义好评率字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “好评率”)
    GoodRate = models.CharField(verbose_name='好评率',default='',max_length=255)

    #中评数
    #(定义中评数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “中评数”)
    GeneralCountStr = models.CharField(verbose_name='中评数',default='',max_length=255)

    #差评数
    #(定义差评数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “差评数”)
    PoorCountStr = models.CharField(verbose_name='差评数',default='',max_length=255)

    #追评数
    #(定义追评数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “追评数”)
    AfterCountStr = models.CharField(verbose_name='追评数',default='',max_length=255)

    #视频晒单数
    #(定义视频晒单数字段，字符型，默认值为空字符串，最大长度 255，显示名称为 “视频晒单数”)
    VideoCountStr = models.CharField(verbose_name='视频晒单数',default='',max_length=255)






    #方法
    # (模型对象的字符串表示方法，返回商品名称)
    def __str__(self):
        return self.product_name

    #元数据
    #(元数据设置，显示名称为 “商品信息表”，复数形式也一样)
    class Meta:
        verbose_name = "商品信息表"
        verbose_name_plural = verbose_name




# Comment 模型类（商品评论表）
# (定义商品评论模型类，对应存储评论信息的表)
class Comment(models.Model):

    # 主键id
    # (定义自动增长的主键 id 字段，使用 AutoField 会自动生成唯一的整数主键)
    id = models.AutoField(primary_key=True)

    # 商品id
    # (定义商品 id 字段，字符型，最大长度 255，默认值为空字符串，显示名称为 “商品 id”，用于关联对应的商品)
    # product_id = models.CharField(max_length=255, verbose_name='商品id',default='')
    product_id = models.BigIntegerField(verbose_name='商品id', default=0)

    # 时间
    # (定义评论时间字段，日期时间型，auto_now_add=True 表示评论创建时自动设置为当前日期和时间，显示名称为 “时间”)
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    # # 暂时将 comment_date 字段改为 CharField
    # comment_date = models.CharField(max_length=50, verbose_name='时间')

    # 评论
    # (定义评论字段，使用 TextField 可以存储较长的文本评论的内容，显示名称为 “评论”)
    comment = models.TextField(verbose_name='评论')

    # 评分
    # (定义评分字段，整数型，显示名称为 “评分”)
    score = models.IntegerField(verbose_name='评分')




  # # 评论昵称/昵称/即CopyComments.json的guid
  # #(定义评论昵称字段，字符型，最大长度 50，显示名称为 “评论昵称”)
  # comment_name = models.CharField(max_length=50, verbose_name='评论昵称',default='')


    # 方法
    # (模型对象的字符串表示方法，返回评论内容)
    def __str__(self):
        return self.comment

    # 元数据
    # (元数据设置，显示名称为 “商品评论表”，复数形式一样，ordering = ['comment_date'] 表示在获取评论数据时，默认按照评论日期进行排序，这样可以方便地获取按时间先后顺序排列的评论)
    class Meta:
        verbose_name = '商品评论表'
        verbose_name_plural = verbose_name
        ordering = ['comment_date']








# Article模型类（文章表）（用来测试后台用户权限功能）
from django.db import models

class Article(models.Model):
    title   = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_publish", "Can publish article"),   # 自定义权限
        ]

    def __str__(self):
        return self.title


# class Article:
#     pass