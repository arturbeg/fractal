from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from interactive.models import Message, Post, PostComment
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.staticfiles.templatetags.staticfiles import static

User = settings.AUTH_USER_MODEL

# Notifications system 1.0
class Notification(models.Model):
	text 			= models.TextField()
	user 			= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user") # you
	user_2 			= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_2") # User who does action upon you

	message 		= models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True) # if a message is relevant to the notification
	post 			= models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True) # if a message is relevant to the notification 
	post_comment 	= models.ForeignKey(PostComment, on_delete=models.CASCADE, blank=True, null=True) # if a message is relevant to the notification 


	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
   	    return self.text

# Above is the initial version
# text referes to the view that initiates the creation of the notification



