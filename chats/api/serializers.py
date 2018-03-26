from django.contrib.auth.models import User
from rest_framework import serializers

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile 
# Can have a LocalChat serializer class for the Topic and LocalChat (for now keep it simple)

class ChatGroupSerializer(serializers.ModelSerializer):
	members = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
	url = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = ChatGroup
		fields = ('url', 'pk', 'owner', 'name', 'about', 'members', 'describtion', 'label', 'timestamp', 'avatar')

		# owner, name, about, describtion, members, timestamp, avatar, label -> model fields
	def get_url(self, obj):
		return self.context.get("request")

	# A ChatGroup should have a unique name	
	def validate_name(self, value):
		qs = ChatGroup.objects.filter(name__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This ChatGroup name has already been used!")	
		return value
						
class LocalChatSerializer(serializers.ModelSerializer):
	online_participants = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
	url = serializers.SerializerMethodField(read_only=True)
	saves = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	#chatgroup = serializers.HyperlinkedRelatedField(view_name='chatgroup-rud')
	# use serializermethod field or some shit

	class Meta:
		model = LocalChat
		fields = fields = [ 'url', 'pk', 'name', 'owner', 'about', 'describtion', 'label', 'timestamp', 'avatar', 'online_participants', 'saves']
		# chatgroup, name, about, describtion, owner, avatar, saves, timestamp, label, online_participants

	def get_url(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)
	



class TopicSerializer(serializers.ModelSerializer):
	
	arrow_ups = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	arrow_downs = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
	url = serializers.SerializerMethodField(read_only=True)
	#chatgroup = serializers.HyperlinkedRelatedField(view_name='chatgroup-rud')
	# Need to destinguish between those

	# Okay have a pause here -> more theory
	class Meta:
		model = Topic
		fields = [ 'url', 'chatgroup', 'pk', 'name', 'owner', 'about', 'describtion', 'label', 'timestamp', 'avatar', 'arrow_ups', 'arrow_downs']
		read_only_fields = ['pk', 'owner']



	# Getting the url here for the Serializer
	
	def get_url(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)	
	
	# Below is an example of how a validation of a field would work -> will delete later

	def validate_name(self, value):
		qs = Topic.objects.filter(name__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This name has already been used")	
		return value	




class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model  = User
		fields = ('url', 'username', 'email')		
		# The url goes to the model's User Detail page
		# When the User is represented as a ForeignKey to other objects
		# the URL will be displayed instead of a simple pk


# A serializer does 2 things
# Converts to JSON
# validations for data passed