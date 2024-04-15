import os
import django
import json

from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmsys.settings")  # MB：项目名称
django.setup()  # 这一步就加载了Django环境

# 必须是django.setup()之后，才能引入模型类
from common.models import Outorder, Customer, Clothes, OutorderClothes,Inorder,InorderClothes

def foo():
    filters = Q()
    qs2 = InorderClothes.objects.filter(filters).values(
        'inorder_id',
        'inorder__clothes__name',
        'inorder__clothes__sn',
        'inorder__clothes__price',
        'inorder__inorderclothes__amount',

    )
    print(qs2)

if __name__ == '__main__':
    foo()

def add(request):
    if request.method == "POST":
        outbound_form = OutboundForm(request.POST)
        time = request.POST.get('start_time')
        if outbound_form.is_valid():
            costomer = outbound_form.cleaned_data['customer']
            uid = request.session.get('user_id')
            user = User.objects.get(id=uid)
            now = datetime.now().strftime('%Y%m%d%H%M')
            code = 'OUT' + now
            name = outbound_form.cleaned_data['name']
            clothes = outbound_form.cleaned_data['clothes']
            amount = outbound_form.cleaned_data['amount']
            print(time)
            if time:
                with transaction.atomic():  # 事务
                    # 库存足够才成功
                    if clothes.stock >= amount:
                        # 出库减少库存
                        clothes.stock -= amount
                        clothes.save()

                        new_outbound = Outbound.objects.create(code=code,
                                                   customer=costomer,
                                                   user=user,
                                                   name=name,
                                                   clothes=clothes,
                                                   amount=amount,create_time= timezone.datetime.strptime(time, '%Y-%m-%d'))
                        print(new_outbound.create_time)
                        context = {
                            'id': new_outbound.id
                        }
                        messages.add_message(request, messages.SUCCESS, '添加成功')
                        return redirect(reverse('outbound:index', ))

                    else:
                        context = {
                            'outbound_form': outbound_form
                        }
                        messages.add_message(request, messages.WARNING, '请检查填写的内容')
                        return render(request, 'outbound/add.html', context)
            else:
                with transaction.atomic():  # 事务
                    # 库存足够才成功
                    if clothes.stock >= amount:
                        # 出库减少库存
                        clothes.stock -= amount
                        clothes.save()
                        new_outbound = Outbound.objects.create(code=code,
                                                               customer=costomer,
                                                               user=user,
                                                               name=name,
                                                               clothes=clothes,
                                                               amount=amount,
                                                               )
                        context = {
                            'id': new_outbound.id
                        }
                        messages.add_message(request, messages.SUCCESS, '添加成功')
                        return redirect(reverse('outbound:index'))

                    else:
                        context = {
                            'outorder_form': outbound_form,

                        }
                        messages.add_message(request, messages.WARNING, '添加失败，库存不足')
                        return render(request, 'outbound/add.html', context)

    else:
        outorder_form = OutboundForm()

        context = {
            'outorder_form': outorder_form,

        }
        return render(request, 'outbound/add.html', context)
