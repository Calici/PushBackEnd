from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import FCMToken_Testing
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


def test_send(request):
    username='admin'
    user, created = User.objects.get_or_create(username=username)
    model_instance, _ = FCMToken_Testing.objects.get_or_create(user=user)

    # Assuming you have at least one instance for testing purposes
    if not model_instance.tokens:
        return JsonResponse({"detail": "No tokens."}, status=status.HTTP_400_BAD_REQUEST)
    
    model_instance.send_notification(
        'pharmaco-net.org',
        'Simulation Completed. You can view the results now.',
        'https://imgtr.ee/images/2023/08/15/44d1375ec2f1260a80f1d56b88a346be.jpeg'
    )
    
    return JsonResponse({"detail": "Notification sent successfully."})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_token(request):
    token = request.data.get('token')
    username = request.data.get('username')
   
    if not token:
        return Response({"detail": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    user, created = User.objects.get_or_create(username=username)
    model_instance, _ = FCMToken_Testing.objects.get_or_create(user=user)
    
    model_instance.unique_subscribe(token, True)

    return Response({"detail": "Token registered successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def unsubscribe(request):
    username='admin'
    device_id = request.data.get('device_id')
    if not device_id:
        return Response({"detail": "No device_id provided."}, status=status.HTTP_400_BAD_REQUEST)
    user, created = User.objects.get_or_create(username=username)
    
    # Check if the user is authenticated and get the appropriate FCMToken_Testing instance
    model_instance = FCMToken_Testing.objects.get(user=user)
    
    
    model_instance.unsubscribe(device_id, True)

    return Response({"detail": "Device unsubscribed successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def unsubscribe_all(request):
    username='admin'
    # Check if the user is authenticated and get the appropriate FCMToken_Testing instance
    user, created = User.objects.get_or_create(username=username)
    model_instance = FCMToken_Testing.objects.get(user=user)
    
    
    model_instance.unsubscribe_all(True)

    return Response({"detail": "All devices unsubscribed successfully."}, status=status.HTTP_200_OK)
