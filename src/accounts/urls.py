from django.urls import path, include
from .views import LogoutView, CrossAuthView, UserUpdateView, CustomLoginView
from django.contrib.auth.views import LoginView

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth')
]


