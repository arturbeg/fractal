from rest_framework import APITestCase
from django.contrib.auth.models import User
from chats.models import Topic

# automated
# new db is created 
# Work on the tests when done with more important bits
'''

class TopicAPITestCase(APITestCase):
	def setUp(self):
		# Setting up the user
		user = User.objects.create(username='artur', email='test@test.com')
		user.set_password('arturchikk')
		user.save()

		# Creating the topic
		topic = Topic.objects.create()


'''