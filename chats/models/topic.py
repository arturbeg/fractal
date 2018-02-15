class Topic(Room):
	arrow_ups = models.ManyToManyField(User, related_name='arrow_ups')
    arrow_downs = models.ManyToManyField(User, related_name='arrow_downs')


    # Methods later