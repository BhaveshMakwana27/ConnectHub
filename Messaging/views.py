from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Accounts.models import UserProfile
from django.contrib.auth.models import User
from Messaging.models import Message,Room
from Followers.models import Follow
from itertools import chain


def allMessageRoomListFetch(request):
    CurrUserInfo = UserProfile.objects.get(user=request.user.id)
    followers = Follow.objects.filter(follower=CurrUserInfo).values('follower')
    allMessagesRoomList = Follow.objects.filter(follower__in=followers)

    # distinct_senders = Message.objects.filter(receiver=CurrUserInfo).values('sender').distinct()
    # print(distinct_senders)
    # distinct_receivers = Message.objects.filter(sender=CurrUserInfo).values('receiver').distinct()

    # allMessages = Message.objects.filter(
    #     receiver__in=distinct_receivers,
    # ).order_by('timeStamp')
    # print(allMessages)

    return allMessagesRoomList

def handleMessageRoomList(request):
    # getting all messages list to display in messages list
    allMessages = allMessageRoomListFetch(request)
    allRooms = Room.objects.filter(follow_det__in=allMessages).values('room_name')
    messages_with_rooms = zip(allMessages, allRooms)
    return render(request,'Messaging/messages_list.html',{'messages_with_rooms':messages_with_rooms})

@login_required
def handleMessages(request,room_name):
    
    currRoom = Room.objects.filter(room_name=room_name).first() # getting curent active message room
    follow_instance = currRoom.follow_det # get following details from current room 

    # getting sender and recevier details
    sender = UserProfile.objects.get(user=request.user.id)
    receiverDet = User.objects.get(username=follow_instance.following.user)
    if receiverDet == request.user:
        currRoom = Room.objects.filter(room_name=room_name)[1]
        follow_instance = currRoom.follow_det # get following details from current room 
        receiverDet = User.objects.get(username=follow_instance.following.user)
    receiver = UserProfile.objects.get(user=receiverDet)

    # getting all messages list to display in messages list
    allMessagesList = allMessageRoomListFetch(request)
    allRooms = Room.objects.filter(follow_det__in=allMessagesList)
    messages_with_rooms = zip(allMessagesList, allRooms)

    # getting sent and recevied messages
    sentMessages = Message.objects.filter(sender=sender,receiver=receiver)
    receivedMessages = Message.objects.filter(sender=receiver,receiver=sender)
    all_messages = (sentMessages | receivedMessages).order_by('timeStamp')

    context = {
        'sender':sender,
        'room_name':currRoom,
        'receiver':receiver,
        'all_messages':all_messages,
        'messages_with_rooms':messages_with_rooms
    }

    # if request.method == 'POST':
    #     messageContent = request.POST.get('message')
    #     sendMassage = Message(sender=sender,receiver = receiver, content = messageContent)
    #     sendMassage.save()

    #     return redirect(f'/messaging/do_message/{username}')
    return render(request,'Messaging/do_message.html',context)
