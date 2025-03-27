from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def api_home(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)