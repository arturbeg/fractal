class Profile(models.Model):
   
   	# Media Upload To -> decide how to store media files 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="is_following")
    about = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to="profile_avatar", blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)



    # methods later
    