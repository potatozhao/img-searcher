# coding: utf-8
'''
运行时需要selenium的jar包运行支持，下载地址：http://docs.seleniumhq.org/download/
terminal运行jar包：
java -jar selenium-server-standalone-xxxxxx.jar
'''

from selenium import webdriver
import time

class ImgSearcher:
    def __init__(self, engine='baidu'):
        # 调用Firefox浏览器模拟爬取
        # 也可以调用PhantomJS，但需要下载PhantomJS.exe（http://phantomjs.org/download.html）并加入系统path
        self.browser = webdriver.Firefox()  # 打开浏览器
        # 此处以baidu搜索为例
        if engine == 'baidu':
            self.imgsite = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=detail&fr=&sf=1&fmq=1450017075637_R&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=test'
        self.browser.get(self.imgsite)
        self.browser.maximize_window()  # 窗口最大化
        print 'connection built, page title: ' + self.browser.title

    def search(self, query, pages=10):
        urls = set()  # 存储爬取到的图片url
        self.browser.find_element_by_id('kw').clear()  # 清除搜索框的现有文字
        self.browser.find_element_by_id('kw').send_keys(query) # 输入查询内容
        self.browser.find_element_by_class_name('s_btn_wr').submit()  # 点击提交
        time.sleep(5)
        numinfo = self.browser.find_element_by_id('resultInfo').text  # 本次查询共有多少图片
        numinfo = int(filter(str.isdigit, numinfo.encode('utf-8', errors='ignore')))
        # 下面模拟浏览器的页面滚动，以逐步加载更多图片
        position = 0
        for i in range(pages):
            position += i*500
            js = "document.documentElement.scrollTop=%d" % position  # 浏览器翻页的js脚本
            self.browser.execute_script(js)
            time.sleep(5)
            # 得到网页内容后，根据html/xml结构，找到图片下载链接的标签即可
            # 以百度为例，图片下载链接的xpath是"//ul/li/div/div/a[@class='down']"
            # 不同的搜索引擎，如google、bing，其下载链接标签路径可能不一样
            for link in self.browser.find_elements_by_xpath("//ul/li/div/div/a[@class='down']"):
                url = link.get_attribute('href')
                print url
                urls.add(url)
                # 如果需要下载，可以在此处加入
                # 例如 urllib.urlretrieve(url, './yourfolder/%s' % filename)
        return numinfo, urls

if __name__ == '__main__':
    iser = ImgSearcher(engine='baidu')
    # 如果是中文词条，注意先处理编码问题
    numinfo, urls = iser.search('starbucks', pages=5)
    print numinfo