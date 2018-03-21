# -*- coding:utf-8 -*-
import requests
import random
from bs4 import BeautifulSoup

inputStr = input(f"{'请输入要查询的电影名字:'}")
inputData = {
    'keyword': inputStr
}
baseUrl = 'https://www.80s.tw/search'

#uer_agent库，随机选取，防止被禁
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]



class Spider():
    def __init__(self):
        self.movieIdList = []
        self.selectId = 0

    def getMovieIdList(self):
        headers = {'user-agent': random.choice(USER_AGENT_LIST)}
        response = requests.post(baseUrl, data=inputData, headers=headers, verify=False)
        soup = BeautifulSoup(response.content)
        searchResult = soup.find('ul', attrs={'class': "clearfix search_list"})
        searchList = searchResult.find_all('li')
        i = 0
        for movie in searchList:
            i += 1
            move_a = movie.find('a')
            name = move_a.text
            href = move_a['href']
            self.movieIdList.append(href)
            print('资源序号:%d,%s' % (i, name.replace("\n", "").replace(" ", "")))

    def getInputId(self):
        while True:
            self.selectId = int(input(f"{'输入资源序号:'}"))
            if (self.selectId > len(self.movieIdList)) | (self.selectId < 0):
                print('序号不在查询列表范围内!!!')
            else:
                self.getThunder()
                break

    def getThunder(self):
        headers = {'user-agent': random.choice(USER_AGENT_LIST)}
        movieUrl = 'https://www.80s.tw%s' % self.movieIdList[self.selectId - 1]
        response_movie = requests.get(movieUrl, headers=headers, verify=False)
        soup_movie = BeautifulSoup(response_movie.content)
        thunder = soup_movie.find('ul', attrs={'class': 'dllist1'})
        thunderList = thunder.find_all('li')
        for thunder_li in thunderList:
            thunder_span = thunder_li.find('span', attrs={'class': 'xunlei dlbutton1'})
            if thunder_span:
                thunder_a = thunder_span.find('a')
                print('%s,地址:%s' % (thunder_a['thunderrestitle'], thunder_a['href']))
                self.getInputId()




spider = Spider()
spider.getMovieIdList()
spider.getInputId()
