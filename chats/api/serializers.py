from django.contrib.auth.models import User
from rest_framework import serializers

from chats.models import Topic

'''
Serializers allow complex data such as
querysets and model instances to be converted to
native Python datatypes that cna be easily rendered into JSON,
XML or other content types.

Serializers also provide decerialization, allowing parsed data to be
converted back into complex types, after validating the incoming data

Work very similarly to Django's Form and ModelForm classes

There are 2 main uses of serializers:

1) Get model data from the db in JSON
2) Use them like forms to validate date and create instances of a model

Different types of serializers -> focus on HyperlinkedModelSerializers

HyperlinkedModelSerializers build on top fo ModelSerializers by using URL
instead of pk values to define relations.

'''



class ChatGroupSerializer(serializers.HyperlinkedModelSerializer):
		owner = serializers.ReadOnlyField(source='owner.username')
		members = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)


		class Meta:
			model = Topic
			fields = ('url', 'name', 'about', 'describtion', 'id', 'label', 'timestamp', 'avatar')





class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model  = User
		fields = ('url', 'username', 'email')		
		# The url goes to the model's User Detail page
		# When the User is represented as a ForeignKey to other objects
		# the URL will be displayed instead of a simple pk


class TopicSerializer(serializers.HyperlinkedModelSerializer):
	
	arrow_ups = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	arrow_downs = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
	# Need to destinguish between those

	# Okay have a pause here -> more theory
	#class Meta:
		#model = Topic

