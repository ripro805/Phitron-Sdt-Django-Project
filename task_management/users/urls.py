from django.urls import path

from users.views import user_login, sign_up
urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', user_login, name='login'),
]
