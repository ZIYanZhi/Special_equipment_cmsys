# Generated by Django 3.2.9 on 2023-08-04 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0033_auto_20230804_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='outorderclothes',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]