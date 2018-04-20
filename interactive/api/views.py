from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from interactive.models import Message, Post, PostComment, Notification


from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import MessageSerializer, PostSerializer, PostCommentSerializer, NotificationSerializer


from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Configure post saves + add post_save signals where necessary
# Reconfigure permissions if necessary

class MessageViewSet(viewsets.ModelViewSet):
	serializer_class 	= MessageSerializer
	queryset 			= Message.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['text']

	permission_classes	= [IsOwnerOrReadOnly]
	lookup_field		= 'id'	

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)		

	@detail_route(methods=['post', 'get'], permission_classes = [IsAuthenticated])
	def like(self, request, *args, **kwargs):

		user = request.user
		message = self.get_object()

		if message.likers.filter(id=user.id).exists():
			message.likers.remove(user)
			return Response({'status': 'message unliked'})
		else:
			message.likers.add(user)
			return Response({'status': 'message liked'})	
	

class PostViewSet(viewsets.ModelViewSet):
	serializer_class 	= PostSerializer
	queryset 			= Post.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['message__text']

	permission_classes	= [IsOwnerOrReadOnly]



class PostCommentViewSet(viewsets.ModelViewSet):
	serializer_class 	= PostCommentSerializer
	queryset 			= PostComment.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['text']

	permission_classes	= [IsOwnerOrReadOnly]	


class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class 	= NotificationSerializer
	queryset 			= Notification.objects.all()

	filter_backends 	= [OrderingFilter]	


