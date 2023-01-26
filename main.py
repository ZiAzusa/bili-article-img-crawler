from requests import get
from json import loads
from time import sleep
import os

print("欢迎使用B站专栏图片爬虫\n" + "-" * 30)
uid = input("请输入要爬取用户的UID：")
if not os.path.exists(uid):
    os.makedirs(uid)

length = 30
pn = 0
while length == 30:
    pn += 1
    print("页数：" + str(pn))
    api = "https://api.bilibili.com/x/space/article?ps=30&mid=" + uid + "&pn=" + str(pn)
    res = loads(get(api).content)
    if (res['code'] != 0):
        print("\033[1;31m错误！\n错误代码：" + str(res['code']) + "\n错误信息：" + res['message'] + "\033[0m!\n程序将在3秒后退出...")
        sleep(3)
        exit()
    ids = [str(i['id']) for i in res['data']['articles']]
    for i in ids:
        if not os.path.exists(uid + "/" + i):
            os.makedirs(uid + "/" + i)
        print("正在下载：CV" + i)
        url = "https://www.bilibili.com/read/cv" + i
        html = get(url).content
        html = str(html).encode('utf8').decode('unicode_escape')
        data = html.split('__INITIAL_STATE__=')[-1]
        data = data.split('"')
        imgs = ["https:" + j.replace("\\u002F", "/").replace("\\", "/")[:-1] for j in data if 'hdslb.com' in j if not 'http' in j if not '/' in j]
        for j in imgs:
            filename = j.split('/')[-1]
            img = get(j).content
            with open(uid + "/" + i + "/" + filename ,'wb') as f:
                f.write(img)
        print("CV" + i + "下载完成，共下载图片：" + str(len(imgs)))
    length = len(ids)
print("\033[1;32m全部图片下载完成！\033[0m!\n程序将在3秒后退出...")
sleep(3)
exit()