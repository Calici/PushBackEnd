from django.db import models
from typing import Generic, TypeVar


T = TypeVar('T', bound=models.Model)
class UserTokens(models.Model, Generic[T]):
    user: models.OneToOneField = models.OneToOneField(
        'self', 
        on_delete=models.CASCADE, 
        related_name='fcm_tokens', 
        null=True, 
        blank=True
    )
    name: models.CharField = models.CharField(max_length=100, default="unauthenticated")
    tokens = models.JSONField(default=list)

    from firebase_admin import credentials, messaging
    from fcm_nonitication import settings
    import firebase_admin
    cred = credentials.Certificate(settings.cred)
    app = firebase_admin.initialize_app(cred)
    def subscribe(self, device_id: str):
        if self.user:
            # Check if the user for this instance is set. If so, it's an authenticated token.
            user_tokens_instance, created = FCMUserTokens.objects.get_or_create(user=self.user)
        else:
            # If not, then it's an unauthenticated token.
            user_tokens_instance, created = FCMUserTokens.objects.get_or_create(name="unauthenticated")

        if device_id not in user_tokens_instance.tokens:
            user_tokens_instance.tokens.append(device_id)
            user_tokens_instance.save()

    def unsubscribe(self, device_id: str):
        """
        Unsubscribe a specific device (remove the token) from the instance.
        """
        # Ensure that the instance is retrieved from the database.
        if self.user:
            user_tokens_instance = FCMUserTokens.objects.get(user=self.user)
        else:
            user_tokens_instance = FCMUserTokens.objects.get(name="unauthenticated")

        # If the device_id exists in the tokens, remove it and save.
        if device_id in user_tokens_instance.tokens:
            user_tokens_instance.tokens.remove(device_id)
            user_tokens_instance.save()

    def unsubscribe_all(self):
        """
        Unsubscribe all devices (clear all tokens) from the instance.
        """
        # Ensure that the instance is retrieved from the database.
        if self.user:
            user_tokens_instance = FCMUserTokens.objects.get(user=self.user)
        else:
            user_tokens_instance = FCMUserTokens.objects.get(name="unauthenticated")

        # Clear the tokens and save.
        user_tokens_instance.tokens.clear()
        user_tokens_instance.save()

    def send_notification(self, title: str, body: str, image:str):
        if self.user:
            # The instance is associated with an authenticated user.
            tokens = self.tokens
        else:
            # For unauthenticated users
            unauthenticated_tokens_entry = FCMUserTokens.objects.filter(name="unauthenticated").first()
            if not unauthenticated_tokens_entry:
                return {
                    'message': 'No tokens available for unauthenticated users.'
                }
            tokens = unauthenticated_tokens_entry.tokens
        
        if not tokens:
            return {
                'message': 'No tokens available.'
            }
        
        messages = [
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                    image=image,
                ),
                token=token
            )
            for token in tokens
        ]
        
        responses = messaging.send_all(messages)
        return {
            'message': 'Messages sent successfully.',
        }

    class Meta:
        abstract = True
class FCMUserTokens(UserTokens):
    pass
