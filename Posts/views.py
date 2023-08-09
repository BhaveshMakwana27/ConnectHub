from django.shortcuts import render,redirect,HttpResponse
from Posts.models import Post,PostImages,PostLike,PostComment
from django.contrib import messages
from django.db.models import Q
from Accounts.models import UserProfile
from Posts.templatetags import getDict
from django.contrib.auth.models import User
import json


def getPostDetails(request,filteredPost):
    '''Getting All Posts with details'''
    postDict = {}
    liker = UserProfile.objects.filter(user=request.user.id)
    for post in filteredPost:
        postId = post.post_id
        photoSet = PostImages.objects.filter(post=post) # getting set of photos of post
        post_like = PostLike.objects.filter(post=post) # getting likes to count
        post_liker = PostLike.objects.filter(post=post,liker__in=liker).values('liker') # getting liker to check if the liker is the current logged in user
        post_comments = PostComment.objects.filter(post=post,parent=None).order_by('-timeStamp') # getting all comments that are not replies
        post_comments_replies = PostComment.objects.filter(post=post).exclude(parent=None).order_by('-timeStamp') # getting all replies
        post_comments_replies_dict = {}
        for reply in post_comments_replies: # dividing all replies to their parent comments with key and value
            if reply.parent.comment_id not in post_comments_replies_dict.keys():
                post_comments_replies_dict[reply.parent.comment_id] = [reply]
            else:
                post_comments_replies_dict[reply.parent.comment_id].append(reply)
        postDict['post'+str(postId)] = {
            'post':post,
            'post_images':photoSet,
            'post_like_count':post_like,
            'post_liker':post_liker,
            'post_comments':post_comments,
            'post_comments_replies':post_comments_replies_dict,
        }
    return postDict


def handlePosts(request):
    if UserProfile.objects.filter(user=request.user.id).exists():
        currUser = UserProfile.objects.get(user=request.user.id)
    else:
        currUser = None
    allPosts = Post.objects.all().order_by('-uploadDate')
    postDict = getPostDetails(request,allPosts)
    context = {
        'allPost':postDict,
        'currUser': currUser
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
        
def handleComments(request):
    if request.method=='POST':
        comment = request.POST.get('comment')
        user = UserProfile.objects.get(user=request.user.id)
        post_id = request.POST.get('post_id')
        post = Post.objects.get(post_id=post_id)
        parent_id = request.POST.get('parent_id')
        if parent_id=='':
            comm = PostComment(comment=comment,commenter=user,post=post)
        else:
            parent = PostComment.objects.get(comment_id=parent_id)
            comm = PostComment(comment=comment,commenter=user,post=post,parent=parent)

        comm.save()
        return redirect('/')
    return redirect('/')


def handleSearch(request):
    if request.method == 'POST':
        searchTxt = request.POST.get('search')

        qUserResult = UserProfile.objects.filter(user__in=User.objects.filter(
            Q(username__icontains=searchTxt) | 
            Q(first_name__icontains=searchTxt) | 
            Q(last_name__icontains=searchTxt)
        ).values('id'))

        if UserProfile.objects.filter(user=request.user.id).exists():
            currUser = UserProfile.objects.get(user=request.user.id)
        else:
            currUser = None
        qPostResults = Post.objects.filter(
            Q(uploader__in=qUserResult) | Q(post_description__icontains=searchTxt)
        ).order_by('-uploadDate')
        postDict = getPostDetails(request,qPostResults)
        
        context = {
            'qUserResults':qUserResult,
            'qPostResults':postDict,
            'currUser': currUser,
            'query':searchTxt
        }
        return render(request,'Posts/search.html',context)
    return render(request,'Posts/search.html')

def handleProfilePosts(request,uname):
    user = User.objects.get(username=uname)
    if UserProfile.objects.filter(user=request.user.id).exists():
        currUser = UserProfile.objects.get(user=request.user.id)
    else:
        currUser = None
    profile = UserProfile.objects.get(user=user.id)
    filterPosts = Post.objects.filter(uploader=profile).order_by('-uploadDate')
    profilePosts = getPostDetails(request,filterPosts)

    context = {
        'currUser': currUser,
        'profilePosts':profilePosts,
        'user':user
    }

    return render(request,'Posts/profilePosts.html',context)