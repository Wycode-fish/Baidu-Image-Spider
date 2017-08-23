#！-*-coding:utf-8-*-
import subprocess
import re
import urllib
import urllib2
import time
import socket
import types
import requests
import sys
import string
import os
import itertools
import threading
from multiprocessing import Pool
from BaiduURLDecoder import BaiduURLDecoder

'''
Goal: 爬取百度图片
'''      

class BaiduPicCrawler(object):
    def __init__(self, obj_name):
        self.url_pre = 'https://image.baidu.com/search/index'+\
            '?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&'+\
            'fm=result&fr=&sf=1&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&'+\
            'width=&height=&face=0&istype=2&ie=utf-8&word='; 
        self.obj_name = obj_name;
        self.decoder = BaiduURLDecoder();
        #-- check directory
        if not os.path.exists((os.getcwd()+'/images').replace('/','\\')):
            os.mkdir((os.getcwd()+'/images').replace('/','\\'));
        dir_path = (os.getcwd()+'/images/'+obj_name).replace('/','\\');
        if os.path.exists(dir_path):
            self.dir_path = dir_path;
        else :
            os.mkdir(dir_path);
            self.dir_path = dir_path;
        #-- end check directory
        self.url = self.url_pre + urllib.quote(self.obj_name.encode('utf-8'));
        self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"};
        self.img_count = 0;
        
    def getPage(self, url):
        '''
                    获取网页html，并保存至"page.txt"
        '''
        request = urllib2.Request(url, headers=self.headers);
        try:
            response = urllib2.urlopen(request).read();
            f = open(self.dir_path+'\\'+"page.txt",'w+');
            f.writelines(response);
            f.close();
            print self.getCurrentTime()+' getPage(): success.'
            return response;
        except urllib2.URLError or IOError,e:
            print self.getCurrentTime()+' getPage(): fail. - Log: '+e.reason;
            return;   
    
    def getPics(self, page):
        '''
                    爬取图片保存为"[obj_name]_[number].jpg"                                            
        '''
        print self.getCurrentTime()+' getPics() start...'
        pattern = re.compile('"objURL":"(.*?)"');
        img_urls = re.findall(pattern, page);
        if len(img_urls) == 0:
            return -1;
        #map(lambda x:x.decode('utf-8'), img_urls);
        for i,img_url in enumerate(img_urls):
            img_url = self.decoder.decode(img_url);
            req = urllib2.Request(img_url, headers=self.headers);
            file_name = self.dir_path+'\\'+self.obj_name+'_'+str(self.img_count)+'.jpg';
            try:
                res = urllib2.urlopen(req);
                f = open(file_name,'wb');
                f.writelines(res.read());
                f.close();
                print file_name + ' saved.'
                self.img_count += 1;
            except urllib2.URLError or IOError,e:
                print self.getCurrentTime()+' getPage(): fail. - Log: '+file_name+'->'+str(e.reason);
                return;
        print self.getCurrentTime()+' getPics(): success.'
        return 1;
    
    def getJSONURLs(self):
        json_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={obj_name}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={obj_name}&face=0&istype=2&qc=&nc=1&fr=&pn={page_num}&rn=30';
        json_urls_iter = (json_url.format(obj_name = urllib.quote(self.obj_name.encode('utf-8')), page_num = x) for x in itertools.count(start=0, step=30));
        return json_urls_iter;
    
    def getPics2(self):
        print self.getCurrentTime()+' getPics2() start...'
        json_urls_iter = self.getJSONURLs();
        for json_url in json_urls_iter:
            page = self.getPage(json_url);
            status = self.getPics(page);
            if status == -1:
                break;
        print self.getCurrentTime()+' getPics2() over.'
             
    def getCurrentTime(self):
        return time.strftime("[%Y/%m/%d]-%H:%M:%S]:", time.localtime(time.time()));
       
    def start(self):
        print self.getCurrentTime()+' start...';
        #page = self.getPage(self.url);
        self.getPics2();
        

def run(obj_name):
    crawler = BaiduPicCrawler(obj_name);
    crawler.start();
    
def threads_crawl():
    '''
            多线程同时爬多类图（慢）
    '''
    thread_list = [];
    while True:
        obj_name = raw_input("Object name >> ");
        obj_name = obj_name.strip();
        if obj_name == 'exit()':
            break;
        else:
            thread = threading.Thread(target=run, args=(obj_name,));
            thread_list.append(thread);
    for t in thread_list:
        t.start(); 
    
def process_crawl():
    '''
            多进程同时爬多类图（较快）
    '''
    obj_list = [];
    p = Pool();
    while True:
        obj_name = raw_input("Object name >> ");
        obj_name = obj_name.strip();
        if obj_name == 'exit()':
            print 'collection of images has started...'
            break;
        else:
            obj_list.append(obj_name);
    for obj in obj_list:
        p.apply_async(run, args=(obj,));
    p.close();
    p.join();
    
if __name__=='__main__':
    process_crawl();
    
    '''
    obj_list = [];
    p = Pool();
    while True:
        obj_name = raw_input("Object name >> ");
        obj_name = obj_name.strip();
        if obj_name == 'exit()':
            break;
        else:
            obj_list.append(obj_name);
    for obj in obj_list:
        p.apply_async(run, args=(obj,));
    p.close();
    p.join();
    '''
    
    '''
    thread_list = [];
    while True:
        obj_name = raw_input("Object name >> ");
        obj_name = obj_name.strip();
        if obj_name == 'exit()':
            break;
        else:
            thread = threading.Thread(target=run, args=(obj_name,));
            thread_list.append(thread);
    for t in thread_list:
        t.start();    
    '''
    #crawler = BaiduPicCrawler(obj_name);
    #crawler.start();
    
'''
print os.getcwd().replace('\\','/');
dir_name = '/images'.replace('/', '\\')
os.mkdir(os.getcwd()+dir_name);
if os.path.exists(os.getcwd()+'/images'.replace('/', '\\')):
    print 'exist.'
test_str = 'ippr_z2C$qAzdH3FAzdH3F48_z&e3Bw7p5_z&e3Btpv_z&e3BvgAzdH3Fvw6AzdH3FuAzdH3Fb9AzdH3F00AzdH3FI42ndn00b9_u_z&e3B3r2';
decoder = BaiduURLDecoder();
print decoder.decode(test_str);
'''

'''
print urllib.unquote('%E4%B8%B0%E7%94%B0').decode('utf-8');
char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
str_table = {
    '_z2C\$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}
test_str = 'ippr_z2C$qAzdH3FAzdH3F48_z&e3Bw7p5_z&e3Btpv_z&e3BvgAzdH3Fvw6AzdH3FuAzdH3Fb9AzdH3F00AzdH3FI42ndn00b9_u_z&e3B3r2';
for (key,value) in str_table.items():
    test_str = re.sub(key, value, test_str);
code_tab = 'wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla';
decode_tab = 'abcdefghijklmnopqrstuvw1234567890';
match_tab = string.maketrans(code_tab,decode_tab);
str_trans = str.translate(test_str,match_tab);
print str_trans;
'''
     
        
'''       
    url_pre = 'https://image.baidu.com/search/index'+\
            '?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&'+\
            'fm=result&fr=&sf=1&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&'+\
            'width=&height=&face=0&istype=2&ie=utf-8&word='; 


url = url_pre + urllib.quote('丰田'.encode('utf-8'));
print url;
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"};
request = urllib2.Request(url,headers=headers);
response = urllib2.urlopen(request);

page = response.read();
if page is None:
    print 'read failed';
else:
    f = open('page.txt','w+');
    f.writelines(page);
    f.close();
    pattern = re.compile('"objURL":"(.*?)"');
    img_urls = re.findall(pattern, page);
    map(lambda x:x.decode('utf-8'), img_urls);
    for i,img_url in enumerate(img_urls):
        req = urllib2.Request(img_url, headers=headers);
        file_name = '丰田'+str(i)+'.jpg';
        try:
            res = urllib2.urlopen(req);
            f = open(file_name, 'wb');
            f.writelines(res.read());
            f.close();
        except URLError,e:
            print 'error:'+e.reason;
            exit(1) ;
'''


#print urllib.unquote('%E8%BD%A6').decode('utf-8');