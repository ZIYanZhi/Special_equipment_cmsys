# 6th
from django.shortcuts import render, redirect  # 导入渲染和重定向函数
from django.contrib import messages  # 导入消息模块
from django.views.generic import ListView  # 导入列表视图类
from django.views.generic.edit import (  # 导入创建和更新视图类
    CreateView, UpdateView
)

from .forms import (  # 导入自定义表单
    VariantForm, VariantFormSet,
)
from common.models import (  # 导入自定义模型
    Outbound,
)


class ProductInline():  # 定义产品内联类
    form_class = VariantForm  # 表单类
    model = Outbound  # 模型类
    template_name = "products/product_create_or_update.html"  # 模板名称

    def form_valid(self, form):  # 处理表单验证通过的情况
        named_formsets = self.get_named_formsets()  # 获取命名的表单集合
        if not all((x.is_valid() for x in named_formsets.values())):  # 检查所有表单集合是否有效
            return self.render_to_response(self.get_context_data(form=form))  # 返回包含表单的响应

        self.object = form.save()  # 保存主表单

        # 对于每个表单集，尝试找到一个特定的表单集保存函数
        # 否则，就保存。
        # 遍历每个命名的表单集合，尝试调用特定的保存函数，否则直接保存表单集合
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('products:list_products')  # 重定向到产品列表页面

    def formset_variants_valid(self, formset):  # 处理变体表单集合保存的情况
        """
        用于保存自定义表单集的挂钩..如果有多个表单集，这很有用
        """
        variants = formset.save(commit=False)  # 保存变体表单集合  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        # 删除被标记为删除的对象
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.product = self.object  # 将产品与变体关联
            variant.save()  # 保存变体对象




class ProductCreate(ProductInline, CreateView):  # 创建产品视图类

    def get_context_data(self, **kwargs):  # 获取上下文数据
        ctx = super(ProductCreate, self).get_context_data(**kwargs)  # 调用父类的get_context_data方法获取上下文数据，并将其赋值给变量ctx
        ctx[
            'named_formsets'] = self.get_named_formsets()  # 将self.get_named_formsets()的结果赋值给上下文数据字典ctx的'named_formsets'键
        return ctx  # 返回包含上下文数据的字典ctx作为方法的返回值

    def get_named_formsets(self):  # 获取命名的表单集合
        if self.request.method == "GET":
            return {
                'variants': VariantFormSet(prefix='variants'),  # 创建变体表单集合

            }
        else:
            return {
                'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                # 创建变体表单集合


            }


class ProductUpdate(ProductInline, UpdateView):  # 更新产品视图类

    def get_context_data(self, **kwargs):  # 获取上下文数据
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):  # 获取命名的表单集合
        return {
            'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                       prefix='variants'),  # 创建变体表单集合

        }





def delete_variant(request, pk):  # 删除变体的视图函数
    try:
        variant = Outbound.objects.get(id=pk)  # 根据主键获取变体对象
    except Outbound.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'  # 变体对象不存在时显示消息
        )
        return redirect('products:update_product', pk=id)  # 重定向到产品更新页面

    variant.delete()  # 删除变体对象
    messages.success(
        request, 'Variant deleted successfully'  # 显示删除成功的消息
    )
    return redirect('products:update_product', pk=id)  # 重定向到产品更新页面


class ProductList(ListView):  # 产品列表视图类
    model = Outbound  # 模型类
    template_name = "products/product_list.html"  # 模板名称
    context_object_name = "products"  # 上下文对象名称
