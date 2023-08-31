from django.urls import path

from accounts.views import (SignInView,
                            SignUpView,
                            SignOutView,
                            ProfileView,
                            ChangePasswordView,
                            ChangeAvatarView)

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('sign-out', SignOutView.as_view(), name='sign-out'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/password', ChangePasswordView.as_view(), name='password'),
    path('profile/avatar', ChangeAvatarView.as_view(), name='avatar'),

]