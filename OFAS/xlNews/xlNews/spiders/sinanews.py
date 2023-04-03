import scrapy
from ..items import XlnewsItem


class SinanewsSpider(scrapy.Spider):
    name = 'sinanews' # 爬虫名，用于运行
    allowed_domains = ['news.sina.com.cn', 'finance.sina.com.cn', 'sports.sina.com.cn', 'ent.sina.com.cn',
                       'mil.news.sina.com.cn', 'tech.sina.com.cn'] #允许域名
    start_urls = ['https://finance.sina.com.cn/roll/'] # 起始域名

    # def parse(self, response):
    #     print('-------------------------------开始------------------------------------------')
    #     news_href_list = response.xpath('//div[@class="d_list_txt"]/ul/li/span[@class="c_tit"]/a/@href')
    #     print('爬到list咯')
    #     print(list)
    #     for href in news_href_list:
    #         url = response.urljoin(href.extract())
    #         print("爬到一个连接")
    #         yield scrapy.Request(url=url, callback=self.parse_news, dont_filter=True)
    def parse(self, response):
        news_list = response.text.split(',') #用,切分 得到url
        print('---------------------' + str(len(news_list)))
        for news_url in news_list:
            if news_url:  #第一个是空串 不考虑
                yield scrapy.Request(url=news_url,callback=self.parse_news, dont_filter=True)

    def parse_news(self, response):
        print('！！！！！！！！！！！！！！！！！！！这里是一条新闻！！！！！！！！！！！！！')
        item = XlnewsItem()
        item['link'] = response.url
        # 解析标题
        '''
        <h1 class="main-title">招商银行：上半年实现净利润506.12亿 同比增13.08%</h1>
        '''
        title = response.css('.main-title::text')
        # 可能有少部分新闻的标题不符合上述格式 单独处理
        if not title:
            title = response.css('#artibodyTitle::text')
        if title:
            title = title.extract()[0]  # title = title.extract_first()
            item['title'] = title

        # 解析日期
        '''
        <span class="date">2019年07月24日 17:19</span>
        '''
        date = response.css('.date::text')
        # 可能有少部分新闻的日期不符合上述格式 单独处理
        if not date:
            date = response.css('#pub_date::text')
        if date:
            date = date.extract()[0]
            item['date'] = date

        # 解析来源
        '''
        <span class="source ent-source">新浪财经</span>
        '''
        source = response.css('.source::text')
        # 可能有少部分新闻的来源不符合上述格式 单独处理
        if not source:
            # <a href="http://tech.sina.com.cn/" target="_blank" data-sudaclick="media_name">新浪科技</a>
            source = response.css('[data-sudaclick="media_name"]::text')
        if source:
            source = source.extract()[0]
            item['source'] = source

        # 解析正文
        article = response.xpath('//div[@class="article"]/p//text()')
        if not article:
            article = response.xpath('//div[@id="artibody"]/p//text()')
        if article:
            article_list = article.extract()  # 列表
            item['article'] = ''.join(article_list)
        yield item
