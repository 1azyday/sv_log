import requests
import sqlite3
import os
from pyquery import PyQuery as pq
import time
import db

# 页面缓存
def get_page(target_url, filename):
    # 建立 cached 文件夹
    folder = 'cached'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        print('sleep~')
        time.sleep(10)
        r = requests.get(target_url)
        print('get request!')

        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content

# 网页数据清洗
def data_from_html(html):
    page = pq(html)
    datas = page('#table1 tbody')
    data_for_play = []
    data_for_win = []
    data_for_class = []

    for data_line in datas.items('tr'):
        data_list = data_line.text().split()
        data_list.remove('vs')
        data_for_play.append(data_list[2])
        data_for_win.append(data_list[3])

    data_for_class.append(' '.join(data_for_play))
    data_for_class.append(' '.join(data_for_win))
    return data_for_class

# 遍历爬取当周内数据
def data_for_week(week_url):
    count = 1
    week_data = []
    for _ in range(7):
        target_url = week_url + str(count)
        filename = '_'.join(target_url.split('/')[-4:]) + '.html'
        html = get_page(target_url, filename)
        data_for_class = data_from_html(html)
        week_data.append(data_for_class)
        count += 1
    return week_data


def main():
    # 初始的爬取目标
    year, week = 2016, 37
    db_path = 'sv.sqlite'

    with sqlite3.connect(db_path) as connection:
        db.create(connection)
        # 爬取2016——2017数据
        while not year==2018:
            week_url = 'https://shadowlog.com/trend/{}/{}/4/'.format(year, week)
            week_data = data_for_week(week_url)
            date = str(year) + '_' + str(week)

            db.save_data(connection, week_data, date)

            week += 1
            if week > 52:
                year += 1
                week = 1


main()
