import datetime
import random
from collections import Counter
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction, DataError
from django.db.models.functions import Rank
from django.shortcuts import render, redirect, reverse
from django.db.models import F,Count
# Create your views here.
from common.models import Outorder, OutorderClothes, User, Customer,Clothes,Man
from outorder.forms import OutorderForm, OutorderClothesForm, EditmoreForm
from django.db.models import Window

from common.models import Outorder, Customer, Clothes, OutorderClothes
from django import forms
from collections import defaultdict



# 定义一个视图函数，处理客户列表请求
def customer_list_view(request):


    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    print(start_time)
    # 从Customer模型中获取所有车号的地址
    address = Customer.objects.values_list('address', flat=True)
    # 初始化一个空列表，用于存储客户信息
    customers = []
    # 遍历每个地址
    for addr in address:
        # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息
        if not start_time or not end_time:
            customer = Customer.objects.filter(address=addr).values('id', 'address','outorder__outorderclothes__amount',
                                                                'outorder__clothes__name', 'outorder__clothes__sn',
                                                                'outorder__clothes__price','outorder__outorderclothes__id','outorder__outorderclothes__create_time','outorder__outorderclothes__name__name')
        else:
            customer = Customer.objects.filter(address=addr, outorder__outorderclothes__create_time__range=[start_time,
                                                                                                            end_time]).values(
                'id', 'address', 'outorder__outorderclothes__amount',
                'outorder__clothes__name', 'outorder__clothes__sn',
                'outorder__clothes__price', 'outorder__outorderclothes__id', 'outorder__outorderclothes__create_time','outorder__outorderclothes__name__name')
        # 将获取的客户信息添加到列表中
        customers.append(customer)

    # 初始化一个空列表，用于存储处理后的客户信息
    customer_list = []
    # 初始化一个变量，用于存储衣物数量的总和
    amount_sum = 0
    # 初始化一个空字典，用于存储每个地址的衣物数量的总和
    amount_sum_dict = {}
    # 遍历每个客户信息
    for customer in customers:
        for cust in customer:
            # 初始化一个空字典，用于存储当前客户的信息
            d = {}

            # 如果当前客户的衣物名称不为空
            if cust['outorder__clothes__name'] is not None:
                # 将当前客户的信息添加到字典中
                d['id'] = cust['id']
                d['outorder__clothes__name'] = cust['outorder__clothes__name']
                d['outorder__clothes__sn'] = cust['outorder__clothes__sn']
                d['amount'] = cust['outorder__outorderclothes__amount']
                d['price'] = cust['outorder__clothes__price']
                d['address'] = cust['address']
                d['outorderclothesid']=cust['outorder__outorderclothes__id']
                d['time'] = cust['outorder__outorderclothes__create_time']
                d['name'] = cust['outorder__outorderclothes__name__name']
                # 将字典添加到列表中
                if d not in customer_list:
                    customer_list.append(d)

                #print(customer_list)
                # 对列表进行排序，根据衣物数量从大到小排序，并只保留前10个元素
                customer_order = sorted(customer_list, key=lambda x: (x['amount'], x['address']), reverse=True)
                #print(customer_order)
                customer_list = customer_order[:20]

                # 计算列表中所有元素的衣物数量的总和
                amount_sum = sum(item['amount'] for item in customer_list)

                # 遍历列表，计算每个地址的衣物数量的总和
        amount_sum_dict = {}
        for item in customer_list:
            address = item['outorder__clothes__name']
            if address not in amount_sum_dict:
                amount_sum_dict[address] = item['amount']
            else:
                amount_sum_dict[address] += item['amount']
    # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
    context = {
        'customer_list': customer_list,
        'amount_sum': amount_sum,
        'amount_sum_dict': amount_sum_dict,
        'address': address,
        # 将 address 添加到上下文中
    }
    # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
    return render(request, 'sous/index.html', context)


    
def ranking(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')


    # 从Customer模型中获取所有车号的地址
    address = Customer.objects.values_list('address', flat=True)
    # 初始化一个空列表，用于存储客户信息

    customers = []

    # 遍历每个地址
    for addr in address:
        # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息
        if not start_time or not end_time:
            customer = Customer.objects.filter(address=addr).values('id', 'address',
                                                                    'outorder__outorderclothes__amount',
                                                                    'outorder__clothes__name', 'outorder__clothes__sn',
                                                                    'outorder__clothes__price',
                                                                    'outorder__outorderclothes__id',
                                                                    'outorder__outorderclothes__create_time',
                                                                    'outorder__outorderclothes__name__name')
        else:
            customer = Customer.objects.filter(address=addr, outorder__outorderclothes__create_time__range=[start_time,
                                                                                                            end_time]).values(
                'id', 'address', 'outorder__outorderclothes__amount',
                'outorder__clothes__name', 'outorder__clothes__sn',
                'outorder__clothes__price', 'outorder__outorderclothes__id', 'outorder__outorderclothes__create_time',
                'outorder__outorderclothes__name__name')
        # 将获取的客户信息添加到列表中
        customers.append(customer)

    # 初始化一个空列表，用于存储处理后的客户信息
    customer_list = []
    # 初始化一个变量，用于存储衣物数量的总和
    amount_sum = 0
    # 初始化一个空字典，用于存储每个地址的衣物数量的总和
    amount_sum_dict = {}
    # 遍历每个客户信息

    count_dict = defaultdict(int)
    for customer in customers:
        for cust in customer:
            # 初始化一个空字典，用于存储当前客户的信息
            d = {}

            # 如果当前客户的衣物名称不为空
            if cust['outorder__clothes__name'] is not None:
                # 将当前客户的信息添加到字典中
                d['id'] = cust['id']
                d['outorder__clothes__name'] = cust['outorder__clothes__name']
                d['outorder__clothes__sn'] = cust['outorder__clothes__sn']
                d['amount'] = cust['outorder__outorderclothes__amount']
                d['price'] = cust['outorder__clothes__price']
                d['address'] = cust['address']
                d['outorderclothesid'] = cust['outorder__outorderclothes__id']
                d['time'] = cust['outorder__outorderclothes__create_time']
                d['name'] = cust['outorder__outorderclothes__name__name']
                # 将字典添加到列表中
                if d not in customer_list:
                    customer_list.append(d)
                #sorted_list = sorted(customer_list, key=lambda x: (x['address'], x['amount']), reverse=True)

                #customer_list = sorted_list[:20]

                # 重新整理得到address对应amount前三的列表，显示需要的字段

                # 计算列表中所有元素的衣物数量的总和
                amount_sum = sum(item['amount'] for item in customer_list)

                # 遍历列表，计算每个地址的衣物数量的总和



        amount_sum_dict = {}
        for item in customer_list:
            address = item['outorder__clothes__name']
            if address not in amount_sum_dict:
                amount_sum_dict[address] = item['amount']
            else:
                amount_sum_dict[address] += item['amount']
    # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
    context = {
        'customer_list': customer_list,
        'amount_sum': amount_sum,
        'amount_sum_dict': amount_sum_dict,
        'address': address,
        # 将 address 添加到上下文中
    }
    # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
    return render(request, 'sous/index.html', context)


def search(request):
    if request.method == "POST":
        object = Outorder.objects
        qs = object.values()
        id = request.POST.get('id')
        code = request.POST.get('code')
        customer_name = request.POST.get('customer_name')
        customer_address = request.POST.get('customer_address')
        man_name = request.POST.get('user_name')
        if id:
            qs = object.filter(id=id)
        if code:
            qs = object.filter(code=code)
        if customer_name:
            customer = Customer.objects.get(name=customer_name,address=customer_address)
            print(customer)
            qs = object.filter(customer_id=customer.id)
        if customer_address:
            customer = Customer.objects.get(name=customer_name,address=customer_address)
            qs = object.filter(customer_id=customer.id)


        if man_name:
            man = Man.objects.get(name=man_name)
            qs = object.filter(man_id=man.id)
        paginator = Paginator(qs, 10)
        page = request.GET.get('page', '1')
        result = paginator.page(page)

        context = {
            'result': result
        }
        messages.add_message(request, messages.SUCCESS, '查询成功')
        return render(request, 'outorder/index.html', context)
    else:
        context = {
            'outorder_form': object

        }


        messages.add_message(request, messages.SUCCESS, '查询失败')
        return render(request, 'outorder/index.html',context)


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