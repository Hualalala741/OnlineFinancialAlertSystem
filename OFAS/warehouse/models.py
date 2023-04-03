from django.db import models

# Create your models here.
class news(models.Model):
    # 爬取的新闻数据
    link = models.CharField(max_length=200, primary_key=True)
    title = models.TextField()
    date = models.CharField(max_length=30)
    source = models.CharField(max_length=50)
    article = models.TextField()

    # def __str__(self):
    #     return "%s:%s:%s:%s:%s" % (self.link, self.title, self.date, self.source, self.article)
    #
    # class Meta:
    #     db_table = "news"