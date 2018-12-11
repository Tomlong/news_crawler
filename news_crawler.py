
import os
import ast
import requests
import json
import time

def read_and_delete_job():  
    job = open('jobs_list.txt','r')
    jobs = job.readlines()

    #No jobs to do
    if len(jobs) == 0:
        return jobs

    #Get job id and remove from list
    now_job = jobs[0].rstrip('\n')
    del jobs[0]
    job = open('jobs_list.txt','w')
    job.writelines(jobs)
    job.close()
    return now_job

def news_crawler():
    
    news_list = json.loads(open('news_list.json').read())  
    job_id = read_and_delete_job() 
    print(job_id)
    # Check whether get job
    if len(job_id) == 0:    
        return False
    
    print("Crawl ",job_id)
    html = requests.get(news_list[job_id]['url'])
    html.encoding = 'GB2312'
    
    file = open('news_html/'+job_id+'.html','w')
    file.writelines(html.text)
    file.close()
    return True
def main():
    
    if not os.path.isdir('news_html/'):
        os.mkdir('news_html/')
    
    while 1:
        try:
            if news_crawler():
                time.sleep(2)
            else:
                print ("No news could crawl.\nWait for job list.")
                time.sleep(60)
        except:
            print ("Crawl news error!")
            time.sleep(20)
if __name__ == '__main__':
    main()

