#£¡-*-coding:utf-8-*-
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

class BaiduURLDecoder(object):
    def __init__(self):
        self.str_table = {
                          '_z2C\$q': ':',
                          '_z&e3B': '.',
                          'AzdH3F': '/'
                          };
        self.code_tab = 'wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla';
        self.decode_tab = 'abcdefghijklmnopqrstuvw1234567890';
        self.match_tab = string.maketrans(self.code_tab,self.decode_tab);
        
    def decode(self, test_str):
        for (key,value) in self.str_table.items():
            test_str = re.sub(key, value, test_str);
        str_trans = str.translate(test_str,self.match_tab);
        return str_trans;