from django.urls import path
from . import views

APP_NAME = 'StockWatch'

urlpatterns = [
    path('', views.home, name="list"),
    path('insertgtin/', views.insert_gtin, name="insertgtin"),
    path('query', views.srch_gtin, name="srchgtin"),#TODO add dynamic URL to the search (srchgtin/<int: gtin>/ for ex)
    path('home_link/', views.home_link, name='homelink')
]