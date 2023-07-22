from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from Accounts.models import UserProfile
from django.contrib.auth.models import User
from Followers.models import Follow

def handleFollowers(request):
    return HttpResponse('Followers')


def list_profiles(request):
    profiles_list = UserProfile.objects.all()
    

    return render(request,'Followers/list_profile.html',{'profile_list':profiles_list})

def visit_profile(request,uname):
    user_detail = User.objects.get(username=uname)
    profile_detail = UserProfile.objects.get(user=user_detail)

    context = {
        'user_detail':user_detail,
        'profile_detail':profile_detail
    }
    if request.method == 'POST':
        follower = request.user
        print(follower)
        user_to_follow = get_object_or_404(User, username=uname)

        return redirect(f'/followers/visit_profile/{user_detail.username}')

    return render(request,'Followers/visit_profile.html',context)