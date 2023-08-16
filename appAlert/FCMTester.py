from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import FCMUserTokens
from rest_framework.permissions import AllowAny


def test_send(request):
    model_instance = FCMUserTokens()
    response_data = model_instance.send_notification('pharmaco-net.org', 'Simulation Completed. You can view the results now.', 'https://imgtr.ee/images/2023/08/15/44d1375ec2f1260a80f1d56b88a346be.jpeg')
    return JsonResponse(response_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_token(request):
    token = request.data.get('token')
    
    if not token:
        return Response({"detail": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user is authenticated and get or create the appropriate FCMUserTokens instance
    if request.user.is_authenticated:
        model_instance, _ = FCMUserTokens.objects.get_or_create(user=request.user)
    else:
        model_instance, _ = FCMUserTokens.objects.get_or_create(name="unauthenticated")
    
    model_instance.subscribe(token)

    return Response({"detail": "Token registered successfully."}, status=status.HTTP_201_CREATED)
@api_view(['POST'])
@permission_classes([AllowAny])
def unsubscribe(request):
    device_id = request.data.get('device_id')
    
    if not device_id:
        return Response({"detail": "No device_id provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user is authenticated and get the appropriate FCMUserTokens instance
    if request.user.is_authenticated:
        model_instance = FCMUserTokens.objects.get(user=request.user)
    else:
        model_instance = FCMUserTokens.objects.get(name="unauthenticated")
    
    model_instance.unsubscribe(device_id)

    return Response({"detail": "Device unsubscribed successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def unsubscribe_all(request):
    
    # Check if the user is authenticated and get the appropriate FCMUserTokens instance
    if request.user.is_authenticated:
        model_instance = FCMUserTokens.objects.get(user=request.user)
    else:
        model_instance = FCMUserTokens.objects.get(name="unauthenticated")
    
    model_instance.unsubscribe_all()

    return Response({"detail": "All devices unsubscribed successfully."}, status=status.HTTP_200_OK)