from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Accounts.models import UserProfile
from Followers.models import Follow
from Posts.models import Post,PostComment,PostImages,PostLike
import os

def handleAccount(request):
    return HttpResponse('Account')

def handleLogin(request):
    if request.method == "POST":
        loginUsername = request.POST.get('loginusername')
        loginPassword = request.POST.get('loginpassword')
        loginUser = authenticate(username=loginUsername,password=loginPassword)

        if loginUser is not None:
            login(request,loginUser)
            messages.success(request,'LoggedIn successfully...')
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials.. Please Try Again..')
            return redirect('/')
            

    return render(request,'Accounts/login.html')

def handleSignin(request):
    if request.method == "POST" :
        registration_date = datetime.now()
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('emailId')
        choosePassword = request.POST.get('choosePassword')
        confirmPassword = request.POST.get('confirmPassword')

        if choosePassword != confirmPassword:
            messages.error(request, 'Your password didnot match....')
            return redirect('/account/signin/')

        user = User.objects.create_user(username=username,email=email,password=confirmPassword)
        user.first_name = fname
        user.last_name = lname
        user.save()

        newUser = user
        userProfile = UserProfile(user=newUser,registration_date=registration_date)
        profileImage = request.FILES.get('profilePhoto')
        bio = request.POST.get('bio')

        if profileImage is not None:
            userProfile.profile_photo = profileImage
            
        if bio is not None:
            userProfile.bio = bio

        userProfile.save()
        return redirect('/account/login/')

    return render(request,'Accounts/signin.html')


def userProfileHandle(request,uname):
    curr_user = request.user
    userProfile = UserProfile.objects.filter(user=curr_user.id).first()

    # getting howmany followers and howmany following the loggedin user have
    followers_count = Follow.objects.filter(following = userProfile).count()
    following_count = Follow.objects.filter(follower = userProfile).count()

    # getting user posts
    posts = Post.objects.filter(uploader=userProfile).order_by('uploadDate')
    post_photos = PostImages.objects.filter(post__in=posts)
    cover_photos = {}
    for post_photo in post_photos:
        if post_photo.post not in cover_photos.keys():
            cover_photos[post_photo.post] = post_photo


    if request.method == 'POST':
        updateBio = request.POST.get('bio')
        profileImage = request.FILES.get('profilePhoto')
        if updateBio is not None:
            userProfile.bio = updateBio
        if profileImage is not None:
            userProfile.profile_photo = profileImage
        userProfile.save()

    context = {
        'userDetail':userProfile,
        'following_count':following_count,
        'followers_count':followers_count,
        'post_photos':post_photos,
        'cover_photos':cover_photos,
        'posts':posts
    } 
    return render(request,'Accounts/profile.html',context)


def editProfileHandle(request,uname):
    curr_user_id = request.user.id
    curr_user_profile = UserProfile.objects.filter(user=curr_user_id).first()
    context={
        'curr_detail' : curr_user_profile
    }

    if request.method == 'POST':
        #Edit User details
        curr_user = User.objects.get(username=uname)
        newUsername = request.POST.get('editUsername')
        newFirstname = request.POST.get('editFname')
        newLastname = request.POST.get('editLname')

        curr_user.username = newUsername 
        curr_user.first_name = newFirstname 
        curr_user.last_name = newLastname 
        curr_user.save()

        #Edit Profile Photo
        newProfilePhoto = request.FILES.get('editProfilePhoto')
        if newProfilePhoto is not None:
            curr_user_profilePhoto = UserProfile.objects.filter(user=curr_user_id).values('profile_photo').first()['profile_photo']
            if curr_user_profilePhoto is not None:
                os.remove('media/'+curr_user_profilePhoto)

            curr_user_profile.profile_photo = newProfilePhoto
            
        #Edit Bio
        newBio = request.POST.get('editBio')
        if newBio is not None : 
            curr_user_profile.bio = newBio

        curr_user_profile.save()
        print(curr_user.username)
        return redirect('/account/profile/'+curr_user.username)

    return render(request,'Accounts/editProfile.html',context)



def handleLogout(request):
    logout(request)
    messages.info(request,'Logged out')
    return redirect('/')