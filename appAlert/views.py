# from django.shortcuts import render
# from appAlert import FCMManager
# from django.http.response import HttpResponse
# from pyfcm import FCMNotification
# from fcm_django.models import FCMDevice
from django.conf import settings
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, messaging
from fcm_nonitication import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import UserTokens
from rest_framework.permissions import AllowAny

cred = credentials.Certificate(settings.cred)
app= firebase_admin.initialize_app(cred)
def test_send(request):
    # This registration token comes from the client FCM SDKs.
    # Get tokens for unauthenticated users.
    unauthenticated_tokens_entry = UserTokens.objects.filter(name="unauthenticated").first()

    # If there is no entry for unauthenticated users or no tokens, return a message.
    if not unauthenticated_tokens_entry or not unauthenticated_tokens_entry.tokens:
        return JsonResponse({
            'message': 'No tokens available for unauthenticated users.'
        })

    registeration_tokens = unauthenticated_tokens_entry.tokens

    # Construct a list of messaging.Message objects
    messages = [
        messaging.Message(
            notification=messaging.Notification(
                title='Jowi/nur',
                body='are bullying me',
            ),
            token=token
        )
        for token in registeration_tokens
    ]
    
    # Send all messages in a single batch
    responses = messaging.send_all(messages)

    # You might want to loop through responses to see if any failed
    # and handle each response accordingly

    return JsonResponse({
        'message': 'Messages sent successfully.',
        
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_token(request):
    token = request.data.get('token')
    print('hale')
    if not token:
        return Response({"detail": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.is_authenticated:
        # If the user is authenticated, add the token to their list
        user_tokens_instance, created = UserTokens.objects.get_or_create(user=request.user, name=request.user)

    else:
        # If the user isn't authenticated, store under "unauthenticated"
        user_tokens_instance, created = UserTokens.objects.get_or_create(name="unauthenticated")

    # If the token is not already in the list, add it
    if token not in user_tokens_instance.tokens:
        user_tokens_instance.tokens.append(token)
        user_tokens_instance.save()

    return Response({"detail": "Token registered successfully."}, status=status.HTTP_201_CREATED)

# # Create your views here.
# def sendNotifications(request):
#     if request.method == 'GET':
#         title = "this is title"
#         desc = "this is description"
       
#         # image = notification_image.objects.all()
#         # # all token
#         # tokens = user_push_token.objects.all()
#         # all token array
#         #alltokens = ['eqo1b1RoTSiGBJ-anw90HW:APA91bEW-IFaaj9PrC2nTd0g7Kc5J3mrxPfP72LM4V_V09lZQ_g0uYVuQ0TU--NDrrrkhOI6OG6VoNW1M6DvgBeMeCldR2kMOrMNWawlZ2WddGy9zVFRyQbBr1Mj_K2nfK0wYbQzujzF']
#         # image
#         alltokens = []
#         push_img = {}
#         tokens = FCMDevice.objects.all()
#         print(tokens)
#         for tokenlist in tokens:
#             alltokens.append(tokenlist.registration_id)
#         print(alltokens)
#         # if image:
#         #     push_img = {'image': image[0].image.url}
#         FCMManager.sendPush(title, desc, alltokens, push_img)
        
#         return HttpResponse(request,'yes')
    
# def send_push(request):
#     title = "this is title"
#     desc = "this is description"
#     data_message = {
#                 "title": title,
#                 "body": desc,
#             }
#     push_service = FCMNotification(api_key=settings.FCM_API_KEY)
#     try:
#         tokens = 'e19ipXE1NYEk9s4A5TUPg9:APA91bFk4runBo34gvRqQMCFJL9eVRKQO7toveJ9s1GQFGEjcJxw8JV2DwpX0iVWn3kgDx202f-iXmV0mUOY8csl_uu38wap6itMyhkSLZ9XJkQfFGBbKMzZhX5rdrHsmuU-r5qlaHF7'
#         registration_ids = [tokens]
#         result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
#                                                                 data_message=data_message)
#         #FCMManager.test_send()
#         print(result)
#         return HttpResponse(request,'yes')
#     except Exception as e:
#         print(e)
#         return HttpResponse(request,'yes')
