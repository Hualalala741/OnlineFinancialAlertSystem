import scrapy

from ..items import ScrapyPdfItem
from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class CninfoSpider(scrapy.Spider):
    name = 'cninfo'
    allowed_domains = ['www.cninfo.com.cn']
    start_urls = ['http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice#szse']
    cookies ={"JSESSIONID" : 'FEDEDCA7D37C3092D161474469E3DE7C',
    '_sp_ses.2141' :'*',
    'SID' : '01a9a503-e0b0-4122-bf9d-7db76f6ab6be',
    'routeId' :'.uc2',
    'cninfo_user_browse' : '300317,9900022019,%E7%8F%88%E4%BC%9F%E6%96%B0%E8%83%BD',
    'insert_cookie' : '37836164',
    '_sp_id.2141' : 'd88426a0-c75c-4be4-a874-328278366e62.1672833630.14.1677835947.1677159992.3375f347-d7ff-418f-9221-508c7a4262a0'}
    # rules = [
    #     Rule(LinkExtractor(allow=("/disclosure/detail/.*\.html$"), callback='parse'))
    #          ]

    def parse(self, response):
        headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Host': 'www.cninfo.com.cn'
        }

        cookies = {"JSESSIONID": '4C3930BBAE6A9B2D9DA16226CFF66129',
                   'routeId': '.uc2',
                   'cninfo_user_browse': '300317,9900022019,%E7%8F%88%E4%BC%9F%E6%96%B0%E8%83%BD',
                   'insert_cookie': '37836164',
                   '_sp_ses.2141' : '*',
                   'SID' : 'aa70c94e-dbf5-4114-be6f-2e1394bc2415',
                   '_sp_id.2141': 'd88426a0-c75c-4be4-a874-328278366e62.1672833630.16.1677847532.1677845327.957c1592-3ba4-4b98-a1e5-65aeef0020e7'}
        news_href_list = response.xpath('//div[@id="main"]//table//td[4]/div/a/@href')
        for href in news_href_list:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url,headers=headers,cookies=cookies,callback=self.parse_news, dont_filter=True)

    def parse_news(self, response):
        Item = ScrapyPdfItem()
        title = response.xpath('//*[@id="noticeDetail"]/div/div[1]/div[2]/div[2]/text()').get()
        Item['file_name'] = title
        link = response.xpath('//*[@id="noticeDetail"]/div/div[2]/div[1]/a/@href').get()
        # if link == '':
        #     print(title + "++++++++++++++++++++++++++++++++++++"+response.url)
        # else:
        #     print(title + "---------------------------"+response.url)
        # link = response.css("div.abc a::attr(href)").extract()[0] #noticeDetail > div > div.nt-bd > div.fullscreen > a
        Item['file_url'] = link
        yield Item

