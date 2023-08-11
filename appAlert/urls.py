from django.urls import path
from . import views

urlpatterns = [
                #   path('send_notifications/', views.sendNotifications, name='send_notifications'),
                #   path('send_push/', views.send_push, name='send_push'),
                    path('test_send/', views.test_send, name='test_send'),
                    
                    path('register_token/', views.register_token, name='register_token'),
              ] 
