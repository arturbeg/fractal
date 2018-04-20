from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Message(models.Model):
	user 			= models.ForeignKey(User, on_delete=models.CASCADE)

	# Need a validator that ensures that at least 1 of the following 3 fields is not blank	
	globalchat 		= models.ForeignKey(GlobalChat, on_delete=models.CASCADE, blank=True, null=True, related_name="globalchat_messages")
	localchat 		= models.ForeignKey(LocalChat, on_delete=models.CASCADE, blank=True, null=True, related_name="localchat_messages")
	topic 			= models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True, related_name="topic_messages")

	# Need a validator that ensures that at least 1 of the following 4 fields is not blank
	text 			= models.TextField(blank=True, null=True)
	photo 			= models.ImageField(upload_to="message_photo", blank=True, null=True)
	file			= models.FileField(upload_to="message_file", blank=True, null=True)
	# Flag should be a choices filed -> won't be used in the MVP (most likely) 
	flag 			= models.TextField(blank=True, null=True)

	likers 			= models.ManyToManyField(User, blank=True, related_name="likers")
	dislikers 		= models.ManyToManyField(User, blank=True, related_name="dislikers")

	timestamp 		= models.DateTimeField(auto_now_add=True, blank=True, null=True)

	
	@property
	def owner(self):
		return self.user

	def likers_count(self):
		return self.likers.count()	

	# Add the rest of the methods later (while working on the angular app)		