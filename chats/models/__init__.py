# The packages that the components require to function
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.staticfiles.templatetags.staticfiles import static

# Creating the user object so it can be referenced by the models
User = settings.AUTH_USER_MODEL



# The components of the database
from .localchat import LocalChat
from .topic import Topic
from .chatgroup import ChatGroup
from .profile import Profile
from .globalchat import GlobalChat
