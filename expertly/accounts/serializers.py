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
        # Handle password separately
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# For creation-only serializers (if needed)
class ClientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ClientRegistration
        fields = ['user', 'bio', 'location']

class ClientDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = ClientRegistration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # Update user fields
        for attr, value in user_data.items():
            if attr == 'password' and value:
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()
        
        # Update client fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    
class ExpertRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ExpertRegistration
        fields = ['user', 'expertise', 'bio', 'hourly_rate', 'experiance_years']

class ExpertDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = ExpertRegistration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_approved']  # is_approved might need admin approval
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # Update user fields
        for attr, value in user_data.items():
            if attr == 'password' and value:
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()
        
        # Update expert fields
        for attr, value in validated_data.items():
            # Add any special field handling here
            setattr(instance, attr, value)
        instance.save()
        
        return instance


