# Generated by Django 3.2.9 on 2023-07-27 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_auto_20230727_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='outorder',
            name='name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.man', verbose_name='领取人'),
            preserve_default=False,
        ),
    ]
