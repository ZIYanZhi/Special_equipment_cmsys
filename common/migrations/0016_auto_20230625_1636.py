# Generated by Django 3.2.19 on 2023-06-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_auto_20230624_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='changjia',
            field=models.CharField(default=1, max_length=32, verbose_name='厂家'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='sn',
            field=models.CharField(max_length=32, verbose_name='机件号'),
        ),
    ]
