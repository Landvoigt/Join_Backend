from rest_framework.authtoken.views import ObtainAuthToken, Token, Response, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import traceback
from tasks.serializers import TaskSerializer, TopicSerializer
from .models import Task, Topic
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, get_connection
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from django.http import JsonResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
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


from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print("Signal received!")

    subject = 'Password Reset'
    message = (
        f'Hello {reset_password_token.user.username},\n\n'
        'You have requested to reset your password. Please click the following link to reset it:\n'
        f'{instance.request.build_absolute_uri(reverse("password_reset:reset-password-confirm"))}?token={reset_password_token.key}'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [reset_password_token.user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # """
    # Handles password reset tokens
    # When a token is created, an e-mail needs to be sent to the user
    # :param sender: View Class that sent the signal
    # :param instance: View Instance that sent the signal
    # :param reset_password_token: Token Model Object
    # :param args:
    # :param kwargs:
    # :return:
    # """
    # # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     'email': reset_password_token.user.email,
    #     'reset_password_url': "{}?token={}".format(
    #         instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #         reset_password_token.key)
    # }

    # # render email text
    # # email_html_message = render_to_string('email/user_reset_password.html', context)
    # # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     # email_plaintext_message,
    #     # from:
    #     "noreply@somehost.local",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()


# reset_password_token_created.connect(password_reset_token_created, sender=User)
# import string
# import secrets 

# def generate_new_password(length=12):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     password = ''.join(secrets.choice(characters) for _ in range(length))
#     return password


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, a response with a token needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """

#     # Check if the user is found
#     if reset_password_token.user:
#         # Generate a new password or token (modify this part as needed)
#         new_password = generate_new_password()

#         # Set the new password for the user (you may want to save it to the user model)
#         reset_password_token.user.set_password(new_password)
#         reset_password_token.user.save()

#         # Generate a token for the user
#         uidb64 = urlsafe_base64_encode(force_bytes(reset_password_token.user.pk))
#         token = PasswordResetTokenGenerator().make_token(reset_password_token.user)

#         # Include the new password or token in the response
#         response_data = {
#             'status': 'OK',
#             'uidb64': uidb64,
#             'token': token,
#         }

#         # context = {
#         #     'current_user': reset_password_token.user,
#         #     'username': reset_password_token.user.username,
#         #     'email': reset_password_token.user.email,
#         #     'reset_password_url': "{}?token={}".format(
#         #         instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
#         #         reset_password_token.key),
#         #     'new_password': new_password,
#         # }

#         # # render email text
#         # email_html_message = render_to_string('email/user_reset_password.html', context)
#         # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)


#         # msg = EmailMultiAlternatives(
#         #     # title:
#         #     "Password Reset for {title}".format(title="Hallo"),
#         #     # message:
#         #     # email_plaintext_message,
#         #     # from:
#         #     "noreply@somehost.local",
#         #     # to:
#         #     [reset_password_token.user.email]
#         # )
#         # # msg.attach_alternative(email_html_message, "text/html")
#         # msg.send()

#         connection = get_connection() # uses SMTP server specified in settings.py
#         connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()

#         # html_content = render_to_string('newsletter.html', {'newsletter': n,})               
#         text_content = "Yes"                     
#         msg = EmailMultiAlternatives("subject", text_content, "from@bla", [reset_password_token.user.email], connection=connection)                                      
#         # msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
#         msg.send() 

#         connection.close()
#     else:
#         response_data = {
#             'status': 'User not found',
#         }

#     return JsonResponse(response_data)


        
# from django.http import JsonResponse

# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # Check if the user associated with the token exists
#     user = reset_password_token.user
#     if user:
#         # For testing purposes, return a JSON response
#         response_data = {'message': 'It works!', 'user_found': True}
#     else:
#         response_data = {'message': 'User not found!', 'user_found': False}

#     return JsonResponse(response_data)
