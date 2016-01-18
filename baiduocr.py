# -*- coding: utf-8 -*-
import sys, urllib, json
import base64
import urllib.parse
import urllib.request

def get_image_data():
    '''
    # local image
    with open("chineseVal.jsp", 'rb') as f:
        jpg_data = f.read()
        jpg_data = base64.b64encode(jpg_data)
        #print(content)
    '''
    image_addr = "http://zzxh.zjsgat.gov.cn:6081/zjwwzzxh/include/chineseVal.jsp"
    req = urllib.request.Request(image_addr)
    resp = urllib.request.urlopen(req)
    jpg_data = resp.read()
    jpg_data = base64.b64encode(jpg_data)
    print(jpg_data)
    return jpg_data

def get_words_from_img(img_data):
    ocr_url = 'http://apis.baidu.com/apistore/idlocr/ocr'
    post_data = {
            'fromdevice' : "pc",
            'clientip' : "10.10.10.0",
            'detecttype' : "LocateRecognize",
            'languagetype' : "CHN_ENG",
            'imagetype' : "1",
            'image' : img_data,
    }
    
    post_data = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(ocr_url, data = post_data)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("apikey", "04d3977f3751c9ba2e7fb2663059cb94")
    
    resp = urllib.request.urlopen(req)
    content = resp.read()
    if content:
        print(content)
        content = eval(content.decode('utf-8'))
        if content["errNum"] == "0":
            try:
                words = content["retData"][0]["word"]
                print(words)
            except:
                return None
        else:
            return None
    return words

def get_words():
    img_data = get_image_data()
    return get_words_from_img(img_data)

# get_words()
