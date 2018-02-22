from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
	'''
	API endpoint that allows users to be viewed or edited
	'''

	queryset = User.objects.all()
	serializer_class = UserSerializer

	# There are more attributes and functions
	# one can override in ModelViewSet

	# queryset -> queryset that will return objects on .list()
	