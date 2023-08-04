from typing import Collection, Optional
from django.db import models
from Accounts.models import UserProfile

class Follow(models.Model):

    # setting foreignKey to link with UserProfile Model
    # so now we have to get or set the value with UserProfile type
    follower = models.ForeignKey(UserProfile,related_name='following',default='',on_delete=models.CASCADE) # the current loggedin user
    following = models.ForeignKey(UserProfile,related_name='follower',default='',on_delete=models.CASCADE) # visited profile user

    timeStamp = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f'{self.follower.user} follows {self.following.user}'