from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from django.conf import settings
from .message import Message

User = settings.AUTH_USER_MODEL



class Post(models.Model):
    message 		= models.OneToOneField(Message, on_delete=models.CASCADE)
    timestamp 		= models.DateTimeField(auto_now_add=True)

    likers 			= models.ManyToManyField(User, blank=True, related_name="post_likers")
    dislikers 		= models.ManyToManyField(User, blank=True, related_name="post_dislikers")
