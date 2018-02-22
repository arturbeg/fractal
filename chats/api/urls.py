from django.conf.urls import url, include
from rest_framework import routers
from . import views

# the prefix is a re that will start our URLs


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
] 

# With that we should be able to manipulate User models in
# a RESTful way


