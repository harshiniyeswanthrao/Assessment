from django.urls import path
from .views import RegisterView, LoginView, ProfileView, login_page, register_page, admin_dashboard, user_dashboard, logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),


    path('login-page/', login_page, name='login_page'),
    path('register-page/', register_page, name='register_page'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
]
