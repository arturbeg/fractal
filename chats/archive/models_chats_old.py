from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime
from django.urls import reverse
import interactive
from .utilities import unique_label_generator
from allauth.account.models import EmailAddress
from django.contrib.staticfiles.templatetags.staticfiles import static

# The packages needed for ranking purposes 
from datetime import datetime, timedelta
from math import log

#from .managers import TopicManager

from django.utils.timezone import make_aware
from django.utils import timezone



User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="is_following")
    about = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to="profile_avatar", blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)


    def account_verified(self): # Checks if the user's email address has been verified
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False



    def get_number_of_followers(self):
        return self.followers.count()

    def get_number_of_following(self):
        return self.user.is_following.count()


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def get_absolute_url_for_avatar(self):
        
        if not self.avatar:

            try:


                return static('chats/default-img/default-user.jpg')

            except:
                import sys
                print(str(sys.exc_info()))    

        else:
            
            return self.avatar.url



    def get_absolute_url_followers(self):

        return reverse("profile-followers", kwargs={'pk': self.pk})


    def get_absolute_url_following(self):
        return reverse("profile-following", kwargs={'pk': self.pk})

    def get_absolute_url_chatgroups(self):

        return reverse("profile-chatgroups", kwargs={'pk': self.pk})






def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)



class ChatGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name="is_member")
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="group_avatar", blank=True)
    label = models.SlugField(unique=True)

    def get_number_of_members(self):
        return self.members.count()

    def get_absolute_url_for_avatar(self):



        if not self.avatar:
            #print("This chatgroup doesn't have an avatar yet")
            try:
                #return reverse("static", kwargs={'path': "chats/default-img/default-chatgroup.jpg"})
                return static("chats/default-img/default-chatgroup.jpg")

            except:
                import sys
                print(str(sys.exc_info()))    

        else:
            #return  reverse("media", kwargs={'path': self.avatar})
            return self.avatar.url



    def get_owner(self):
        return self.owner


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chatgroup-detail', kwargs={'pk': self.pk})








class Topic(models.Model):
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)  # the parent chat group
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    arrow_ups = models.ManyToManyField(User, related_name='arrow_ups')
    arrow_downs = models.ManyToManyField(User, related_name='arrow_downs')
    avatar = models.ImageField(upload_to="topic_avatar", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.SlugField(unique=True)

    current_participants = models.ManyToManyField(User, related_name='topic_current')



    


    # Ranking functions below, trensfer those functions into a model manager!

    def get_short_about(self):
        return self.about[0:25]


    def epoch_seconds(self):
        
        epoch = datetime(1970, 1, 1)
        epoch = make_aware(epoch, timezone.get_default_timezone())
        td = self.timestamp - epoch
        print(td)
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)




    def score(self):
        print(self.arrow_ups.count() - self.arrow_downs.count())
        return (self.arrow_ups.count() - self.arrow_downs.count())


    def trending(self):
        score = self.score()
        print(score)

        order = log(max(abs(score), 1), 10)
        if score > 0:
            sign = 1
        elif score < 0:
            sign = -1
        else:
            sign = 0    

        seconds = self.epoch_seconds() - 1134028003

        final_rank = round(sign * order + seconds / 45000, 7)

        print("The final rank of " + self.name + " is " + str(final_rank))
        return round(sign * order + seconds / 45000, 7)



    # End of the ranking functions    

    def get_name(self):
        return self.name


    def get_owner(self):
        return self.owner.id


    def get_chatgroup_owner(self):
        return self.chatgroup.owner


    def __str__(self):
        return self.name


    def get_room_type(self):
        return "Topic"

    def get_absolute_url(self):
        return reverse('chatroom', kwargs={'chat_room_type': 'topic', "label": self.label})

    def get_topic_rating(self):
        return self.arrow_ups.count() - self.arrow_downs.count()


    def get_the_most_recent_message(self):

        list_of_messages = self.topic_messages.filter(flag__isnull=True).order_by('-timestamp')[:1]

        if len(list_of_messages) == 0:
            #print("There is no messages in the local chat")
            top_message = None


        else:
            top_message = list_of_messages[0]

            # Shorten the string if necessary to fit two lines, do it as a method for the message

            print(top_message.text)

        return top_message

    def get_absolute_url_for_avatar(self):
        if not self.avatar:
            try:
                #return reverse("static", kwargs={'path': "chats/default-img/default-topic.png"})
                return static("chats/default-img/default-topic.png")
            except:
                import sys
                print(str(sys.exc_info()))    

        else:
            #return  reverse("media", kwargs={'path': self.avatar})
            return self.avatar.url

            
        




'''  Implementing the slug generator for the topic


def pre_save_topic_receiver(sender, instance, created, *args, **kwargs):
    if not instance.label:
        print("Making a label for the topic")
        instance.label = unique_label_generator(instance)


post_save.connect(pre_save_topic_receiver, sender=Topic)


'''




class LocalChat(models.Model):
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE) # the parent chat group
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="local_chat_avatar", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="is_participant")
    label = models.SlugField(unique=True)
    current_participants = models.ManyToManyField(User, related_name='localchat_current')


    def get_name(self):
        return self.name

    def get_owner(self):
        return self.chatgroup.owner.id

    def get_room_type(self):
        return "Local Chat"

    def get_absolute_url_for_avatar(self):
        if not self.avatar:
            try:
                #return reverse("static", kwargs={'path': "chats/default-img/default-localchat.png"})
                return static("chats/default-img/default-localchat.png")
            except:
                import sys
                print(str(sys.exc_info()))    

        else:
            #return  reverse("media", kwargs={'path': self.avatar})
            return self.avatar.url

    def get_absolute_url(self):
        return reverse('chatroom', kwargs={'chat_room_type': 'localchat', "label": self.label})


    def get_number_of_participants(self):
        return self.participants.count()


    def get_the_most_recent_message(self):

        list_of_messages = self.localchat_messages.filter(flag__isnull=True).order_by('-timestamp')[:1]

        if len(list_of_messages) == 0:
            #print("There is no messages in the local chat")
            top_message = None


        else:
            top_message = list_of_messages[0]
            print(top_message.text)

        return top_message


    def __str__(self):
        return self.name



class GlobalChat(models.Model):
    chatgroup = models.OneToOneField(ChatGroup, on_delete=models.CASCADE) # the parent chat group -> one to one relationship
    label = models.SlugField(unique=True)
    current_participants = models.ManyToManyField(User, related_name='globalchat_current')


    def get_name(self):
        return self.chatgroup.name

    def get_owner(self):
        return self.chatgroup.owner.id

    def get_room_type(self):
        return "Global Chat"

    def get_absolute_url_for_avatar(self):

        if not self.chatgroup.avatar:

            #return reverse("media", kwargs={'path': "group_avatar/group.png"})
            return static("chats/default-img/default-chatgroup.jpg")

        else:

            #return reverse("media", kwargs={'path': self.chatgroup.avatar}) # Uses the same avatar as the chatgroup it belongs to
            return self.chatgroup.avatar.url


    def __str__(self):
        return self.chatgroup.name


    def get_globalchat_name(self):
        return self.chatgroup.name

    def get_absolute_url(self):
        return reverse('chatroom', kwargs={'chat_room_type': 'globalchat', "label": self.label})

    def get_the_most_recent_message(self):

        list_of_messages = self.globalchat_messages.filter(flag__isnull=True).order_by('-timestamp')[:1]

        if len(list_of_messages) == 0:
            #print("There is no messages in the local chat")
            top_message = None


        else:
            top_message = list_of_messages[0]
            print(top_message.text)

        return top_message



def post_save_chatgroup_receiver(sender, instance, created, *args, **kwargs): # check if it is working/more research on signals
    if created:
        
        chatgroup_label = unique_label_generator(instance)
        instance.label = chatgroup_label

        instance.save()




        globalchat, is_created = GlobalChat.objects.get_or_create(chatgroup=instance, label=instance.label)

        #globalchat.label = instance.label

        #globalchat.save()


    

post_save.connect(post_save_chatgroup_receiver, sender=ChatGroup)




