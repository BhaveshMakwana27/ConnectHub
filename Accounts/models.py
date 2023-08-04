from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    userProfile_id = models.AutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to='user/images/',default='', height_field=None, width_field=None, max_length=None)
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    bio = models.TextField(default='')
    registration_date = models.DateField(auto_now=False)
    last_login_date = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"id - {self.userProfile_id} : {self.user.username}"
    

    