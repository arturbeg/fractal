from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route
from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from .serializers import TopicSerializer, ChatGroupSerializer, LocalChatSerializer, GlobalChatSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

 
# Viewsets -> combine the logic for a set of related views in a single class

# Viewsets are registered with a router class -> automatically determines the urlconf 


# The app uses ModelViewSet class
# Later on have a module to store separate ViewSets


# ChatGroupViewSet
class ChatGroupViewSet(viewsets.ModelViewSet):
	''' 
	A viewset for viewing and editing ChatGroup instances
		1. Need search functionality for the chatgroup table
		2. Follow ChatGroup
	'''


	serializer_class = ChatGroupSerializer
	queryset = ChatGroup.objects.all()

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

	def get_queryset(self):
		qs = ChatGroup.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(name__icontains=query)
		return qs

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)	

	# Below making extra actions for routing

	@detail_route(methods=['post', 'get'])
	def follow(self, request, *args, **kwargs):

		user = request.user
		chatgroup = self.get_object()

		if chatgroup.members.filter(id=user.id).exists():
			chatgroup.members.remove(user)
			return Response({'status': 'chatgroup unfollowed'})
		else:
			chatgroup.members.add(user)
			return Response({'status': 'chatgroup followed'})

			
# User View Set
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profile View Set

class ProfileViewSet(viewsets.ModelViewSet):
	serializer_class = ProfileSerializer
	queryset = Profile.objects.all()


# Topic View Set
class TopicViewSet(viewsets.ModelViewSet):

	'''
		1. UpVote a Topic - done
		2. Downvote a Topic - done
		3. Save a Topic - done
		4. Become a Topic Participant - done
		5. Get Trending Topics (filters)
		6. Get New Topics (filters)

		Need a validation check that the same user doesn't
		have the same topic upvoted and downvoted at the same time
	'''
	serializer_class = TopicSerializer
	queryset = Topic.objects.all()

	def perform_create(self, serializer):

		serializer.save(owner=self.request.user)

	# Extra actions for routing
	
	@detail_route(methods=['post', 'get'])
	def upvote(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.arrow_ups.filter(id=user.id).exists():
			topic.arrow_ups.remove(user)
			return Response({"status": "topic upvote is removed"})
		elif topic.arrow_downs.filter(id=user.id).exists():
			topic.arrow_downs.remove(user)
			topic.arrow_ups.add(user)
			return Response({"status": "topic downvote is removed, topic is upvoted"})

		else:
			topic.arrow_ups.add(user)
			return Response({"status": "topic is upvoted"})



	@detail_route(methods=['post', 'get'])
	def downvote(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()


		if topic.arrow_downs.filter(id=user.id).exists():
			topic.arrow_downs.remove(user)
			return Response({"status": "topic downvote is removed"})
		elif topic.arrow_ups.filter(id=user.id).exists():
			topic.arrow_ups.remove(user)
			topic.arrow_downs.add(user)
			return Response({"status": "topic upvote is removed, topic is downvoted"})
		else:
			topic.arrow_downs.add(user)
			return Response({"status": "topic is downvoted"}) 		



	@detail_route(methods=['post', 'get'])
	def save(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.saves.filter(id=user.id).exists():
			topic.saves.remove(user)
			return Response({"status":"topic removed from saves"})
		else:
			topic.saves.add(user)
			return Response({"status":"topic added to saves"})



	@detail_route(methods=['post', 'get'])
	def participate(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.online_participants.filter(id=user.id).exists():
			topic.online_participants.remove(user)
			return Response({"status":"topic removed from online_participants"})
		else:
			topic.online_participants.add(user)
			return Response({"status":"topic added to online_participants"})


# LocalChat View Set
class LocalChatViewSet(viewsets.ModelViewSet):

	serializer_class = LocalChatSerializer
	queryset = LocalChat.objects.all()

	def perform_create(self, serializer):
		# Configure this separately -> unique-label-generator
		serializer.save(owner=self.request.user)	

	# Custom Router Urls

	@detail_route(methods=['post', 'get'])
	def save(self, request, *args, **kwargs):
		user = request.user
		localchat = self.get_object()

		if localchat.saves.filter(id=user.id).exists():
			localchat.saves.remove(user)
			return Response({"status":"localchat removed from saves"})
		else:
			localchat.saves.add(user)
			return Response({"status":"localchat added to saves"})



	@detail_route(methods=['post', 'get'])
	def participate(self, request, *args, **kwargs):
		user = request.user
		localchat = self.get_object()

		if localchat.online_participants.filter(id=user.id).exists():
			localchat.online_participants.remove(user)
			return Response({"status":"localchat removed from online_participants"})
		else:
			localchat.online_participants.add(user)
			return Response({"status":"localchat added to online_participants"})			


# GlobalChat View Set
class GlobalChatViewSet(viewsets.ModelViewSet):
	serializer_class = GlobalChatSerializer
	queryset = GlobalChat.objects.all()

	# Custom Router Urls

	@detail_route(methods=['post', 'get'])
	def save(self, request, *args, **kwargs):
		user = request.user
		globalchat = self.get_object()

		if globalchat.saves.filter(id=user.id).exists():
			globalchat.saves.remove(user)
			return Response({"status":"globalchat removed from saves"})
		else:
			globalchat.saves.add(user)
			return Response({"status":"globalchat added to saves"})



	@detail_route(methods=['post', 'get'])
	def participate(self, request, *args, **kwargs):
		user = request.user
		globalchat = self.get_object()

		if globalchat.online_participants.filter(id=user.id).exists():
			globalchat.online_participants.remove(user)
			return Response({"status":"globalchat removed from online_participants"})
		else:
			globalchat.online_participants.add(user)
			return Response({"status":"globalchat added to online_participants"})			







