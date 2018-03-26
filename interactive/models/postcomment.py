from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from django.conf import settings
from .message import Message
from .post import Post

User = settings.AUTH_USER_MODEL




class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, blank=True, related_name="comment_likers")
    dislikers = models.ManyToManyField(User, blank=True, related_name="comment_dislikers")

