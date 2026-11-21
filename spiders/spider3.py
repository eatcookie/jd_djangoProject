


#############################自动版，如果代理IP有效，那这是成功的
#                                        如果代理IP被封或无效，则这是失败的
#



import csv
import os
import  random
import time

import requests
import pandas as pd
from lxml import etree

cookie = '在此处粘贴你自己的京东Cookie'
#cookie = '在此处粘贴你自己的京东Cookie'

headers = [
    {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'cookie':cookie
    },
    {
    'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)',
    'cookie': cookie
    },
    {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'cookie': cookie
    },
    {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'cookie': cookie
    },
    {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'cookie': cookie
    },
    {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'cookie': cookie
    },
    {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'cookie': cookie
    },

]



def getip():
    with open("ipdaili.txt") as f:
        iplist = f.readlines()
    proxy = iplist[random.randint(0,len(iplist)-1)]
    proxy = proxy.replace("\n","")
    proxies = {
        'http':'http://' + str(proxy)
    }
    return proxies






def data_processing(inputpath, outputpath):
    def if_wan(x):
        if '万' in str(x):
            x = float(x[:-1]) * 10000
        return x

    df = pd.read_csv(inputpath)
    df = df.dropna(subset=['总评数'])
    df = df.drop_duplicates(subset=['商品id'])

    df['总评数'] = df['总评数'].str.replace('+','')
    df['总评数'] = df['总评数'].str.replace('万','0000')
    df['总评数'] = df['总评数'].astype(int)

    df['好评数'] = df['好评数'].str.replace('+','')
    df['好评数'] = df['好评数'].map(if_wan)
    df['好评数'] = df['好评数'].astype(int)

    df['默认好评数'] = df['默认好评数'].str.replace('+','')
    df['默认好评数'] = df['默认好评数'].map(if_wan)
    df['默认好评数'] = df['默认好评数'].astype(int)

    df['中评数'] = df['中评数'].str.replace('+','')
    df['中评数'] = df['中评数'].map(if_wan)
    df['中评数'] = df['中评数'].astype(int)

    df['差评数'] = df['差评数'].str.replace('+','')
    df['差评数'] = df['差评数'].map(if_wan)
    df['差评数'] = df['差评数'].astype(int)

    df['追评数'] = df['追评数'].str.replace('+','')
    df['追评数'] = df['追评数'].map(if_wan)
    df['追评数'] = df['追评数'].astype(int)

    df['视频晒单数'] = df['视频晒单数'].str.replace('+','')
    df['视频晒单数'] = df['视频晒单数'].map(if_wan)
    df['视频晒单数'] = df['视频晒单数'].astype(int)

    # 商品id，总评数，平均分，好评数，默认好评数，好评率，中评数，差评数，追评数，视频晒单数

    df.to_csv(outputpath)






def getdata(url,pinpai):
    res = requests.get(url, headers=random.choice(headers), proxies=getip())
    res.encoding = 'utf-8'
    text = res.text

    selector = etree.HTML(text)
    list = selector.xpath('//*[@id="J_goodsList"]/ul/li')

    rows=[]
    for i in list:
        title = i.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')
        price = i.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
        img = i.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')[0]
        product_id = i.xpath('.//div[@class="p-commit"]/strong/a/@id')[0].replace('J_comment_','')
        try:
            shop = i.xpath('.//div[@class="p-shop"]/span/text()')[0]
        except IndexError:
            shop = ''
        title = ''.join(title)
        rows.append([product_id,title.replace('\n',''),price,shop,pinpai,img])
    return rows




def getcommit(data):

    kv = {
    'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'cookie':cookie
    }

#     # pids = data[0]
#     pids=data[0]
#     endnum = int(len(data)/100)
#     for i in range(1,endnum):
# #       price(pids[100*(i-1):100*1],type(pids))
#         newpids = pids[100*(i-1):100*i]
#         comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="
#         for pid in newpids:
#             if pid == '商品id':
#                 continue
#             else:
#                 comment_url += str(pid) + ","
#             comment_r = requests.get(comment_url, headers=headers[0], proxies=getip())
#             p_comment = []
#             for comment in comment_r.json()["CommentsCount"]:

    pids = data[0]
    endnum = int(len(data)/100)
    for i in range(1, endnum):
        # print(pids[100*(i-1):100*i],type(pids))
        newpids = pids[100 * (i - 1):100 * i]
        comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="
        for pid in newpids:
            if pid == '商品id':
                continue
            else:
                comment_url += pid + ','
        comment_r = requests.get(comment_url, headers=headers[0], proxies=getip())
        p_comment = []
        for comment in comment_r.json()["CommentsCount"]:
            p_comment.append([comment["ProductId"],
                            comment["CommentCountStr"],comment["AverageScore"],
                            comment["GoodCountStr"],comment["DefaultGoodCountStr"],comment["GoodRate"],
                            comment["GeneralCountStr"],comment["PoorCountStr"],
                            comment["AfterCountStr"], comment["VideoCountStr"]
                            ])

        with open('result1.csv', mode='a', newline='', encoding='utf-8') as f1:
            writerf1 = csv.writer(f1)
            writerf1.writerow(
                    ['商品id', '总评数', '平均分',
                     '好评数', '默认好评数', '好评率',
                     '中评数', '差评数', '追评数',
                     '视频晒单数'])
            for item in p_comment:
                writerf1.writerow(item)

# 商品id，总评数(注意：这里的评是评价，而不是评论。这里的CommentCountStr在index.html的下方表格数据，引用了并作为了销量，它和评论内容无关，本质上是商品交易成功后的评价信息)，平均分，好评数，默认好评数，好评率，中评数，差评数，追评数，视频晒单数




def getcommit(data):
    kv = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "cookie": cookie
    }
    '''抓评论'''
    pids = data[0]
    endnum = int(len(data)/100)
    for i in range(1, endnum):
        # print(pids[100*(i-1):100*i],type(pids))
        newpids = pids[100 * (i - 1):100 * i]
        comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="
        for pid in newpids:
            if pid == '商品id':
                continue
            else:
                comment_url += str(pid) + ","
        comment_r = requests.get(comment_url, headers=headers[0], proxies=getip())
        p_comment = []
        for comment in comment_r.json()["CommentsCount"]:
            p_comment.append([comment["ProductId"],
                            comment["CommentCountStr"],comment["AverageScore"],
                            comment["GoodCountStr"],comment["DefaultGoodCountStr"],comment["GoodRate"],
                            comment["GeneralCountStr"],comment["PoorCountStr"],
                            comment["AfterCountStr"], comment["VideoCountStr"]
                            ])
            # 总评数，平均得分，好评数，默认好评，好评率，追评数，视频晒单数，差评数，中评数
        # 将抓取的结果保存到本地CSV文件中
        with open('result1.csv', mode='a', encoding='utf-8', newline='') as f1:

            writer = csv.writer(f1)
            writer.writerow(['商品id', '总评数', '平均分',
                            '好评数', '默认好评数', '好评率',
                            '中评数', '差评数', '追评数',
                            '视频晒单数'])
            for item in p_comment:
                writer.writerow(item)


def getpinpai(url):
    res = requests.get(url, headers=headers[0], proxies=getip())
    res.encoding = 'utf-8'
    text = res.text

    selector = etree.HTML(text)
    list = selector.xpath('.//ul[@class="J_valueList v-fixed"]/li')
    # print(list)
    rows = []
    for i in list:
        pinpai1 = i.xpath('.//a/text()')[-1].replace('\n\t\t\t\t\t\t\t\t\t\t','').replace('\n\t\t\t\t\t\t\t\t\t','')
        rows.append(pinpai1)
    return rows




def savedata(data):
    if os.path.exists('result.csv'):
        with open('result.csv',mode='a+',newline='',encoding='utf-8') as f:
            writerf = csv.writer(f)
            for item in data:
                writerf.writerow(item)

    else:
        with open('result.csv',mode='a+',newline='',encoding='utf-8') as f:
            writerf = csv.writer(f)
            writerf.writerows(['商品id','标题','价格','店铺','品牌','图片'])
            for item in data:
                writerf.writerow(item)





# pinpai = getpinpai('https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=手机&pvid=8917aa3c960c420fbd585763a6f55d02')
# print(pinpai)
# for item in pinpai:
#     for i in range(1, 10):
#             time.sleep(random.random()*10)
#             url = 'https://search.jd.com/search?keyword=手机&wq=手机&ev=exbrand_{}%5E'.format(item)
#             n = i * 2 - 1
#             url = url + "&pvid=8917aa3c960c420fbd585763a6f55d02&page={}".format(n)
#             savedata(getdata(url, item))
#
#             print(url)




data = pd.read_csv('result.csv', header=None)
getcommit(data)

df1 = pd.read_csv('result.csv', encoding='utf-8')#读取第一个文件
df2 = pd.read_csv('result1.csv', encoding='utf-8')#读取第二个文件
df1['商品id'] = df1['商品id'].astype(str)
df2['商品id'] = df2['商品id'].astype(str)
outfile = pd.merge(df1, df2,  left_on='商品id', right_on='商品id')#
outfile.to_csv('result2.csv', index=False,encoding='utf-8')#输出文件

data_processing('result2.csv', 'result3.csv')


# 过程：先运行pinpai，得到result，在rusult里面的文本加上表头  商品id,标题,价格,店铺,品牌,图片
#      再运行data，得到result1，result和result1合并得到result2，result2格式，得到result3
















#############################其他代码，手动版，失败了



# import csv
# import os
# import random
# import time
# import requests
# import pandas as pd
# from lxml import etree
#
# cookie = ''#
# headers = [
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
#         'cookie': cookie
#     },
#     {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
#         'cookie': cookie
#     },
# ]
#
#
# def getip():
#     with open("ipdaili.txt") as f:
#         iplist = f.readlines()
#     proxy = iplist[random.randint(0, len(iplist)-1)]
#     proxy = proxy.replace("\n", "")
#     proxies = {
#         'http': 'http://' + str(proxy)
#     }
#     return proxies
#
#
# def data_processing(inputpath, outputpath):
#     def if_wan(x):
#         if '万' in str(x):
#             x = float(x[:-1]) * 10000
#         return x
#
#     df = pd.read_csv(inputpath)
#     df = df.dropna(subset=['总评数'])
#     df = df.drop_duplicates(subset=['商品id'])
#
#     df['总评数'] = df['总评数'].str.replace('+', '')
#     df['总评数'] = df['总评数'].str.replace('万', '0000')
#     df['总评数'] = df['总评数'].astype(int)
#
#     df['好评数'] = df['好评数'].str.replace('+', '')
#     df['好评数'] = df['好评数'].map(if_wan)
#     df['好评数'] = df['好评数'].astype(int)
#
#     df['默认好评数'] = df['默认好评数'].str.replace('+', '')
#     df['默认好评数'] = df['默认好评数'].map(if_wan)
#     df['默认好评数'] = df['默认好评数'].astype(int)
#
#     df['中评数'] = df['中评数'].str.replace('+', '')
#     df['中评数'] = df['中评数'].map(if_wan)
#     df['中评数'] = df['中评数'].astype(int)
#
#     df['差评数'] = df['差评数'].str.replace('+', '')
#     df['差评数'] = df['差评数'].map(if_wan)
#     df['差评数'] = df['差评数'].astype(int)
#
#     df['追评数'] = df['追评数'].str.replace('+', '')
#     df['追评数'] = df['追评数'].map(if_wan)
#     df['追评数'] = df['追评数'].astype(int)
#
#     df['视频晒单数'] = df['视频晒单数'].str.replace('+', '')
#     df['视频晒单数'] = df['视频晒单数'].map(if_wan)
#     df['视频晒单数'] = df['视频晒单数'].astype(int)
#
#     df.to_csv(outputpath)
#
#
# def getdata(url, pinpai):
#     res = requests.get(url, headers=random.choice(headers), proxies=getip())
#     res.encoding = 'utf-8'
#     text = res.text
#
#     selector = etree.HTML(text)
#     list = selector.xpath('//*[@id="J_goodsList"]/ul/li')
#
#     rows = []
#     for i in list:
#         title = i.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')
#         price = i.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
#         img = i.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')[0]
#         product_id = i.xpath('.//div[@class="p-commit"]/strong/a/@id')[0].replace('J_comment_', '')
#         try:
#             shop = i.xpath('.//div[@class="p-shop"]/span/text()')[0]
#         except IndexError:
#             shop = ''
#         title = ''.join(title)
#         rows.append([product_id, title.replace('\n', ''), price, shop, pinpai, img])
#     return rows
#
#
# def getcommit(pids):
#     if not isinstance(pids, list):
#         print("pids 不是一个列表，请检查数据格式。")
#         return
#
#     endnum = int(len(pids) / 100)
#     chunk_size = 100  # 每次请求最多100个商品ID
#
#     # 写入表头
#     with open('result1.csv', mode='w', newline='', encoding='utf-8') as f1:
#         writerf1 = csv.writer(f1)
#         writerf1.writerow([
#             '商品id', '总评数', '平均分',
#             '好评数', '默认好评数', '好评率',
#             '中评数', '差评数', '追评数',
#             '视频晒单数'
#         ])
#
#     for i in range(1, endnum):
#         newpids = pids[100 * (i - 1):100 * i]
#         comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="  # 修正这一行的缩进
#         for pid in newpids:
#             if pid == '商品id':
#                 continue
#             else:
#                 comment_url += str(pid) + ','  # 添加逗号分隔
#
#         try:
#             # 发送请求
#             comment_r = requests.get(comment_url, headers=headers[0], proxies=getip(), timeout=15)
#             comment_r.raise_for_status()  # 检查请求是否成功
#             comment_data = comment_r.json()
#
#             # 检查键是否存在
#             if "commentsCount" not in comment_data:
#                 print(f"未找到 'commentsCount' 键。响应内容：{comment_data}")
#                 continue
#
#             p_comment = []
#             for comment in comment_data["commentsCount"]:
#                 p_comment.append([
#                     comment.get("ProductId", ""),
#                     comment.get("CommentCountStr", ""),
#                     comment.get("AverageScore", ""),
#                     comment.get("GoodCountStr", ""),
#                     comment.get("DefaultGoodCountStr", ""),
#                     comment.get("GoodRate", ""),
#                     comment.get("GeneralCountStr", ""),
#                     comment.get("PoorCountStr", ""),
#                     comment.get("AfterCountStr", ""),
#                     comment.get("VideoCountStr", "")
#                 ])
#
#             # 写入数据
#             with open('result1.csv', mode='a', newline='', encoding='utf-8') as f1:
#                 writerf1 = csv.writer(f1)
#                 for item in p_comment:
#                     writerf1.writerow(item)
#
#         except requests.exceptions.RequestException as e:
#             print(f"请求错误：{e}")
#         except ValueError as e:
#             print(f"JSON 解码错误：{e}")
#             print(f"响应内容：{comment_r.text}")
#         except Exception as e:
#             print(f"处理评论数据时出错：{e}")
#         time.sleep(random.random() * 5)  # 添加随机延时，避免请求过于频繁
#
#
# def getpinpai(url):
#     res = requests.get(url, headers=headers[0], proxies=getip())
#     res.encoding = 'utf-8'
#     text = res.text
#
#     selector = etree.HTML(text)
#     list = selector.xpath('.//ul[@class="J_valueList v-fixed"]/li')
#     rows = []
#     for i in list:
#         pinpai1 = i.xpath('.//a/text()')[-1].replace('\n\t\t\t\t\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t\t\t\t\t', '')
#         rows.append(pinpai1)
#     return rows
#
#
# def savedata(data):
#     if os.path.exists('result.csv'):
#         with open('result.csv', mode='a+', newline='', encoding='utf-8') as f:
#             writerf = csv.writer(f)
#             for item in data:
#                 writerf.writerow(item)
#     else:
#         with open('result.csv', mode='a+', newline='', encoding='utf-8') as f:
#             writerf = csv.writer(f)
#             writerf.writerow(['商品id', '标题', '价格', '店铺', '品牌', '图片'])
#             for item in data:
#                 writerf.writerow(item)
#
#
# if __name__ == '__main__':
#     # try:
#         #获取品牌列表
#         pinpai = getpinpai('https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=手机&pvid=8917aa3c960c420fbd585763a6f55d02')
#         print(pinpai)
#         for item in pinpai:
#             for i in range(1, 10):
#                 time.sleep(random.random() * 10)
#                 url = f'https://search.jd.com/search?keyword=手机&wq=手机&ev=exbrand_{item}%5E&pvid=8917aa3c960c420fbd585763a6f55d02&page={i * 2 - 1}'
#                 savedata(getdata(url, item))
#                 print(url)
#
#         获取评论数据
#         data = pd.read_csv('result.csv', header=None, encoding='utf-8', names=['商品id', '标题', '价格', '店铺', '品牌', '图片'])
#         pids = data['商品id'].tolist()
#         getcommit(pids)
#
#         # 合并数据
#         df1 = pd.read_csv('result.csv', encoding='utf-8')
#         df2 = pd.read_csv('result1.csv', encoding='utf-8')
#         df1['商品id'] = df1['商品id'].astype(str)
#         df2['商品id'] = df2['商品id'].astype(str)
#         outfile = pd.merge(df1, df2, left_on='商品id', right_on='商品id')
#         outfile.to_csv('result2.csv', encoding='utf-8', index=False)
#
#         # 数据处理
#         data_processing('result2.csv', 'result3.csv')
#
#     except Exception as e:
#         print(f"主程序出错：{e}")