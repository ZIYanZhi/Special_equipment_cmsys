from django.urls import path

from . import views

app_name = 'man'
urlpatterns = [
    path('', views.list, name='index'),
    path('add', views.add, name='add'),
    path('search', views.search, name='search'),
    path('update/<int:man_id>', views.update, name='update'),
    path('delete/<int:man_id>', views.delete, name='delete'),

]