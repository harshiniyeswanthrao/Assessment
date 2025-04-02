# from django.contrib.auth.models import User
# from rest_framework import serializers
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']
#
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['user', 'role']




# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Profile  # ✅ Import Profile model
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']
#
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile  # ✅ Ensure Profile is correctly referenced
#         fields = ['user', 'role']





from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile  # ✅ Import Profile model

# 🟢 User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # ✅ Added email for better API responses

# 🟢 Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # ✅ Serialize user details instead of just ID

    class Meta:
        model = Profile
        fields = ['user', 'role']

