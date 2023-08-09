from django.db import models
from Accounts.models import UserProfile
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post_description = models.TextField(default='')
    uploadDate = models.DateTimeField(auto_now=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post_id} : {self.uploader.user}'
    
class PostImages(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE ,default=None)
    image = models.ImageField(upload_to='posts/images/', verbose_name='Image',default='', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f'{self.post} : {self.image}'
    
class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE ,default=None)
    liker = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.liker} liked {self.post.post_description[:10]}'

class PostComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    commenter = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.comment_id} : {self.comment[0:20]} by {self.commenter.user.username}'
    