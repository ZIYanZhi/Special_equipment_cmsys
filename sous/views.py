import datetime
import random
from collections import Counter, defaultdict
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction, DataError
from django.db.models.functions import Rank
from django.shortcuts import render, redirect, reverse
from django.db.models import F, Count, Q

from clothes.forms import ClothesForm
# Create your views here.
from common.models import Outorder, OutorderClothes, User, Customer, Clothes, Man
from outorder.forms import OutorderForm, OutorderClothesForm, EditmoreForm
from django.db.models import Window

from common.models import Outorder, Customer, Clothes, OutorderClothes, InorderClothes, Inorder,Outbound
from django import forms


# 定义一个视图函数，处理客户列表请求
def customer_list_view(request):

    if request.method == "POST":
        outorderclothes_form = OutorderClothesForm(request.POST)
        if outorderclothes_form.is_valid():
            costomer = outorderclothes_form.cleaned_data['clothes']
            print(costomer)
        address = Customer.objects.values_list("address", flat=True)
        # 初始化一个空列表，用于存储客户信息
        customers = []
        # 遍历每个地址
        for addr in address:
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            addr = request.POST.get('addr')
            name = request.POST.get('name')
            sn = request.POST.get('sn')
            man_name = request.POST.get('man_name')

            filters = Q()

            if start_time and end_time:
                filters &= Q(outorder__outorderclothes__create_time__range=[start_time, end_time])
            if addr:
                filters &= Q(address__icontains=addr)
            if name:
                filters &= Q(outorder__clothes__name__icontains=name)
            if sn:
                filters &= Q(outorder__clothes__sn__icontains=sn)
            if man_name:
                filters &= Q(outorder__outorderclothes__name__icontains=man_name)
            customer = Customer.objects.filter(filters).values(
                'id',
                'address',
                'outorder__outorderclothes__amount',
                'outorder__clothes__name',
                'outorder__clothes__sn',
                'outorder__clothes__price',
                'outorder__outorderclothes__id',
                'outorder__outorderclothes__create_time',
                'outorder__outorderclothes__name__name'
            )
            # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息

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
                if cust["outorder__clothes__name"] is not None:
                    # 将当前客户的信息添加到字典中
                    d["id"] = cust["id"]
                    d["outorder__clothes__name"] = cust["outorder__clothes__name"]
                    d["outorder__clothes__sn"] = cust["outorder__clothes__sn"]
                    d["amount"] = cust["outorder__outorderclothes__amount"]
                    d["price"] = cust["outorder__clothes__price"]
                    d["address"] = cust["address"]
                    d["outorderclothesid"] = cust["outorder__outorderclothes__id"]
                    d["time"] = cust["outorder__outorderclothes__create_time"]
                    d["name"] = cust["outorder__outorderclothes__name__name"]
                    # 将字典添加到列表中
                    if d not in customer_list:
                        customer_list.append(d)

                    # print(customer_list)
                    # 对列表进行排序，根据衣物数量从大到小排序，并只保留前10个元素
                    customer_order = sorted(
                        customer_list,
                        key=lambda x: (x["amount"], x["address"]),
                        reverse=True,
                    )
                    # print(customer_order)
                    customer_list = customer_order[:20]

                    # 计算列表中所有元素的衣物数量的总和
                    amount_sum = sum(item["amount"] for item in customer_list)
                    print(amount_sum)
                    price_sum = sum(item["price"] for item in customer_list)
                    print("jiage", price_sum)

                    # 遍历列表，计算每个地址的衣物数量的总和
            amount_sum_dict = {}
            for item in customer_list:
                address = item["outorder__clothes__name"]
                if address not in amount_sum_dict:
                    amount_sum_dict[address] = item["amount"]
                else:
                    amount_sum_dict[address] += item["amount"]
        # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
        context = {
            "outorderclothes_form":outorderclothes_form,
            "customer_list": customer_list,
            "amount_sum": amount_sum,
            "amount_sum_dict": amount_sum_dict,
            "address": address,
            "price_sum": price_sum,
            # 将 address 添加到上下文中
        }
        # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
        return render(request, "sous/index.html", context)
    else:
        outorderclothes_form = OutorderClothesForm(request.POST)

        # 从Customer模型中获取所有车号的地址
        address = Customer.objects.values_list("address", flat=True)
        # 初始化一个空列表，用于存储客户信息
        customers = []
        # 遍历每个地址
        for addr in address:
            # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息

            customer = Customer.objects.filter(address=addr).values(
                'id',
                'address',
                'outorder__outorderclothes__amount',
                'outorder__clothes__name',
                'outorder__clothes__sn',
                'outorder__clothes__price',
                'outorder__outorderclothes__id',
                'outorder__outorderclothes__create_time',
                'outorder__outorderclothes__name__name'
            )
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
                if cust["outorder__clothes__name"] is not None:
                    # 将当前客户的信息添加到字典中
                    d["id"] = cust["id"]
                    d["outorder__clothes__name"] = cust["outorder__clothes__name"]
                    d["outorder__clothes__sn"] = cust["outorder__clothes__sn"]
                    d["amount"] = cust["outorder__outorderclothes__amount"]
                    d["price"] = cust["outorder__clothes__price"]
                    d["address"] = cust["address"]
                    d["outorderclothesid"] = cust["outorder__outorderclothes__id"]
                    d["time"] = cust["outorder__outorderclothes__create_time"]
                    d["name"] = cust["outorder__outorderclothes__name__name"]
                    # 将字典添加到列表中
                    if d not in customer_list:
                        customer_list.append(d)

                    # print(customer_list)
                    # 对列表进行排序，根据衣物数量从大到小排序，并只保留前10个元素
                    customer_order = sorted(
                        customer_list,
                        key=lambda x: (x["amount"], x["address"]),
                        reverse=True,
                    )
                    # print(customer_order)
                    customer_list = customer_order[:20]

                    # 计算列表中所有元素的衣物数量的总和
                    amount_sum = sum(item["amount"] for item in customer_list)

                    # 遍历列表，计算每个地址的衣物数量的总和
            amount_sum_dict = {}
            total_price = 0
            for item in customer_list:
                address = item["outorder__clothes__name"]
                if address not in amount_sum_dict:
                    amount_sum_dict[address] = item["amount"]
                else:
                    amount_sum_dict[address] += item["amount"]
                price = item["price"]
                amount = item["amount"]
                contact_total_price = price * amount

                # 更新总价
                total_price += contact_total_price
        # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
        context = {
            "outorderclothes_form": outorderclothes_form,

            "customer_list": customer_list,
            "amount_sum": amount_sum,
            "amount_sum_dict": amount_sum_dict,
            "address": address,
            "price_sum": total_price,
            # 将 address 添加到上下文中
        }
        # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
        return render(request, "sous/index.html", context)


def ranking(request):
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    addresses = set()
    customers = []

    q = (
        Q()
        if not (start_time and end_time)
        else Q(outorder__outorderclothes__create_time__range=[start_time, end_time])
    )

    # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息
    customers = Customer.objects.filter(q).values(
        "id",
        "address",
        "outorder__outorderclothes__amount",
        "outorder__clothes__name",
        "outorder__clothes__sn",
        "outorder__clothes__price",
        "outorder__outorderclothes__id",
        "outorder__outorderclothes__create_time",
        "outorder__outorderclothes__name__name",
    )

    # 初始化一个空列表，用于存储处理后的客户信息
    customer_list = []
    # 初始化一个变量，用于存储衣物数量的总和
    amount_sum = 0
    # 初始化一个空字典，用于存储每个地址的衣物数量的总和
    amount_sum_dict = {}
    # 遍历每个客户信息
    # 序列化
    for customer in customers:
        # 初始化一个空字典，用于存储当前客户的信息
        d = {}
        # 如果当前客户的衣物名称不为空
        if not customer["outorder__clothes__name"]:
            continue
        # 将当前客户的信息添加到字典中
        d["id"] = customer["id"]
        d["outorder__clothes__name"] = customer["outorder__clothes__name"]
        d["outorder__clothes__sn"] = customer["outorder__clothes__sn"]
        d["amount"] = customer["outorder__outorderclothes__amount"]
        d["price"] = customer["outorder__clothes__price"]
        d["address"] = customer["address"]
        d["outorderclothesid"] = customer["outorder__outorderclothes__id"]
        d["time"] = customer["outorder__outorderclothes__create_time"]
        d["name"] = customer["outorder__outorderclothes__name__name"]
        # 将字典添加到列表中
        customer_list.append(d)
        addresses.add(customer["address"])
    # 排序
    sorted_list = sorted(
        customer_list, key=lambda x: (x["address"], x["amount"]), reverse=True
    )
    # 重新整理得到address对应amount前三的列表，显示需要的字段
    count_dict = defaultdict(int)
    new_list = []
    for item in sorted_list:
        if count_dict.get(item["address"]) == 3:
            continue
        new_item = {
            "address": item["address"],
            "amount": item["amount"],
            "outorder__clothes__name": item["outorder__clothes__name"],
            "outorder__clothes__sn": item["outorder__clothes__sn"],
            "price": item["price"],
            "outorderclothesid": item["outorderclothesid"],
            "time": item["time"],
            "name": item["name"],
        }
        new_list.append(new_item)
        count_dict[item["address"]] += 1

    amount_sum = sum(item["amount"] for item in customer_list)

    # 遍历列表，计算每个地址的衣物数量的总和

    amount_sum_dict = {}
    for item in customer_list:
        address = item["outorder__clothes__name"]
        if address not in amount_sum_dict:
            amount_sum_dict[address] = item["amount"]
        else:
            amount_sum_dict[address] += item["amount"]
    # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
    context = {
        "customer_list": new_list,
        "amount_sum": amount_sum,
        "amount_sum_dict": amount_sum_dict,
        "address": list(addresses),
        # 将 address 添加到上下文中
    }
    # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
    return render(request, "sous/ranking.html", context)
def qsss(request):

    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    addr = request.GET.get('addr')
    name = request.GET.get('name')
    sn = request.GET.get('sn')
    man_name = request.GET.get('man_name')
    filters = Q()
    print(sn)


    addresses = set()
    customers = []

    q = (
            Q()
            if not (start_time and end_time)
            else Q(outorder__create_time__range=[start_time, end_time])
        ) & (
            Q()
            if not addr
            else Q(address=addr)
        ) & (
            Q()
            if not name
            else Q(outorder__clothes__name__icontains=name)
        ) & (
            Q()
            if not sn
            else Q(outorder__clothes__sn__icontains=sn)
        ) & (
            Q()
            if not man_name
            else Q(outorder__name__name__icontains=man_name)
        )

    # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息
    customers = Customer.objects.filter(q).values(
        "id",
        "address",
        "outorder__outorderclothes__amount",
        "outorder__clothes__name",
        "outorder__clothes__sn",
        "outorder__clothes__price",
        "outorder__outorderclothes__id",
        "outorder__outorderclothes__create_time",
        "outorder__outorderclothes__name__name",
    )

    # 初始化一个空列表，用于存储处理后的客户信息
    customer_list = []
    # 初始化一个变量，用于存储衣物数量的总和
    amount_sum = 0
    # 初始化一个空字典，用于存储每个地址的衣物数量的总和
    amount_sum_dict = {}
    # 遍历每个客户信息
    # 序列化
    for customer in customers:
        # 初始化一个空字典，用于存储当前客户的信息
        d = {}
        # 如果当前客户的衣物名称不为空
        if not customer["outorder__clothes__name"]:
            continue
        # 将当前客户的信息添加到字典中
        d["id"] = customer["id"]
        d["outorder__clothes__name"] = customer["outorder__clothes__name"]
        d["outorder__clothes__sn"] = customer["outorder__clothes__sn"]
        d["amount"] = customer["outorder__outorderclothes__amount"]
        d["price"] = customer["outorder__clothes__price"]
        d["address"] = customer["address"]
        d["outorderclothesid"] = customer["outorder__outorderclothes__id"]
        d["time"] = customer["outorder__outorderclothes__create_time"]
        d["name"] = customer["outorder__outorderclothes__name__name"]
        # 将字典添加到列表中
        customer_list.append(d)
        addresses.add(customer["address"])
    # 排序
    sorted_list = sorted(
        customer_list, key=lambda x: (x["address"], x["amount"]), reverse=True
    )
    # 重新整理得到address对应amount前三的列表，显示需要的字段
    count_dict = defaultdict(int)
    new_list = []
    for item in sorted_list:
        if count_dict.get(item["address"]) == 3:
            continue
        new_item = {
            "address": item["address"],
            "amount": item["amount"],
            "outorder__clothes__name": item["outorder__clothes__name"],
            "outorder__clothes__sn": item["outorder__clothes__sn"],
            "price": item["price"],
            "outorderclothesid": item["outorderclothesid"],
            "time": item["time"],
            "name": item["name"],
        }
        new_list.append(new_item)
        count_dict[item["address"]] += 1

    amount_sum = sum(item["amount"] for item in customer_list)

    # 遍历列表，计算每个地址的衣物数量的总和

    amount_sum_dict = {}
    for item in customer_list:
        address = item["outorder__clothes__name"]
        if address not in amount_sum_dict:
            amount_sum_dict[address] = item["amount"]
        else:
            amount_sum_dict[address] += item["amount"]
    # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
    context = {
        "customer_list": new_list,
        "amount_sum": amount_sum,
        "amount_sum_dict": amount_sum_dict,
        "address": list(addresses),
        # 将 address 添加到上下文中
    }
    # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
    return render(request, "sous/ranking.html", context)

def search(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    addr = request.POST.get('addr')
    name = request.POST.get('name')
    sn = request.POST.get('sn')
    man_name = request.POST.get('man_name')
    filters = Q()
    if start_time and end_time:
        filters &= Q(outorder__create_time=[start_time, end_time])
    if addr:
        filters &= Q(address__icontains=addr)
    if name:
        filters &= Q(outorder__clothes__name__icontains=name)
    if sn:
        filters &= Q(outorder__clothes__sn__icontains=sn)
    if man_name:
        filters &= Q(outorder__name__name__icontains=man_name)
    filters &= ~Q(outorder__clothes__name="计算器")  # 排除名称为"锭带"的数据

    # 从Customer模型中过滤出与当前地址匹配的所有客户，并获取他们的相关信息
    customers = Customer.objects.filter(filters).values(
        "id",
        "address",
        "outorder__outorderclothes__amount",
        "outorder__clothes__name",
        "outorder__clothes__sn",
        "outorder__clothes__price",
        "outorder__outorderclothes__id",
        "outorder__outorderclothes__create_time",
        "outorder__outorderclothes__name__name",
    ).order_by('man_name')

    # 初始化一个空列表，用于存储处理后的客户信息
    customer_list = []
    # 初始化一个变量，用于存储衣物数量的总和
    amount_sum = 0
    # 初始化一个空字典，用于存储每个地址的衣物数量的总和
    amount_sum_dict = {}
    # 遍历每个客户信息
    # 序列化
    for customer in customers:
        # 初始化一个空字典，用于存储当前客户的信息
        d = {}
        # 如果当前客户的衣物名称不为空
        if not customer["outorder__clothes__name"]:
            continue
        # 将当前客户的信息添加到字典中
        d["id"] = customer["id"]
        d["outorder__clothes__name"] = customer["outorder__clothes__name"]
        d["outorder__clothes__sn"] = customer["outorder__clothes__sn"]
        d["amount"] = customer["outorder__outorderclothes__amount"]
        d["price"] = customer["outorder__clothes__price"]
        d["address"] = customer["address"]
        d["outorderclothesid"] = customer["outorder__outorderclothes__id"]
        d["time"] = customer["outorder__outorderclothes__create_time"]
        d["name"] = customer["outorder__outorderclothes__name__name"]
        # 将字典添加到列表中
        customer_list.append(d)

    # 排序

    # 重新整理得到address对应amount前三的列表，显示需要的字段

    amount_sum = sum(item["amount"] for item in customer_list)
    price_sum = sum(item["price"] for item in customer_list)
    # 遍历列表，计算每个地址的衣物数量的总和

    amount_sum_dict = {}
    for item in customer_list:
        address = item["outorder__clothes__name"]
        if address not in amount_sum_dict:
            amount_sum_dict[address] = item["amount"]
        else:
            amount_sum_dict[address] += item["amount"]
    # 创建一个字典，将客户列表，衣物数量的总和，每个地址的衣物数量的总和和地址添加到字典中
    context = {
        "customer_list": customer_list,
        "amount_sum": amount_sum,
        "amount_sum_dict": amount_sum_dict,
        "price_sum": price_sum,

        # 将 address 添加到上下文中
    }
    # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
    return render(request, "sous/index.html", context)


def foo():
    address = "03#"
    customer_list = Customer.objects.filter(address=address)

    print("1", customer_list)
    # api_obj = Outorder.objects.filter(customer__address=address)
    # for i in api_obj:
    #     print(i, i.id)

    # for i in customer_list:
    #     obj = Clothes.objects.filter(outorder__customer_id=i.id)
    #     for i in obj:
    #         print(i)
    customer_list = Customer.objects.filter(address=address).values(
        "id",
        "outorder__outorderclothes__amount",
        "outorder__clothes__name",
        "outorder__clothes__price",
    )
    print(customer_list)
    d = {}
    for item in customer_list:
        if item["outorder__clothes__name"] is None:
            continue
        d["id"] = item["id"]
        d["outorder__clothes__name"] = item["outorder__clothes__name"]
        d["amount"] = item["outorder__outorderclothes__amount"]
        d["price"] = item["outorder__clothes__price"]

    # print(d['outorder__clothes__name'] ,d['amount'],d['price'])
    # feiyong =d['amount'] * d['price']
    # print(feiyong)
    # json_str = json.dumps(d)

    # obj = Clothes.objects.filter(outorder__customer_id__in=customer_list)
    # for i in obj:
    #     amount = OutorderClothes.objects.filter(clothes_id=i.id, outorder_id=i.id)
    #     print(i, i.id, i.name, amount)


if __name__ == "__main__":
    foo()


def huafei(request):
    if request.method == "POST":
        customer_list = []
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        name = request.POST.get('name')
        sn = request.POST.get('sn')

        filters = Q()
        if start_time and end_time:
           filters &= Q(create_time__range=[start_time, end_time])
        if name:
           filters &= Q(inorder__clothes__name__icontains=name)
        if sn:
           filters &= Q(inorder__clothes__sn=sn)
        print('过滤：',filters)
        customers = InorderClothes.objects.filter(filters).values(
            'id',
            'inorder__clothes__name',
            'inorder__clothes__sn',
            'inorder__clothes__price',
            'amount',
        ).distinct().order_by('inorder__clothes__sn')
        results = InorderClothes.objects.filter(filters)
        print(results)
        # 遍历结果并打印
        for result in results:
            print('测试',result.inorder, result.clothes)
        print('customers:',customers)
        for customer in customers:
            # 初始化一个空字典，用于存储当前客户的信息
            d = {}


            # 将当前客户的信息添加到字典中
            d["id"] = customer["id"]
            d["name"] = customer["inorder__clothes__name"]
            d["sn"] = customer["inorder__clothes__sn"]
            d["price"] = customer["inorder__clothes__price"]
            d["amount"] = customer["amount"]
            print(d)
            # 将字典添加到列表中
            if d not in customer_list:
                customer_list.append(d)

        #print("搜索：",customer_list)
        amount_sum = sum(item["amount"] for item in customer_list)
        price_sum = sum(item["amount"] * item["price"] for item in customer_list)
        context = {

            "sou_list": customer_list,
            "amount_sum": amount_sum,
            "price_sum": price_sum,
            # 将 address 添加到上下文中
        }

        # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
        return render(request, "sous/huafei.html", context)
    else:
        qs2 = InorderClothes.objects.all()
        total_price = 0
        amount_sum = 0
        for foo in qs2:
            total_price += foo.clothes.price * foo.amount
            amount_sum += foo.amount

        context = {
            "customer_list": qs2,
            "amount_sum": amount_sum,

            "price_sum": total_price,
            # 将 address 添加到上下文中
        }
        # 返回一个HTTP响应，渲染模板，并将字典作为上下文传递给模板
        return render(request, "sous/huafei.html", context)

def charts(request):
    top_5_book = Outbound.objects.order_by('-amount')[:5].values_list('clothes', 'amount')
    print('排5：', top_5_book)
    top_5_book_titles = [b[0] for b in top_5_book]
    top_5_book__quantities = [b[1] for b in top_5_book]