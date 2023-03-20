import scrapy
from ..items import Scrapy1Item


class XinlangSpider(scrapy.Spider):
    #爬虫名字 用运行
    name = 'xinlang'
    #允许访问的域名
    allowed_domains = ['finance.sina.com.cn']

    # 起始的url地址 指的是第一次要访问的域名
    # start_urls 实在allowed domains的前面加一个
    start_urls = ['http://finance.sina.com.cn/roll']
# 返回网页
    def parse(self, response):
        news_href_list = response.xpath('//div[@class="d_list_txt"]/ul/li/span[@class="c_tit"]/a/@href')
        # print response.url
        for href in news_href_list:

            url = response.urljoin(href.extract())
            #print('-----------' + str(url))
            yield scrapy.Request(url=url, callback=self.parse_news,dont_filter=True)


        # news_list = response.text.split(',')
        # print('---------------------' + str(len(news_list)))
        # for news_url in news_list:
        #     print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        #     if news_url:  # 第一个是空串 不考虑
        #         print(news_url)
        #         yield scrapy.Request(url=news_url, callback=self.parse_news)

    def parse_news(self, response):
        item = Scrapy1Item()
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