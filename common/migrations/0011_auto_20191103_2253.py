# Generated by Django 2.2.6 on 2019-11-03 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20191028_2141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clothes',
            options={'ordering': ['create_time'], 'verbose_name': '器材', 'verbose_name_plural': '器材'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['create_time'], 'verbose_name': '客户', 'verbose_name_plural': '客户'},
        ),
        migrations.AlterModelOptions(
            name='inorder',
            options={'ordering': ['create_time'], 'verbose_name': '入库单', 'verbose_name_plural': '入库单'},
        ),
        migrations.AlterModelOptions(
            name='inorderclothes',
            options={'ordering': ['id'], 'verbose_name': '入库单', 'verbose_name_plural': '入库单'},
        ),
        migrations.AlterModelOptions(
            name='outorder',
            options={'ordering': ['create_time'], 'verbose_name': '出库单', 'verbose_name_plural': '出库单'},
        ),
        migrations.AlterModelOptions(
            name='outorderclothes',
            options={'ordering': ['id'], 'verbose_name': '出库单详情', 'verbose_name_plural': '出库单详情'},
        ),
        migrations.RemoveField(
            model_name='clothes',
            name='amount',
        ),
        migrations.AddField(
            model_name='clothes',
            name='image',
            field=models.ImageField(default=1, upload_to='clothes', verbose_name='图片'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clothes',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='库存'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outorder',
            name='clothes',
            field=models.ManyToManyField(through='common.OutorderClothes', to='common.Clothes', verbose_name='器材'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='color',
            field=models.CharField(max_length=32, verbose_name='颜色'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='modify_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='机件名'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='size',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=32, verbose_name='尺寸'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='sn',
            field=models.CharField(max_length=32, unique=True, verbose_name='机件号'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=32, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='modify_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=32, verbose_name='客户名'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=32, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='clothes',
            field=models.ManyToManyField(through='common.InorderClothes', to='common.Clothes', verbose_name='器材'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='code',
            field=models.CharField(max_length=32, verbose_name='入库单号'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Customer', verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='modify_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='inorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.User', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='inorderclothes',
            name='clothes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Clothes', verbose_name='器材'),
        ),
        migrations.AlterField(
            model_name='inorderclothes',
            name='inorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Inorder', verbose_name='入库单'),
        ),
        migrations.AlterField(
            model_name='outorder',
            name='code',
            field=models.CharField(max_length=32, verbose_name='出库单号'),
        ),
        migrations.AlterField(
            model_name='outorder',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='outorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Customer', verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='outorder',
            name='modify_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='outorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.User', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='outorderclothes',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='outorderclothes',
            name='clothes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Clothes', verbose_name='器材'),
        ),
        migrations.AlterField(
            model_name='outorderclothes',
            name='outorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Outorder', verbose_name='出库单'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='modify_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=32, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('操作员', '操作员'), ('管理员', '管理员')], default='操作员', max_length=32, verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户名'),
        ),
    ]