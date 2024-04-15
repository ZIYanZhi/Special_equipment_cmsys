from django.urls import path

from . import views
from .views import ChartView
app_name = 'charts'
urlpatterns = [
    path('charts/',ChartView.as_view(),name="charts"),


]

