from django.db import models
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse


User = settings.AUTH_USER_MODEL

class ChatGroup(models.Model):
	owner 		= models.ForeignKey(User, on_delete=models.CASCADE)
	name 		= models.CharField(max_length=200, blank=False)
	about 		= models.CharField(max_length=200, blank=True)
	describtion = models.TextField(blank=True)
	members 	= models.ManyToManyField(User, blank=True, related_name="is_member")

	timestamp 	= models.DateTimeField(auto_now_add=True)

	avatar 		= models.ImageField(upload_to="chatgroup_avatar", blank=True, null=True)

	label 		= models.SlugField(unique=True, blank=False) # unique way to name a chatgroup in the url

	# methods will be added later
	def __str__(self):
		return self.name

	
	def get_api_url(self, request=None):
		return api_reverse("chatgroup-rud", kwargs={'pk':self.pk}, request=request)


