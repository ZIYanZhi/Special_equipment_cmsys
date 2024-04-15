def add(request):
    if request.method == "POST":
        outorder_form = OutorderForm(request.POST)
        outorderclothes_form= OutorderClothesForm(request.POST)
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
            'outorder_form': outorder_form
        }
        return render(request, 'outorder/add.html', context)