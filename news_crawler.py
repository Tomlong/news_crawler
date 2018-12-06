
import os
import ast
import requests
import json
import time

def read_and_delete_job():  
    job = open('jobs_list.txt','r')
    jobs = job.readlines()
    now_job = jobs[0].rstrip('\n')
    del jobs[0]
    job = open('jobs_list.txt','w')
    job.writelines(jobs)
    job.close()
    return now_job

def news_crawler():
    
    news_list = json.loads(open('news_list.json').read())
    job_id = read_and_delete_job()
    if job_id =='':
        
        return False
    print("Crawl ",job_id)
    html = requests.get(news_list[job_id]['url']).text
    file = open('news_html/'+job_id+'.txt','w')
    file.writelines(html)
    file.close()
    return True
def main():
    
    while 1:
        if news_crawler():
            time.sleep(2)
        else:
            print ("No news could crawl.\n Wait for job list.")
            time.sleep(300)

if __name__ == '__main__':
    main()

