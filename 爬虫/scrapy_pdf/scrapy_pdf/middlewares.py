# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from logging import getLogger
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
from .settings import USER_AGENT_LIST



#定义一个中间件类
class RandomUserAgent(object):
    def prcess_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        request.header['User-Agent'] = ua

class ScrapyPdfSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyPdfDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumDownloaderMiddleware():
    def __init__(self, timeout=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')   #无界面浏览器
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT') #在配置文件中拿到SELENIUM_TIMEOUT 需要自己定义
        )

    def process_request(self, request, spider):
        self.logger.debug('------------Chrome is starting-------------' + request.url)
        try:
            self.browser.get(request.url)
            #需要爬两次 第一次在滚动新闻页面 爬取所有新闻的url；第二次在爬取新闻的详细信息
            # if 'https://finance.sina.com.cn/roll' in request.url:  #如果是滚动新闻页面
            #     news_list = ''   #存储所有新闻的url
            #     page = 0
            #     while page < 1:  #只爬两页
            #         try:
            #             page = page + 1
            #             '''
            #             <div class="d_list_txt" id="d_list" style="width:100%;">
            #             <ul>
            #             <li onmouseover="this.className='hover'" onmouseout="this.className=''" class="">
            #             <span class="c_chl">[全部]</span><span class="c_tit">
            #             <a href="https://finance.sina.com.cn/money/bank/gsdt/2019-07-24/doc-ihytcerm5959531.shtml" target="_blank">招商银行：上半年实现净利润506.12亿 同比增13.08%</a></span><span class="c_time" s="1563959946">07-24 17:19</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/w/2019-07-24/doc-ihytcerm5973095.shtml" target="_blank">为寻失踪36年少女 梵蒂冈掘公主墓发现数千根人骨</a></span><span class="c_time" s="1563959920">07-24 17:18</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexanaly/2019-07-24/doc-ihytcitm4320345.shtml" target="_blank">李鼎缘:黄金原油怎么操作 日内走势分析及操作建议</a></span><span class="c_time" s="1563959917">07-24 17:18</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/s/2019-07-24/doc-ihytcerm5961028.shtml" target="_blank">5000元欠了六年才还上 背后的故事却这么温暖</a></span><span class="c_time" s="1563959862">07-24 17:17</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/future/roll/2019-07-24/doc-ihytcitm4320124.shtml" target="_blank">沪镍下滑震荡 需求疲弱打压</a></span><span class="c_time" s="1563959860">07-24 17:17</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/relnews/us/2019-07-24/doc-ihytcerm5959813.shtml" target="_blank">美股科技股盘前走低 美司法部启动大范围反垄断调查</a></span><span class="c_time" s="1563959797">07-24 17:16</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/relnews/hk/2019-07-24/doc-ihytcerm5965807.shtml" target="_blank">中信建投证券完成兑付30亿元本年度第一期短期融资券</a></span><span class="c_time" s="1563959760">07-24 17:16</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexanaly/2019-07-24/doc-ihytcitm4319691.shtml" target="_blank">陈一铭:美元三连阳非美承压 黄金多空拉锯如过山车</a></span><span class="c_time" s="1563959755">07-24 17:15</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/c/2019-07-24/doc-ihytcitm4327565.shtml" target="_blank">交通部：新申请的跨省客运班线不得超过800公里</a></span><span class="c_time" s="1563959640">07-24 17:14</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://tech.sina.com.cn/i/2019-07-24/doc-ihytcitm4326190.shtml" target="_blank">澎湃新闻：孙宇晨是黑是白，谁来说清楚？</a></span><span class="c_time" s="1563959640">07-24 17:14</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5958736.shtml" target="_blank">子公司对外追讨逾4亿货款 *ST尤夫五跌停后收获3连板</a></span><span class="c_time" s="1563959640">07-24 17:14</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/o/2019-07-24/doc-ihytcitm4319399.shtml" target="_blank">澎湃：孙宇晨是黑是白 谁来说清楚？</a></span><span class="c_time" s="1563959640">07-24 17:14</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/jhzx/2019-07-24/doc-ihytcerm5958217.shtml" target="_blank">深交所投教：详解股东的基本权利</a></span><span class="c_time" s="1563959640">07-24 17:14</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''" class=""><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5963095.shtml" target="_blank">欧元区、德法7月制造业PMI惨淡 市场押注欧央行降息</a></span><span class="c_time" s="1563959630">07-24 17:13</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexanaly/2019-07-24/doc-ihytcerm5958168.shtml" target="_blank">方威铭:降息前夕黄金上蹿下跳 唯白银独秀</a></span><span class="c_time" s="1563959629">07-24 17:13</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5962740.shtml" target="_blank">7月土地市场降温：热点一二线城市溢价率走低</a></span><span class="c_time" s="1563959597">07-24 17:13</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a class="videoNewsLeft" href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcitm4320009.shtml" target="_blank">共享汽车途歌董事长卸任 拖欠的押金还退得了吗？</a></span><span class="c_time" s="1563959580">07-24 17:13</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcitm4319187.shtml" target="_blank">摩拜单车又涨价！上海起步价涨至1.5元(视频)</a></span><span class="c_time" s="1563959580">07-24 17:13</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/s/2019-07-24/doc-ihytcerm5957739.shtml" target="_blank">招商银行：上半年净利润506.12亿 同比增长13.08%</a></span><span class="c_time" s="1563959540">07-24 17:12</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/future/roll/2019-07-24/doc-ihytcerm5957518.shtml" target="_blank">AP910期价下探回升 短期或延续弱势</a></span><span class="c_time" s="1563959498">07-24 17:11</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexanaly/2019-07-24/doc-ihytcerm5957450.shtml" target="_blank">周品源:黄金最新走势分析 今日最新黄金操作建议</a></span><span class="c_time" s="1563959487">07-24 17:11</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/c/2019-07-24/doc-ihytcitm4318741.shtml" target="_blank">公安部督办特大制毒案告破 23人落网</a></span><span class="c_time" s="1563959480">07-24 17:11</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5962314.shtml" target="_blank">刚兑打破后债市违约不再稀奇 市场风险正被重新定价</a></span><span class="c_time" s="1563959468">07-24 17:11</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexanaly/2019-07-24/doc-ihytcerm5956829.shtml" target="_blank">戴鑫伟:早间黄金原油走势分析 实时操作策略</a></span><span class="c_time" s="1563959380">07-24 17:09</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/bond/research/2019-07-24/doc-ihytcerm5956719.shtml" target="_blank">社科院学部委员王国刚：逐步实现利率市场化改革</a></span><span class="c_time" s="1563959355">07-24 17:09</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5975917.shtml" target="_blank">广州酒家收购陶陶居 能否“盘活”老字号？</a></span><span class="c_time" s="1563959329">07-24 17:08</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/future/roll/2019-07-24/doc-ihytcitm4317600.shtml" target="_blank">外盘提振 期价大幅反弹</a></span><span class="c_time" s="1563959326">07-24 17:08</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/c/2019-07-24/doc-ihytcerm5956286.shtml" target="_blank">海外网：岂止是香烟 这才是民进党最大的私货</a></span><span class="c_time" s="1563959251">07-24 17:07</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/china/2019-07-24/doc-ihytcitm4317284.shtml" target="_blank">美企对特定儿童安全型可开闭密封条提起337调查申请</a></span><span class="c_time" s="1563959241">07-24 17:07</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexfxyc/2019-07-24/doc-ihytcerm5956226.shtml" target="_blank">邦达亚洲:欧洲央行有望率先降息 欧元刷新8周低位</a></span><span class="c_time" s="1563959238">07-24 17:07</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5957520.shtml" target="_blank">华为回应美国子公司裁员：这是个困难决定 涉600余人</a></span><span class="c_time" s="1563959159">07-24 17:05</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/world/gjcj/2019-07-24/doc-ihytcerm5955654.shtml" target="_blank">欧元区制造业健康程度明显恶化 经济前景黯淡</a></span><span class="c_time" s="1563959103">07-24 17:05</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/c/2019-07-24/doc-ihytcerm5956204.shtml" target="_blank">今年征兵工作下月开始：将多征集大学生毕业生</a></span><span class="c_time" s="1563959100">07-24 17:05</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcerm5958094.shtml" target="_blank">papi酱公司被诉侵权 律师：原告证明为权利人成关键</a></span><span class="c_time" s="1563959100">07-24 17:05</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/hkstock/ggscyd/2019-07-24/doc-ihytcerm5955599.shtml" target="_blank">卡宾：8月5日举行董事会会议 批准中期业绩</a></span><span class="c_time" s="1563959087">07-24 17:04</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/chanjing/gsnews/2019-07-24/doc-ihytcitm4317048.shtml" target="_blank">或参与负债累累的托马斯库克重组谈判 复星图啥？</a></span><span class="c_time" s="1563959078">07-24 17:04</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/relnews/cn/2019-07-24/doc-ihytcerm5959394.shtml" target="_blank">江南化工全资控股中金立华 能否缓解盾安危机成疑</a></span><span class="c_time" s="1563959065">07-24 17:04</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/s/2019-07-24/doc-ihytcerm5955502.shtml" target="_blank">淮南市委通报巡视情况：支持淮南矿业集团整体上市</a></span><span class="c_time" s="1563959054">07-24 17:04</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/fund/jjsy/2019-07-24/doc-ihytcitm4316467.shtml" target="_blank">明星挂名受监管 几类基金要小心</a></span><span class="c_time" s="1563959052">07-24 17:04</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcitm4316339.shtml" target="_blank">广西准入准营退出 实现企业开办1个工作日内办结目标</a></span><span class="c_time" s="1563958980">07-24 17:03</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/hkstock/marketalerts/2019-07-24/doc-ihytcerm5954921.shtml" target="_blank">盘后部署：投资者以观望态度为主 港股28800点料受阻</a></span><span class="c_time" s="1563958921">07-24 17:02</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://tech.sina.com.cn/it/2019-07-24/doc-ihytcitm4315862.shtml" target="_blank">TCL回应拟并购日本JDI传闻：暂无一致性意向和协议</a></span><span class="c_time" s="1563958917">07-24 17:01</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/chanjing/gsnews/2019-07-24/doc-ihytcerm5955297.shtml" target="_blank">福布斯中国慈善榜:许家印居首 近半数来自房地产业</a></span><span class="c_time" s="1563958886">07-24 17:01</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexfxyc/2019-07-24/doc-ihytcitm4315669.shtml" target="_blank">牛汇:美联储再受抨击金价又该如何</a></span><span class="c_time" s="1563958886">07-24 17:01</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://news.sina.com.cn/o/2019-07-24/doc-ihytcitm4316476.shtml" target="_blank">将毒品渗入纤维逃避检测 澳门破2019最大宗毒品案</a></span><span class="c_time" s="1563958865">07-24 17:01</span></li></ul><ul><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcitm4316232.shtml" target="_blank">TCL回应拟并购日本JDI传闻：暂无一致性意向和协议</a></span><span class="c_time" s="1563958862">07-24 17:01</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/s/2019-07-24/doc-ihytcitm4317606.shtml" target="_blank">汇通能源一季度盈转亏 控股股东仍溢价收购谋控制权</a></span><span class="c_time" s="1563958860">07-24 17:01</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/stock/hkstock/marketalerts/2019-07-24/doc-ihytcerm5955900.shtml" target="_blank">汇丰控股将于9月26日派发第二次股息</a></span><span class="c_time" s="1563958785">07-24 16:59</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/money/forex/forexfxyc/2019-07-24/doc-ihytcerm5953996.shtml" target="_blank">牛汇:API多空交织 EIA枕戈待旦</a></span><span class="c_time" s="1563958746">07-24 16:59</span></li><li onmouseover="this.className='hover'" onmouseout="this.className=''"><span class="c_chl">[全部]</span><span class="c_tit"><a href="https://finance.sina.com.cn/roll/2019-07-24/doc-ihytcitm4315229.shtml" target="_blank">TCL回应并购日本JDI:进行交流 暂无一致性意向和协议</a></span><span class="c_time" s="1563958740">07-24 16:59</span></li></ul><div class="pagebox"> <span class="pagebox_pre"><a href="javascript:void(0)" onclick="newsList.page.pre();return false;">上一页</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(1);return false;">1</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(2);return false;">2</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(3);return false;">3</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(4);return false;">4</a></span> <span class="pagebox_num_nonce">5</span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(6);return false;">6</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(7);return false;">7</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(8);return false;">8</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(9);return false;">9</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(10);return false;">10</a></span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(11);return false;">11</a></span> <span class="pagebox_num_ellipsis">..</span> <span class="pagebox_num"><a href="javascript:void(0)" onclick="newsList.page.goTo(16277);return false;">16277</a></span> <span class="pagebox_pre"><a href="javascript:void(0)" onclick="newsList.page.next();return false;">下一页</a></span></div></div>
            #             '''
            #
            #             self.wait.until(EC.presence_of_element_located(
            #                 (By.XPATH, '//div[@class="d_list_txt"]/ul/li/span/a')))
            #             elements = self.browser.find_elements_by_xpath('//div[@class="d_list_txt"]/ul/li/span/a')
            #             for i in elements:
            #                 news_list = news_list + ',' + i.get_attribute('href')#用,拼接
            #             # <a href="javascript:void(0)" onclick="newsList.page.next();return false;">下一页</a>
            #             #找到并点击下一页
            #             next = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@onclick="newsList.page.next();return false;"]')))
            #             next.click()
            #             self.wait.until(EC.presence_of_element_located(
            #                 (By.XPATH, '//div[@class="d_list_txt"]/ul/li/span/a')))
            #             print('------------Chrome is starting-------------' + self.browser.current_url)
            #         except TimeoutException:
            #             break
            #             # return HtmlResponse(url=request.url, body=news_list, request=request, encoding='utf8', status=200)
            #     return HtmlResponse(url=request.url, body=news_list, request=request, encoding='utf8', status=200) #返回所有新闻url
            # #如果不是滚动新闻页面 具体新闻页面  则返回页面源码
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)