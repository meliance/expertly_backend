from rest_framework import serializers
from .models import User, ClientRegistration, ExpertRegistration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_client', 'is_expert', 'created_at', 
                'phone_number', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ClientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = ClientRegistration
        fields = ['user', 'bio', 'location']
        # No 'id' field needed here since we're creating new records

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_client=True)
            return ClientRegistration.objects.create(user=user, **validated_data)
        raise serializers.ValidationError(user_serializer.errors)

class ClientDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = ClientRegistration
        fields = ['user_id', 'email', 'bio', 'location']
        read_only_fields = ['user_id', 'email']

class ExpertRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ExpertRegistration
        fields = ['user', 'expertise', 'bio', 'hourly_rate', 'experience_years', 
                 'license_file', 'degree_file', 'certificate_file', 'id_proof_file']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_expert=True)
            return ExpertRegistration.objects.create(user=user, **validated_data)
        raise serializers.ValidationError(user_serializer.errors)

class ExpertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertRegistration
        fields = ['id', 'expertise', 'bio', 'hourly_rate', 'experience_years',
                 'license_file', 'degree_file', 'certificate_file', 'id_proof_file',
                 'is_approved', 'documents_verified']
        read_only_fields = ['id', 'is_approved', 'documents_verified']