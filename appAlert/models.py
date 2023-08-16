from django.db import models
from django.contrib.auth.models import User
from typing import Generic, TypeVar, Any, Union
from firebase_admin import messaging


T = TypeVar('T', bound=models.Model)
class UserTokens(models.Model, Generic[T]):
    user : models.OneToOneField[T]
    tokens = models.JSONField(default = list)
    def unique_subscribe(self, device_id : Any, commit : bool = False):
        if device_id not in self.tokens:
            self.subscribe(device_id, commit)
    def subscribe(self, device_id : Any, commit : bool = False):
        self.tokens.append(device_id)
        if commit : self.save()
    def unsubscribe(self, device_id : Any, commit : bool = False):
        self.tokens.remove(device_id)
        if commit : self.save()
    def unsubscribe_all(self, commit : bool = False):
        self.tokens.clear()
        if commit : self.save()
    def send_notification(self, title : str, body : str, image : Union[str, None]):
        raise NotImplementedError
    class Meta:
        abstract = True

class FCMToken(UserTokens[T], Generic[T]):
    def send_notification(self, title: str, body: str, image: Union[str, None]):
        tokens = self.tokens
        messages = [
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                    image=image,
                ),
                token = token
            )
            for token in tokens
        ]
        messaging.send_all(messages)
    class Meta:
        abstract = True

class FCMToken_Testing(FCMToken[User]):
    user = models.OneToOneField(
        to = User, on_delete = models.CASCADE, related_name = 'fcm_tokens', null = True
    )

