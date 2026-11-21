# import os
# import django
# import numpy as np
# import pandas as pd
# from django.utils import timezone
# from sqlalchemy import create_engine
#
# # 手动配置 Django 设置
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jd_djangoProject.settings')
# django.setup()
#
# # 数据库连接
# engine = create_engine("mysql://root:123456@localhost/django_jd_ksh?charset=utf8mb4")
#
# # 读取商品数据
# df_xinxi = pd.read_csv('result3.csv', index_col=0)
# df_xinxi.columns = [
#     'product_id', 'product_name', 'price', 'shop', 'brand', 'img_url',
#     'CommentCountStr', 'AverageScore', 'GoodCountStr', 'DefaultGoodCountStr',
#     'GoodRate', 'GeneralCountStr', 'PoorCountStr', 'AfterCountStr', 'VideoCountStr'
# ]
#
# # 读取评论数据
# df_comment = pd.read_csv('comments.csv')
# df_comment.columns = ['skuid', 'name', 'time_str', 'comment', 'score', 'image', 'video', 'after_comment', 'reply', 'like']
#
# # 确保 product_id 列存在
# if 'product_id' not in df_xinxi.columns:
#     raise ValueError("商品数据中没有 'product_id' 列")
#
# # 随机分配商品 ID 给评论数据
# product_ids = df_xinxi['product_id'].tolist()
# df_comment['product_id'] = np.random.choice(product_ids, size=len(df_comment), replace=True)
#
# # 处理日期
# df_comment['comment_date'] = pd.to_datetime('2025-06-10')
# df_comment['comment_date'] = df_comment['comment_date'].apply(lambda x: timezone.make_aware(x))
#
# # 写入数据库
# df_xinxi.to_sql('myapp_xinxi', engine, if_exists='replace', index_label='id')
# df_comment[['product_id', 'comment', 'score', 'comment_date']].to_sql('myapp_comment', engine, if_exists='replace', index_label='id')

#
# import os
# import django
# import numpy as np
# import pandas as pd
# from django.utils import timezone
# from sqlalchemy import create_engine
#
# # 手动配置 Django 设置
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jd_djangoProject.settings')
# django.setup()
#
# # 数据库连接
# engine = create_engine("mysql://root:123456@localhost/django_jd_ksh?charset=utf8mb4")
#
# # 读取商品数据
# df_xinxi = pd.read_csv('result3.csv', index_col=0)
# df_xinxi.columns = [
#     'product_id', 'product_name', 'price', 'shop', 'brand', 'img_url',
#     'CommentCountStr', 'AverageScore', 'GoodCountStr', 'DefaultGoodCountStr',
#     'GoodRate', 'GeneralCountStr', 'PoorCountStr', 'AfterCountStr', 'VideoCountStr'
# ]
#
# # 读取评论数据
# df_comment = pd.read_csv('comments.csv')
# df_comment.columns = ['skuid', 'name', 'time_str', 'comment', 'score', 'image', 'video', 'after_comment', 'reply', 'like']
#
# # 确保 product_id 列存在
# if 'product_id' not in df_xinxi.columns:
#     raise ValueError("商品数据中没有 'product_id' 列")
#
# # 随机分配商品 ID 给评论数据
# product_ids = df_xinxi['product_id'].tolist()
# df_comment['product_id'] = np.random.choice(product_ids, size=len(df_comment), replace=True)
#
# # 处理日期
# df_comment['comment_date'] = pd.to_datetime('2025-06-10')
# df_comment['comment_date'] = df_comment['comment_date'].apply(lambda x: timezone.make_aware(x))
#
# # 写入数据库
# df_xinxi.to_sql('myapp_xinxi', engine, if_exists='replace', index_label='id')
# df_comment[['product_id', 'comment', 'score', 'comment_date']].to_sql('myapp_comment', engine, if_exists='replace', index_label='id')


#
# import os
# import django
# import numpy as np
# import pandas as pd
# from django.utils import timezone
# from sqlalchemy import create_engine
#
# # 手动配置 Django 设置
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jd_djangoProject.settings')
# django.setup()
#
# # 数据库连接
# engine = create_engine("mysql://root:123456@localhost/django_jd_ksh?charset=utf8mb4")
#
# # 读取商品数据
# df_xinxi = pd.read_csv('result3.csv', index_col=0)
# df_xinxi.columns = [
#     'product_id', 'product_name', 'price', 'shop', 'brand', 'img_url',
#     'CommentCountStr', 'AverageScore', 'GoodCountStr', 'DefaultGoodCountStr',
#     'GoodRate', 'GeneralCountStr', 'PoorCountStr', 'AfterCountStr', 'VideoCountStr'
# ]
#
# # 读取评论数据
# df_comment = pd.read_csv('comments.csv')
# df_comment.columns = ['skuid', 'name', 'time_str', 'comment', 'score', 'image', 'video', 'after_comment', 'reply', 'like']
#
# # 确保 product_id 列存在
# if 'product_id' not in df_xinxi.columns:
#     raise ValueError("商品数据中没有 'product_id' 列")
#
# # 随机分配商品 ID 给评论数据
# product_ids = df_xinxi['product_id'].tolist()
# df_comment['product_id'] = np.random.choice(product_ids, size=len(df_comment), replace=True)
#
# # 处理日期
# df_comment['comment_date'] = pd.to_datetime('2025-06-10')
# df_comment['comment_date'] = df_comment['comment_date'].apply(lambda x: timezone.make_aware(x))
#
# # 写入数据库
# df_xinxi.to_sql('myapp_xinxi', engine, if_exists='replace', index_label='id')
# df_comment[['product_id', 'comment', 'score', 'comment_date']].to_sql('myapp_comment', engine, if_exists='replace', index_label='id')






# 随机分配商品 ID 给评论数据————————————————————————————data_to_mysql的成功版本之二
import os
import django
import numpy as np
import pandas as pd
from django.utils import timezone
from sqlalchemy import create_engine

# 手动配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jd_djangoProject.settings')
django.setup()

# 数据库连接
engine = create_engine("mysql+pymysql://root:你的MySQL密码@localhost:3306/django_jd_ksh?charset=utf8mb4")

# 读取商品数据
df_xinxi = pd.read_csv('result3.csv', index_col=0)
df_xinxi.columns = [
    'product_id', 'product_name', 'price', 'shop', 'brand', 'img_url',
    'CommentCountStr', 'AverageScore', 'GoodCountStr', 'DefaultGoodCountStr',
    'GoodRate', 'GeneralCountStr', 'PoorCountStr', 'AfterCountStr', 'VideoCountStr'
]

# 读取评论数据
df_comment = pd.read_csv('comments.csv')
df_comment.columns = ['skuid', 'name', 'time_str', 'comment', 'score', 'image', 'video', 'after_comment', 'reply', 'like']

# 确保 product_id 列存在
if 'product_id' not in df_xinxi.columns:
    raise ValueError("商品数据中没有 'product_id' 列")

# 随机分配商品 ID 给评论数据
product_ids = df_xinxi['product_id'].tolist()
df_comment['product_id'] = np.random.choice(product_ids, size=len(df_comment), replace=True)

# 处理日期
df_comment['comment_date'] = pd.to_datetime('2025-06-10')
df_comment['comment_date'] = df_comment['comment_date'].apply(lambda x: timezone.make_aware(x))

# 写入数据库
df_xinxi.to_sql('myapp_xinxi', engine, if_exists='replace', index_label='id')
df_comment[['product_id', 'comment', 'score', 'comment_date']].to_sql('myapp_comment', engine, if_exists='replace', index_label='id')
