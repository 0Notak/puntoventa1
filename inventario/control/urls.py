# control/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('reporte/', views.reporte_view, name='reporte'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('concentrado/', views.concentrado_view, name='concentrado')
]
