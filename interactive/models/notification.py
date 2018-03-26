from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from django.conf import settings
from .message import Message
from .post import Post
from .postcomment import PostComment

User = settings.AUTH_USER_MODEL


# Notification system 1.0
# Text referes to the view that initiates the creation of the notification
### Later will have choices instead of the TextField
# Example -> user_2 liked user's message


class Notification(models.Model):
	# will later be a choices field
	text 			= models.TextField()
	user 			= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="notification_user") # you
	user2 			= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="notification_user2") # User who does action upon you

	# The Notification is related to a message object, analogously for the post and post_comment fields
	message 		= models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True)
	post 			= models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
	postcomment 	= models.ForeignKey(PostComment, on_delete=models.CASCADE, blank=True, null=True)

	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	# Methods and @properties added later