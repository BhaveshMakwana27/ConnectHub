from django.shortcuts import render,redirect,HttpResponse
from Posts.models import Post,PostImages,PostLike
from django.contrib import messages
from Accounts.models import UserProfile
import json

def handlePosts(request):
    allPosts = Post.objects.all()
    liker = UserProfile.objects.filter(user=request.user.id)
    postDict = {}
    for post in allPosts:
        postId = post.post_id
        photoSet = PostImages.objects.filter(post=post)
        post_like = PostLike.objects.filter(post=post)
        post_liker = PostLike.objects.filter(post=post,liker__in=liker).values('liker')
        postDict['post'+str(postId)] = {
            'post':post,
            'post_images':photoSet,
            'post_like_count':post_like,
            'post_liker':post_liker
        }
    context = {
        'allPost':postDict
    }
    return render(request,'Posts/allPost.html',context)


def handlePostCreating(request,username):
    if request.method == "POST":
        uploader = UserProfile.objects.get(user=request.user.id)
        images = request.FILES.getlist('postImages')
        desc = request.POST.get('post_desc')
        if len(images) !=0 or desc != '':
            createPost = Post()
            if desc!='':
                createPost.post_description = desc

            createPost.uploader = uploader
            createPost.save()
            createdPostId = createPost.post_id
            for image in images:
                photo = PostImages.objects.create(post_id=createdPostId,image=image)
        else:
            messages.warning(request,'You have to fill either one field or both to create a post!!')
            return redirect('/createPost/username/')
    return render(request,'Posts/createPost.html')

def handleLikes(request,post_id):
    if request.method == 'POST':
        liker = UserProfile.objects.get(user=request.user.id)
        post = Post.objects.get(post_id=post_id)
        if PostLike.objects.filter(liker=liker,post=post).exists():
            like_post = PostLike.objects.get(liker=liker,post=post).delete()
            return HttpResponse(json.dumps({'like_status':False}))
        else:
            like_post = PostLike.objects.create(liker=liker,post=post)
            return HttpResponse(json.dumps({'like_status':True}))
