import os
import django
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsys.settings")  # MB：项目名称
django.setup()  # 这一步就加载了Django环境

# 必须是django.setup()之后，才能引入模型类
from common.models import Outorder, Customer, Clothes, OutorderClothes

def foo():
    address = "03#"
    customer_list = Customer.objects.filter(address=address)

    print("1",customer_list)
    # api_obj = Outorder.objects.filter(customer__address=address)
    # for i in api_obj:
    #     print(i, i.id)

    # for i in customer_list:
    #     obj = Clothes.objects.filter(outorder__customer_id=i.id)
    #     for i in obj:
    #         print(i)
    customer_list = Customer.objects.filter(address=address).values('id', 'outorder__outorderclothes__amount', 'outorder__clothes__name','outorder__clothes__price')
    print(customer_list)
    d = {}
    for item in customer_list:
        if item['outorder__clothes__name'] is None:
            continue
        d['id'] = item['id']
        d['outorder__clothes__name'] = item['outorder__clothes__name']
        d['amount'] = item['outorder__outorderclothes__amount']
        d['price'] = item['outorder__clothes__price']

    #print(d['outorder__clothes__name'] ,d['amount'],d['price'])
    #feiyong =d['amount'] * d['price']
    #print(feiyong)
    #json_str = json.dumps(d)



    # obj = Clothes.objects.filter(outorder__customer_id__in=customer_list)
    # for i in obj:
    #     amount = OutorderClothes.objects.filter(clothes_id=i.id, outorder_id=i.id)
    #     print(i, i.id, i.name, amount)

if __name__ == '__main__':
    foo()