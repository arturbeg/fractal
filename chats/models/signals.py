# All the signals are stored in here
# They typically command logic that happens when an object is
# saved: post_save


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)



def post_save_chatgroup_receiver(sender, instance, created, *args, **kwargs): # check if it is working/more research on signals
    
    if created:
        
        chatgroup_label = unique_label_generator(instance)
        instance.label = chatgroup_label
		instance.save()
		globalchat, is_created = GlobalChat.objects.get_or_create(chatgroup=instance, label=instance.label)



post_save.connect(post_save_chatgroup_receiver, sender=ChatGroup)

