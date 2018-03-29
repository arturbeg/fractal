from django.contrib.auth.models import User
from rest_framework import serializers

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from .validators import lowercase
# Can have a LocalChat serializer class for the Topic and LocalChat (for now keep it simple)



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Profile
		fields = ['url', 'id', 'user', 'followers', 'about', 'avatar', 'timestamp']

		read_only_fields = ['url', 'user', 'id', 'timestamp']

class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model  = User
		fields = ['url', 'id', 'username', 'email', 'password']

	extra_kwargs = {"password":{"write_only":True}}	


	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']

		user = User(username=username, email=email)
		user.set_password(password)
		user.save()

		return validated_data
	# make sure the username is lowercase	
	def validate_username(self, value):

		return lowercase(value)



class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model 				= ChatGroup
		fields 				= ['url', 'id', 'owner', 'name', 'about', 'members', 'describtion', 'label', 'timestamp', 'avatar']
		read_only_fields	= ['owner', 'url', 'id', 'label', 'timestamp']

						
class LocalChatSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LocalChat
		fields = [ 'url', 'id', 'name', 'owner', 'about', 'describtion', 'label', 'timestamp', 'avatar', 'online_participants', 'saves']

	
class TopicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Topic
		fields = [ 'url', 'chatgroup', 'id', 'name', 'owner', 'about', 'describtion', 'label', 'timestamp', 'avatar', 'arrow_ups', 'arrow_downs', 'saves', 'online_participants']
		read_only_fields = ['pk', 'owner']

	# def validate_name(self, value):
	# 	qs = Topic.objects.filter(name__iexact=value)
	# 	if self.instance:
	# 		qs = qs.exclude(pk=self.instance.pk)
	# 	if qs.exists():
	# 		raise serializers.ValidationError("This name has already been used")	
	# 	return value	


class GlobalChatSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GlobalChat
		fields = [ 'url', 'id', 'chatgroup', 'label', 'online_participants']


