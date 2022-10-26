from requests_html import HTMLSession
from selenium import webdriver
session = HTMLSession()


import os, time, re


def parse_cookie_str():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.kuaishou.com/brilliant')
    time.sleep(3)  # 等待3秒保证cookie加载完毕，也可以自行写一个判断
    cookie_str = driver.get_cookies()
    str1 = cookie_str[2]['value']
    driver.quit()  # 关闭后台浏览器
    return str1

class KsSpider(object):

    os_path = os.getcwd() + '/快手视频/'
    if not os.path.exists(os_path):
        os.mkdir(os_path)

    def __init__(self):
        '''
        爬虫第一步：数据准备
        '''
        self.start_url = 'https://www.kuaishou.com/graphql'
        self.headers = {
            'Cookie': f'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did={parse_cookie_str()}',
            'Host': 'www.kuaishou.com',
            'Origin': 'https://www.kuaishou.com',
            'Referer': 'https://www.kuaishou.com/brilliant',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
                    }
        self.data = {"operationName":"brilliantTypeDataQuery","variables":{"hotChannelId":"00","page":"brilliant"},"query":"fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}

    def parse_start_url(self):
        '''
        爬虫第二步：发送请求，获取响应
        :return:
        '''
        response = session.post(url=self.start_url, headers=self.headers, json=self.data).json()
        self.parse_response_data(response)

    def parse_response_data(self, response):
        '''
        爬虫第三步：解析响应，获取数据
        :return:
        '''
        start_num = 0
        data = response['data']['brilliantTypeData']['feeds']
        for feeds in data:
            start_num += 1
            name = feeds['photo']['caption'].split(' ')[0]
            name = re.sub(r'\W', '', name)
            # name = name.split(' ')[0].replace(' ', '')
            photo_url = feeds['photo']['photoUrl']
            data_data = {
                'name': name,
                'photo_url': photo_url
            }
            self.parse_save_data(data_data, start_num)

    def parse_save_data(self, data, start_num):
        '''
        爬虫第四步：保存数据
        :return:
        '''
        Mp3_name = data['name']
        Mp3_data = session.get(data['photo_url']).content
        with open(self.os_path + Mp3_name + '.mp4', 'wb') as f:
            f.write(Mp3_data)
        print(f'第{start_num}个视频----下载完成---logging！！！')

if __name__ == '__main__':
    s = KsSpider()
    s.parse_start_url()