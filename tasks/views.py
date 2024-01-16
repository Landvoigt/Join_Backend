from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, Token, Response, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import traceback
from tasks.serializers import TaskSerializer, TopicSerializer
from .models import Task, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

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
    
class login_user_view(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })

class create_user_view(APIView):
    def post(self, request, format=None):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        password = request.data.get('password')
        email = request.data.get('email')
        username = f"{firstname.lower()}{lastname.lower()}"

        try:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password, email=email)
                return Response({'success': 'Benutzer erfolgreich erstellt.'}, status=status.HTTP_201_CREATED)
                # return render(request, 'chat/index.html', {'user_exists': True, 'redirect': redirect})
            else:
                print(f'Benutzer bereits vorhanden für E-Mail: {email}')
                return Response({'error': 'Benutzer bereits vorhanden.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': f'Fehler beim Erstellen des Benutzers: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)