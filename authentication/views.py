from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Profile
from .serializers import UserSerializer, ProfileSerializer  # ✅ Import serializers

# 🟢 Function to Generate JWT Tokens
class RegisterView(APIView):
    def post(self, request):
        print("Received data:", request.data)  # 🔍 Debugging statement

        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        role = request.data.get('role', None)

        # 🔴 Debug which field is missing
        missing_fields = []
        if not username:
            missing_fields.append("username")
        if not email:
            missing_fields.append("email")
        if not password:
            missing_fields.append("password")
        if not role:
            missing_fields.append("role")

        if missing_fields:
            print("Missing fields:", missing_fields)  # 🔍 Debugging
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(user=user, role=role)

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile)

        tokens = get_tokens_for_user(user)

        return Response({
            "message": "User registered successfully!",
            "user": user_serializer.data,
            "profile": profile_serializer.data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

# Register API
# class RegisterView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         role = request.data.get('role')
#
#         if not username or not password or not role:
#             return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.create_user(username=username, password=password)
#         Profile.objects.create(user=user, role=role)
#         return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)



# 🟢 Helper Function to Generate JWT Tokens


# Login API
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.profile.role  # Send role for redirection in frontend
        })


# Profile API (Protected Route)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        return Response({
            'username': user.username,
            'role': profile.role
        })


# Django Views for HTML Pages

def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


@login_required
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})


@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login_page')
