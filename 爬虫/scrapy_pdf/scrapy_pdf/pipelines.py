# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.files import FilesPipeline
import io
from itemadapter import ItemAdapter
from urllib.parse import urlparse
from os.path import basename, dirname, join


class ScrapyPdfPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        headers = {'Host': 'static.cninfo.com.cn',
                   'Connection': 'keep-alive',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
                   }
        cookies = {'routeId':'.uc2',
                   'cninfo_user_browse':'300317,9900022019,%E7%8F%88%E4%BC%9F%E6%96%B0%E8%83%BD',
                   'insert_cookie':'37836164; SID=aa70c94e-dbf5-4114-be6f-2e1394bc2415',
        }



        print(item['file_name']+"+++++++++++++++++++++++++++")
        yield scrapy.Request(url=item['file_url'],headers=headers,cookies=cookies, meta={'title': item['file_name']})

    # def file_path(self, request, response, info, *, item=None):
    #     pdf_url = urlparse(request.url).path
    #     pdf_name = request.meta.get('title') + '.pdf'
    #     return join(basename(dirname(pdf_url)), basename(pdf_name))

    # def item_completed(self, results, item, info):
    #     return item