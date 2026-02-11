from django.urls import path

from users.views import admin_dashboard, sign_in, sign_up, sign_out, activate_account
urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-in/', sign_in, name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
    path('activate/<int:uid>/<str:token>/', activate_account, name='activate_account'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]
