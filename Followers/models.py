from django.db import models
from Accounts.models import UserProfile

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name="follower", on_delete=models.CASCADE)
    followe_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self) :
        return f'{self.follower.user.username} follows {self.following.user.username}'