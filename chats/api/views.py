from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import generics, mixins
from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from .serializers import TopicSerializer, ChatGroupSerializer, LocalChatSerializer
from .permissions import IsOwnerOrReadOnly




class LocalChatAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = LocalChatSerializer

	def get_queryset(self):
		# Performing the search functionality in here

		qs = LocalChat.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(name__icontains=query)
		return qs

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)	

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

	def get_serializer_context(self, *args, **kwargs):
		return 	{'request': self.request}	



class LocalChatRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = LocalChatSerializer
	permission_classes = [IsOwnerOrReadOnly]


	def get_queryset(self):
		return LocalChat.objects.all()

	# getting the request for the serializer
	
	def get_serializer_context(self, *args, **kwargs):
		return 	{'request': self.request}




class ChatGroupAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = ChatGroupSerializer

	def get_queryset(self):
		qs = ChatGroup.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(name__icontains=query)
		return qs

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.users)

	def get_serializer_context(self, *args, **kwargs):
		return {'request':self.request}			


class ChatGroupRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = ChatGroupSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def get_queryset(self):
		return ChatGroup.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		return {'request':self.request}



class TopicAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = TopicSerializer

	def get_queryset(self):
		# Performing the search functionality in here

		qs = Topic.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(name__icontains=query)
		return qs

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)	

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

	def get_serializer_context(self, *args, **kwargs):
		return 	{'request': self.request}	


class TopicRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = TopicSerializer
	permission_classes = [IsOwnerOrReadOnly]


	def get_queryset(self):
		return Topic.objects.all()

	# getting the request for the serializer
	
	def get_serializer_context(self, *args, **kwargs):
		return 	{'request': self.request}





class UserViewSet(viewsets.ModelViewSet):
	'''
	API endpoint that allows users to be viewed or edited
	'''

	queryset = User.objects.all()
	serializer_class = UserSerializer

	# There are more attributes and functions
	# one can override in ModelViewSet

	# queryset -> queryset that will return objects on .list()




		




