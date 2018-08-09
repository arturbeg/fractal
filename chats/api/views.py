from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route
from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from .serializers import TopicSerializer, ChatGroupSerializer, LocalChatSerializer, GlobalChatSerializer, ProfileSerializer, UserSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyUserClass
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination
	)

# Filtering related imports
from rest_framework.filters import SearchFilter, OrderingFilter
#from .filters import FollowersCountFilterBackend


from chats.models.utilities import unique_label_generator


# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView
# from rest_auth.registration.views import SocialConnectView

 
# Later on have a module to store separate ViewSets


# ChatGroupViewSet
class ChatGroupViewSet(viewsets.ModelViewSet):
	serializer_class 	= ChatGroupSerializer
	queryset 			= ChatGroup.objects.all()
	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['name', 'about', 'describtion', 'label']
	permission_classes  = [IsOwnerOrReadOnly]
	pagination_class	= CustomPageNumberPagination
	lookup_field		= 'label'

	# use get_queryset when run out of options; or apply a filter from filters.py

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
	
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)	

	# Below making extra actions for routing

	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def follow(self, request, *args, **kwargs):

		user = request.user
		chatgroup = self.get_object()

		if chatgroup.members.filter(id=user.id).exists():
			chatgroup.members.remove(user)
			return Response({'status': 'chatgroup unfollowed'})
		else:
			chatgroup.members.add(user)
			return Response({'status': 'chatgroup followed'})

	@detail_route(methods=['get'], permission_classes = [IsAuthenticated])
	def topics(self, request, *args, **kwargs):
		chatgroup = self.get_object()
		queryset = Topic.objects.filter(chatgroup=chatgroup)
		serializer = TopicSerializer(queryset, many=True, context={'request':request})

		return Response(serializer.data)







			
class UserViewSet(viewsets.ModelViewSet):
    queryset 			= User.objects.all()
    serializer_class 	= UserSerializer	
    filter_backends 	= [SearchFilter, OrderingFilter]
    search_fields 		= ['username', 'email', 'profile__about']
    permission_classes	= [IsOwnerOrReadOnlyUserClass]
    pagination_class	= CustomPageNumberPagination
    lookup_field		= 'username'



# Profile View Set
class ProfileViewSet(viewsets.ModelViewSet):
	serializer_class 	= ProfileSerializer
	queryset 			= Profile.objects.all()	
	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['user__username', 'user__email', 'about']
	# TODO: change to IsOwnerOrReadOnly later
	permission_classes  = [IsOwnerOrReadOnly]
	pagination_class	= CustomPageNumberPagination
	lookup_field		= 'label'


	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def follow(self, request, *args, **kwargs):
		profile = self.get_object()
		user = request.user

		if profile.followers.filter(id=user.id).exists():
			profile.followers.remove(user)
			return Response({"status": "profile unfollowed"})
		else:
			profile.followers.add(user)
			return Response({"status": "profile followed"})


	@detail_route()
	def topics(self, request, *args, **kwargs):
		profile = self.get_object()
		queryset = Topic.objects.filter(chatgroup__members__id=profile.user.id)

		serializer = TopicSerializer(queryset, many=True, context={'request':request})

		return Response(serializer.data)

	# Chatgroups that are followed by the user
	@detail_route()
	def chatgroups(self, request, *args, **kwargs):
		profile = self.get_object()
		queryset = ChatGroup.objects.filter(members__id=profile.user.id)

		serializer = ChatGroupSerializer(queryset, many=True, context={'request':request})
		return Response(serializer.data)

	# Fix the fact that the followers (User model) and following (Profile model)	
	@detail_route()
	def followers(self, request, *args, **kwargs):
		profile = self.get_object()
		queryset = profile.followers.all()

		serializer = UserSerializer(queryset, many=True, context={'request':request})
		return Response(serializer.data)


	@detail_route()
	def following(self, request, *args, **kwargs):
		profile = self.get_object()
		queryset = profile.is_following.all()

		serializer = self.get_serializer(queryset, many=True, context={'request':request})
		return Response(serializer.data)		



# Topic View Set
class TopicViewSet(viewsets.ModelViewSet):

	'''
		1. Get Trending Topics (filters)
		2. Get New Topics (filters)

		Need a validation check that the same user doesn't
		have the same topic upvoted and downvoted at the same time
	'''
	serializer_class 	= TopicSerializer
	queryset 			= Topic.objects.all()
	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['name', 'about', 'describtion', 'label']
	permission_classes	= [IsOwnerOrReadOnly]
	pagination_class	= CustomPageNumberPagination
	lookup_field		= 'label'


	def perform_create(self, serializer):

		serializer.save(owner=self.request.user)

	# Extra actions for routing
	

	

	
	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
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



	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
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



	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def save(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.saves.filter(id=user.id).exists():
			topic.saves.remove(user)
			return Response({"status":"topic removed from saves"})
		else:
			topic.saves.add(user)
			return Response({"status":"topic added to saves"})



	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def participate(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.online_participants.filter(id=user.id).exists():
			
			return Response({"status":"no changes to online_participants"})
		else:
			topic.online_participants.add(user)
			return Response({"status":"topic added to online_participants"})
				

	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def leave(self, request, *args, **kwargs):
		user = request.user
		topic = self.get_object()

		if topic.online_participants.filter(id=user.id).exists():
			topic.online_participants.remove(user)
			return Response({"status":"topic removed from online_participants"})
		else:
			return Response({"status":"no changes to online_participants"})	

					
	# # get list of messages of the topic		
	# @detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	# def messages(self)			


# LocalChat View Set
class LocalChatViewSet(viewsets.ModelViewSet):

	serializer_class 	= LocalChatSerializer
	queryset 			= LocalChat.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['name', 'about', 'describtion', 'label']

	permission_classes	= [IsOwnerOrReadOnly]
	pagination_class	= CustomPageNumberPagination
	lookup_field		= 'label'


	def perform_create(self, serializer):
		# Configure this separately -> unique-label-generator
		serializer.save(owner=self.request.user)	

	# Custom Router Urls

	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def save(self, request, *args, **kwargs):
		user = request.user
		localchat = self.get_object()

		if localchat.saves.filter(id=user.id).exists():
			localchat.saves.remove(user)
			return Response({"status":"localchat removed from saves"})
		else:
			localchat.saves.add(user)
			return Response({"status":"localchat added to saves"})



	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
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

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['chatgroup__name', 'chatgroup__about', 'chatgroup__describtion']

	permission_classes	= [IsOwnerOrReadOnly]
	pagination_class	= CustomPageNumberPagination
	lookup_field		= 'label'

	


	# Custom Router Urls

	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def save(self, request, *args, **kwargs):
		user = request.user
		globalchat = self.get_object()

		if globalchat.saves.filter(id=user.id).exists():
			globalchat.saves.remove(user)
			return Response({"status":"globalchat removed from saves"})
		else:
			globalchat.saves.add(user)
			return Response({"status":"globalchat added to saves"})



	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def participate(self, request, *args, **kwargs):
		user = request.user
		globalchat = self.get_object()

		if globalchat.online_participants.filter(id=user.id).exists():
			globalchat.online_participants.remove(user)
			return Response({"status":"globalchat removed from online_participants"})
		else:
			globalchat.online_participants.add(user)
			return Response({"status":"globalchat added to online_participants"})			



# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter


# class FacebookConnect(SocialConnectView):
# 	adapter_class = FacebookOAuth2Adapter

