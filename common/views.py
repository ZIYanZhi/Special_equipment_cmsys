import hashlib
import json

from django.contrib import messages
from django.db.models import Sum , F,Q

from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from common import models
from common.forms import LoginForm, RegisterForm, ChangepwdForm
from common.models import User, Outbound
from common.models import Outorder, Customer, Clothes, OutorderClothes



from django.utils import timezone
from datetime import datetime, timedelta
def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_role'] = user.role
                    return redirect(reverse('index'))
                else:
                    messages.add_message(request, messages.WARNING, '密码不正确')
            except User.DoesNotExist:
                messages.add_message(request, messages.WARNING, '用户不存在')
        return render(request, 'login.html', locals())
    login_form = LoginForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            if password1 != password2:  # 判断两次密码是否相同
                messages.add_message(request, messages.WARNING, '两次输入的密码不同')
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    messages.add_message(request, messages.WARNING, '用户已存在，请重新选择用户名')
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create(username=username,
                                                      password=hash_code(password1),
                                                      name=name)
                new_user.save()
                messages.add_message(request, messages.SUCCESS, '注册成功')
                return redirect(reverse('login'))  # 自动跳转到登录界面
        else:
            messages.add_message(request, messages.WARNING, '格式错误或验证码错误')
            register_form = RegisterForm()
            return render(request, 'register.html', locals())
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有注销一说
        return redirect(reverse(reverse('index')))
    request.session.flush()
    return redirect(reverse('index'))


def changepwd(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('index'))
    user = User.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        changepwd_form = ChangepwdForm(request.POST)
        if changepwd_form.is_valid():
            password_now = changepwd_form.cleaned_data['password_now']
            print(hash_code(password_now))
            password1 = changepwd_form.cleaned_data['password1']
            print(password1)
            password2 = changepwd_form.cleaned_data['password2']
            print(password2)

            if hash_code(password_now) == user.password:
                if password1 == password2:
                    user.password = hash_code(password1)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, '修改成功')
                    return redirect(reverse('index'))
                else:
                    context = {
                        'changepwd_form': changepwd_form
                    }
                    messages.add_message(request, messages.WARNING, '两次输入的密码不一致')
                    return render(request, 'changepwd.html', context)
            else:
                context = {
                    'changepwd_form': changepwd_form
                }
                messages.add_message(request, messages.WARNING, '原密码不正确')
                return render(request, 'changepwd.html', context)
        else:
            context = {
                'changepwd_form': changepwd_form
            }
            messages.add_message(request, messages.WARNING, '请检查填写的内容')
            return render(request, 'changepwd.html', context)
    else:
        changepwd_form = ChangepwdForm()
        context = {
            'changepwd_form': changepwd_form,
        }
        return render(request, 'changepwd.html', context)


def checkusername(request, username):
    same_name_user = User.objects.filter(username=username)
    if not same_name_user:
        return JsonResponse({'ret': 0, 'msg': '用户名可使用'})
    return JsonResponse({'ret': 1, 'msg': '用户名已存在'})


def hash_code(s, salt='psf'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接受bytes类型
    return h.hexdigest()

def chart_list(request):
    """ 数据统计页面 """
    top_5_book = Outbound.objects.order_by('-amount')[:5].values_list('clothes__name', 'amount')
    print('排5：', top_5_book)
    top_5_book_titles = [b[0] for b in top_5_book]
    print(top_5_book_titles)

    top_5_book__quantities = [b[1] for b in top_5_book]
    print(top_5_book__quantities)

    total_price = Clothes.objects.aggregate(
        total=Sum(F('price') * F('stock'), ))['total']
    total_price = total_price if total_price else 0
    total_price ='%.2f' % total_price
    print(total_price)

    context={
        'total_price':total_price
    }
    return render(request, 'chart_list.html',context)


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 获取当前日期
    current_date = timezone.now().date()

    # 创建一个列表来存储每个月的消耗总价
    monthly_totals = []

    # 循环遍历过去12个月的日期
    for i in range(1, 13):
        # 计算每个月的起始日期和结束日期
        month = current_date.month - i
        year = current_date.year

        # 处理月份小于1的情况
        if month <= 0:
            month += 12
            year -= 1

        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, month=month % 12 + 1, year=year) - timedelta(days=1)

        # 计算每个月的消耗总价
        monthly_total = \
        Outbound.objects.filter(create_time__range=(start_date, end_date)).aggregate(total=Sum('clothes__price'))[
            'total']
        monthly_totals.append(monthly_total or 0)  # 如果没有消耗数据，则将总价设为0

    # 将 monthly_totals 转换为字符串
    monthly_totals_str = [str(total) for total in monthly_totals]


    # 数据可以去数据库中获取
    legend = ["2024年", "2023年"]
    series_list = [
        {
            "name": '2024年',
            "type": 'bar',
            "data": monthly_totals_str
        },
        {
            "name": '2023年',
            "type": 'bar',
            "data": []
        }

    ]
    x_axis = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']

    for i in range(1, 13):
        start_date = datetime(2023, i, 1)
        end_date = start_date.replace(day=1, month=i % 12 + 1, year=2023) - timedelta(days=1)

        monthly_total = \
        Outbound.objects.filter(create_time__range=(start_date, end_date)).aggregate(total=Sum('clothes__price'))[
            'total']
        series_list[1]['data'].append(str(monthly_total) if monthly_total is not None else '0')

        # 计算2022年每个月的消耗数据

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {"value": 2048, "name": '前纺'},
        {"value": 1735, "name": '细纱'},
        {"value": 580, "name": '后纺'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    # 获取当前日期
    current_date = timezone.now().date()

    # 创建一个列表来存储每个月的消耗总价
    monthly_totals = []

    # 循环遍历过去12个月的日期
    for i in range(1, 13):
        # 计算每个月的起始日期和结束日期
        month = current_date.month - i
        year = current_date.year

        # 处理月份小于1的情况
        if month <= 0:
            month += 12
            year -= 1

        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, month=month % 12 + 1, year=year) - timedelta(days=1)

        # 计算每个月的消耗总价
        monthly_total = Outbound.objects.filter(create_time__range=(start_date, end_date)).aggregate(
            total=Sum(F('clothes__price') * F('amount')))['total']
        monthly_totals.append(monthly_total or 0)  # 如果没有消耗数据，则将总价设为0

    # 将 monthly_totals 转换为字符串
    monthly_totals_str = [str(total) for total in monthly_totals]

    legend = ["2024年", "2023年","2022年"]
    series_list = [
        {
            "name": '2024年',
            "type": 'line',

            "data": monthly_totals_str
        },
        {
            "name": '2023年',
            "type": 'line',

            "data": []
        },
        {
            "name": '2022年',
            "type": 'line',

            "data": []
        },
    ]
    x_axis = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
    for i in range(1, 13):
        start_date = datetime(2023, i, 1)
        end_date = start_date.replace(day=1, month=(i % 12) + 1, year=2023) - timedelta(days=1)

        monthly_total = Outbound.objects.filter(create_time__range=(start_date, end_date)).aggregate(
            total=Sum(F('clothes__price') * F('amount')))['total']
        series_list[1]['data'].append(str(monthly_total) if monthly_total is not None else '0')

        # 计算2022年每个月的消耗数据
    for i in range(1, 13):
        start_date = datetime(2022, i, 1)
        end_date = start_date.replace(day=1, month=i % 12 + 1, year=2022) - timedelta(days=1)

        monthly_total = Outbound.objects.filter(create_time__range=(start_date, end_date)).aggregate(
            total=Sum(F('clothes__price') * F('amount')))['total']
        series_list[2]['data'].append(str(monthly_total) if monthly_total is not None else '0')

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)

def foo(request):


    return render(request, 'chart_list.html')