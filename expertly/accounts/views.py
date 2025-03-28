from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import User, ClientRegistration, ExpertRegistration
from .serializers import UserSerializer, ClientDetailSerializer, ExpertDetailSerializer
class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]

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
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
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
                    'message': f"Unexpected error: {str(e)}",
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'error',
            'message': serializer.errors,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)  # Hash password
        user.save()
        
user_list_create_api_view = UserListCreateApiView.as_view()

class ClientDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientDetailSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_object(self):
        """
        Returns the client profile for:
        - The authenticated user if no PK is provided (via /clients/me/)
        - The requested PK if the user is admin/staff (via /clients/<pk>/)
        """
        pk = self.kwargs.get('pk')  # Check if URL has a PK
        
        # Case 1: User requests their own profile (e.g., /clients/me/)
        if pk is None or str(pk) == 'me':
            try:
                return self.request.user.clientregistration
            except ClientRegistration.DoesNotExist:
                raise NotFound("Client profile not found for this user")
        
        # Case 2: Admin requests another client's profile (e.g., /clients/1/)
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can view other clients' profiles")
        
        try:
            return ClientRegistration.objects.get(pk=pk)
        except ClientRegistration.DoesNotExist:
            raise NotFound("Client not found")

client_detail_api_view = ClientDetailApiView.as_view()

class ExpertDetailApiView(generics.RetrieveUpdateAPIView):
    queryset = ExpertRegistration.objects.all()
    serializer_class = ExpertDetailSerializer
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.expertregistration
    
expert_detail_api_view = ExpertDetailApiView.as_view()