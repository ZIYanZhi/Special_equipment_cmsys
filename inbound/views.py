import datetime
import random
from decimal import Decimal

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
# Create your views here.
from django.urls import reverse

from common.models import Inbound, Inorder, User, InorderClothes, Customer, Clothes
from inbound.forms import InboundForm, InorderForm, InorderClothesForm, EditmoreForm


def list(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Inbound.objects.all().order_by('-create_time')
    total_amount = Inbound.objects.aggregate(total=Sum('amount'))['total']
    total_price = 0  # 初始化总价为 0
    total_cheng = 0
    #cha_price = 0
    #cha = 0

    for inbound in qs:

        if inbound.price is not None:
            price = inbound.price
        else:
            price = inbound.clothes.price

        amount = inbound.amount
        product_price = price * amount
        #dan_price =inbound.clothes.price - price
        #cha = inbound.clothes.price * amount - price * amount
        total_price += product_price
        #cha_price += cha
        product_price = round(product_price, 2)
        #cha = round(cha, 2)
        #inbound.dan_price = dan_price
        #inbound.cha = cha
        inbound.product_price = product_price
        total_cheng += inbound.product_price





    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result,
        'total_price ': total_price,
        'total_amount': total_amount,
        'total_price': total_cheng,

    }
    return render(request, 'inbound/index.html', context)


def add(request):
    if request.method == "POST":
        inbound_form = InboundForm(request.POST)

        if inbound_form.is_valid():

            uid = request.session.get('user_id')
            user = User.objects.get(id=uid)
            now = datetime.datetime.now().strftime('%Y%m%d%H%M')
            clothes = inbound_form.cleaned_data['clothes']
            amount = inbound_form.cleaned_data['amount']
            price = inbound_form.cleaned_data['price']
            code = 'IN' + now
            with transaction.atomic():  # 事务

                new_inbound = Inbound.objects.create(code=code,
                                                 user=user,
                                                 clothes=clothes,
                                                 amount=amount,
                                                 price=price,
                                                 )
                clothes.stock += amount
                clothes.save()
            context = {
                'id': new_inbound.id
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect(reverse('inbound:index'))

        else:
            context = {
                'inorder_form': inbound_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inbound/add.html', context)
    else:
        inorder_form = InboundForm()
        context = {
            'inorder_form': inorder_form
        }
        return render(request, 'inbound/add.html', context)


def search(request):
    inbound_objects = Inbound.objects
    qs = inbound_objects.all()
    clothes_name = request.GET.get('clothes_name')
    clothes_sn = request.GET.get('clothes_sn')
    lei = request.GET.get('lei')
    conditions = Q()
    if clothes_name:
        conditions &= Q(clothes__name=clothes_name)
    if clothes_sn:
        conditions &= Q(clothes__sn=clothes_sn)
    if lei:
        conditions &= Q(clothes__lei=lei)

    # 应用查询条件
    qs = qs.filter(conditions).order_by('-create_time')
    total_amount = qs.aggregate(total=Sum('amount'))['total']
    # total_price = qs.aggregate(total=Sum('clothes__price'))['total']
    total_price = 0
    for inbound in qs:
        price = inbound.clothes.price
        amount = inbound.amount
        product_price = price * amount
        total_price += product_price
        product_price = round(product_price, 2)
        inbound.product_price = product_price
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result,
        'total_amount': total_amount,
        'total_price': total_price,
    }
    messages.add_message(request, messages.SUCCESS, '查询成功')
    return render(request, 'inbound/index.html', context)


def update(request, inbound_id):
    inbound = Inbound.objects.get(id=inbound_id)

    if request.method == "POST":
        inbound_form = InboundForm(request.POST)
        if inbound_form.is_valid():
            amount = inbound_form.cleaned_data['amount']
            price = inbound_form.cleaned_data['price']

            if amount:
                with transaction.atomic():
                    add_amount = amount - inbound.amount
                    inbound.amount = amount
                    inbound.price = price
                    inbound.clothes.stock += add_amount
                    inbound.save()
                    inbound.clothes.save()

            inbound.save()
            context = {
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('inbound:index'))
        else:
            context = {
                'inbound_form': inbound_form,

            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inbound/edit.html', context)
    else:
        inbound_form = InboundForm({'id': inbound.id,
                                    'code': inbound.code,
                                    'clothes': inbound.clothes,
                                    'price': inbound.price,
                                    'amount': inbound.amount,
                                    'create_time': inbound.create_time})
        context = {
            'inbound_form': inbound_form,
            'inbound_id': inbound_id,

        }
        return render(request, 'inbound/edit.html', context)


def delete(request, inbound_id):
    inbound = Inbound.objects.get(id=inbound_id)
    inbound.delete()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('inbound:index'))


def detail(request, inorder_id):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs1 = Inorder.objects.filter(id=inorder_id)
    qs2 = InorderClothes.objects.filter(inorder_id=inorder_id)
    sum = 0
    for foo in qs2:
        sum += foo.clothes.price * foo.amount
    context = {
        'qs1': qs1,
        'qs2': qs2,
        'sum': sum,
        'inorder_id': inorder_id
    }
    return render(request, 'inorder/detail.html', context)


def addmore(request, inorder_id, ):
    if request.method == "POST":
        shuju = Clothes.objects.all()
        pid = request.POST.get('id')
        did = request.GET.get('id')
        print("od", pid)
        print("dd", did)
        inorderclothes_form = InorderClothesForm(request.POST)
        if inorderclothes_form.is_valid():

            clothes = inorderclothes_form.cleaned_data['clothes']
            amount = inorderclothes_form.cleaned_data['amount']

            with transaction.atomic():  # 事务
                new_inorderclothes = InorderClothes.objects.create(clothes=clothes, inorder_id=inorder_id,
                                                                   amount=amount)
                # 入库增加库存
                clothes.stock += amount
                clothes.save()

            context = {
                'id': new_inorderclothes.id
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect(reverse('inorder:detail', args={inorder_id}))

        else:
            context = {
                'inorderclothes_form': inorderclothes_form,
                'inorder_id': inorder_id,
                'shuju': shuju,
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/addmore.html', context)
    else:
        inorderclothes_form = InorderClothesForm()
        shuju = Clothes.objects.all()

        did = request.GET.get('clothes_id')
        print("dd", did)
        # clothes = Clothes.objects.get(id=clothes_id)

        print(shuju)
        context = {
            'inorderclothes_form': inorderclothes_form,
            'inorder_id': inorder_id,

        }
        return render(request, 'inorder/addmore.html', context)


def editmore(request, inorder_id, inorderclothes_id):
    inorderclothes = InorderClothes.objects.get(id=inorderclothes_id)

    if request.method == "POST":
        editmore_form = EditmoreForm(request.POST)
        if editmore_form.is_valid():
            clothes = editmore_form.cleaned_data['clothes']
            amount = editmore_form.cleaned_data['amount']

            if amount:
                with transaction.atomic():
                    add_amount = amount - inorderclothes.amount
                    inorderclothes.amount = amount
                    inorderclothes.clothes.stock += add_amount
                    inorderclothes.save()
                    inorderclothes.clothes.save()
            context = {
                'inorderclothes_id': inorderclothes_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('inorder:detail', args={inorder_id}))
        else:
            context = {
                'editmore_form': editmore_form,
                'inorder_id': inorder_id,
                'inorderclothes_id': inorderclothes_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'inorder/editmore.html', context)
    else:
        editmore_form = EditmoreForm({'clothes': inorderclothes.clothes,
                                      'amount': inorderclothes.amount})
        context = {
            'editmore_form': editmore_form,
            'inorder_id': inorder_id,
            'inorderclothes_id': inorderclothes_id,
        }
        return render(request, 'inorder/editmore.html', context)


def deletemore(request, inorder_id, inorderclothes_id):
    inorderclothes = InorderClothes.objects.get(id=inorderclothes_id)
    with transaction.atomic():
        inorderclothes.delete()
        inorderclothes.clothes.stock -= inorderclothes.amount
        inorderclothes.clothes.save()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('inorder:detail', args={inorder_id}))

def bd(request):
    # 获取所有 Inbound 对象
    inbounds = Inbound.objects.all()

    # 创建一个空列表，用于存储价格不同的条目
    qs = []
    total_price = 0  # 初始化总价为 0
    total_cheng = 0
    total_amount = 0
    cha_price = 0
    # 遍历每个 Inbound 对象
    for inbound in inbounds:
        if inbound.clothes.price != inbound.price:
            qs.append({

                'clothes_name': inbound.clothes.name,
                'clothes_sn': inbound.clothes.sn,
                'clothes_price': inbound.clothes.price,
                'inbound_price': inbound.price,
                'amount': inbound.amount,
                'create_time': inbound.create_time,
                'modify_time': inbound.modify_time,
                'id': inbound.id,
            })

    for item in qs:
        if item.get('inbound_price') is not None:
            price = item.get('inbound_price')
        else:
            price = item.get('clothes_price')
        amount = item.get('amount')
        product_price = price * amount
        dan_price = item.get('clothes_price') - price
        cha = item.get('clothes_price') * amount - price * amount
        total_price += product_price
        cha_price += cha
        product_price = round(product_price, 2)
        cha = round(cha, 2)
        item['dan_price'] = dan_price
        item['cha'] = cha
        item['cha_price'] = cha_price
        item['product_price'] = product_price
        total_cheng += product_price
        total_amount += item['amount']


    paginator = Paginator(qs, 1000)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result,
        'total_amount': total_amount,
        'total_price': total_cheng,
        'cha_price': cha_price,

    }
    return render(request, 'inbound/bd.html', context)
