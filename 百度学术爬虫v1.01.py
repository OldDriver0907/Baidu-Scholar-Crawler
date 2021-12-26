'''
Statement:
Author: OldDriver0907
Email: lifan.xu17@student.xjtlu.edu.cn
Prohibit Commercial Use
'''

import os
import re
import time
import requests
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def get_sub_url(html):
    return re.findall(r'"(https://xueshu.baidu.com/usercenter/paper/show.*?)"', html)


def save_url(file_name):
    file = open(file_name, 'r', encoding = 'utf-8')
    c = file.readlines()
    for line in c:
        title = line.replace(' ', '+')
        try:
            os.makedirs(os.getcwd() + '/文献网址')
        except:
            0
        f = open(os.getcwd() + '/文献网址/' + title + '.txt', 'a', encoding='utf-8')
        for a in range(0,400,10):
            # url=line+str(a)+'&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_hit=1&sc_as_para=sc_lib%3A'
            url = 'https://xueshu.baidu.com/s?wd=' + title + '&pn=' + str(a) + '&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_hit=1&sc_as_para=sc_lib%3A'
            html = get_one_page(url)
            for item in get_sub_url(html):
                print(item)
                f.write(item + '\n')
            time.sleep(0.2)
        f.close()



def get_paper_information():
    folder_path = os.getcwd() + '/文献网址/'
    file_list = os.listdir(folder_path)
    try:
        os.makedirs(os.getcwd() + '/文献详细内容')
    except:
        0
    for file_element in file_list:
        url_list = []
        file_path = folder_path + file_element
        f = open(file_path, 'r', encoding='utf-8')
        line = f.read()
        # url_list.append(line)
        url_list.append(line.split('\n'))
        # paper_information = []
        # print(file_element)
        # print(os.getcwd() + '/文献详细内容/' + str(file_element))
        f = open(os.getcwd() + '/文献详细内容/' + str(file_element).replace('%', '_'), 'a', encoding='utf-8')
        for topic in url_list:
            for url in topic:
                # print(url)
                html = get_one_page(url)
                try:
                    title = re.findall(r'<title>(.*?) - 百度学术</title>', html)[0]
                except:
                    title = "Title not find"
                print(title)
                try:
                    abstract = re.findall(r'<p class="abstract.*data-sign="">(.*?)</p>', html)[0]
                # print(abstract)
                except:
                    abstract = "Abstract not find"
                # print(abstract)
                # keywords = re.findall(r'<p class="kw.*?main(.*?)</p>', html)
                # keywords = re.findall(r'<p class="kw_main" data-click=.*class="">(.*?)</a></span>.*</p>', html.strip())
                # keywords = re.findall(r'<p class=.*>(.*)</p>', html.replace('\n', ''))
                # keywords = re.findall(r'<p class="kw_main"(.*)</p>', html.replace('\n', ''))
                try:
                    keywords = re.findall(r'=utf-8" target="_blank" class="">(.*?)</a></span>', html)
                except:
                    keywords = "Keywords not find"
                # print(keywords)
                # paper_information.append([title, abstract, keywords, url])
                time.sleep(0.3)

                f.write(title + '\t' + abstract + '\t' + str(keywords) + '\t' + url + '\n')
        f.close()



if __name__ == '__main__':
    # 可以修改括号中的文件名，网址需要按照范例格式书写
    save_url('要搜索的关键词.txt')
    get_paper_information()
