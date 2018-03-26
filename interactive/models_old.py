from django.db import models
from chats.models import ChatGroup, LocalChat, Topic, GlobalChat
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.staticfiles.templatetags.staticfiles import static


User = settings.AUTH_USER_MODEL


class Message(models.Model):
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, blank=True, null=True, related_name="chatgroup_messages")
    globalchat = models.ForeignKey(GlobalChat, on_delete=models.CASCADE, blank=True, null=True, related_name="globalchat_messages")
    localchat = models.ForeignKey(LocalChat, on_delete=models.CASCADE, blank=True, null=True, related_name="localchat_messages")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True, related_name="topic_messages")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # If a message has a photo or is a photo, then it will be stored here
    photo = models.ImageField(upload_to="message_photo", blank=True, null=True)

    # A flag message -> used to display if someone joins or leaves the chat, etc
    # Pretty much should consist of a user and an action
    # Already have a used, the action is called a flag
    flag = models.TextField(blank=True, null=True)




    # new fieds
    likers = models.ManyToManyField(User, blank=True, related_name="likers")
    dislikers = models.ManyToManyField(User, blank=True, related_name="dislikers")



    def __str__(self):
        return str(self.user.username) + " : " + self.text[:40]

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def get_absolute_url_room(self): # get the absolute url of the room the message is in
        if self.globalchat:
            return reverse("chatroom", kwargs={'chat_room_type': "globalchat", 'label': self.globalchat.label })
        elif self.topic:
            return reverse("chatroom", kwargs={'chat_room_type': "topic", 'label': self.topic.label})

        elif self.localchat:
            return reverse("chatroom", kwargs={'chat_room_type': "localchat", 'label': self.localchat.label})


    def get_message_type(self):
        # Currently the message can be of 2 types
        # A text message or a photo message

        if self.photo:
            return "photo"

        elif self.text:
            return "text"

        elif self.flag:
            return "flag"        
        

    def get_number_of_likes(self):
        return self.likers.count()

    def get_number_of_dislikes(self):
        return self.dislikers.count()


    def has_related_post(self):
        return hasattr(self, 'post')

    def get_url_for_avatar_of_message_sender(self):
           

        return self.user.profile.get_absolute_url_for_avatar()

    def as_dict(self):
        return {'user': self.user.username, 'text': self.text, 'timestamp': self.formatted_timestamp, 'profile_avatar': self.get_url_for_avatar_of_message_sender(), 'message_id': self.id, 'number_of_likes': self.get_number_of_likes(), 'profile_link': self.user.profile.get_absolute_url(), 'message_type': self.get_message_type()}

    def as_dict_photo_message(self):
        return {'user': self.user.username, 'timestamp': self.formatted_timestamp, 'profile_avatar': self.get_url_for_avatar_of_message_sender(), 'message_id': self.id, 'number_of_likes': self.get_number_of_likes(), 'profile_link': self.user.profile.get_absolute_url(), 'message_type': self.get_message_type(), 'photo_url': self.photo.url}

    def as_dict_flag_message(self):
        return {'user': self.user.username, 'timestamp': self.formatted_timestamp, 'profile_avatar': self.get_url_for_avatar_of_message_sender(), 'message_id': self.id, 'profile_link': self.user.profile.get_absolute_url(), 'message_type': self.get_message_type(), 'flag': self.flag}    

            
    @property
    def short_text(self):
        # returns a shortened text of the message
        return self.text[0:144]

    def very_short_text(self):
    
        return self.text[0:40]


    def longer_than_144(self):
        # returns true if the message is longer than 144 character
        if len(self.text) > 144:
            return True
        else:
            return False    


class Post(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    likers = models.ManyToManyField(User, blank=True, related_name="post_likers")
    dislikers = models.ManyToManyField(User, blank=True, related_name="post_dislikers")




    def __str__(self):
        return self.message.text[:40]

    def get_number_of_comments(self):
        return self.postcomment_set.all().count()

    class Meta:
        ordering = ['-timestamp']

    def get_total_number_of_likes(self):
        return self.likers.all().count() + self.message.get_number_of_likes()


    def get_number_of_likes(self):
        return self.likers.all().count()    
            


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, blank=True, related_name="comment_likers")
    dislikers = models.ManyToManyField(User, blank=True, related_name="comment_dislikers")


    def __str__(self):
        return self.text[:40]

    def get_number_of_likes(self):
        return self.likers.count()

    def short_text(self):

        return self.text[0:144]





