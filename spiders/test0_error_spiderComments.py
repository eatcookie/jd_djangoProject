




#############################
# 原代码，手动(复制粘贴商品id)+自动(爬)+手动(error json随便输入内容，继续爬),
#
# 但下面的全部是失败的


import csv

import requests


def collect(skuid):
    # global i
    page = 1

    url = f'https://club.jd.com/comment/productPageComments.action?productId={skuid}&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&rid=0&fold=1'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/91.0.4472.106Safari/537.36',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
        'Referer': url
    }
    print(skuid, page)
    while True:
        try:
            dic = requests.get(url=url, headers=headers).json()
            break
        except:
            input('error json: ')
    if not dic['comments']:
        return
    for li in dic['comments']:
        name = li['nickname']
        comment = li['content']
        time = li['creationTime']
        score = li['score']
        image = len(li.get('images', []))
        video = len(li.get('videos', []))
        after = li.get('afterUserComment', {}).get('content', '')
        reply = ([i for i in li.get('replies', []) if 'venderShopInfo' in i.keys()] + [{}])[0].get('content', '')
        like = li['usefulVoteCount']
        row = [skuid, name, time, comment, score, image, video, after, reply, like]
        print(row)
        csv.writer(open('comments.csv', 'a', encoding='utf-8-sig', newline='')).writerow(row)
        # i += 1
        # page += 1


if __name__ == '__main__':
    i = 0
    csv.writer(open('TitleComment.csv', 'w', encoding='utf-8-sig', newline='')).writerow(
        ['商品ID', '昵称', '时间', '评论', '评分', '图片', '视频', '追评', '回复', '点赞'])

    collect('100056884537')
#         # collect('这里填商品id，然后手动爬20次')
#         # collect('这里填商品id，然后手动爬20次')
#         # collect('这里填商品id，然后手动爬20次')
