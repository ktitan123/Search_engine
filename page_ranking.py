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
    graph={}
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
           content=get_content(url)
           addpage_to_index(index,url,content)
           outlinks=get_all_links(content)
           graph[url]=outlinks
           union(tocrawl,outlinks)
           crawled.append(url)


    return graph
           
           


   

def get_content(url):
    import urllib
    myurl=urllib.urlopen(url)
    page=myurl.read()
    start=page.find('<body>')
    end=page.find('</body>')
    page=page[start+1:end]
    return page

def addpage_to_index(index,url,content):
    word=content.split()
    for key in word:
        if key in index:
            index[key].append(url)
        else:
            index[key]=[url]
    return None


def compute_rank(graph):
    d=0.8
    numloops=10
    ranks={}
    npages=len(graph)
    for page in graph:
        ranks[page]=1.0/npages
    for i in range(0,numloops):
        newranks={}
        for page in graph:
            newranks={}
            for page in graph:
                newrank=(1-d)/npages
                for node in graph:
                    if page in graph[node]:
                        newrank=newrank+d*(ranks[node]/len(graph[node]))
                        newranks[page]=newrank
    ranks=newranks
    return ranks
