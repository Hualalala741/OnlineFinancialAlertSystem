# Generated by Django 3.2 on 2023-04-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_alter_news_emo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='emo',
            field=models.TextField(max_length=5),
        ),
    ]
