from django.db import models
from django.conf import settings
from django.db.models import JSONField
class UserTokens(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens', null=True, blank=True)
    name = models.CharField(max_length=100, default="unauthenticated")
    tokens = JSONField(default=list)

    def __str__(self):
        return self.name

# from typing import Generic, TypeVar

# T = TypeVar('T', bound = models.Model)
# class UserTokens(models.Model, Generic[T]):
#     user : models.OneToOneField[T]
#     tokens = models.JSONField(default = list)

#     def subscribe(self, device_id : str):
#         raise NotImplementedError
#     def unsubscribe(self, device_id : str):
#         raise NotImplementedError
#     def unsubscribe_all(self):
#         raise NotImplementedError
#     def send_notification(self, title : str, content : str):
#         raise NotImplementedError
    
#     class Meta:
#         abstract = True

# class FCMUserTokens(UserTokens[settings.AUTH_USER_MODE]):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens', null=True, blank=True)
#     name = models.CharField(max_length=100, default="unauthenticated")
#     tokens = JSONField(default=list)

#     def __str__(self):
#         return self.name