# Generated by Django 3.2 on 2023-04-12 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_alter_news_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='news',
        ),
    ]