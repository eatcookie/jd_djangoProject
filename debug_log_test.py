# # 日志使用
#
# import structlog
# logger = structlog.get_logger(__name__)
#
# def article_detail(request, pk):
#     logger.info("article_requested", user=request.user.id, pk=pk)