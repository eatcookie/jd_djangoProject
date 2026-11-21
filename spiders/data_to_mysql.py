
# 随机分配商品 ID 给评论数据————————————————————————————data_to_mysql的成功版本之一


import os

import django
############################ 把爬取的数据存到mysql,先在models.py，进行迁移保存migrations，再迁移migrate，再运行data_to_mysql.py

# 导入库
#   (导入 numpy 库，用于数值计算等操作，这里主要用于随机选择商品 id)
#   (导入 pandas 库，用于数据处理和分析，方便对数据进行读取、清洗、转换等操作)
#   (导入 SQLAlchemy 的 create_engine 函数，用于创建数据库引擎，连接到数据库)
import numpy as np
import pandas as pd
from django.utils import timezone
from sqlalchemy import create_engine

# from django.utils import timezone

# 手动配置 Django 设置(新添，为了处理comment_date和comment的问题)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jd_djangoProject.settings')
django.setup()

# 数据库连接（使用 SQLAlchemy）
#   (创建数据库引擎，指定数据库连接信息，包括用户名（root）、密码（123456）、主机地址（localhost）、数据库名（django_jd_ksh），以及字符集（utf8mb4）)
engine = create_engine("mysql+pymysql://root:你的MySQL密码@localhost:3306/django_jd_ksh?charset=utf8mb4")


# 数据读取与清洗
#   (读取名为 result3.csv 的 CSV 文件，指定索引列为第 0 列，将数据加载到 DataFrame 对象 df 中)
#   (删除 df 中有缺失值的行，inplace=True 表示直接在原 df 上进行修改，保证数据的完整性)
df = pd.read_csv('result3.csv',index_col=0)
df.dropna(inplace=True)


# 数据写入 MySQL（商品信息表）
#   (打印出清洗后的 DataFrame 对象 df，查看数据情况)
#   (对result3.csv的列名进行中文变英文的重命名，
#       重新定义 df 的列名，使其与数据库中相应表的字段名对应; 这里对应result3.csv的"",商品id,标题,价格,店铺,品牌,图片,总评数,平均分,好评数,默认好评,好评率,中评数,差评数,追评数,视频晒单数)
#   (再次打印 df，查看修改列名后的数据)
#   (打印列名 df确保 product_id 列存在)
print(df)
df.columns = ['product_id','product_name',
              'price','shop',
              'brand','img_url',
              'CommentCountStr','AverageScore',
              'GoodCountStr','DefaultGoodCountStr','GoodRate','GeneralCountStr','PoorCountStr',
              'AfterCountStr','VideoCountStr',]
print(df)
print(df.columns)


# 重置索引（新添部分）
#   (重置 df 的索引，drop=True 表示丢弃原来的索引，inplace=True 表示直接在原 df 上进行修改，保证数据的完整性)
#   (df确保 DataFrame 的索引唯一且从 1 开始，避免主键冲突)
df.reset_index(drop=True, inplace=True)
df.index += 1


# 尝试删除表并重新创建（如果表已存在，先删除再创建，确保表结构正确）（新添部分）
#   (try尝试，用pandas的to_sql 将 df 中的数据写入到名为 myapp_xinxi 的数据库表中，使用 replace 模式（如果表已存在，则去除数据），将索引作为 id 字段)
#   (except那么，用pandas的to_sql 将 df 中的数据写入到名为 myapp_xinxi 的数据库表中，使用 append 模式（如果表已存在，则追加数据），将索引作为 id 字段)
try:
    df.to_sql('myapp_xinxi', engine, if_exists='replace', index_label='id')
except:
    df.to_sql('myapp_xinxi', engine, if_exists='append', index_label='id')


# 评论数据处理与写入
#   (指定所有列名为columns,
#       即UrlComments.py的row = [skuid, name, time_str, comment, score, image, video, after_comment, reply, like]
#       对应comments.csv的['商品ID', '评论昵称', '时间', '评论', '评分', '图片', '视频', '追评', '回复', '点赞']
#   (读取 comments.csv 文件，指定所有列名为columns赋值为names)
#   (在 df2 中添加一个 product_id 列，初始值为 None)
#       这里是df2，确保 df 和 df2 中的列名的"商品id"列正确，即特别是 product_id
#   (使用已经处理好的 df，避免重复读取文件，提取 df 中的 “product_id” 列，存储到 product_ids 变量中，后续用于随机分配给评论数据)
#       这里是df，确保 df 和 df2 中的列名的"商品id"列正确，即特别是 product_id
columns = ['skuid', 'name', 'time_str', 'comment', 'score', 'image', 'video', 'after_comment', 'reply', 'like']
df2 = pd.read_csv('comments.csv', names=columns)
df2['product_id'] = None
product_ids = df['product_id']


# 随机分配商品 id 给评论数据，即前端网页的 商品精选评论 的显示
#   (if判断，product_ids即df['商品id'] 的长度是否大于等于 len(df2))
#   (如果是，则使用np.random.choice从 product_ids 中随机选择 len(df2) 个值，replace=False表示不重复选择，得到 random_product_ids)
#   (else否则，使用np.tile重复 product_ids 列表，直到长度满足要求（即 int(np.ceil(len(df2)/len(product_ids)))[:len(df2)] 倍的长度），计算需要重复的次数，
#           计算需要重复的次数，确保生成的int(np.ceil(len(df2)/len(product_ids))))的random_product_ids数组长度 与 [:len(df2)]的df2的行数 一致，
#           得到 random_product_ids)
#   (将随机生成的商品 id 列表赋值给 df2 的 product_id 列，为每条评论分配一个商品 id)

if len(product_ids) >= len(df2):
    random_product_ids = np.random.choice(product_ids,size=len(df2),replace=False)
else:
    random_product_ids = np.tile(product_ids,int(np.ceil(len(df2)/len(product_ids))))[:len(df2)]
df2['product_id'] = random_product_ids


# 评分
#   (给 df2 添加一个 score 列，值设为 5，表示默认的评分)
df2['score'] = 5


# 索引处理与日期填充
#   (重置 df2 的索引，drop=True 表示丢弃原来的索引，inplace=True 表示直接在原 df2 上修改)
#   (将索引值加 1，使索引从 1 开始，方便后续写入数据库时作为 id 字段)
df2.reset_index(drop=True,inplace=True)
df2.index += 1

# # 原方法 comment_date
# #   (添加一个 comment_date 列，值设为固定日期 “2025-06-10”)
# #       ecommerce_products_details.html不显示评论的原因，这里的源代码，models的comment_date是时间，但是这里的comment_data是字符串，而这里字符串不是有效的datatime对象。
# #           所以表现为views的def ecommerce_products_details(request)的{% for ...%}遍历失败
# #           即表现为ecommerce_products_details.html的商品精选评论无法显示，即返回{% empty %}<li>No comments yet.</li>
# df2['comment_date'] = '2025-06-10'

#改正方法comment_date 如下 1. 使用正确的 datetime 格式
# 将字符串转换为 datetime 并设置时区
df2['comment_date'] = pd.to_datetime('2025-06-10')
df2['comment_date'] = df2['comment_date'].apply(lambda x: timezone.make_aware(x))


# # 改正方法comment_date 如下 2. 使用当前时间（推荐做法）
# # 使用当前时间，记录数据导入的时间（带时区信息）
# df2['comment_date'] = timezone.now()


# # #改正方法 如下3 使用 ORM 导入数据示例 可以自动处理类型转换
# from myapp.models import Comment
#
# for _, row in df2.iterrows():
#     Comment.objects.create(
#         product_id=row['product_id'],
#         comment=row['comment'],
#         score=row['score'],
#         comment_date=timezone.now()
#     )



# 写入评论数据到 MySQL（评论表）
#   (打印 df2 中的 comment_date 列)
#   (从 df2 中选取 product_id、comment、score、comment_date 这几列，写入到名为 myapp_comment 的数据库表中，使用 replace 模式（清空表后再写入），并将索引作为 id 字段)
print(df2['comment_date'])
# df2[['product_id','comment_date','comment','score']].to_sql('myapp_comment',engine,if_exists='append',index_label='id')
df2[['product_id','comment_date','comment','score']].to_sql('myapp_comment', engine, if_exists='replace', index_label='id')
#
##   注意，上面的comments的评论['product_id','comment_date','comment','score']，真实的实际评论只有整数的200行，我新复制粘贴了很多次，即共计有14个的相同的评论的内容块，每个块大约200行评论，实际上的comments.csv有2800行评论。
#         SQLyog数据库的my_comment表，实际有2800行。




###########


###########


# ######测试 运行这段代码检查是否能动态导入(测试后，测试结果 ：导入成功)
# try:
#     from sqlalchemy import create_engine
#     print("导入成功")
# except ImportError as e:
#     print(f"导入失败: {e}")



# ######测试 确保列名正确映射
# df = pd.read_csv('result3.csv', index_col=0)
# df.rename(columns={"原列名": "新列名"}, inplace=True)
#
# # 打印检查列名
# print(df.columns)
#
# # 检查数据框内容
# print(df.head())









