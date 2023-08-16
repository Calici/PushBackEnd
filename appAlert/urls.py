from django.urls import path
from . import FCMTester as views

urlpatterns = [
                    path('test_send/', views.test_send, name='test_send'),
                    path('register_token/', views.register_token, name='register_token'),
                    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
                    path('unsubscribe_all/', views.unsubscribe_all, name='unsubscribe_all'),
              ] 
