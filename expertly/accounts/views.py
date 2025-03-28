from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import User, ClientRegistration, ExpertRegistration
from .serializers import (
    UserSerializer, 
    ClientRegistrationSerializer,
    ClientDetailSerializer, 
    ExpertDetailSerializer,
    ExpertRegistrationSerializer
)

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Default to allow any
    
    def get_permissions(self):
        # Only admins can list users
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'status': 'success',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors,
                'message': 'Validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'User creation failed',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class ProfileDetailMixin:
    """Common functionality for client/expert profile views"""
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        
        # Handle 'me' endpoint for authenticated users
        if pk is None or str(pk).lower() == 'me':
            if not self.request.user.is_authenticated:
                raise PermissionDenied("Authentication required")
                
            try:
                return self.get_profile_model().objects.get(user=self.request.user)
            except self.get_profile_model().DoesNotExist:
                raise NotFound(f"{self.get_profile_model().__name__} not found")
        
        # Admin access to specific profiles
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can view other profiles")
            
        try:
            return self.get_profile_model().objects.get(pk=pk)
        except self.get_profile_model().DoesNotExist:
            raise NotFound("Profile not found")

class ClientRegistrationAPIView(generics.CreateAPIView):
    """
    API endpoint for client registration
    """
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow registration without auth
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'success',
                'message': 'Client registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Client registration failed',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow registration without auth
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'success',
                'message': 'Client registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Client registration failed',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        # This will use the create method defined in ClientRegistrationSerializer
        serializer.save()

class ClientDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ClientDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        
        # Handle 'me' endpoint
        if str(pk) == 'me':
            pk = self.request.user.pk

        try:
            # Get the user first
            user = User.objects.get(pk=pk)
            # Return the client profile or raise 404
            return user.client_profile
        except (User.DoesNotExist, ClientRegistration.DoesNotExist):
            raise NotFound("Profile not found")


class ExpertDetailAPIView(ProfileDetailMixin, generics.RetrieveAPIView):
    serializer_class = ExpertDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_profile_model(self):
        return ExpertRegistration


class ExpertRegistrationAPIView(generics.CreateAPIView):
    serializer_class = ExpertRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.is_expert:
            raise PermissionDenied("You are already registered as an expert")
            
        serializer.save(user=self.request.user)
        self.request.user.is_expert = True
        self.request.user.save()


# View instances
user_list_create_api_view = UserListCreateAPIView.as_view()
client_registration_api_view = ClientRegistrationAPIView.as_view()
client_detail_api_view = ClientDetailAPIView.as_view()
expert_detail_api_view = ExpertDetailAPIView.as_view()
expert_registration_api_view = ExpertRegistrationAPIView.as_view()

class ExpertDetailApiView(generics.RetrieveAPIView):
    serializer_class = ExpertDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        try:
            if self.kwargs.get('pk') == 'me':
                user = self.request.user
            else:
                user = User.objects.get(pk=self.kwargs.get('pk'))
            
            return user.expert_profile  # Changed to match related_name
            
        except User.DoesNotExist:
            raise NotFound("User not found")
        except ExpertRegistration.DoesNotExist:
            raise NotFound("Expert profile not found")
    
expert_detail_api_view = ExpertDetailApiView.as_view()