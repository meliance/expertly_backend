from rest_framework import generics, permissions
from .models import ExpertDocument
from .serializers import ExpertDocumentSerializer
from accounts.models import Expert
from rest_framework.exceptions import PermissionDenied

class ExpertDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpertDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        expert_id = self.kwargs.get('expert_id')
        queryset = ExpertDocument.objects.filter(expert_id=expert_id)
        
        # Experts can only see their own documents
        if not self.request.user.is_staff:
            expert = Expert.objects.get(user=self.request.user)
            if expert.id != int(expert_id):
                raise PermissionDenied("You can only view your own documents.")
        
        return queryset

    def perform_create(self, serializer):
        expert_id = self.kwargs.get('expert_id')
        expert = Expert.objects.get(pk=expert_id)
        
        # Verify the requesting user owns this expert profile
        if expert.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only upload documents to your own profile.")
        
        serializer.save(expert=expert)

class ExpertDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpertDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ExpertDocument.objects.all()

    def get_object(self):
        doc = super().get_object()
        
        # Only allow owners or admin to access
        if doc.expert.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You don't have permission to access this document.")
        
        return doc

    def perform_update(self, serializer):
        doc = self.get_object()
        
        # Only allow updating certain fields (not the file itself)
        allowed_fields = {'title', 'description'}
        if set(serializer.validated_data.keys()) - allowed_fields:
            raise PermissionDenied("You can only update title and description.")
        
        serializer.save()
