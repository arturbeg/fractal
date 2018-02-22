from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL



class Profile(models.Model):
   
    # Media Upload To -> decide how to store media files 
    user 		= models.OneToOneField(User, on_delete=models.CASCADE)
    followers 	= models.ManyToManyField(User, related_name="is_following")
    about 		= models.CharField(max_length=200, blank=True)
    avatar 		= models.ImageField(upload_to="profile_avatar", blank=True, null=True)

    timestamp 	= models.DateTimeField(auto_now_add=True)


    # Some info about the REST API related to the Profile Class

    
    # methods are below

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
        

