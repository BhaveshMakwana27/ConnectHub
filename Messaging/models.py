from django.db import models
from Accounts.models import UserProfile
from Followers.models import Follow

# Create your models here.
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserProfile,related_name='receiver',on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile,related_name='sender',on_delete=models.CASCADE)
    content = models.TextField(default='')
    timeStamp = models.DateTimeField()

    def __str__(self):
        return f'{self.sender.user} to {self.receiver.user}'   

class Room(models.Model):
    follow_det = models.ForeignKey(Follow,on_delete=models.CASCADE,related_name='follow_details')
    room_name = models.SlugField(default='chat')

    def __str__(self):
        return self.room_name
      

