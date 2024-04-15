import os
import django
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsys.settings")  # MB：项目名称
django.setup()  # 这一步就加载了Django环境

# 必须是django.setup()之后，才能引入模型类
from common.models import Outorder, Customer, Clothes, OutorderClothes

def foo():
    popular_posts = OutorderClothes.objects.order_by('-amount').values('clothes__name','amount')[0:9]
    print(popular_posts,)
if __name__ == '__main__':
    foo()