@[TOC](【爬虫技术】公益捐赠数据的爬取)
# welfare_spider
## 序言
因近期毕业设计需求，设计了一套基于区块链的公益捐赠系统。该系统助理公益捐赠行业，并大量分析捐赠数据为参与公益的人群进行引导与激励。因此公益的原始数据变得更为重要，本篇文章将讲解如何从现有的公益组织获取公益数据。


## 元数据来源
我们对红十字会、壹基金、韩红慈善公益基金会等多个知名的公益组织进行调研，目前只有韩红慈善公益基金会提供了信息公开公益数据记录。因此本次的爬虫将从韩红慈善公益基金会获取原始数据记录。读者可以自行前往并查看，[韩红慈善公益基金会捐赠查询](http://www.hhax.org/g.html?id=c97033d8-0d74-4762-8f5f-7ade64754536&URLparamName=%E6%8D%90%E8%B5%A0%E6%9F%A5%E8%AF%A2)。

## 爬虫架构图
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200709104347764.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpdHRsZV9zdHVwaWRfY2hpbGQ=,size_16,color_FFFFFF,t_70#pic_center)
本爬虫模块架构主要分为，url队列管理模块、数据下载模块、数据解析模块、数据存储（输出）模块，以及数据引擎模块。
数据引擎模块：负责原始数据、格式化数据等各种数据的流程控制。
url队列管理模块：主要负责管理一个url的队列，可以push推入和pop弹出一个url以供存储和使用。
数据下载模块：按照获取的url，下载url中的数据，该部分数据需要解析，可能是一个html的页面，也可能是json格式的数据，
数据解析模块：将下载下来的数据，提供给本模块，可以使用beautiful soup等工具包对raw data原始数据进行解析，并获得需要的格式化数据。
数据存储模块：将格式化后的数据，以格式再处理的方式，输出到数据库、csv表格或是html页面中。
## 关键代码分析
```
import url_manager, html_downloader, html_parser, html_outputer
import logging

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

   def crawl_walfare(self, root_url):
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("crawl No1")
                html_cont = self.downloader.download(new_url)
                list_person = self.parser.parse_welfare(html_cont)
                self.outputer.collect_walfare_data(list_person)
                print(list_person[0])
            except Exception as e:
                logging.warning("crawl walfare failed, err = ", e)
            self.outputer.ouput_walfare_mysql()

if __name__ == "__main__":
    root_url = "http://www.hhax.org/api/trade/trade/es/front/listByFront?pageNo=1&pageSize=20&payState=1&startDate=2020-6-27%2000:00:00&endDate=2020-7-4%2017:34:59"
    obj_spider = SpiderMain()
    obj_spider.crawl_walfare(root_url)
```
这是代码的主要逻辑流程，首先在main函数中定义爬虫对象，声明要爬取数据的URL，然后调用crawl_walfare函数进行爬取数据。在crawl_walfare函数中先将URL地址添加到URL队列管理中，然后在一个循环中读取队列中的URL。在爬取过程中如果产生需要爬取的衍生URL，则将衍生的URL添加到。从队列中获取到URL后，将URL地址交给download模块，去下载整个URL页面。获取到的页面内容交给parse模块进行解析，本次数据爬取获得的是json数据，并且包含分页内容。解析后将会获得一个捐赠记录的list数组，数组在output输出模块临时存储，最后写入mysql数据库中。
## 参考文章及源码下载
[分布式爬虫](https://chai2010.cn/advanced-go-programming-book/ch6-cloud/ch6-07-crawler.html)
[Golang实现简单爬虫框架（1）](https://juejin.im/post/5ce3f3b66fb9a07ef3763daf)
[Golang实现简单爬虫框架（2）](https://juejin.im/post/5ce3f5c4f265da1bd4245524)
[Golang实现简单爬虫框架（3）](https://juejin.im/post/5ce4ba2fe51d45775c73dc45)
[Golang实现简单爬虫框架（4）](https://juejin.im/post/5ceb5dff51882530e4653637)

[源代码](https://github.com/StupidTAO/welfare_spider)
https://github.com/StupidTAO/welfare_spider
