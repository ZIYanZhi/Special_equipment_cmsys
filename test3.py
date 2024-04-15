import os
import django
import json

from django.db.models import Sum
from django.db.models import Q
from django. db. models import F
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsys.settings")  # MB：项目名称
django.setup()  # 这一步就加载了Django环境

# 必须是django.setup()之后，才能引入模型类
from common.models import Outorder, Customer, Clothes, OutorderClothes

def foo():
    #popular_posts = Clothes.objects.aggregate(Sum('price'))
    #popular_posts1 = Clothes.objects.aggregate(Sum( 'stock'))
    #kucun = popular_posts.values('price','stock')
    #print(popular_posts)
    #print(popular_posts1)
    total_price = Clothes.objects.aggregate(
        total=Sum(F('price') * F('stock'),))['total']
    total_price = total_price if total_price else 0
    fell = '%.2f'%total_price
    print(fell)


if __name__ == '__main__':
    foo()