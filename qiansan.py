import os
import django
import json
from django.db.models import F


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsys.settings")  # MB：项目名称
django.setup()  # 这一步就加载了Django环境

# 必须是django.setup()之后，才能引入模型类
from common.models import Outorder, Customer, Clothes, OutorderClothes

def foo():
    address = "02#"
    #customer_list = Customer.objects.filter(address=address)


    result_list = []
    query_result = Customer.objects.filter(address="02#").values('id', 'outorder__outorderclothes__amount', 'outorder__clothes__name','outorder__clothes__price').annotate(amount=F('outorder__outorderclothes__amount')).order_by('-amount')[:3]
    result_list.extend(query_result)

    print(result_list)

    distinct_results = {item['outorder__clothes__name']: item for item in result_list}.values()
    print(distinct_results)
    for item in result_list:
        amount = item['amount']
        name = item['outorder__clothes__name']

        print(amount)
        print(name)
if __name__ == '__main__':
    foo()


