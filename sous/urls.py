from django.urls import path

from . import views

app_name = 'sous'
urlpatterns = [
    path('', views.customer_list_view,name='index'),
    path('ranking', views.ranking,name='ranking'),
    path('qsss', views.qsss, name='qsss'),
    path('search', views.search, name='search'),
    path('huafei', views.huafei, name='huafei'),

]