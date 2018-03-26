from django.contrib.auth.models import User
from rest_framework import serializers

# Chats App models
from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile

# Interactive App models
from interactive.models import Message, Post, PostComment, Notification


class MessageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Message
		fields = ['url', 'pk', 'user', 'globalchat', 'localchat', 'topic', 'text', 'photo', 
		'file', 'flag', 'likers', 'dislikers', 'timestamp']


class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ['url', 'pk', 'message', 'likers', 'dislikers', 'timestamp']



class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Message
		fields = ['url', 'pk', 'user', 'post', 'text', 'likers', 'dislikers', 'timestamp']		


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Notification
		fields = ['url', 'pk', 'text', 'user', 'user2', 'message', 'post', 'postcomment', 'timestamp']
