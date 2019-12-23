# coding=utf-8
#动态加载数据处理
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os, time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver_path = '../backend/flask_nlp/static/chromedriver.exe'
driver_path = os.path.abspath(driver_path)
driver_path = driver_path.replace('\\', '/')
"""
爬虫api：
    搜索结果页：get_index_result(search)
    小说章节页：get_chapter(url)
    章节内容：get_content(url)
"""


class CpSpider(object):
    def __init__(self):
        time.sleep(5)
        self.search_url = 'https://www.gongzicp.com/novel/search/module/novel/keyword/'
        self.base_url = 'https://www.gongzicp.com/'
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        # 本地driver运行：
        '''
        self.browser = webdriver.Chrome(executable_path=driver_path,options=chrome_options)
        '''
        # docker运行

        self.browser = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            options=chrome_options)

    def parse_url(self, url):
        try:
            self.browser.get(url)
            # 需要等一下，直到页面加载完成
            # 超时时间10s,每0.2秒检查一次
            wait = WebDriverWait(self.browser, 10, 0.2)
            wait.until(EC.presence_of_element_located((By.ID, 'vueBox')))
        except ConnectionError:
            print('Error.')

    # 搜索结果页数据
    def get_index_result(self, keyword, page=0):
        #TODO 解决有些小说搜索页没有tag无法一起打包yield的情况
        url = self.search_url + keyword
        self.parse_url(url)

        try:
            titles = self.browser.find_elements_by_xpath(
                '//*[@class="cp-novel-name"]')
            urls = self.browser.find_elements_by_xpath(
                '//*[@class="cp-novel-name"]')
            images = self.browser.find_elements_by_xpath(
                '//*[@class="cp-novel-cover"]/img')
            authors = self.browser.find_elements_by_xpath(
                '//*[@id="vueBox"]/div[3]/div/div[1]/div/div[2]/div[2]/a')
            profiles = self.browser.find_elements_by_xpath(
                '//*[@id="vueBox"]/div[3]/div/div[1]/div/div[2]/p')
            types = self.browser.find_elements_by_xpath(
                '//*[@class="cp-novel-type"]')
            # tags = self.browser.find_elements_by_xpath('//*[@class="cp-novel-tag"]')
            times = self.browser.find_elements_by_xpath(
                '//*[@class="cp-novel-update"]')
        except Exception as e:
            print(e)
        finally:
            # print(len(titles),len(urls),len(images),len(authors),len(profiles),len(types),len(tags),len(times))
            for title, url, image, author, profile, type, tim in zip(
                    titles, urls, images, authors, profiles, types, times):
                data = {
                    'title': title.text,
                    'url': url.get_attribute('href'),
                    'image': image.get_attribute('src'),
                    'author': author.text,
                    'profile': profile.text,
                    'type': type.text,
                    'time': tim.text
                }
                yield data

    # 小说章节页数据
    def get_chapter(self, url):
        self.parse_url(url)
        chapters = self.browser.find_elements_by_xpath(
            '//*[@id="vueBox"]/div[1]/div[3]/div[2]/div[3]/ul/li/a/span[2]')
        urls = self.browser.find_elements_by_xpath(
            '//*[@id="vueBox"]/div[1]/div[3]/div[2]/div[3]/ul/li/a')
        for chapter_url, chapter in zip(urls, chapters):
            url = chapter_url.get_attribute('href')
            if url != 'javascript:;':
                chapter_text = chapter.text
            else:
                chapter_text = '章节已锁定'

            data = {'url': url, 'chapter': chapter_text}
            yield data

    # 章节内容页数据
    def get_content(self, url):
        self.parse_url(url)
        contents = self.browser.find_elements_by_xpath(
            '//*[@id="cpReadContent"]/p')
        return '\n'.join(i.text for i in contents)


# Test
# cp = CpSpider()
# print("2")
# for i in cp.get_index_result('卡比丘', page=0):

#    print(i)

# cp.parse_url(cp.search_url + '{keyword}'.format(keyword='卡比丘'))
# print(cp.get_content('https://www.gongzicp.com/read-112530.html'))