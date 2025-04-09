from rest_framework import generics
from accounts.models import Expert
from .serializers import ExpertSerializer
from django.db.models import Q

class ExpertSearchView(generics.ListAPIView):
    serializer_class = ExpertSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Expert.objects.filter(
                Q(name__icontains=query) | Q(consultation_fields__icontains=query)
            )
        return Expert.objects.all()