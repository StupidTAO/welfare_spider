# coding:utf-8
import url_manager, html_downloader, html_parser, html_outputer
import logging

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def crawl(self, root_url):
        count = 1 # record the current number url
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('crawl No.%d: %s'%(count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count == 10:
                    break
                count += 1
            except:
                logging.warning('crawl failed')
        self.outputer.output_html()
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
    root_url = "https://baike.baidu.com/item/Python/407313"
    #root_url2 = "http://www.hhax.org/api/trade/trade/es/front/listByFront?pageNo=1&pageSize=20&payState=1&startDate=2020-6-27%2000:00:00&endDate=2020-7-4%2017:34:59"
    #root_url2 = "http://www.hhax.org/api/trade/trade/es/front/listByFront?pageNo=4&pageSize=200&payState=1&startDate=2013-7-1%2000:00:00&endDate=2014-7-1%2000:00:00"
    root_url2 = "http://www.hhax.org/api/trade/trade/es/front/listByFront?pageNo=1&pageSize=40000&payState=1&startDate=2019-07-01%2000:00:00&endDate=2020-07-01%2000:00:00"
    obj_spider = SpiderMain()
    obj_spider.crawl_walfare(root_url2)
