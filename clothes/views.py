from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from clothes.forms import ClothesForm
from common.models import Clothes




def list(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    order = request.GET.get('order')  # 获取排序参数
    qs = Clothes.objects.all()

    if order == 'asc':
        qs = qs.order_by('stock')  # 按照库存正序排序
    elif order == 'desc':
        qs = qs.order_by('-stock')  # 按照库存倒序排序




    short = [] # 声明一个空列表，用于存储库存不足的商品名字
    print(short)
    for foo in qs:
        if foo.stock < foo.stock_down:
            short.append(foo.name)
    if short: # 只有当 short 列表不为空时，才会显示库存不足的消息
        short_str = '、'.join(short)
        messages.add_message(request, messages.WARNING, f'{str(short_str)}库存不足')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)

    context = {

        'result': result,
    }
    return render(request, 'clothes/index.html', context)


def add(request):
    if request.method == "POST":
        clothes_form = ClothesForm(request.POST)

        if clothes_form.is_valid():
            name = clothes_form.cleaned_data['name']
            sn = clothes_form.cleaned_data['sn']
            price = clothes_form.cleaned_data['price']
            danwei = clothes_form.cleaned_data['danwei']
            lei = clothes_form.cleaned_data['lei']
            stock = clothes_form.cleaned_data['stock']
            stock_down = clothes_form.cleaned_data['stock_down']
            changjia = clothes_form.cleaned_data['changjia']
            desc = clothes_form.cleaned_data['desc']

            new_clothes = Clothes.objects.create(name=name,
                                                 sn=sn,
                                                 price=price,
                                                 danwei=danwei,
                                                 lei=lei,
                                                 stock=stock,
                                                 stock_down=stock_down,
                                                 changjia=changjia,
                                                 desc=desc)
            context = {
                'id': new_clothes.id,
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect('/clothes/')

        else:
            context = {
                'clothes_form': clothes_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'clothes/add.html', context)
    else:
        clothes_form = ClothesForm()
        context = {
            'clothes_form': clothes_form
        }
        return render(request, 'clothes/add.html', context)


def search(request):
    object = Clothes.objects
    qs = object.values()
    id = request.POST.get('id')
    name = request.POST.get('name')
    sn = request.POST.get('sn')
    min = request.POST.get('min')
    max = request.POST.get('max')
    lei= request.POST.get('lei')
    danwei = request.POST.get('danwei')
    if id:
        qs = object.filter(id=id)
    if name:
        qs = object.filter(name=name)
    if sn:
        qs = object.filter(sn=sn)
    if min:
        qs = object.filter(price__gte=min)
    if max:
        qs = object.filter(price__lte=max)
    if lei:
        qs = object.filter(lei=lei)
    if danwei:
        qs = object.filter(color=danwei)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result
    }
    messages.add_message(request, messages.SUCCESS, '查询成功')
    return render(request, 'clothes/index.html', context)


def update(request, clothes_id):
    clothes = Clothes.objects.get(id=clothes_id)

    if request.method == "POST":
        clothes_form = ClothesForm(request.POST)
        if clothes_form.is_valid():
            name = clothes_form.cleaned_data['name']
            sn = clothes_form.cleaned_data['sn']
            price = clothes_form.cleaned_data['price']
            lei = clothes_form.cleaned_data['lei']
            danwei = clothes_form.cleaned_data['danwei']
            stock = clothes_form.cleaned_data['stock']
            stock_down = clothes_form.cleaned_data['stock_down']
            desc = clothes_form.cleaned_data['desc']

            if name:
                clothes.name = name
            if sn:
                clothes.sn = sn
            if price:
                clothes.price = price
            if lei:
                clothes.lei = lei
            if danwei:
                clothes.danwei = danwei

            if stock:
                clothes.stock = stock
            if stock_down:
                clothes.stock_down = stock_down
            if desc:
                clothes.desc = desc

            clothes.save()

            context = {
                'clothes_id': clothes_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('clothes:index'))
        else:
            context = {
                'clothes_form': clothes_form,
                'clothes_id': clothes_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'clothes/edit.html', context)
    else:
        clothes_form = ClothesForm({'id': clothes.id,
                                    'name': clothes.name,
                                    'sn': clothes.sn,
                                    'price': clothes.price,
                                    'lei': clothes.lei,
                                    'danwei': clothes.danwei,
                                    'stock': clothes.stock,
                                    'stock_down': clothes.stock_down,
                                    'desc': clothes.desc})
        print(clothes_form)
        context = {
            'clothes_form': clothes_form,
            'clothes_id': clothes_id
        }

        return render(request, 'clothes/edit.html', context)


def delete(request, clothes_id):
    clothes = Clothes.objects.get(id=clothes_id)
    clothes.delete()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('clothes:index'))


def checkstock(request, clothes_id):
    clothes = Clothes.objects.get(id=clothes_id)
    return JsonResponse({'stock': clothes.stock,'price':clothes.price,'id':clothes.id})

