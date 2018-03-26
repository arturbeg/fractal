from .localchat import LocalChat
from django.db import models
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
User = settings.AUTH_USER_MODEL

class Topic(LocalChat):
	
	arrow_ups 	= models.ManyToManyField(User, blank=True, related_name='arrow_ups')
	arrow_downs = models.ManyToManyField(User, blank=True, related_name='arrow_downs')


	def get_api_url(self, request=None):
		return api_reverse("topic-rud", kwargs={'pk':self.pk}, request=request)


    # Step by step bring other methods back