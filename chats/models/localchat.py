from django.db import models
from .chatgroup import ChatGroup
from django.conf import settings
User = settings.AUTH_USER_MODEL


class LocalChat(models.Model):
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)  # the parent chat group
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    describtion = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="topic_avatar", blank=True)

    saves = models.ManyToManyField(User, blank=True, related_name="saves")
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.SlugField(unique=True) # Unique way to name a topic/localchat in the URL

    online_participants = models.ManyToManyField(User, blank=True, related_name="online_participants")


    # need to fully undertand how the related_name attribute functions
    # is_hidden and is_private will be added later
    # No methods for now -> need to pin down the structure of the database tables


    #class Meta:
        #abstract=True

