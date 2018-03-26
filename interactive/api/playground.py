# Consumers.py


import re
import json
from channels import Group
from chats.models import GlobalChat, LocalChat, Topic
from django.contrib.auth.models import User

from channels.sessions import channel_session
from chats.models import Topic, LocalChat, GlobalChat
from interactive.models import Message
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from channels.asgi import get_channel_layer




@http_session_user
@channel_session
def ws_connect(message):





    list = message['path'].strip('/').split('/')
    prefix = list[0]
    room_type = list[1]
    room_label = list[2]



    # In here creating a flag message
    if room_type == "topic":
        room = Topic.objects.get(label=room_label)
        #m = room.topic_messages.create(text="", flag="ws_connect", user=User.objects.get(id=message.user.id), chatgroup=room.chatgroup)  


    elif room_type == "localchat":
        room = LocalChat.objects.get(label=room_label)
        #m = room.localchat_messages.create(text="", flag="ws_connect", user=User.objects.get(id=message.user.id), chatgroup=room.chatgroup)

    elif room_type == "globalchat":
        room = GlobalChat.objects.get(label=room_label)
        #m = room.globalchat_messages.create(text="", flag="ws_connect", user=User.objects.get(id=message.user.id), chatgroup=room.chatgroup)

    # Later in this function need to send this message as a    


    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    message.channel_session['room_label'] = room.label

    message.channel_session['room_type'] = room_type




    message.channel_session['message_user_id'] = message.user.id


    user = User.objects.get(id=message.user.id)

    room.current_participants.add(user)







    message.channel_session['message_user_avatar_url'] = message.user.profile.get_absolute_url_for_avatar()





    Group('m-' + room_type + room_label, channel_layer=message.channel_layer).add(message.reply_channel)


    username = user.username
    avatar = user.profile.get_absolute_url_for_avatar()

    #Group('m-' + room_type + room_label, channel_layer=message.channel_layer).send({'data': json.dumps(m.as_dict_flag_message())})


   





















@channel_session
@channel_session_user
def ws_receive(message):


    data = json.loads(message['text'])
    message_type = data['message_type']
    print("The message type has been received by the consumer, it is " + message_type)


    if message_type=="photo":
        data = json.loads(message['text'])
        message_id = int(data['text'])
        m = Message.objects.get(id=message_id)
        room_type = message.channel_session['room_type']
        room_label = message.channel_session['room_label']
        print("The photo url is " + m.photo.url)
        Group('m-' + room_type + room_label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict_photo_message())})

    elif message_type=="text":    
        print("The message type is text")
        message_user_id = message.channel_session['message_user_id']

        room_type = message.channel_session['room_type']
        room_label = message.channel_session['room_label']


        data = json.loads(message['text'])

        if room_type == "topic":
            room = Topic.objects.get(label=room_label)
            m = room.topic_messages.create(text=data['text'], user=User.objects.get(id=message_user_id), chatgroup=room.chatgroup)  

        elif room_type == "localchat":
            room = LocalChat.objects.get(label=room_label)
            m = room.localchat_messages.create(text=data['text'], user=User.objects.get(id=message_user_id), chatgroup=room.chatgroup)

        elif room_type == "globalchat":
            room = GlobalChat.objects.get(label=room_label)
            m = room.globalchat_messages.create(text=data['text'], user=User.objects.get(id=message_user_id), chatgroup=room.chatgroup)

        Group('m-' + room_type + room_label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

    elif message_type=="flag":
        data = json.loads(message['text'])
        message_id = int(data['text'])
        m = Message.objects.get(id=message_id)
        room_type = message.channel_session['room_type']
        room_label = message.channel_session['room_label']
        #print("The photo url is " + m.photo.url)
        Group('m-' + room_type + room_label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict_flag_message())}) 







@channel_session_user
@channel_session
def ws_disconnect(message):


    room_label = message.channel_session['room_label']
    room_type = message.channel_session['room_type']



    if room_type == "topic":
        room = Topic.objects.get(label=room_label)

    elif room_type == "localchat":
        room = LocalChat.objects.get(label=room_label)

    elif room_type == "globalchat":
        room = GlobalChat.objects.get(label=room_label)




    user_id = message.channel_session['message_user_id']
    user = User.objects.get(id=user_id)

    room.current_participants.remove(user)





    Group('m-' + room_type + room_label).discard(message.reply_channel)

    Group('m-' + room_type + room_label, channel_layer=message.channel_layer).discard(message.reply_channel)




# Views.py

from django.shortcuts import render, get_object_or_404
from .models import Message, Post
from chats.models import Topic, LocalChat, GlobalChat, ChatGroup
from django.shortcuts import render, redirect
from django.views.generic import RedirectView, DetailView
from chats.forms import TopicUpdateForm, LocalChatCreateForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.http import HttpResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from chats.utilities import unique_label_generator
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.models import Notification



def new_flag_message(request):

    
    room_id = request.POST.get("room_id")
    room_type = request.POST.get("room_type")
    flag = request.POST.get("flag")




    if room_type == "Topic":
        room = Topic.objects.get(id=room_id)
        m = room.topic_messages.create(text="", user=request.user, chatgroup=room.chatgroup, flag=flag)

    elif room_type == "Local Chat":
        room = LocalChat.objects.get(id=room_id)
        m = room.localchat_messages.create(text="", user=request.user, chatgroup=room.chatgroup, flag=flag)

    elif room_type == "Global Chat":
        room = GlobalChat.objects.get(id=room_id)
        m = room.globalchat_messages.create(text="", user=request.user, chatgroup=room.chatgroup, flag=flag)


    message_id = m.id

    # Flag is created at this point


    
    return JsonResponse({'room_id': room_id, 'message_id':message_id})    


def load_more_messages(request):

    template_name = 'interactive/load_new_messages.html'
    
    room_type = request.GET.get('type')
    print(room_type)
    label = request.GET.get('label')

    if room_type == "topic":
        room = Topic.objects.get(label=label)
        queryset = room.topic_messages.order_by('-timestamp')
    elif room_type == "localchat":
        room = LocalChat.objects.get(label=label)
        queryset = room.localchat_messages.order_by('-timestamp')
    else:
        room = GlobalChat.objects.get(label=label)
        queryset = room.globalchat_messages.order_by('-timestamp')






    paginator = Paginator(queryset, 20) # Show 20 messages per page

    page = request.GET.get('page')
    
    messages = paginator.page(page)

    # Here we reverse the messages

    messages = reversed(messages) 

    context = {"messages": messages} 

    



    return render(request,template_name=template_name,context=context)



def upload_message_photo(request):

   
    if request.method == 'POST':
        room_id = request.POST.get("room_id")
        room_type = request.POST.get("room_type")
        photo = request.FILES.get('photo')
        print(photo)

        if room_type == "Topic":
            room = Topic.objects.get(id=room_id)
            m = room.topic_messages.create(text="", user=User.objects.get(id=request.user.id), chatgroup=room.chatgroup, photo=photo)  # need to finish editing

        elif room_type == "Local Chat":
            room = LocalChat.objects.get(id=room_id)
            m = room.localchat_messages.create(text="", user=User.objects.get(id=request.user.id), chatgroup=room.chatgroup, photo=photo)

        elif room_type == "Global Chat":
            room = GlobalChat.objects.get(id=room_id)
            m = room.globalchat_messages.create(text="", user=User.objects.get(id=request.user.id), chatgroup=room.chatgroup, photo=photo)


        message_id = m.id


    return JsonResponse({'message':'The photo was successfully uploaded','room_id': room_id, 'message_id':message_id})

def delete_topic(request):

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id)

        chatgroup = topic.chatgroup

        topic.delete()

        print("The topic has been deleted")


        # The remaining code is needed to redirect the user to the globalchat page

        redirect_url = chatgroup.globalchat.get_absolute_url()




    return JsonResponse({"topic_id": topic_id, 'redirect_url': redirect_url})


def delete_localchat(request):

    if request.method == 'POST':
        localchat_id = request.POST.get('localchat_id')
        localchat = get_object_or_404(LocalChat, id=localchat_id)

        chatgroup = localchat.chatgroup

        localchat.delete()

        print("The localchat has been deleted")


        # The remaining code is needed to redirect the user to the globalchat page

        redirect_url = chatgroup.globalchat.get_absolute_url()




    return JsonResponse({"localchat_id": localchat_id, 'redirect_url': redirect_url})

def share_post(request):

    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        already_posted = False


        if Post.objects.filter(message = message).exists():

            Post.objects.filter(message = message).delete()
            already_posted = False


        else:
            post = Post.objects.create(message=message)

            post.save()

            #notification = Notification.objects.create(text="share_post",user=post_owner, user_2=user, post=post)
            already_posted = True



    return JsonResponse({"already_posted": already_posted, "message_id": message_id})





def like_a_message(request):
    print("Ajax liking a message........")
    if request.method == 'POST':
        user = request.user
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        message_owner = message.user

        if message.likers.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            message.likers.remove(user)
            print("You removed your like")
            is_liked = False
        else:
            # add a new like for a company
            message.likers.add(user)
            print("You liked this")

            notification = Notification.objects.create(text="like_a_message",user=message_owner, user_2=user, message=message)
            notification.save()
            # Saved the notification to the database
            
            is_liked = True

    context = {'likes_count': message.get_number_of_likes(), 'message_id': message_id, 'is_liked': is_liked}

    return HttpResponse(json.dumps(context), content_type='application/json')



def search_chat_room(request):

    print("Ajax Searching Chat Rooms..........")
    query = request.GET.get('q')
    modelToSearch = request.GET.get('modelToSearch')
    chatgroup_id = request.GET.get('chatgroup_id')
    is_localchat = modelToSearch == 'localChat'

    if query is not None and query != '' and request.is_ajax():

        if modelToSearch == "localChat":
            results = LocalChat.objects.filter(
                Q(name__icontains=query) & Q(chatgroup__id=chatgroup_id)
            )

            print(results)
        else:
            results = Topic.objects.filter(

                Q(name__icontains=query) & Q(chatgroup=chatgroup_id)
            )
            print(results)


        return render(
            request, 'interactive/results.html',
            {'results': results, 'is_localChat': is_localchat}
        )
    return render(
        request, 'interactive/results.html', {'is_localChat': is_localchat}
    )

'''
def chat_room_search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        model = request.GET.get('modelToSearch')
        print(model)
        is_localchat = model == 'localChat'
        #print(is_localchat)



        if q is not "":
            if model == 'localChat':
                results = LocalChat.objects.filter(
                    Q(name__icontains=q))
            else:
                results = Topic.objects.filter(
                    Q(name__icontains=q))

                print(results)







            return render(request, 'interactive/results.html', {'results': results, 'is_localchat': is_localchat})



'''



@ensure_csrf_cookie
def chat_room(request, label, chat_room_type):

    print(label)
    print(chat_room_type)

    if chat_room_type == "topic":
        room, created = Topic.objects.get_or_create(label=label)
        messages = reversed(room.topic_messages.order_by('-timestamp')[0:20])
        total_number_of_messages = room.topic_messages.count()


    elif chat_room_type == "localchat":
        room, created = LocalChat.objects.get_or_create(label=label)
        messages = reversed(room.localchat_messages.order_by('-timestamp')[0:20])
        total_number_of_messages = room.localchat_messages.count()
    elif chat_room_type == "globalchat":
        room, created = GlobalChat.objects.get_or_create(label=label)
        messages = reversed(room.globalchat_messages.order_by('-timestamp')[0:20])
        total_number_of_messages = room.globalchat_messages.count()
    else:
        print("Nothing")
        total_number_of_messages = 0

    
    if request.user.is_authenticated:
        request_user_avatar_url = request.user.profile.get_absolute_url_for_avatar()    
        print(request_user_avatar_url)
        user_is_authenticated = True

    else:
        user_is_authenticated = False
        request_user_avatar_url = None


    # Count the number of pages

    number_of_pages = (total_number_of_messages // 20) + 1





    list_of_localchats = room.chatgroup.localchat_set.all()


    list_of_topics = room.chatgroup.topic_set.all()






    # Now need to get the most liked message in the localchat


    chatgroup = room.chatgroup.name

    chatgroup_id = room.chatgroup.id

    is_owner = request.user.id == room.get_owner()
    print(is_owner)




    # Settings of the room -> changes made to the chatroom







    if request.method == "POST":

        if chat_room_type == "topic":
            form = TopicUpdateForm(request.POST, request.FILES)
        elif chat_room_type == "localchat":
            form = LocalChatCreateForm(request.POST, request.FILES)


        if form.is_valid():


            chatgroup_id = room.chatgroup.id


            # updateRoom is the same object as the room since it has the same id, have to do it because the form does not
            # contain all the necessary fields, otherwise a new instance is created

            updatedRoom = form.save(commit=False)

            updatedRoom.chatgroup = ChatGroup.objects.get(id=chatgroup_id)

            updatedRoom.id = room.id

            updatedRoom.label = room.label

            updatedRoom.timestamp = room.timestamp



            if not updatedRoom.avatar: # If the user does not put anything for the avatar, we assign the old one
                updatedRoom.avatar = room.avatar

            if updatedRoom.get_room_type() == "Topic":
                updatedRoom.owner = room.owner # carefully check the part with the owner



            updatedRoom.save()


            return HttpResponseRedirect(room.get_absolute_url())























    return render(request, "interactive/room.html", context = {
        'chatgroup': chatgroup,
        'chat_room_type': chat_room_type,
        'room': room,
        'messages': messages,
        'localchats': list_of_localchats,
        'is_owner': is_owner,
        'topics': list_of_topics,
        'request_user_avatar': request_user_avatar_url,
        'chatgroup_id': chatgroup_id,
        'user_is_authenticated': user_is_authenticated,
        'total_number_of_messages': total_number_of_messages,
        'number_of_pages': number_of_pages
        #'form': form,
    })




def create_local_chat(request, chatgroup_id):

    chatgroup_id = chatgroup_id
    form         = LocalChatCreateForm(request.POST, request.FILES)

    if form.is_valid():

        newLocalChat = form.save(commit=False)
        newLocalChat.chatgroup = ChatGroup.objects.get(id=chatgroup_id)
        #Put this in the post save method in the chats.models

        newLocalChat.save()

        user = request.user
        newLocalChat.participants.add(user)

        newLocalChat.save()

    try:
        label = unique_label_generator(newLocalChat)
        newLocalChat.label = label
        newLocalChat.save()    
    except:
        print("The localchat was not created")

    return HttpResponseRedirect(newLocalChat.get_absolute_url())



'''
def new_local_chat(request):



    chatgroup_id = request.POST.get('chatgroup_id')
    form  = LocalChatCreateForm(request.POST, request.FILES)




    if form.is_valid():



        newLocalChat = form.save(commit=False)

        newLocalChat.chatgroup = ChatGroup.objects.get(id=chatgroup_id)

        newLocalChat.label = unique_label_generator(newLocalChat)








        newLocalChat.save()


    redirect_url = newLocalChat.get_absolute_url    
    return HttpResponseRedirect(redirect_url)     

'''



















'''

    Show the room, with latest messages.
    The template for this view has the WebSocket business to send and stream messages,
    so see the template for where the magic happens.

    '''
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit.    