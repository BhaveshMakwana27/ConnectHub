from django.shortcuts import render,HttpResponse

def handlePosts(request):
    return render(request,'Posts/allPost.html')