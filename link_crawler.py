#coding=utf-8
import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue



def download(url, headers, proxy, num_retries, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error(lin24):', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                html = download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1,
                 headers=None, user_agent='GoodCrawler', proxy=None, num_retries=1,scrape_callback=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    # 对于可能会出现重复进出队列的地址，由下面的seen控制
    crawl_queue = Queue.deque([seed_url])

    # the URL's that have been seen and at what depth
    # 功能1 ：value表示这个link的深度，第几次跳转后获取的这个链接
    # 功能2 ：in seen 表示已经下载过，不会放入下载deque
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    #地图属性对象
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        #判断下载深度是否到了
        depth = seen[url]

        #检查地图属性中限制条件
        #Returns True if the useragent is allowed to fetch the url according to
        # the rules contained in the parsed robots.txt file.
        #if rp.can_fetch(user_agent, url):
        if 1:
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])

            if depth != max_depth:
                #还可以下载
                if link_regex:
                    #寻找符合正则的URL地址放入links
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    #检查这个地址是不是下载过,如果没下载过且域名一致则加入待下载队列
                    if link not in seen:
                        seen[link] = depth + 1
                        #检查地址是否在同一个网域里面
                        if same_domain(seed_url, link):
                            #添加到下载队列里面
                            crawl_queue.append(link)

            #检查下载任务是否达到最大下载数量
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt(line 93):',url

def same_domain(url1, url2):
    '''
    .netloc e.g  ‘bitbucket.org’
    :param url1:
    :param url2:
    :return:
    '''
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def normalize(seed_url, link):
    '''
    把seed_url,和从里面抓取的link,拼成一个整体的link
    :param seed_url:
    :param link:
    :return:
    '''
    #urldefrag
    #fragment  拆分文档中的特殊锚  '#'后面的部分
    #返回元组(newurl, fragment), 其中newurl是片段的url部分, fragment是包含片段部分的字符串(如果有)
    # return tuple(defragmented, fragment)
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)

def get_links(html):
    '''
    从html里面获取links,返回 list
    :param html:
    :return:
    '''
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        self.delay = delay
        #上一次访问这个域名的时间戳
        self.domains = {}

    def wait(self,url):
        # 获取域名比如 ‘bitbucket.org’
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()




def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

if __name__ == '__main__':
    #link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com/', '/(index|view)',delay=0,
                 num_retries=1, max_depth=1, user_agent='GoodCrawler')

