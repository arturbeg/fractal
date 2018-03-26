from django.conf.urls import url, include
from rest_framework import routers
from . import views
from .views import TopicRudView, TopicAPIView, ChatGroupRudView, ChatGroupAPIView

# the prefix is a re that will start our URLs


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    

    # Topic related urls
    url(r'^topics/(?P<pk>\d+)/$', TopicRudView.as_view(), name="topic-rud"),
    url(r'^topics/$', TopicAPIView.as_view(), name="topic-create"),


    # ChatGroup related urls
    url(r'^chatgroups/$', ChatGroupAPIView.as_view(), name="chatgroup-create"),
    url(r'^chatgroups/(?P<pk>\d+)/$', ChatGroupRudView.as_view(), name="chatgroup-rud"),


    # LocalChat related urls -> uncomment when the views and serializer are created
    url(r'^localchats/$', ChatGroupAPIView.as_view(), name="localchat-create"),
    url(r'^localchats/(?P<pk>\d+)/$', ChatGroupRudView.as_view(), name="localchat-rud"),


    # GlobalChat related urls




    # Profile related urls




] 

# With that we should be able to manipulate User models in
# a RESTful way


