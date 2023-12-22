from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .utils import validate_email, clearbit_additional

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        if not validate_email(data.get('email')):
            raise exceptions.ValidationError(
                {'email': 'Please enter validate email!'}
            )
        
        try:
            validate_password(password, user)
        except exceptions.ValidationError as error:
            raise exceptions.ValidationError(
                {'password': error}
            )

        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],
        )
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if 'password' in representation:
            del representation['password']
        
        return representation

class UserSerializer(serializers.ModelSerializer):
    clearbit_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'clearbit_info')

    def get_clearbit_info(self, obj):
        return clearbit_additional(obj.email)