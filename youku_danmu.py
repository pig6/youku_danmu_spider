import os
import time
import json
import random

import jieba
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 词云字体
WC_FONT_PATH = '/Library/Fonts/Songti.ttc'

# 弹幕数据保存文件
DANMU_FILE_PATH = 'youku_danmu.txt'


def spider_danmu(page, vid):
    """
    爬取某酷指定页的弹幕
    :param vid: 每集id
    :param page: 页数
    :return: 1 爬取成功 0 爬取失败或结束
    """
    url = 'https://service.danmu.youku.com/list?jsoncallback=jQuery111203412576115734338_1562833192066&mat=%s&mcount=1&ct=1001&iid=%s&aid=322943&cid=97&lid=0&ouid=0&_=1562833192070' % (
        page, vid)
    kv = {'user-agent': 'Mozilla/5.0',
          'Referer': 'https://v.youku.com/v_show/id_XNDI0NDYyNjk1Mg==.html?spm=a2h0k.11417342.soresults.dselectbutton&s=efbfbd78efbfbd5cefbf'}
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
        return 0
    # 提取json数据并转为json对象
    r_json_obj = jsonp_func_to_json_obj(r.text)
    # 如果请求的总数count=0则说明这集的弹幕爬取完成
    if not r_json_obj['count']:
        return 0
    # 获取弹幕列表数据
    r_json_result = r_json_obj['result']
    # 遍历评论对象列表
    for r_json_danmu in r_json_result:
        # 以追加模式换行写入每条评价
        with open(DANMU_FILE_PATH, 'a+') as file:
            file.write(r_json_danmu['content'] + '\n')
        # 打印弹幕对象中的评论内容
        # print(r_json_danmu['content'])
    return 1


def spider_vid():
    """
    爬取所有集数的id
    :return:
    """
    url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1562949127232&sign=7c7f0662179318842702df90ba93d279&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22v7PUFNUi6SYCASQYH5kNuhB3%5C%22%2C%5C%22client_ts%5C%22%3A1562949127%2C%5C%22version%5C%22%3A%5C%221.7.1%5C%22%2C%5C%22ckey%5C%22%3A%5C%22118%23ZVWZz2eNuT9bVeCrBZyeZYquZYT4zHgzagC2NsTIi95GwDHTyHRV7ZZuusqhzeWZZgZZXoqVzeAuZZZh0HWWGcb%2FZzqTqhZzZgZCcfq4zH2ZZZChXHWVZgZZusqhzeWZZgCuTOq4zH2ZweZKWZW4Zg2ZZCTTcG0aZvQZSpihtGmY4HzeQDu2U8USUgMADCoUCAfqWanH7YR0yJgtuZQZuYPAPQqZZyjCZHtTFU2ZXGtCtF8Qm9N7R9eFEPPeEEKGm8VRHuK%2B7pskURPnCcw4CzaBE%2F3AYapX3A1QlSgnhRYxJXO%2BlamAqZIHM%2F1acUZEw0vef5nygZ%2BQp%2BMOTyVvW4WGaROTt5nd9um2hDsQ%2BoixCfTI6YiFF02LUmmuQ4QDHslLMagCapaEZI2mku9J2str7NI%2F9uEzKvTRc1kFeyKSDQHV%2Bjr3lsKTyQtZMwl3qovtPSUQO9bLnsPNhRpCm1aS13XMjPymveRzgnMIsuyaZbgN6uRVqyz2BJaYBmCYxDyFZO2jFD89%2FPOXiI2Ea19OGJKnVAJ%2By4MzfJ13ntoyttH6wFo2kHNtxXKpME%2FQEdTcriNs%2BUgv0HF3qcv%2BjDYgvlQjFlZmLhI1OA0LfieaTpc7%2FF%2BBoy8lpMkl5UbG7YaOtcvhmVKKH7sYYHWfXt7bwHj4qTjx1Ga7rRvLzwINGpYOObSd8cOa0Gqt0L2HNJMM39bnUb3nK7waTrc6reltlBY5UXtqY7GeVn63muFg%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNDI0NDQ0ODEwNA%3D%3D%5C%22%2C%5C%22play_ability%5C%22%3A1280%2C%5C%22current_showid%5C%22%3A%5C%22322943%5C%22%2C%5C%22master_m3u8%5C%22%3A1%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%221.7.1%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%221.7.1%5C%22%2C%5C%22sver%5C%22%3A%5C%221.3%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22mac%5C%22%2C%5C%22osv%5C%22%3A%5C%22%5C%22%2C%5C%22dq%5C%22%3A%5C%22auto%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22AjEwNjExMTIwMjYCdi55b3VrdS5jb20CL3Zfc2hvdy9pZF9YTkRJME5EWXlOamsxTWc9PS5odG1s%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%7D%22%7D'
    kv = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://v.youku.com/v_show/id_XNDI0NDQ0ODEwNA==.html?spm=a2h0j.11185381.listitem_page1.5!2~A&&s=efbfbd78efbfbd5cefbf',
        'Cookie': 'u_l_v_t=0; cna=v7PUFNUi6SYCASQYH5kNuhB3; __ysuid=1562949024337ztT; __ayft=1562949024339; __aysid=1562949024340978; __arycid=dz-3-00; __ayscnt=1; __arcms=dz-3-00; _m_h5_tk=02ce6d6b0eceed8aae67776021e3a497_1562953344744; _m_h5_tk_enc=6e38b39815fb2ec3f45a085fe47d49db; juid=01dfjgavou2nps; seid=01dfjgavp031a7; referhost=https%3A%2F%2Fv.youku.com; yseid=15629490257243Sa96L; yseidcount=1; ycid=0; __arpvid=15629491247659iDslU-1562949124784; __aypstp=2; __ayspstp=2; seidtimeout=1562950927582; ypvid=1562949128258xomaB4; ysestep=2; yseidtimeout=1562956328261; ystep=2; __ayvstp=4; __aysvstp=4; isg=BPb2HuUMt2kKwkLwJFW9XfNGRyo4vzvdrLzMy2Df4ll1o5Y9yKeKYVxRuz9qSjJp'}
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
    # 提取json数据并转为json对象
    r_json_obj = jsonp_func_to_json_obj(r.text)
    # 获取电视剧简介集数
    video_list = r_json_obj['data']['data']['videos']['list']
    # 创建一个生成器并返回
    return (video['vid'] for video in video_list)


def jsonp_func_to_json_obj(jsonp_func):
    """
    jsonp返回函数提取json并转为对象
    :param jsonp_func: jsonp请求返回的数据，格式：xxx(json)
    :return: json对象
    """
    # 找到jsonp数据的左括号位置并+1
    json_start_index = jsonp_func.index('(') + 1
    # 找到最后一个)的位置
    json_end_index = jsonp_func.rindex(')')
    # 截取json数据字符串
    r_json_str = jsonp_func[json_start_index:json_end_index]
    # 字符串转json对象
    return json.loads(r_json_str)


def batch_spider_danmu():
    """
    批量爬取某酷弹幕
    """
    # 写入数据前先清空之前的数据
    if os.path.exists(DANMU_FILE_PATH):
        os.remove(DANMU_FILE_PATH)
    # 爬取所有集数的vid
    vids = spider_vid()
    # 第一层循环遍历集数
    for vid in vids:
        print(vid)
        i = 0
        # 第二层循环遍历页数（分钟数）
        while spider_danmu(i, vid):
            # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
            time.sleep(random.random() * 5)
            i += 1
    print('爬取完毕')


def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open(DANMU_FILE_PATH) as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=False)
        wl = " ".join(wordlist)
        print(wl)
        return wl


def create_word_cloud():
    """
    生成词云
    :return:
    """
    # 数据清洗词列表
    stop_words = ['哈哈', '哈哈哈', '哈哈哈哈', '啊啊啊', '什么', '为什么', '不是', '就是', '还是', '真是', '这是', '是不是',
                  '应该', '不能', '这个', '电视','电视剧', '怎么',
                  '这么', '那么', '那个', '没有', '不能', '不知', '知道']
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=900, width=940, height=400, scale=10,
                   max_font_size=50, random_state=42, stopwords=stop_words, font_path=WC_FONT_PATH)
    # 生成词云
    wc.generate(cut_word())
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()


if __name__ == '__main__':
    # 爬取所有弹幕
    # batch_spider_danmu()
    # 生成词云
    create_word_cloud()
