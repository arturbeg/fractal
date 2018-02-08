from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve



from .views import chat_room, search_chat_room, like_a_message, share_post, delete_localchat, create_local_chat,delete_topic, upload_message_photo, load_more_messages, new_flag_message      #, MessageLikeRedirect






urlpatterns = [

   url(r'^(?P<chat_room_type>[\w-]{,50})/(?P<label>[\w-]{,50})/$', chat_room, name='chatroom'),



   #url(r'^chat_search/$', chat_room_search, name='chat_room_search'),

   url(r'^search_chat_room/$', search_chat_room, name='search_chat_room'),


   url(r'^like/$', like_a_message, name='like'),

   url(r'^share_post/$', share_post, name='share_post'),

   url(r'^delete_localchat/$', delete_localchat, name='delete_localchat'),

   url(r'^delete_topic/$', delete_topic, name='delete_topic'),


   url(r'^load_more_messages/$', load_more_messages, name='load_more_messages'),




   # Old new_local_chat that uses Ajax -> hard to extract image from there
   #url(r'^new_local_chat/$', new_local_chat, name='new_local_chat'),


   # New new_local_chat below

   url(r'^create/localchat/(?P<chatgroup_id>[-\w]+)/$', create_local_chat, name='create-local-chat'),

   url(r'^upload_message_photo/$', upload_message_photo, name='upload_message_photo'),


   url(r'^new_flag_message/$', new_flag_message , name='new_flag_message'),





]




























#url(r'^(?P<chat_room_type>[\w-]{,50})/(?P<label>[\w-]{,50})/(?P<message_pk>[-\w]+)/like$', MessageLikeRedirect.as_view(), name='messagelike'),

   # In the case of a global chat, the chat_room_type is globalchat and the label is just the
   # chatgroup label
   #url(r'^(?P<chat_room_type>[\w-]{,50})/(?P<label>[\w-]{,50})/media/(?P<path>.*)$', serve, {
    #        'document_root': settings.MEDIA_ROOT,
     #  })


    #url(r'^hello/$', chat_room, name='chatroom'),


#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# work out the deal with the media files

