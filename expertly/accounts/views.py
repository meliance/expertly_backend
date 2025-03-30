from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Client, Expert, ExpertDocument
from .serializers import (
    UserSerializer, DetailedUserSerializer, ClientSerializer, ExpertSerializer,
    LoginSerializer, RegisterSerializer, ChangePasswordSerializer,
    ClientUpdateSerializer, ExpertUpdateSerializer, ExpertApprovalSerializer,
    ExpertDetailSerializer, ExpertDocumentSerializer
)
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import update_session_auth_hash

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = DetailedUserSerializer
    permission_classes = [permissions.IsAdminUser]

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ClientUpdateSerializer
        return ClientSerializer
    
    def get_object(self):
        return self.request.user.client_profile
    
    def perform_destroy(self, instance):
        user = instance.user
        user.is_active = False
        user.save()

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.select_related('user').filter(user__is_active=True)
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ExpertProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ExpertUpdateSerializer
        return ExpertSerializer
    
    def get_object(self):
        return self.request.user.expert_profile
    
    def perform_destroy(self, instance):
        user = instance.user
        user.is_active = False
        user.save()

class ExpertPublicProfileView(generics.RetrieveAPIView):
    queryset = Expert.objects.select_related('user').filter(
        is_approved=True,
        user__is_active=True
    )
    serializer_class = ExpertDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class ExpertAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.select_related('user').filter(user__is_active=True)
    serializer_class = ExpertDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_destroy(self, instance):
        instance.user.is_active = False
        instance.user.save()

class ExpertListView(generics.ListAPIView):
    queryset = Expert.objects.filter(is_approved=True, user__is_active=True)
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpertDetailView(generics.RetrieveUpdateAPIView):
    queryset = Expert.objects.filter(is_approved=True, user__is_active=True)
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.is_staff:
            return ExpertApprovalSerializer
        return ExpertSerializer

class AdminExpertApprovalView(generics.ListAPIView):
    queryset = Expert.objects.filter(is_approved=False, user__is_active=True)
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('user_type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ExpertDocumentListView(generics.ListCreateAPIView):
    serializer_class = ExpertDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        expert_id = self.kwargs['expert_id']
        return ExpertDocument.objects.filter(expert_id=expert_id)
    
    def perform_create(self, serializer):
        expert_id = self.kwargs['expert_id']
        expert = Expert.objects.get(id=expert_id)
        if expert.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only add documents to your own profile")
        serializer.save(expert=expert)

class ExpertDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpertDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExpertDocument.objects.all()
    
    def perform_update(self, serializer):
        if serializer.instance.expert.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only update your own documents")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.expert.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only delete your own documents")
        instance.delete()

class ExpertDocumentVerificationView(generics.UpdateAPIView):
    serializer_class = ExpertDocumentSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return ExpertDocument.objects.all()
    
    def perform_update(self, serializer):
        serializer.save(is_verified=True)