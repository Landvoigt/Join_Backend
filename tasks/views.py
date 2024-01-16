from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, Token, Response, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tasks.serializers import TaskSerializer, TopicSerializer
from .models import Task, Topic

class view_tasks(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)  

class view_topics(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Topic.objects.all()
        serializer = TopicSerializer(tasks, many=True)
        return Response(serializer.data)      
    
class login_view(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username':user.username,
            'email': user.email,
        })