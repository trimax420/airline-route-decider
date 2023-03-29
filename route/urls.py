from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('airport/',views.airport,name='airport'),
    path('demand/',views.demand,name='demand'),
    path('distance/',views.distance,name='distance')
]