from myapp.models import Comment

# 示例插入数据
comment = Comment.objects.create(
    product_id=10089087346095,
    comment="这是一个测试评论",
    comment_date="2025-06-25 16:17:55"
)