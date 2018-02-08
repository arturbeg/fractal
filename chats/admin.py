from django.contrib import admin
from .models import ChatGroup, Topic, LocalChat, Profile, GlobalChat


# Register your models here.



admin.site.register(ChatGroup)
admin.site.register(Topic)
admin.site.register(LocalChat)
admin.site.register(Profile)
admin.site.register(GlobalChat)

