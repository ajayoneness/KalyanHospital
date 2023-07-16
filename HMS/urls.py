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
    path('lab',views.lab, name="lab"),
    path('lab_search',views.lab_search_api, name="labsearch"),
    path('patient_lab',views.patient_lab_api, name="patientlab"),
    path('testbill',views.testBill, name="testbill"),
    path('labresult',views.labresult, name="labresult"),

]
