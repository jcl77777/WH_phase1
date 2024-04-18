'''
Format of article.csv:
ArticleTitle,Like/DislikeCount,PublishTime
'''
import urllib.request as request
from bs4 import BeautifulSoup
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.ptt.cc/bbs/Lottery/index.html"

titles_list =[]
like_dislike_list = []
publish_time_list = []

#capture titles and likes on the page
def parse_page_metadata(url):
    headers = {
            "Cookie": "over18=1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
        }
    
    response = request.Request(url, headers=headers)

    with request.urlopen(response) as response:
        content = response.read().decode("utf-8")

    soup = BeautifulSoup(content, "html.parser")

    #capture all titles in the first page
    titles = soup.find_all("div", class_="title")
    for title in titles:
        if title.a != None:
            titles_list.append(title.a.string)
            #print(titles_list)
        else: 
            #if title does not exist = 刪文
            # not add to the list
            pass

    #capture all likes in the first page
    like_dislike_num = soup.find_all("div", class_="nrec")
        
    for like_dislike in like_dislike_num:
        if like_dislike.span != None: 
            #print(like_dislike_num)
            like_dislike_num = like_dislike.span.string
            like_dislike_list.append(like_dislike_num)
        else:
            like_dislike_num = 0
            like_dislike_list.append(like_dislike_num)
        #print(like_dislike_list)


    #capture time for each titles 
    for title in titles:        
        if title.a != None: 
            URL_next = "https://www.ptt.cc" + title.a["href"]

            headers_next = {
            "Cookie": "over18=1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            response_next = request.Request(URL_next, headers=headers_next)

            with request.urlopen(response_next) as response_next:
                content_next = response_next.read().decode("utf-8")

            soup_next = BeautifulSoup(content_next, "html.parser")

        #capture time for each titles
            publish_time_elem = soup_next.find("span", string="時間")
            if publish_time_elem != None:
                publish_time = publish_time_elem.next_sibling.string
                #print(publish_time)
                publish_time_list.append(publish_time)
            else:
                publish_time = "0"
                publish_time_list.append(publish_time)
            #print(publish_time_list)
            
    next_url = "https://www.ptt.cc" + soup.find("a", string = "‹ 上頁")["href"]
    print(next_url)   
    return next_url

count = 0 
while count < 3:
    url = parse_page_metadata(url)
    count += 1

output = []
for Article_Title, like_Dislike_Count, Publish_Time in zip(titles_list, like_dislike_list, publish_time_list):
    output.append([Article_Title, like_Dislike_Count, Publish_Time])
    #print(output)
    
header = ["ArticleTitle", "Like/DislikeCount", "PublishTime"]
with open("article.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for row in output:
        writer.writerow(row)
