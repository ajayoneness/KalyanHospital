from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('signup',views.signup, name="signup"),
    path('logout',views.logout, name="logout"),
    #path('home',views.home, name="home"),
    path('opd',views.opd, name="opd"),
    path('opdbill/<int:idd>',views.opdbill, name="opdbill"),
    path('patients',views.patients, name="patients"),
    path('doctors',views.doctors, name="doctors"),

]
