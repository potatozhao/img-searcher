#coding:utf8
import requests,json,os,urllib,re,xml.dom.minidom,os,json,time
from io import open as iopen
from urlparse import urlsplit
import time,random, bs4
import pdb

import logging

logger = logging.getLogger('mylogger')

logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)

def Download(objURL,path,name):
    #time.sleep(1)
    logger.info("Start Downlaod img :%s"%(objURL))
    file_name =  urlsplit(objURL)[2].split('/')[-1]
    file_suffix = file_name.split('.')[-1].lower()

    Header2={"HOST":urlsplit(objURL)[1],
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            'Connection':'close',
            }

    try:
	#print objURL
        if 'imgurl:"' in objURL:
	        objURL_final = objURL.split('imgurl:"')[1]
        else:
            objURL_final = objURL
	    print objURL_final
        i = requests.get(objURL_final,timeout=3,headers=Header2)
        if i.status_code == requests.codes.ok:
            with iopen(os.path.join(path,name+'.%s'%file_suffix), 'wb') as file:
                file.write(i.content)
                logger.info(name + 'save %s' % objURL_final)
                return 1
        else:
            logger.info( name+'could not save %s' % objURL_final+i.status_code)
            return 0
    except Exception,e:
        logger.warning('Downlaod'+e.message+objURL_final)
        return 0




def BaiduDecode(objURL):
    return  objURL
    #print objURL
    objURL=re.sub(r'\_z2C\$q',r':',objURL)
    objURL=re.sub(r'\_z&e3B',r'.',objURL)
    objURL=re.sub(r'AzdH3F',r'/',objURL)
    objURL=objURL.lower()
    code={
        'w':"a",'k':"b",'v':"c",'1':"d",'j':"e",'u':"f",'2':"g",'i':"h",'t':"i",'3':"j",'h':"k",'s':"l",'4':"m",
        'g':"n","5":"o",'r':"p",'q':"q","6":"r",'f':"s",'p':"t","7":"u",'e':"v",'o':"w","8":"1",'d':"2",'n':"3",
        "9":"4",'c':"5",'m':"6","0":"7",'b':"8",'l':"9",'a':"0",
        ':':':','.':'.',"/":"/",'x':'x','y':'y','z':'z','_':'_'
    }
    url=''
    for char in objURL:
        if code.has_key(char):
            url=url+code[char]
        else:
            url=url+char

    return url



def Baidu(word):
    '''
    pageNum从0开始，每个结果都是一个pageNum
    returnNum是返回结果个数，最大60个，如果不足60，返回实际个数

    '''
    print 'Start baidu searching'
    returnNum=60
    word2=word
    BASE_PATH = os.path.join('Download', word2.decode('utf8'))
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    Header={"HOST":"image.baidu.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "Referer":"http://image.baidu.com/",
            }

    try:
        #url=url='http://image.baidu.com/i?tn=baiduimagejson&width=&ie=utf-8&height=&word={0}&rn={1}&pn={2}'.format(urllib.quote(word),5,0)
        url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&&cg=star&itg=0&z=0&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=b4&word={0}&rn={1}&pn={2}'.format(urllib.quote(word),5,0)
        req = requests.get(url,headers=Header)
        result=json.loads(req.text)
        logger.info("Downlaod json url first"+ url)
    except Exception,e:
        logger.warning("Downlaod json first error:"+e.message)
        return
    listNum=int(result['listNum'])
    logger.info( 'I find %d results'%listNum)
    time.sleep(5)
    count=0
    URLList=[]
    pageNum=-1
    for i in range(0,1000):
        try:
            url='http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&cg=star&itg=0&z=0&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=b4&word={0}&rn={1}&pn={2}'.format(urllib.quote(word),returnNum,pageNum+1)
            #url='http://image.baidu.com/i?tn=baiduimagejson&width=&ie=utf-8&height=&word={0}&rn={1}&pn={2}'.format(urllib.quote(word),returnNum,pageNum+1)
            req=requests.get(url,headers=Header)
            result=json.loads(req.text)
            logger.info("Downlaod json %d :"%i + url)
        except requests.HTTPError,e:
            logger.warning("Downlaod json %d error"%i + e.message)
            break
        for num,item in enumerate(result['imgs']):
            try:
                pageNum=item['pageNum']
                objURL=item['objURL']
                URLList.append(objURL)
                count=count+Download(objURL=BaiduDecode(objURL),path=BASE_PATH,name="baidu_%06d"%pageNum)
            except Exception,e:
                logger.warning("get image url error :" + e.message)
                break
        #time.sleep(60)
        if pageNum+1>listNum:
            break
    logger.info('I download {0} pictures in folder {1}'.format(count,word2))


##########################################

def GoogleDecode(objURL):
    url=re.findall(r'(?<=imgurl\=).*?(?=&)',objURL)

    return url[0]

def Google(word):
    print 'Start google searching'
    returnNum=60
    word2=word
    BASE_PATH = os.path.join('Download', word2.decode('utf8'))
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    Header={"HOST":"www.google.com.hk",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "Referer":"https://www.google.com.hk/search?newwindow=1&safe=strict&client=firefox-a&rls=org.mozilla%3Azh"
                          "-CN%3Aofficial&channel=fflb&biw=1680&bih=603&tbm=isch&sa=1&q=python+re&oq=python+re&gs_l=img.12"
                          "...0.0.0.6458.0.0.0.0.0.0.0.0..0.0....0...1c..45.img..0.0.0.PDYBF-VoHds",
                }
    pageNum=0
    count=0

    try:
        url='https://www.google.com.hk/search?newwindow=1&safe=strict&hl=zh-CN&site=imghp&tbm=isch&source=hp&biw=1304&b' \
            'ih=697&q={0}&oq={1}&'.format(urllib.quote(word),urllib.quote(word))

        req=requests.get(url,headers=Header,verify=False)
        soup=bs4.BeautifulSoup(req.text)
        #print soup
        data=soup.findAll("div",attrs={'class':'rg_di'})
        for i,div in enumerate(data):
            pageNum=pageNum+1
            objURL=div.a['href']
            #objURL2=div.img['data-src']
            count=count+Download(objURL=GoogleDecode(objURL),path=BASE_PATH,name="google_%06d"%pageNum)
    except requests.HTTPError,e:
        print e.message

    for i in range(1,10):
        try:
            url='https://www.google.com.hk/search?q={0}&newwindow=1&safe=strict&hl=zh-CN&biw=1304&' \
                'bih=134&site=imghp&tbm=isch&ijn=1&ei=41mVU6L5GoPf8AWZqYLgBQ&start={1}'.format(urllib.quote(word),100*i)

            req=requests.get(url,headers=Header,verify=False)
            soup=bs4.BeautifulSoup(req.text)
            data=soup.findAll("div",attrs={'class':'rg_di'})
            for i,div in enumerate(data):
                pageNum=pageNum+1
                objURL=div.a['href']
                #objURL2=div.img['data-src']
                count=count+Download(objURL=Decode(objURL),path=BASE_PATH,name="google_%06d"%pageNum)
            #time.sleep(60)
        except requests.HTTPError,e:
            print e.message
            break
    print 'I download {0} pictures in folder {1}'.format(count,word2)


###########################################################

def BingDecode(objURL):
    #print objURL
    url=re.findall(r'http.*?jpg|http.*?png|http.*?jpeg|http.*?gif|http.*?tif|http.*?svg|http.*?pic',objURL,re.I)
    #url=re.findall(r'http.*?jpg|http.*?png',objURL,re.I)
    #print url
    return url[-1]

def Bing(word):
    word2=word
    BASE_PATH = os.path.join('Download', word2.decode('utf8'))
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    Header={"HOST":"cn.bing.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "Referer":"http://cn.bing.com/",
                }
    pageNum=0
    while(True):
        try:
            url='http://cn.bing.com/images/async?q={0}&async=content&first={1}&count=' \
                '35&dgst=ro_u768*&IID=images.1&SFX=2&IG=8e2a698f36a14987a6fc1c6f1f7b8f04&CW=1663&CH=392&CT=1402334651966' \
                '&dgsrr=true'.format(urllib.quote(word),pageNum)

            req=requests.get(url,headers=Header)
            soup=bs4.BeautifulSoup(req.text)
            #print req.text
            begin=soup.div['beg']
            end=soup.div['end']
            data=soup.findAll("div",attrs={'class':'dg_u'})
            for i,div in enumerate(data):

                objURL=div.a['m']
                Download(objURL=BingDecode(objURL),path=BASE_PATH,name="bing_%06d"%pageNum)
                pageNum=pageNum+1
            #time.sleep(60)
        except Exception,e:
            print 'Bing',e.message
            break

##################################################################
import sys
def Flickr(word,i=0,key='bf0d807bea897bf98e217a473c8c3489'):
    reload(sys)
    #print sys.getdefaultencoding()
    sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()


    word2=word
    BASE_PATH = os.path.join('Download', word2.decode('utf8'))
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    Header={"HOST":"api.flickr.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "Referer":"http://www.flickr.com/",

                 }
    for page_num in range(1,10):
        url='https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&text={1}&&sort=relevance&per_page=500&page={2}'.format(key,urllib.quote(word2),page_num)
        print url
        r=requests.get(url,verify=False,headers=Header)
        URLList=[]
        doc = xml.dom.minidom.parseString(r.text.encode('utf8'))
        for i,node in enumerate(doc.getElementsByTagName("photo")):
            photo_id=node.getAttribute('id')
            secret=node.getAttribute('secret')
            server=node.getAttribute('server')
            farm=node.getAttribute('farm')
            photo_url='https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg'.format(farm,server,photo_id,secret)
            URLList.append(photo_url)
            Download(photo_url,BASE_PATH,"flickr_%06d"%(500*(page_num-1)+i))
