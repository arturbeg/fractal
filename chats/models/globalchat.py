from django.db import models
from django.conf import settings
from .chatgroup import ChatGroup
User = settings.AUTH_USER_MODEL

class GlobalChat(models.Model):
    
    chatgroup 			= models.OneToOneField(ChatGroup, on_delete=models.CASCADE) # the parent chat group -> one to one relationship
    label 				= models.SlugField(unique=True)
    online_participants = models.ManyToManyField(User, related_name='globalchat_online_participants')



