class Room(models.Model):
	chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)  # the parent chat group
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    describtion = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="topic_avatar", blank=True)

    saves = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.SlugField(unique=True) # Unique way to name a topic/localchat in the URL

    online_participants = models.ManyToManyField(User, blank=True)


    # No methods for now -> need to pin down the structure of the database tables


    class Meta:
    	abstract: True

