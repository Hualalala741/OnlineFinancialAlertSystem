from django.shortcuts import render
from warehouse.models import news
import subprocess
from django.http import HttpResponse
# Create your views here.
def index(request):
    subprocess.Popen('Scrapy crawl sinanews')
    news_list = news.objects.all()
    # print(news_list)
    return render(request, "index.html",{'news_list': news_list})

# def index(request):
#
#     news_list = news.object.all()
#     return render(request, "index.html",{'news_list': news_list})

# def vnews(request):
#     #获取所有news表信息
#     lists = news.objects.all()
#     print(lists)
#     #获取单条学生信息
#     # print(news.objects.get(id=1))
#     return HttpResponse("ok")
