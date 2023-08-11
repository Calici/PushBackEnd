import firebase_admin
from firebase_admin import credentials, messaging
from fcm_nonitication import settings


cred = credentials.Certificate(settings.cred)
firebase_admin.initialize_app(cred)

def sendPush(title, msg, registration_token, dataObject=None):
    dataObject = {'routeKey':"homework"}
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title,body=msg),
        data=dataObject,
        tokens=registration_token
    )
    response = messaging.send_multicast(message)
    print(message)
    print('successfully sent message', response)

def test_send():
    # This registration token comes from the client FCM SDKs.
    registration_token = 'e19ipXE1NYEk9s4A5TUPg9:APA91bFk4runBo34gvRqQMCFJL9eVRKQO7toveJ9s1GQFGEjcJxw8JV2DwpX0iVWn3kgDx202f-iXmV0mUOY8csl_uu38wap6itMyhkSLZ9XJkQfFGBbKMzZhX5rdrHsmuU-r5qlaHF7'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)