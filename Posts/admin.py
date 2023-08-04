from django.contrib import admin
from .models import Post,PostImages,PostLike
# Register your models here.
admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(PostLike)