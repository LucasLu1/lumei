from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
#import time,datetime

today = datetime.now()
start_date = "2018-01-19"
city = "深圳"
birthday = "03-03"

app_id = "wx5bd444544d4e0395"
app_secret = "1093aa59f62f4375edf8eabb10d6e4cc"

user_id = ["o48d-5-RCCfOx2-8LOC2sM4X9BgU","o48d-55VgPhtIDviLsbDRYr0EPPI"]
###陆梅,"o48d-50mOxhy6NH9Tb5wKYM3wGEQ"
template_id = "_5Oy3jvTMZnhSgkPb8lTpJVXkCPXqMTovxMNFXfOrWg"
# user_ids=",".join(user_id)
# o48d-55VgPhtIDviLsbDRYr0EPPI
def firstrom():
  list1 = ['Hi,早安！',
           '嘿嘿，早上好吖~',
           '叮咚(敲门声)~✧(๑•̀ㅁ•́ฅ早',
           '哈喽！Good Morning~',
           '嘿哈，我来啦~早呀',
           '嘻嘻，早安！']
  return random.choice(list1)


def secondrom():
  list2 = [
    '陆陆',
    '陆枚',
    '凉兮小朋友',
    '陆陆小可爱',
    '小仙女🧚',
    '小懒虫',
    '小陆']
  return random.choice(list2)

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  wea = requests.get(url).json()

  date_w=wea['data']['list'][0]['date']
  city_w=wea['data']['list'][0]['city']
  weather_w=wea['data']['list'][0]['weather']
  high_w=wea['data']['list'][0]['high']
  low_w=wea['data']['list'][0]['low']
  return date_w,city_w,weather_w,high_w,low_w

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days


def get_note():
    url = "http://t.csdn.cn/LFPn2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'my-test': 'Hello'
    }
    l = []
    r = requests.get(url, headers=headers)
    y = r.text.split("<p>")

    ci = y[1]
    for i in ci:
        l.append(i)
        if i == "<":
            break
    l.remove("<")
    str1 = ""
    for j in l:
        str1 = str1 + j
    return str1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_week_day(date):
  week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期天',
  }
  day = date.weekday()
  return week_day_dict[day]

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
#星期几
xinqiji=get_week_day(datetime.now())
wm = WeChatMessage(client)
date_r,city_r,weather_r,high_r,low_r = get_weather()
print("-------------")
print(date_r)
print(city_r)
#需要字段
'''
慰问语----en_hello
日期+星期---en_date
城市----en_city
天气----已有：显示字段：weather
最高气温----en_high
最低气温----en_low
纪念----已有：显示字段love_days
生日----已有：显示字段birthday_left
备忘录----en_note

中文名言----已有：显示字段words
英文名言----en_words

'''
'''
"weather":{"value":weather_r, "color":get_random_color()},
'''
wode=get_words()
data1 = { 'doctype': 'json', 'type': 'auto','i': wode }

r = requests.get("http://fanyi.youdao.com/translate",params=data1)
result = r.json()['translateResult'][0][0]['tgt']
data = {
        "en_hello":{"value":firstrom()+","+secondrom(), "color":get_random_color()},#问候语
        "en_date":{"value":date_r+" "+xinqiji,"color":get_random_color()},#日期+星期几
        "en_city":{"value":city_r, "color":get_random_color()},#城市
        "weather":{"value":weather_r, "color":get_random_color()},#天气
        "en_high":{"value":str(int(high_r))+"℃", "color":get_random_color()},
        "en_low":{"value":str(int(low_r))+"℃", "color":get_random_color()},
        "love_days":{"value":str(get_count())+"个日日夜夜", "color":get_random_color()},#纪念
        "birthday_left":{"value":str(get_birthday())+"天", "color":get_random_color()},#生日
        "en_note":{"value":get_note(), "color":get_random_color()},
        "en_words":{"value":result, "color":get_random_color()},
        "words":{"value":wode, "color":get_random_color()}}#中文
for i in user_id:
  res = wm.send_template(i, template_id, data)

print(res)
