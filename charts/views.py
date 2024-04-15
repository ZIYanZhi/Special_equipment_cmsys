import hashlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum , F,Q

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from common import models
from common.forms import LoginForm, RegisterForm, ChangepwdForm
from common.models import User, Outbound
from common.models import Outorder, Customer, Clothes, OutorderClothes
from datetime import datetime, timedelta


class ChartView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        top_5_book = Outbound.objects.order_by('-amount')[:5].values_list('clothes__name', 'amount')
        print('排5：', top_5_book)
        top_5_book_titles = [b[0] for b in top_5_book]
        print(top_5_book_titles)

        top_5_book_quantities = [b[1] for b in top_5_book]
        print(top_5_book_quantities)

        context = {
            'top_5_book_titles': top_5_book_titles,
            'top_5_book_quantities': top_5_book_quantities
        }

        return HttpResponseRedirect('/charts/charts/')