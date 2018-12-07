# encoding=utf-8

import os
import ast
import requests
import json
import time

import sys  
  


def build_dic(dic):
    new_dic = {}
    #Dictionary: key - id, value - url, date, title
    for now_dic in dic:
        key = now_dic['id']
        new_dic[key] = {}
        new_dic[key]['url'] = now_dic['url']
        new_dic[key]['date'] = now_dic['date']
        new_dic[key]['title'] = now_dic['title']
    return new_dic    

def update_news_list(now_news_dic):
    #Initialize the news_list and jobs_list
    if not(os.path.isfile('news_list.json')):
        print ("Building news list & jobs list")
        jsonFile = open("news_list.json", "w")
        jsonFile.write(json.dumps(now_news_dic))
        jsonFile.close()
        
        f = open('jobs_list.txt','a')
        for key in now_news_dic:
            f.write(key+'\n')
        f.close()
        return

    else:
        news_list = json.loads(open('news_list.json').read())
    update_list = set(now_news_dic.keys())-set(news_list.keys()) 
    
    #Update latest news to news_list
    for key in update_list:
        news_list[key] = {}
        news_list[key]['url'] = now_news_dic[key]['url']
        news_list[key]['date'] = now_news_dic[key]['date']
        news_list[key]['title'] = now_news_dic[key]['title']
        
    news_list_json = json.dumps(news_list)
    f = open('news_list.json','w')
    f.write(news_list_json)
    f.close()
    
    #Update job list
    f = open('jobs_list.txt','a')
    print ("Update "+str(len(update_list))+ " news")
    for key in update_list:
        f.write(key+'\n')
    f.close()
    
def list_crawler():

    now_time = int(time.time()*1000)
    now_news_list = requests.get('http://news.people.com.cn/210801/211150/index.js?_='+str(now_time))
    now_news_dic = json.loads(now_news_list.text)['items']
    #Build own dictionary format
    now_news_dic = build_dic(now_news_dic)
    #Update news_list and jobs_list
    update_news_list(now_news_dic)

def main():
    while 1:
        try:
            print ("Starting Crawl news list")
            list_crawler()
            #sleep 20 miniutes
            print ("Sleep")
            time.sleep(1200)
        except:
            print("Crawl news list error!")
            time.sleep(300)
if __name__ == '__main__':
    main()
