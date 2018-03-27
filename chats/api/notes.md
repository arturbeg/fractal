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

Later will turn the views.py into a separate module where the topic related functionality will be
perormed in the topic.py, etc...








