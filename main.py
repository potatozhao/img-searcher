#coding:utf8
from src import Baidu,Google,Bing
from src import Flickr
import chardet
import bs4
import sys
reload(sys)
sys.setdefaultencoding('utf8')

while True:
    print  u'请输入您要查询的关键字：'
    word=raw_input()
    print u'1-百度'
    print u'2-谷歌'
    print u'3-必应'
    print u'4-Flickr'
    print u"请输入对应搜索引擎编号:"
    fun=raw_input()
    
    if fun=='1':
        Baidu(word)
    elif fun=='2':
        Google(word)
    elif fun=='3':
        Bing(word)
    elif fun=='4':
        Flickr(word)
    elif fun=='q':
        break
    else:
        print '输入错误，请重新选择'
        
