import datetime
import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction, DataError
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

# Create your views here.
from common.models import Outorder, OutorderClothes, User, Customer,Clothes,Man
from outorder.forms import OutorderForm, OutorderClothesForm, EditmoreForm


def list(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录

    qs = Outorder.objects.all()
    # 取值
    articles = Outorder.objects.values('id')
    outorder_clothes_list = []
    print(articles)
    for article in articles:
        print('id',article['id'])
        qs2 = OutorderClothes.objects.filter(outorder_id=article['id'])
        outorder_clothes_list += qs2
        print("3",qs2)
    sum = 0
    shuliang = 0
    for foo in outorder_clothes_list:
        sum += foo.clothes.price * foo.amount
        shuliang += foo.amount
    print(sum)
    print(shuliang)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {

        'sum': sum,
        'shuliang': shuliang,
        'result': result
    }

    return render(request, 'outorder/index.html', context)


def add(request):
    if request.method == "POST":
        outorder_form = OutorderForm(request.POST)

        if outorder_form.is_valid():
            costomer = outorder_form.cleaned_data['customer']
            uid = request.session.get('user_id')
            user = User.objects.get(id=uid)
            now = datetime.datetime.now().strftime('%Y%m%d%H%M')
            code = 'OUT' + now + str(random.randint(10000, 99999))



            new_outorder = Outorder.objects.create(code=code,
                                                   customer=costomer,
                                                   user=user,)

            context = {
                'id': new_outorder.id
            }
            messages.add_message(request, messages.SUCCESS, '添加成功')
            return redirect(reverse('outorder:detail', args={new_outorder.id}))

        else:
            context = {
                'outorder_form': outorder_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'outorder/add.html', context)


    else:
        outorder_form = OutorderForm()

        context = {
            'outorder_form': outorder_form,

        }
        return render(request, 'outorder/add.html', context)


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


def update(request, outorder_id):
    outorder = Outorder.objects.get(id=outorder_id)
    qs = OutorderClothes.objects.filter(outorder_id=outorder_id)

    if request.method == "POST":
        outorder_form = OutorderForm(request.POST)
        if outorder_form.is_valid():
            customer = outorder_form.cleaned_data['customer']
            user = outorder_form.cleaned_data['user']
            create_time = outorder_form.cleaned_data['create_time']


            if customer:
                outorder.customer = customer
            if create_time:
                outorder.create_time = create_time
            if user:
                outorder.user = user


            outorder.save()
            context = {
                'outorder_id': outorder_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('outorder:index'))

        else:
            context = {
                'outorder_form': outorder_form,
                'qs': qs
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'outorder/edit.html', context)
    else:
        outorder_form = OutorderForm({'id': outorder.id,
                                      'code': outorder.code,
                                      'customer': outorder.customer,
                                      'user': outorder.user,
                                      'create_time': outorder.create_time})
        context = {
            'outorder_form': outorder_form,
            'outorder_id': outorder_id,
            'qs': qs
        }
        return render(request, 'outorder/edit.html', context)


def delete(request, outorder_id):
    qs = OutorderClothes.objects.filter(outorder_id=outorder_id)
    if qs:
        messages.add_message(request, messages.WARNING, '删除失败，请先删除该订单下的商品')
        return redirect(reverse('outorder:detail', args={outorder_id}))
    outorder = Outorder.objects.get(id=outorder_id)
    outorder.delete()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('outorder:index'))


def detail(request, outorder_id):

    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs1 = Outorder.objects.filter(id=outorder_id)
    qs2 = OutorderClothes.objects.filter(outorder_id=outorder_id)


    sum = 0
    shuliang = 0
    for foo in qs2:
        sum += foo.clothes.price * foo.amount
        shuliang += foo.amount

    context = {
        'qs1': qs1,
        'qs2': qs2,
        'sum': sum,
        'shuliang':shuliang,
        'outorder_id': outorder_id
    }
    return render(request, 'outorder/detail.html', context)

def addmore(request, outorder_id):
    if request.method == "POST":
        time = request.POST.get('start_time')
        print('时间',time)
        outorderclothes_form = OutorderClothesForm(request.POST)
        if outorderclothes_form.is_valid():
            clothes = outorderclothes_form.cleaned_data['clothes']
            amount = outorderclothes_form.cleaned_data['amount']
            name = outorderclothes_form.cleaned_data['name']


            if time:
                with transaction.atomic():  # 事务
                    # 库存足够才成功
                    if clothes.stock >= amount:
                        # 出库减少库存
                        clothes.stock -= amount
                        clothes.save()
                        new_outorderclothes = OutorderClothes.objects.create(clothes=clothes,outorder_id=outorder_id,amount=amount,name=name,create_time=timezone.datetime.strptime(time, '%Y-%m-%d'))
                        print('时间查看',new_outorderclothes)
                        context = {
                            'id': new_outorderclothes.id
                        }
                        messages.add_message(request, messages.SUCCESS, '添加成功')
                        return redirect(reverse('outorder:detail', args={outorder_id}))

                    else:
                        context = {
                            'outorderclothes_form': outorderclothes_form,
                            'outorder_id': outorder_id
                        }
                        messages.add_message(request, messages.WARNING, '添加失败，库存不足')
                        return render(request, 'outorder/addmore.html', context)
            else:
                with transaction.atomic():  # 事务
                    # 库存足够才成功
                    if clothes.stock >= amount:
                        # 出库减少库存
                        clothes.stock -= amount
                        clothes.save()
                        new_outorderclothes = OutorderClothes.objects.create(clothes=clothes, outorder_id=outorder_id,
                                                                             amount=amount, name=name)
                        context = {
                            'id': new_outorderclothes.id
                        }
                        messages.add_message(request, messages.SUCCESS, '添加成功')
                        return redirect(reverse('outorder:detail', args={outorder_id}))

                    else:
                        context = {
                            'outorderclothes_form': outorderclothes_form,
                            'outorder_id': outorder_id
                        }
                        messages.add_message(request, messages.WARNING, '添加失败，库存不足')
                        return render(request, 'outorder/addmore.html', context)
        else:
            context = {
                'outorderclothes_form': outorderclothes_form,
                'outorder_id': outorder_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'outorder/addmore.html', context)
    else:
        outorderclothes_form = OutorderClothesForm()
        shuju = Clothes.objects.all()
        context = {
            'outorderclothes_form': outorderclothes_form,
            'outorder_id': outorder_id,
            'shuju': shuju,
        }
        return render(request, 'outorder/addmore.html', context)


def asmore(request, outorder_id):
    if request.method == "POST":
        shuju = Clothes.objects.all()
        outorderclothes_form = OutorderClothesForm(request.POST)
        if outorderclothes_form.is_valid():
            clothes = outorderclothes_form.cleaned_data['clothes']
            amount = outorderclothes_form.cleaned_data['amount']
            name = outorderclothes_form.cleaned_data['name']
            create_time = outorderclothes_form.cleaned_data['create_time']
            now = datetime.datetime.now().strftime('%Y%m%d%H%M')

            with transaction.atomic():  # 事务
                # 库存足够才成功
                if clothes.stock >= amount:
                    # 出库减少库存
                    clothes.stock -= amount
                    clothes.save()
                    new_outorderclothes = OutorderClothes.objects.create(clothes=clothes, outorder_id=outorder_id, amount=amount,name=name,
 )
                    context = {
                        'id': new_outorderclothes.id
                    }
                    messages.add_message(request, messages.SUCCESS, '添加成功')
                    return redirect(reverse('outorder:detail', args={outorder_id}))

                else:
                    context = {
                        'outorderclothes_form': outorderclothes_form,
                        'outorder_id': outorder_id
                    }
                    messages.add_message(request, messages.WARNING, '添加失败，库存不足')
                    return render(request, 'outorder/addmore.html', context)

        else:
            context = {
                'outorderclothes_form': outorderclothes_form,
                'outorder_id': outorder_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'outorder/addmore.html', context)
    else:
        outorderclothes_form = OutorderClothesForm()
        shuju = Clothes.objects.all()
        context = {
            'outorderclothes_form': outorderclothes_form,
            'outorder_id': outorder_id,
            'shuju': shuju,
        }
        return render(request, 'outorder/addmore.html', context)


def editmore(request, outorder_id, outorderclothes_id):
    outorderclothes = OutorderClothes.objects.get(id=outorderclothes_id)

    if request.method == "POST":
        editmore_form = EditmoreForm(request.POST)
        if editmore_form.is_valid():
            # clothes = editmore_form.cleaned_data['clothes']
            amount = editmore_form.cleaned_data['amount']
            name = editmore_form.cleaned_data['name']
            create_time = editmore_form.cleaned_data['create_time']

            del_amount = amount - outorderclothes.amount
            print('删除',del_amount)
            if del_amount <= outorderclothes.clothes.stock:
                with transaction.atomic():
                    outorderclothes.amount = amount
                    outorderclothes.clothes.stock -= del_amount
                    if create_time:
                        outorderclothes.create_time = create_time
                    if name:
                        outorderclothes.name = name

                    outorderclothes.save()
                    outorderclothes.clothes.save()



                context = {
                    'outorderclothes_id': outorderclothes_id
                }
                messages.add_message(request, messages.SUCCESS, '修改成功')
                return redirect(reverse('outorder:detail', args={outorder_id}))
            else:
                messages.add_message(request, messages.WARNING, '修改失败，库存不足')
                return redirect(reverse('outorder:detail', args={outorder_id}))
        else:
            context = {
                'editmore_form': editmore_form,
                'outorder_id': outorder_id,
                'outorderclothes_id': outorderclothes_id
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'outorder/editmore.html', context)
    else:
        editmore_form = EditmoreForm({'clothes': outorderclothes.clothes,
                                      'amount': outorderclothes.amount,
                                      'name': outorderclothes.name,
                                      'create_time': outorderclothes.create_time,
                                      })
        context = {
            'editmore_form': editmore_form,
            'outorder_id': outorder_id,
            'outorderclothes_id': outorderclothes_id
        }
        return render(request, 'outorder/editmore.html', context)


def deletemore(request, outorder_id, outorderclothes_id):
    outorderclothes = OutorderClothes.objects.get(id=outorderclothes_id)
    with transaction.atomic():
        outorderclothes.delete()
        outorderclothes.clothes.stock += outorderclothes.amount
        outorderclothes.clothes.save()
        messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('outorder:detail', args={outorder_id}))


from django.http.response import HttpResponse
def test(request):
    # 输入车号，获取本机台机件应用情况。
    address = '03#'
    obj = Outorder.objects.filter(customer__address=address)
    print(obj)





    return HttpResponse("OK")