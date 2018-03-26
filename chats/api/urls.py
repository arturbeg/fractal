from django.conf.urls import url, include
from rest_framework import routers
from . import views
from .views import ChatGroupViewSet, UserViewSet, TopicViewSet, LocalChatViewSet

# the prefix is a re that will start our URLs


#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)


router = routers.DefaultRouter()
router.register('chatgroups', ChatGroupViewSet)
router.register('users', UserViewSet)
router.register('topics', TopicViewSet)
router.register('localchats', LocalChatViewSet)




urlpatterns = router.urls


