from django.db import models
from django.conf import settings
from .chatgroup import ChatGroup
from django.db.models.signals import post_save
from .utilities import unique_label_generator

User = settings.AUTH_USER_MODEL


class GlobalChat(models.Model):
    
    chatgroup 			= models.OneToOneField(ChatGroup, on_delete=models.CASCADE)
    label 				= models.SlugField(unique=True)
    online_participants = models.ManyToManyField(User, blank=True, related_name='globalchat_online_participants')
    saves 				= models.ManyToManyField(User, blank=True, related_name='globalchat_saves')

    @property
    def owner(self):
        return self.chatgroup.user

# Signal that generates a new GlobalChat when a Chatgroup is created
def post_save_chatgroup_receiver(sender, instance, created, *args, **kwargs):

	if created:

		chatgroup_label = unique_label_generator(instance)
		instance.label = chatgroup_label
		instance.save()
		globalchat, is_created = GlobalChat.objects.get_or_create(chatgroup=instance, label=instance.label)


post_save.connect(post_save_chatgroup_receiver, sender=ChatGroup)

