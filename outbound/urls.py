from django.urls import path

from . import views
from outbound.views import download,line_chart_view


app_name = 'outbound'
urlpatterns = [
    path('', views.list, name='index'),
    path('add/', views.add, name='add'),
    path('search/', views.search, name='search'),
    path('update/<int:outbound_id>/', views.update, name='update'),
    path('delete/<int:outbound_id>/', views.delete, name='delete'),
    path('detail/<int:outbound_id>/', views.detail, name='detail'),
    path('test/', views.test, name='test'),
    path('biao/', views.your_view_function, name='biao'),
    path('download/', download, name='download'),
    path('chart/', line_chart_view, name='chart'),
    path('zdlist', views.zdlist, name='zdlist'),
    path('zdsearch/', views.zdsearch, name='zdsearch'),

]