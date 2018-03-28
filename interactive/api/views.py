from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from interactive.models import Message, Post, PostComment, Notification


from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import MessageSerializer, PostSerializer, PostCommentSerializer, NotificationSerializer

# Configure post saves + add post_save signals where necessary

class MessageViewSet(viewsets.ModelViewSet):
	serializer_class 	= MessageSerializer
	queryset 			= Message.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['text']	


class PostViewSet(viewsets.ModelViewSet):
	serializer_class 	= PostSerializer
	queryset 			= Post.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['message__text']



class PostCommentViewSet(viewsets.ModelViewSet):
	serializer_class 	= PostCommentSerializer
	queryset 			= PostComment.objects.all()

	filter_backends 	= [SearchFilter, OrderingFilter]
	search_fields 		= ['text']	


class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class 	= NotificationSerializer
	queryset 			= Notification.objects.all()

	filter_backends 	= [OrderingFilter]	


