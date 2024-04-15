from django.urls import path

from . import views

app_name = 'inbound'
urlpatterns = [
    path('', views.list, name='index'),
    path('add', views.add, name='add'),
    path('bd', views.bd, name='bd'),
    path('search', views.search, name='search'),
    path('update/<int:inbound_id>', views.update, name='update'),
    path('delete/<int:inbound_id>', views.delete, name='delete'),
    path('detail/<int:inbound_id>', views.detail, name='detail'),

]

