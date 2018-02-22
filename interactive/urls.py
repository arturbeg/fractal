from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve










urlpatterns = [

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

