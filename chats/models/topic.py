from .localchat import LocalChat
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Topic(LocalChat):
	
	arrow_ups 	= models.ManyToManyField(User, related_name='arrow_ups')
	arrow_downs = models.ManyToManyField(User, related_name='arrow_downs')


    # Methods later