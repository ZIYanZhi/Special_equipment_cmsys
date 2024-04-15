from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from common.models import Man
from man.forms import ManForm


def list(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Man.objects.all()
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result
    }
    return render(request, 'man/index.html', context)


def add(request):
    if request.method == "POST":
        customer_form = ManForm(request.POST)
        if customer_form.is_valid():
            name = customer_form.cleaned_data['name']


            new_customer = Man.objects.create(name=name,
                                                   )
            context = {
                'id': new_customer.id
            }
            messages.add_message(request, messages.WARNING, '添加成功')
            return redirect(reverse('man:index'))

        else:
            context = {
                'customer_form': customer_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'man/add.html', context)
    else:
        customer_form = ManForm()
        context = {
            'customer_form': customer_form
        }
        return render(request, 'man/add.html', context)


def search(request):
    object = Man.objects
    qs = object.values()
    id = request.POST.get('id')
    name = request.POST.get('name')

    if id:
        qs = object.filter(id=id)
    if name:
        qs = object.filter(name=name)

    paginator = Paginator(qs, 10)
    page = request.GET.get('page', '1')
    result = paginator.page(page)
    context = {
        'result': result
    }
    messages.add_message(request, messages.SUCCESS, '查询成功')
    return render(request, 'man/index.html', context)


def update(request, man_id):
    man = Man.objects.get(id=man_id)

    if request.method == "POST":
        man_form = ManForm(request.POST)
        if man_form.is_valid():
            name = man_form.cleaned_data['name']

            if name:
                man.name = name

            man.save()
            context = {
                'man_id': man_id
            }
            messages.add_message(request, messages.SUCCESS, '修改成功')
            return redirect(reverse('man:index'))
        else:
            context = {
                'man_form': man_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'man/edit.html', context)
    else:
        man_form = ManForm({'id': man.id,
                            'name': man.name,

                            })
        context = {
            'man_form': man_form,
            'man_id': man_id
        }
        return render(request, 'man/edit.html', context)


def delete(request, man_id):
    customer = Man.objects.get(id=man_id)
    customer.delete()
    messages.add_message(request, messages.SUCCESS, '删除成功')
    return redirect(reverse('man:index'))

