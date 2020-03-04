from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('extern',views.extern,name='extern'),
    path('test',views.test,name='test')
]