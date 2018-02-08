from django.conf.urls import url
from django.contrib import admin

# Additional imports

from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.conf.urls import include


from .views import user_notifications, single_post

urlpatterns = [



  url(r'^user_notifications/$', user_notifications, name='user_notifications'),


  url(r'^single/post/$', single_post, name='single_post'),



]


