from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from Accounts.models import UserProfile
from django.contrib.auth.models import User
from Followers.models import Follow
from Messaging.models import Room
from Posts.models import Post,PostComment,PostImages,PostLike


def handleFollowers(request):
    return HttpResponse('Followers')

def list_profiles(request):
    # list of all profiles in website except current loggedIn user
    profiles_list = UserProfile.objects.all().exclude(user = request.user.id)
    return render(request,'Followers/list_profile.html',{'profile_list':profiles_list})

def visit_profile(request,uname):
    # getting visited profile details
    user_detail = User.objects.get(username=uname)
    visitedProfile_detail = UserProfile.objects.get(user=user_detail)

    # getting howmany followers and howmany following that user have
    followers_count = Follow.objects.filter(following = visitedProfile_detail).count()
    following_count = Follow.objects.filter(follower = visitedProfile_detail).count()

    # checking if the current user follows the visited profile user
    loggedIn_user = UserProfile.objects.get(user=request.user.id)
    following_status = Follow.objects.filter(follower=loggedIn_user,following=visitedProfile_detail).values('follower').count()

     # getting user posts
    posts = Post.objects.filter(uploader=visitedProfile_detail).order_by('uploadDate')
    post_photos = PostImages.objects.filter(post__in=posts)
    cover_photos = {}
    for post_photo in post_photos:
        if post_photo.post not in cover_photos.keys():
            cover_photos[post_photo.post] = post_photo
    
    context = {
        'user_detail':user_detail,
        'profile_detail':visitedProfile_detail,
        'following_count':following_count,
        'followers_count':followers_count,
        'cover_photos':cover_photos
    }

    if following_status == 0:
        follow_status = False
        context['follow_status'] = follow_status
    else : 
        follow_status = True
        room_name=createRoom(loggedIn_user.user,visitedProfile_detail.user)
        context['follow_status'] = follow_status
        context['room_name'] = room_name


    # if follow or unfollow button clicked
    if request.method == 'POST':
        # the current logged user 
        follower = UserProfile.objects.get(user=request.user)

        # the visited profile user
        user_to_follow = UserProfile.objects.get(userProfile_id=request.POST.get('profileId'))

        # get which button is clicked
        whatTodo = request.POST.get('doFollowUnfollow')

        if whatTodo=='follow':
            #current user follows the visited profile user
            follow = Follow(follower = follower,following=user_to_follow)
            follow.save()
            room_name = createRoom(follower.user,user_to_follow.user)
            room = Room.objects.create(follow_det=follow,room_name=room_name)
            return redirect(f'/followers/visit_profile/{user_detail.username}')
        
        elif whatTodo=='unfollow':
            #current user unfollows the visited profile user
            follow = Follow.objects.filter(follower = follower,following=user_to_follow).delete()
            return redirect(f'/followers/visit_profile/{user_detail.username}')

    return render(request,'Followers/visit_profile.html',context)



def createRoom(sender,receiver):
    roomNameList = [str(sender),str(receiver)]
    sortedRoomname = sorted(roomNameList)
    room = 'chat-'+sortedRoomname[0]+'-'+sortedRoomname[1]
    return room

def followers_list(request,uname):
    visitedProfile = UserProfile.objects.get(user=User.objects.get(username=uname))
    followers = Follow.objects.filter(following=visitedProfile).values('follower')
    profile = UserProfile.objects.filter(userProfile_id__in=followers)
    return render(request,'Followers/followers_list.html',{'followers':profile})

def following_list(request,uname):
    visitedProfile = UserProfile.objects.get(user=User.objects.get(username=uname))
    followings = Follow.objects.filter(follower=visitedProfile).values('following')
    profile = UserProfile.objects.filter(userProfile_id__in=followings)
    return render(request,'Followers/followings_list.html',{'followings':profile})