def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links



def crawl_web(url):
    tocrawl = [url]
    crawled = []
    index={}
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
           content=get_content(url)
           page_to_index(index,url,content)
           union(tocrawl,get_all_links(content))
           crawled.append(url)


    return index



def get_content(url):
    import urllib
    myurl=urllib.urlopen(url)
    page=myurl.read()
    start=page.find('<body>')
    end=page.find('</body>')
    page=page[start+1:end]
    return page

def add_to_index(index,keyword,url):
    flag=0
    for e in index:
        if e[0] == keyword:
            flag=1
            e[1].append(url)
    if flag==0:
        index.append([keyword,[url]])

def lookup(index,keyword):
     flag=0
     for e in index:
         if e[0]==keyword:
             flag=1
             return e[1]
     if flag==0:
         return []
         
        

def page_to_index(index,url,content):
     word=content.split()
     for key in word:
        if key in index:
            index[key].append(url)
        else:
            index[key]=[url]
     return None



        

        





    
    

    
        
    









    
