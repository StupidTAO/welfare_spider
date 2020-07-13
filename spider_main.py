# coding:utf-8
import url_manager, html_downloader, html_parser, html_outputer
import logging
import datetime

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

    def crawl_walfare_one_foundation(self, root_url):
        end = "2020-07-12"
        begin = "2011-07-30"
        url = root_url.format(begin, begin)
        begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d')
        delta=datetime.timedelta(days=1)

        self.urls.add_new_url(url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("crawl No1")
                if str(begin_date.strftime('%Y-%m-%d')) != end:
                    begin_date += delta
                    begin = str(begin_date.strftime('%Y-%m-%d'))
                    url = root_url.format(begin, begin)
                    self.urls.add_new_url(url)
                    print(str(begin_date.strftime('%Y-%m-%d')))
                html_cont = self.downloader.download(new_url)
                list_person = self.parser.parse_one_foundation(html_cont)
                if list_person == None or len(list_person) == 0 :
                    continue
                self.outputer.collect_walfare_data(list_person)
                print(list_person[0])
                print("new_url is ", new_url)
                print("down")
            except Exception as e:
                logging.warning("crawl walfare failed, err = ", e)

            self.outputer.ouput_walfare_one_fundation_mysql()

if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/Python/407313"
    root_url1 = "http://www.onefoundation.cn/xp_api.php?action=searchReqV1&checkCode=&size=1000&startTime={}&endTime={}"
    root_url2 = "http://www.hhax.org/api/trade/trade/es/front/listByFront?pageNo=1&pageSize=40000&payState=1&startDate=2019-07-01%2000:00:00&endDate=2020-07-01%2000:00:00"
    obj_spider = SpiderMain()
    obj_spider.crawl_walfare_one_foundation(root_url1)
