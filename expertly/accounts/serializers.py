from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Client, Expert
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from documents.models import ExpertDocument

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'user_type', 'phone_number', 'profile_picture', 'is_verified']
        read_only_fields = ['id', 'user_type', 'is_verified']

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                 'phone_number', 'profile_picture', 'language']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

class DetailedUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display')
    expert_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'user_type', 'phone_number', 'profile_picture', 'is_verified',
                 'created_at', 'expert_status']

    def get_is_client(self, obj):
        return hasattr(obj, 'client_profile')

    def get_is_expert(self, obj):
        return hasattr(obj, 'expert_profile')

    def get_expert_status(self, obj):
        if hasattr(obj, 'expert_profile'):
            return {
                'is_approved': obj.expert_profile.is_approved,
                'specialization': obj.expert_profile.specialization,
                'rating': obj.expert_profile.rating
            }
        return None

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, user_type='client')
        client = Client.objects.create(user=user, **validated_data)
        return client

class ClientUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(required=False)
    
    class Meta:
        model = Client
        fields = ['user', 'interests']
        extra_kwargs = {
            'interests': {'required': False},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        
        return super().update(instance, validated_data)

class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Expert
        fields = '__all__'
        read_only_fields = ['id', 'user', 'is_approved', 'rating', 'total_sessions']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, user_type='expert')
        expert = Expert.objects.create(user=user, **validated_data)
        return expert

class ExpertUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(required=False)
    
    class Meta:
        model = Expert
        fields = ['user', 'specialization', 'qualifications', 'experience_years', 'hourly_rate']
        extra_kwargs = {
            'specialization': {'required': False},
            'qualifications': {'required': False},
            'experience_years': {'required': False},
            'hourly_rate': {'required': False},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        
        return super().update(instance, validated_data)

class ExpertApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['is_approved']
    
    def update(self, instance, validated_data):
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance

class ExpertDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ExpertDocument
        fields = ['id', 'document_type', 'file_url', 'title', 
                'issuing_organization', 'issue_date', 'expiration_date',
                'is_verified', 'created_at']
        read_only_fields = ['id', 'file_url', 'is_verified', 'created_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("File size must be less than 5MB.")
        return value

class ExpertDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    documents = ExpertDocumentSerializer(many=True, read_only=True)
    # appointment_count = serializers.SerializerMethodField()
    # available_schedules = serializers.SerializerMethodField()
    # upcoming_appointments = serializers.SerializerMethodField()
    
    class Meta:
        model = Expert
        fields = '__all__'
        read_only_fields = ['id', 'user'] 
        # 'appointment_count', 
        #                   'available_schedules', 'upcoming_appointments',
        #                   'has_license', 'has_degree', 'has_masters',
        #                   'has_certificates', 'has_cv']
    
    has_license = serializers.SerializerMethodField()
    has_degree = serializers.SerializerMethodField()
    has_masters = serializers.SerializerMethodField()
    has_certificates = serializers.SerializerMethodField()
    has_cv = serializers.SerializerMethodField()
    
    # def get_appointment_count(self, obj):
    #     return obj.appointments.count()
    
    # def get_available_schedules(self, obj):
    #     from schedules.serializers import ScheduleSerializer
    #     schedules = obj.schedules.filter(is_available=True)
    #     return ScheduleSerializer(schedules, many=True).data
    
    # def get_upcoming_appointments(self, obj):
    #     from appointments.serializers import AppointmentSerializer
    #     from django.utils import timezone
    #     appointments = obj.appointments.filter(
    #         scheduled_time__gte=timezone.now(),
    #         status='confirmed'
    #     ).order_by('scheduled_time')[:5]
    #     return AppointmentSerializer(appointments, many=True).data
    
    def get_has_license(self, obj):
        return obj.documents.filter(document_type='license', is_verified=True).exists()
    
    def get_has_degree(self, obj):
        return obj.documents.filter(document_type='degree', is_verified=True).exists()
    
    def get_has_masters(self, obj):
        return obj.documents.filter(document_type='masters', is_verified=True).exists()
    
    def get_has_certificates(self, obj):
        return obj.documents.filter(document_type='certificate', is_verified=True).exists()
    
    def get_has_cv(self, obj):
        return obj.documents.filter(document_type='cv', is_verified=True).exists()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    hourly_rate = serializers.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        required=False,
        allow_null=True
    )
    specialization = serializers.CharField(required=False, allow_blank=True)
    qualifications = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'user_type', 'phone_number',
            'hourly_rate', 'specialization', 'qualifications', 'experience_years'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        attrs['user_type'] = attrs.get('user_type', '').lower()
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if attrs['user_type'] == 'expert':
            if not attrs.get('specialization'):
                raise serializers.ValidationError({
                    "specialization": "Specialization is required for experts"
                })
            attrs.setdefault('hourly_rate', 0)  # Ensure default if missing
            attrs.setdefault('experience_years', 0)  # Ensure default if missing

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user_type = validated_data.pop('user_type')
        
        expert_data = {
            'hourly_rate': float(validated_data.pop('hourly_rate', 0)),
            'experience_years': int(validated_data.pop('experience_years', 0)),
            'specialization': validated_data.pop('specialization', 'General'),
            'qualifications': validated_data.pop('qualifications', ''),
        }

        user = User.objects.create_user(**validated_data, user_type=user_type)
        
        if user_type == 'expert':
            Expert.objects.create(user=user, **expert_data)
        elif user_type == 'client':
            Client.objects.create(user=user)
            
        return user