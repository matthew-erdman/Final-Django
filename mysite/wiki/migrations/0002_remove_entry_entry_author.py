# Generated by Django 3.1.6 on 2021-04-21 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='entry_author',
        ),
    ]
