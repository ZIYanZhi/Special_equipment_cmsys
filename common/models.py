from django.db import models
from django.utils import timezone


# Create your models here.



class User(models.Model):
    role_choices = (
        ('出库员', '出库员'),
        ('管理员', '管理员')
    )
    # 用户名
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    # 密码
    password = models.CharField(max_length=100, verbose_name='密码')
    # 姓名
    name = models.CharField(max_length=32, verbose_name='姓名')
    # 角色
    role = models.CharField(max_length=32, choices=role_choices, default='出库员', verbose_name='角色')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name

# 车号
class Customer(models.Model):
    # 工序
    name = models.CharField(max_length=32, verbose_name='工序')
    # 车间
    phone = models.CharField(max_length=32, verbose_name='车间')
    # 车号
    address = models.CharField(max_length=32, verbose_name='车号')
    # 机型
    jx = models.CharField(max_length=32, verbose_name='机型')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')


    def __str__(self):
        return "{}-{}-{}".format(self.name,self.phone,self.address,self.jx)


    class Meta:
        ordering = ['create_time']
        verbose_name = '工序'
        verbose_name_plural = verbose_name

# 机件
class Clothes(models.Model):
    lei_choices = (
        (1, "一类"),
        (2, "二类"),
        (3, "三类"),
    )
    lei = models.SmallIntegerField(verbose_name="类别", choices=lei_choices, default=1)

    # 机件名称
    name = models.CharField(max_length=32, verbose_name='机件名')
    # 机件号
    sn = models.CharField(max_length=32,  verbose_name='机件号')
    # 价格
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='价格')
    # 颜色
    danwei_choices = (
        (1, "台"),
        (2, "套"),
        (3, "件"),
        (4, "个"),
        (5, "盒"),
        (6, "箱"),
        (7, "斤"),

    )
    danwei = models.SmallIntegerField(verbose_name="单位",default=1, choices=danwei_choices)

    # 库存
    stock = models.DecimalField(verbose_name='库存',max_digits=7,decimal_places=2)
    # 库存下限
    stock_down = models.DecimalField(verbose_name='最低库存',max_digits=7,decimal_places=2)
    changjia = models.CharField(max_length=32,  default=1,verbose_name='厂家')
    # 图片
    image = models.ImageField(upload_to='clothes', verbose_name='图片')
    # 描述
    desc = models.CharField(max_length=200, verbose_name='描述')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return "{}-{}-{}".format(self.name,self.sn,self.changjia)

    class Meta:
        ordering = ['create_time']
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name


class Department(models.Model):
    """部门表"""
    title = models.CharField( verbose_name="部门", max_length=32)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['id']
        verbose_name = '部门'
        verbose_name_plural = verbose_name

class Man(models.Model):
    """部门表"""
    name = models.CharField( verbose_name="领取人", max_length=32)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id']
        verbose_name = '领取人'
        verbose_name_plural = verbose_name


class Inorder(models.Model):
    # 入库单号
    code = models.CharField(max_length=32, verbose_name='入库单号')
    customer = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='部门')
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 入库单里的器材，和Clothes表是多对多的关系
    clothes = models.ManyToManyField(Clothes, through='InorderClothes', verbose_name='器材')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['id']
        verbose_name = '入库单'
        verbose_name_plural = verbose_name


class InorderClothes(models.Model):
    # 入库单
    inorder = models.ForeignKey(Inorder, on_delete=models.CASCADE, verbose_name='入库单')
    # 器材
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name='产品信息')
    # 入库单中器材的数量
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.clothes.name

    class Meta:
        ordering = ['id']
        verbose_name = '入库单'
        verbose_name_plural = verbose_name
class Inbound(models.Model):
    code = models.CharField(max_length=32, verbose_name='入库单号')
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 入库单里的器材，和Clothes表是多对多的关系
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name='产品信息')

    price = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name='二次价格')
    # 入库单中器材的数量
    amount = models.DecimalField(verbose_name='数量',max_digits=7,decimal_places=3)
    # 创建时间
    create_time = models.DateTimeField (auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['id']
        verbose_name = '入库单'
        verbose_name_plural = verbose_name
class Outbound(models.Model):
    # 出库单号
    code = models.CharField(max_length=32, verbose_name='出库单号')
    # 车号
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='车号')
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='出库员')
    name = models.ForeignKey(Man, on_delete=models.CASCADE, verbose_name='领取人')
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name='产品信息')
    amount = models.DecimalField(verbose_name='数量',max_digits=7,decimal_places=3)
    # 创建时间
    create_time = models.DateTimeField (default=timezone.now, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')


    def __str__(self):
        return self.code

    class Meta:
        ordering = ['id']
        verbose_name = '出库单'
        verbose_name_plural = verbose_name
class Outorder(models.Model):
    # 出库单号
    code = models.CharField(max_length=32, verbose_name='出库单号')
    # 客户
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='工序')
    # 用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='出库员')
    clothes = models.ManyToManyField(Clothes, through='OutorderClothes', verbose_name='产品信息')
    amount = models.DecimalField(verbose_name='数量',max_digits=7,decimal_places=3,default=None, null=True)
    name = models.ForeignKey(Man, on_delete=models.CASCADE, verbose_name='领取人',default=None, null=True)
    # 入库单里的器材，和Clothes表是多对多的关系

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['id']
        verbose_name = '出库单'
        verbose_name_plural = verbose_name


class OutorderClothes(models.Model):
    # 出库单
    outorder = models.ForeignKey(Outorder, on_delete=models.CASCADE, verbose_name='出库单')
    # 器材
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name='产品信息')
    # 出库单中器材的数量
    amount = models.DecimalField(verbose_name='数量',max_digits=7,decimal_places=3)
    name = models.ForeignKey(Man, on_delete=models.CASCADE, verbose_name='领取人')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')


    def __str__(self):
        return self.clothes.name

    class Meta:
        ordering = ['id']
        verbose_name = '出库单详情'
        verbose_name_plural = verbose_name




