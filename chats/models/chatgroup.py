class ChatGroup(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    describtion = models.TextField()
    members = models.ManyToManyField(User, related_name="is_member")
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="group_avatar", blank=True)

    label = models.SlugField(unique=True) # unique way to name a chatgroup in the url
 
 	# methods will be added later


 	