# Generated by Django 3.2 on 2023-04-10 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20230407_0116'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]