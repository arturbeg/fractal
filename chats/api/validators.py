from rest_framework import serializers

# Check if a value consists of only lowercase letters
def lowercase(value):
    if value.lower() != value:
        raise serializers.ValidationError('This field must only consist of lowercase letters')




