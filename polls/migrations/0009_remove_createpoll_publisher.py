# Generated by Django 2.2.6 on 2020-06-09 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_createpoll_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createpoll',
            name='publisher',
        ),
    ]