import os
import re
import sys
import requests
import json
import shutil
from bs4 import BeautifulSoup



def remove_trash(text):
    text = text.replace('&nbsp;','')
    text = text.replace('\u3000','')
    text = text.replace('\t','')
    text = text.replace('\n','')
    return text
def extract_text(soup):
    
    if len(soup.find_all(class_="box01"))!=0:
       
        if soup.find_all(class_="box_con"):
            text=''
            for text0 in soup.find_all(class_="box_con")[0].stripped_strings:
                text=text+text0
        
        elif len(soup.find(class_='gray box_text')) != 0:
            text = soup.find(class_='gray box_text').text
                 
    else:
        text=''
        for text_string in soup.find_all(style="text-indent: 2em"):
            for text0 in text_string.stripped_strings:
                text+=text0  
                
    return remove_trash(text)

def extract_title(soup):
    return soup.title.string.split('--')[0]

def extract_label(soup):
    return soup.title.string.split('--')[1]

def extract_description(soup):
    return remove_trash(soup.find("meta",{"name":"description"})['content'])

def extract_date(soup):
    return soup.find("meta",{"name":"publishdate"})['content']

def extract_keywords(soup):
    return soup.find("meta",{"name":"keywords"})['content']

def extract_id(soup):
    return soup.find("meta",{"name":"contentid"})['content']
    
def extract_relative(soup):
    relative_list = []
    try:
        if soup.find(class_ = "clearfix box_read").find('h2') != None:
            relative = soup.find(class_ = "clearfix box_read").find('h2').text
        
        
            if relative == '推荐阅读':
                for now_relative in soup.find(class_ = "clearfix box_read").find_all(class_='hdNews clearfix'):
                    now_dic = {}
                    now_dic['title'] = now_relative.find('strong').string
                    if now_relative.find('strong').next_sibling == '\u3000\u3000':
                        now_dic['description'] = remove_trash(now_relative.find('strong').next_sibling.next_sibling.text)
                    else:      
                        now_dic['description'] = remove_trash(now_relative.find('strong').next_sibling)
                    now_dic['label'] = extract_label(soup)
                    html_pattern = re.compile(r'[\d]{8}\.html')
                    now_dic['id'] = html_pattern.search(now_relative.find('a')["href"]).group()[:8]
                    relative_list.append(now_dic)
                return relative_list
            
            elif  relative == '深度阅读':
                for now_relative in soup.find(class_ = "clearfix box_read").find_all(class_='hdNews clearfix'):
                    now_dic = {}
                    now_dic['title'] = now_relative.find('strong').string
                    if now_relative.find('strong').next_sibling == '\u3000\u3000':
                        now_dic['description'] = remove_trash(now_relative.find('strong').next_sibling.next_sibling.text)
                    else:
                        now_dic['description'] = remove_trash(now_relative.find('strong').next_sibling)
                    now_dic['label'] = extract_label(soup)
                    html_pattern = re.compile(r'[\d]{8}\.html')
                    now_dic['id'] = html_pattern.search(now_relative.find('a')["href"]).group()[:8]
                    relative_list.append(now_dic)
                return relative_list
            
        elif soup.find(class_ = "clearfix box_read").find('span') != None:
            for (now_relative,now_id) in zip(soup.find(class_ = "clearfix box_read").find(class_='hdNews clearfix').find_all('strong'),
                                        soup.find(class_ = "clearfix box_read").find(class_='hdNews clearfix').find_all('a')):
                now_dic = {}
                now_dic['title'] = now_relative.text
                if now_relative.next_sibling == '\u3000\u3000':
                    now_dic['description'] = remove_trash(now_relative.next_sibling.next_sibling.text)
                else:      
                    now_dic['description'] = remove_trash(now_relative.next_sibling)
                now_dic['label'] = extract_label(soup)
                html_pattern = re.compile(r'[\d]{8}\.html')       
                now_dic['id'] = html_pattern.search(now_id["href"]).group()[:8]
                relative_list.append(now_dic)
            return relative_list
        else:
            return relative_list
    except:
        relative = []
        return relative_list



def parser(filename):
    if not os.path.isfile(filename):
        final_json = {}
        final_json['items'] = []
    else: 
        final_json = json.loads(open(filename,'r').read())
        
    if not os.path.isdir('parsed_html/'):
        os.mkdir('parsed_html/')
        
    if not os.path.isdir('parsed_error_html/'):
        os.mkdir('parsed_error_html/')

    for now_name in os.listdir('news_html/'):
        if now_name.endswith('.html'):
            #print (now_name)
            now_dic = {}
            file = open('news_html/'+now_name,'r')
            test = file.read()
            soup = BeautifulSoup(test,'html.parser')        
            src = 'news_html/'+now_name

            try:
                now_dic['article'] = extract_text(soup)
                now_dic['title'] = extract_title(soup)
                now_dic['label'] = extract_label(soup)
                now_dic['description'] = extract_description(soup)
                now_dic['date'] = extract_date(soup)
                now_dic['keywords'] = extract_keywords(soup)
                now_dic['id'] = extract_id(soup)
                now_dic['relative'] = extract_relative(soup)

                final_json['items'].append(now_dic)
                dst = 'parsed_html/'
                shutil.move(src,dst)
                
                #dump jsons
                print(now_name,"parsed success")
                data_json = json.dumps(final_json)
                f = open(filename,'w')
                f.write(data_json)
                f.close()
            except:
                print(now_name,"parsed error")
                dst = 'parsed_error_html/'
                shutil.move(src,dst)
                pass

def main(filename):
    parser(filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("<Usage: filename.json>")
        exit()
    else:
        filename = sys.argv[1]
        main(filename)
