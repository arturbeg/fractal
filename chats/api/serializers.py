from django.contrib.auth.models import User
from rest_framework import serializers

from chats.models import ChatGroup, GlobalChat, LocalChat, Topic, Profile
from .validators import lowercase
# Can have a LocalChat serializer class for the Topic and LocalChat (for now keep it simple)



# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model 				= Profile
# 		fields 				= [
# 								'url', 'id', 'user', 'followers', 'about', 
# 							    'avatar', 'timestamp', 'label'
# 							  ] 
# 		read_only_fields 	= ['url', 'user', 'id', 'timestamp']
# 		lookup_field		= 'label'
# 		extra_kwargs = {

# 			'url':			{'lookup_field': 'label'},		
# 			'user':			{'lookup_field': 'username'},
# 			'followers':	{'lookup_field': 'username'},

# 		}


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	
	followers_count 	= serializers.SerializerMethodField()	
	following_count		= serializers.SerializerMethodField()
	# posts_count			= serializers.SerializerMethodField()
	chatgroups_count	= serializers.SerializerMethodField()


	class Meta:
		model 				= Profile
		fields 				= [
								'id', 'about', 'label', 'followers_count', 'following_count',
								'chatgroups_count'
							  ] 
		read_only_fields 	= ['id']
		lookup_field		= 'label'

	
	def get_followers_count(self, obj):
		return obj.followers_count()

	def get_following_count(self, obj):
		return obj.following_count()

	def get_chatgroups_count(self, obj):
		return obj.chatgroups_count()	

	# def get_posts_count(self, obj):
	# 	return obj.posts_count()			



		


class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model  			= User
		fields 			= ['url', 'id', 'username', 'email', 'password']
		lookup_field	= 'username'

		extra_kwargs = {

			"password":		{"write_only":True},
			'url': 			{'lookup_field': 'username'},
		}	


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



# class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):

# 	class Meta:
# 		model 				= ChatGroup
# 		fields 				= ['url', 'id', 'owner', 'name', 'about', 'members', 'description', 'label', 'timestamp', 'avatar']
# 		read_only_fields	= ['owner', 'url', 'id', 'label', 'timestamp']
# 		lookup_field		= 'label'
# 		extra_kwargs		= {
# 			'url': 	 	{'lookup_field': 'label'},
# 			'owner': 	{'lookup_field': 'username'},
# 			'members':  {'lookup_field': 'username'},
# 		}

# Used for testing purposes
class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):

	followers_count 	= serializers.SerializerMethodField()
	topics_count		= serializers.SerializerMethodField()
	localchats_count	= serializers.SerializerMethodField()

	class Meta:
		model 				= ChatGroup
		fields 				= ['id', 'name', 'about', 'description', 'label', 'followers_count', 'topics_count', 'localchats_count']
		read_only_fields	= ['id', 'label', 'followers_count']
		lookup_field		= 'label'
		# extra_kwargs		= {
		# 	'url': 	 	{'lookup_field': 'label'},
		# 	'owner': 	{'lookup_field': 'username'},
		# 	'members':  {'lookup_field': 'username'},
		# }

	def get_followers_count(self, obj):
		return obj.followers_count()

	def get_topics_count(self, obj):
		return obj.topics_count()

	def get_localchats_count(self, obj):
		return obj.localchats_count()				


						
class LocalChatSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model 				= LocalChat
		fields 				= [ 'url', 'id', 'chatgroup', 'name', 'owner', 'about', 'description', 'label', 'timestamp', 'avatar', 'online_participants', 'saves']
		lookup_field		= 'label'
		extra_kwargs		= {
			'url': 	 				{'lookup_field': 'label'},
			'chatgroup': 	 		{'lookup_field': 'label'},
			'owner': 				{'lookup_field': 'username'},
			'online_participants':  {'lookup_field': 'username'},
			'saves':  				{'lookup_field': 'username'},
		}
	
class TopicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model 				= Topic
		fields 				= [ 'url', 'chatgroup', 'id', 'name', 'owner', 'about', 'description', 'label', 'timestamp', 'avatar', 'arrow_ups', 'arrow_downs', 'saves', 'online_participants']
		read_only_fields 	= ['pk', 'owner']
		lookup_field		= 'label'
		extra_kwargs		= {
			'url': 	 				{'lookup_field': 'label'},
			'chatgroup': 	 		{'lookup_field': 'label'},
			'owner': 				{'lookup_field': 'username'},
			'online_participants':  {'lookup_field': 'username'},
			'saves':  				{'lookup_field': 'username'},
			'arrow_ups':  			{'lookup_field': 'username'},
			'arrow_downs':  		{'lookup_field': 'username'},
		}		

	# def validate_name(self, value):
	# 	qs = Topic.objects.filter(name__iexact=value)
	# 	if self.instance:
	# 		qs = qs.exclude(pk=self.instance.pk)
	# 	if qs.exists():
	# 		raise serializers.ValidationError("This name has already been used")	
	# 	return value	


class GlobalChatSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model 				= GlobalChat
		fields 				= [ 'url', 'id', 'chatgroup', 'label', 'online_participants'] # add saves to GC model
		lookup_field		= 'label'
		extra_kwargs		= {
			'url': 	 				{'lookup_field': 'label'},
			'chatgroup': 	 		{'lookup_field': 'label'},
			'online_participants':  {'lookup_field': 'username'},
		}

