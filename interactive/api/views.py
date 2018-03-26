from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import detail_route, list_route

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from interactive.models import Message, Post, PostComment, Notification


from rest_framework.response import Response

from .serializers import MessageSerializer, PostSerializer, PostCommentSerializer, NotificationSerializer


class MessageViewSet(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	queryset = Message.objects.all()


class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()


class PostCommentViewSet(viewsets.ModelViewSet):
	serializer_class = PostCommentSerializer
	queryset = PostComment.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class = NotificationSerializer
	queryset = Notification.objects.all()	


