from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import app

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('app/', app.as_view()),
]
