


#############################手动版，手动复制粘贴,这是成功的
#//手动过程：
# 先在result3复制一个商品id，手动在浏览器打开url的网页，自己填上商品id然后回车，
#   url网页如下，更改商品id和页码，即可去网页回车了。
#       https://club.jd.com/comment/productPageComments.action?productId=100055622952&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
# 把下面网页的页面的内容全选复制粘贴，粘贴到CopyComments.json，要确保该json文件只有一行代码。
# 回来这里运行UrlComments.py，内容自动解析到comments.csv。





import csv
import json
import os


def process_comments(input_file, output_file):
    """处理从网页复制的JSON评论数据"""
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
        return

    # 读取文件内容，使用utf-8-sig编码处理BOM
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    try:
        # 解析JSON数据
        data = json.loads(content)
        comments_data = data.get('comments', [])

        # 确保输出文件存在并写入表头
        if not os.path.exists(output_file):
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['商品ID', '评论昵称', '时间', '评论', '评分', '图片', '视频', '追评', '回复', '点赞'])

        # 处理每条评论
        with open(output_file, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for li in comments_data:
                try:

                    #<!--我的代码，评论固定id -->
                    # # 提取评论数据
                    # skuid = "10093141501269"  # 把评论的商品id,设置为固定的商品ID，来自result3.csv的商品id
                    # name = li.get('nickname', '') #评论昵称，来自CopyComments.json的nickname
                    # time_str = li.get('creationTime', '')  #创建时间，来自CopyComments.json的nickname
                    # comment = li.get('content', '').replace('\n', ' ')  #对应models.py的comment
                    # score = li.get('score', 0)
                    # image = len(li.get('images', []))
                    # video = len(li.get('videos', []))
                    # # 处理追评
                    # after_comment = li.get('afterUserComment', {}).get('content', '').replace('\n', ' ')
                    # # 处理回复
                    # replies = li.get('replies', [])
                    # vendor_reply = next((i for i in replies if 'venderShopInfo' in i), {})
                    # reply = vendor_reply.get('content', '')
                    # # 处理点赞数
                    # like = li.get('usefulVoteCount', 0)


                    # <!--源的代码，评论无id -->
                    skuid = li.get('skuid','')
                    name = li['nickname']
                    time_str = li['creationTime']
                    comment = li['content']
                    score = li['score']
                    image = len(li.get('images', []))
                    video = len(li.get('videos', []))
                    after_comment = li.get('afterUserComment', {}).get('content', '')
                    reply = ([i for i in li.get('replies', []) if 'venderShopInfo' in i.keys()] + [{}])[0].get(
                        'content', '')
                    like = li['usefulVoteCount']



                    # 构建数据行
                    row = [skuid, name, time_str, comment, score, image, video, after_comment, reply, like]
                    writer.writerow(row)
                    print(f"已处理评论: {name} - {time_str[:10]}")

                except Exception as e:
                    print(f"处理评论时出错: {e}")

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"请检查 {input_file} 中的JSON格式是否正确")
    except Exception as e:
        print(f"处理数据时出错: {e}")


if __name__ == '__main__':
    # 输入和输出文件路径
    input_file = 'CopyComments.json'  # 建议使用.json扩展名
    output_file = 'comments.csv'

    print("开始处理评论数据...")
    process_comments(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")













##############################自动版，全自动，但是失败了
# import csv
# import json
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
#
#
# def get_user_input():
#     """获取用户输入的商品ID"""
#     while True:
#         sku_id = input("请输入商品ID（例如10077858445858）：").strip()
#         if sku_id.isdigit():
#             return sku_id
#         else:
#             print("输入无效，请输入纯数字的商品ID")
#
#
# def fetch_web_content(sku_id):
#     """自动获取网页内容"""
#     print(f"\n正在获取商品ID为 {sku_id} 的评论数据...")
#
#     # 配置Edge选项
#     edge_options = Options()
#     edge_options.add_argument("--disable-blink-features=AutomationControlled")
#     edge_options.add_argument("--start-maximized")
#     # 取消下面注释可以在无头模式下运行（不显示浏览器窗口）
#     edge_options.add_argument("--headless")
#
#     # 初始化Edge浏览器驱动
#     driver = webdriver.Edge(
#         service=Service(EdgeChromiumDriverManager().install()),
#         options=edge_options
#     )
#
#     # 构建URL
#     url = f"https://club.jd.com/comment/productPageComments.action?productId={sku_id}&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1"
#
#     try:
#         # 打开URL
#         driver.get(url)
#
#         # 等待页面加载完成
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, 'body'))
#         )
#
#         # 等待一段时间，确保内容完全加载
#         time.sleep(12)
#
#         # 获取页面源代码
#         page_source = driver.page_source
#
#         # 保存到JSON文件
#         with open('CopyComments.json', 'w', encoding='utf-8-sig') as f:
#             f.write(page_source)
#
#         print(f"已成功获取并保存内容到 CopyComments.json")
#
#     except Exception as e:
#         print(f"获取网页内容时出错: {e}")
#         page_source = None
#     finally:
#         # 关闭浏览器
#         driver.quit()
#
#     return 'CopyComments.json' if page_source else None
#
#
# def process_comments(input_file, output_file, sku_id):
#     """处理JSON评论数据并保存到CSV"""
#     if not os.path.exists(input_file):
#         print(f"错误：输入文件 {input_file} 不存在")
#         return
#
#     # 读取文件内容
#     with open(input_file, 'r', encoding='utf-8-sig') as f:
#         content = f.read()
#
#     try:
#         # 解析JSON数据
#         data = json.loads(content)
#         comments_data = data.get('comments', [])
#
#         if not comments_data:
#             print("警告：未找到评论数据，请确认获取的内容是否正确")
#             return
#
#         # 确保输出文件存在并写入表头（如果是新文件）
#         is_new_file = not os.path.exists(output_file)
#         with open(output_file, 'a', encoding='utf-8-sig', newline='') as f:
#             writer = csv.writer(f)
#             if is_new_file:
#                 writer.writerow(['商品ID', '昵称', '时间', '评论', '评分', '图片', '视频', '追评', '回复', '点赞'])
#
#             # 处理每条评论
#             for li in comments_data:
#                 try:
#                     name = li.get('nickname', '')
#                     comment = li.get('content', '').replace('\n', ' ')
#                     time_str = li.get('creationTime', '')
#                     score = li.get('score', 0)
#                     image = len(li.get('images', []))
#                     video = len(li.get('videos', []))
#
#                     # 处理追评
#                     after_comment = li.get('afterUserComment', {}).get('content', '').replace('\n', ' ')
#
#                     # 处理回复
#                     replies = li.get('replies', [])
#                     vendor_reply = next((i for i in replies if 'venderShopInfo' in i), {})
#                     reply = vendor_reply.get('content', '')
#
#                     # 处理点赞数
#                     like = li.get('usefulVoteCount', 0)
#
#                     # 构建数据行，使用用户输入的商品ID
#                     row = [sku_id, name, time_str, comment, score, image, video, after_comment, reply, like]
#                     writer.writerow(row)
#                     print(f"已处理评论: {name} - {time_str[:10]}")
#
#                 except Exception as e:
#                     print(f"处理评论时出错: {e}")
#
#     except json.JSONDecodeError as e:
#         print(f"JSON解析错误: {e}")
#         print(f"请检查 {input_file} 中的JSON格式是否正确")
#         print("提示：可能是获取的内容不完整，请尝试调整等待时间")
#     except Exception as e:
#         print(f"处理数据时出错: {e}")
#
#
# if __name__ == '__main__':
#     # 获取用户输入的商品ID
#     sku_id = get_user_input()
#
#     # 自动获取网页内容
#     json_file = fetch_web_content(sku_id)
#
#     if json_file:
#         # 处理JSON文件并保存到CSV
#         output_file = 'comments.csv'
#         print("\n开始处理评论数据...")
#         process_comments(json_file, output_file, sku_id)
#         print(f"\n处理完成，结果已保存到 {output_file}")
#     else:
#         print("获取网页内容失败，程序终止")




