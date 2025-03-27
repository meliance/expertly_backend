from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

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

class UserDetailApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

user_detail_api_view = UserDetailApiView.as_view()


