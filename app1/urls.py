from django.urls import path
from . import views
urlpatterns=[
    path('index/',views.index,name='index'),
    path('testing/',views.testing,name='testing'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('destination/',views.destination,name='destination'),
    path('form/',views.form,name='form'),
]
