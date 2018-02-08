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


