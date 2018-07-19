from django.db import models
from .chatgroup import ChatGroup
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
from .localchat import LocalChat
User = settings.AUTH_USER_MODEL


class Topic(models.Model):
	chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="topic_chatgroup")  # the parent chat group
	name = models.CharField(max_length=200)
	about = models.CharField(max_length=200, blank=True)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="topic_avatar", blank=True)

	saves = models.ManyToManyField(User, blank=True, related_name="topic_saves")
	timestamp = models.DateTimeField(auto_now_add=True)
	label = models.SlugField(unique=True) # Unique way to name a topic/localchat in the URL

	# change to Profile if needed
	online_participants = models.ManyToManyField(User, blank=True, related_name="topic_online")

	arrow_ups 	= models.ManyToManyField(User, blank=True, related_name='arrow_ups')
	arrow_downs = models.ManyToManyField(User, blank=True, related_name='arrow_downs')


	def __str__(self):
		return self.name

	def rating(self):
		return self.arrow_ups.count() - self.arrow_downs.count()

	# not elegant	
	def participants(self):
		participants = []
		for participant in self.online_participants.all():
			participants.append(participant.profile)
		
		return participants		

# class Topic(LocalChat):
	# chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="topics")
	# avatar = models.ImageField(upload_to="topic_avatar", blank=True)
	# owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics")
	# saves = models.ManyToManyField(User, blank=True, related_name="topics")
	# online_participants = models.ManyToManyField(User, blank=True, related_name="topics")
	# chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="topic")
	# arrow_ups 	= models.ManyToManyField(User, blank=True, related_name='arrow_ups')
	# arrow_downs = models.ManyToManyField(User, blank=True, related_name='arrow_downs')


	# def get_api_url(self, request=None):
	# 	return api_reverse("topic-rud", kwargs={'pk':self.pk}, request=request)


    # Step by step bring other methods back