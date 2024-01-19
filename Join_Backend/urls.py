"""Join_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from contacts.views import view_contacts
from tasks.views import login_user, create_user, send_email, view_tasks, view_topics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user.as_view()),
    path('registry/', create_user.as_view()),
    path('tasks/', view_tasks.as_view()),
    path('topics/', view_topics.as_view()),
    path('contacts/', view_contacts.as_view()),
    url('send-email', send_email.as_view()),
]
