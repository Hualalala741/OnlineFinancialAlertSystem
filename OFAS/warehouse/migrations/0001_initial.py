# Generated by Django 3.2 on 2023-04-02 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='news',
            fields=[
                ('link', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('date', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=50)),
                ('article', models.TextField()),
            ],
        ),
    ]
