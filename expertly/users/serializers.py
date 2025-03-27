from rest_framework import serializers
from .models import User, ClientRegistration, ExpertRegistration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_client', 'is_expert', 'created_at', 
                'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

    
class ClientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ClientRegistration
        fields = ['user', 'bio', 'location']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        return ClientRegistration.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
        
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance
    
    
class ExpertRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ExpertRegistration
        fields = ['user', 'expertise', 'bio', 'hourly_rate', 'experiance_years', 'is_approved']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        return ExpertRegistration.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
        
        instance.expertise = validated_data.get('expertise', instance.expertise)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.hourly_rate = validated_data.get('hourly_rate', instance.hourly_rate)
        instance.experiance_years = validated_data.get('experiance_years', instance.experiance_years)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance