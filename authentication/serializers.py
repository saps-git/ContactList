# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes 
# that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, 
# allowing parsed data to be converted back into complex types, after first validating the incoming data.

from rest_framework import  serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer): #The ModelSerializer class provides a shortcut that lets you automatically create a Serializer class with fields that correspond to the Model fields.
    password = serializers.CharField(max_length=65, min_length=8, write_only=True) #write_only = will not return this
    email = serializers.EmailField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta: # Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table). None are required, and adding class Meta to a model is completely optional.
        model = User #inheriting from ModelSerializer
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    #when you need to make custom validations, this method gets called before instance is created
    def validate(self, attrs):
        email = attrs.get('email', '') # '' is the default value, which will be returned if we get no email value
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('Email is already in use')})
        return super().validate(attrs)

    #to create a instance
    def create(self, validated_data):
        return User.objects.create_user(**validated_data) # **validated data = two astreiks, spread all the input data, to their particular keys(fields), without it all the data will be set to the first field only

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']