from django.shortcuts import render
from django.utils import timezone
from .models import Customer
from datetime import datetime

def customer_list_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        customers = Customer.objects.filter(outorder__outorderclothes__create_time__range=(start_date, end_date))
    else:
        customers = Customer.objects.all()

    customer_list = []
    amount_sum = 0
    amount_sum_dict = {}

    for customer in customers:
        d = {}
        if customer.outorder__clothes__name is not None:
            d['id'] = customer.id
            d['outorder__clothes__name'] = customer.outorder__clothes__name
            d['outorder__clothes__sn'] = customer.outorder__clothes__sn
            d['amount'] = customer.outorder__outorderclothes__amount
            d['price'] = customer.outorder__clothes__price
            d['address'] = customer.address
            d['outorderclothesid'] = customer.outorder__outorderclothes__id
            d['time'] = customer.outorder__outorderclothes__create_time
            if d not in customer_list:
                customer_list.append(d)

    customer_list = sorted(customer_list, key=lambda x: x['amount'], reverse=True)
    customer_list = customer_list[:10]
    amount_sum = sum(item['amount'] for item in customer_list)

    for item in customer_list:
        address = item['outorder__clothes__name']
        if address not in amount_sum_dict:
            amount_sum_dict[address] = item['amount']
        else:
            amount_sum_dict[address] += item['amount']

    context = {
        'customer_list': customer_list,
        'amount_sum': amount_sum,
        'amount_sum_dict': amount_sum_dict,
        'address': address
    }

    return render(request, 'sous/index.html', context)
