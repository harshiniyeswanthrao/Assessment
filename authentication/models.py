# from django.db import models
# from django.contrib.auth.models import User
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')])
#
#     def __str__(self):
#         return self.user.username
#




from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='user'  # Default role if not provided
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
