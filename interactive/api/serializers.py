from django.contrib.auth.models import User
from rest_framework import serializers

# Chats App models
from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile

# Interactive App models
from interactive.models import Message, Post, PostComment, Notification

from chats.api.serializers import UserSerializer

# TODO: change back to HyperLinked
class MessageSerializer(serializers.ModelSerializer):
	
	likers_count 	= serializers.SerializerMethodField()	

	class Meta:
		model = Message
		# fields = ['url', 'pk', 'user', 'globalchat', 'localchat', 'topic', 'text', 'photo', 
		# 'file', 'flag', 'likers', 'dislikers', 'timestamp']

		# read_only_fields = ['user', 'pk', 'user', 'timestamp']

		fields = ['pk', 'text', 'timestamp', 'user', 'topic', 'likers_count']

		read_only_fields = ['pk', 'timestamp', 'user']

		lookup_field = 'id'

	def get_likers_count(self, obj):
		return obj.likers_count()
	# validate that the message has content	
	# def validate(self, data):
	# 	photo = data['photo']
	# 	text  = data['text']
	# 	file  = data['photo']
	# 	flag  = data['text']

	# 	if photo is None and text is None and file is None and flag is None:
	# 		raise serializers.ValidationError('The message must contain some nonempty content type')

	# 	return data	

	# if the message is of the text type, make sure it's nonempty

	def validate_text(self, value):
		if value.isspace():
			raise serializers.ValidationError('The message must contain some nonempty content type')

		return value	





class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ['url', 'pk', 'message', 'likers', 'dislikers', 'timestamp']

		read_only_fields = ['url', 'pk', 'timestamp', 'message']

class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Message
		fields = ['url', 'pk', 'user', 'post', 'text', 'likers', 'dislikers', 'timestamp']	

		read_only_fields = ['url', 'pk', 'user', 'timestamp']	


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Notification
		fields = ['url', 'pk', 'text', 'user', 'user2', 'message', 'post', 'postcomment', 'timestamp']

		# user, user2?
		read_only_fields = ['url', 'pk', 'timestamp']
