from rest_framework.authtoken.views import ObtainAuthToken, Token, Response, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import traceback
from tasks.serializers import TaskSerializer, TopicSerializer
from .models import Task, Topic
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

class view_tasks(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)  
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create task.'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        task_id = request.data.get('id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to update task.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        task_id = request.data.get('id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({'success': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class view_topics(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)      
    
    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create topic.'}, status=status.HTTP_400_BAD_REQUEST)
    
class login_user(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email doesnt exist.'})

        if not user.check_password(password):
            return Response({'error': 'Invalid password.'})

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': f'{user.first_name} {user.last_name}',
        })

class create_user(APIView):
    def post(self, request, format=None):
        firstname = request.data.get('first_name')
        lastname = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')
        username = f"{firstname.lower()}{lastname.lower()}"

        try:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password, email=email)
                return Response({'success': 'User created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                print(f'Benutzer bereits vorhanden für E-Mail: {email}')
                return Response({'error': 'User already exists.'})
        except Exception as e:
            traceback.print_exc()
            return Response({'error': f'Error creating user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    subject = 'Password Reset'
    message = (
        f'Hello {reset_password_token.user.username},\n\n'
        'You have requested to reset your password. Please click the following link to reset it:\n'
        f'https://joinnew.timvoigt.ch/html/resetPassword.html?token={reset_password_token.key}'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reset_password_token.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class reset_user_pw(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({'error': 'Token and new_password are required.'}, status=400)
        
        user = get_object_or_404(User, password_reset_token=token)
        user.password = make_password(new_password)
        user.save()

        return Response({'message': 'Password reset successfully.'})