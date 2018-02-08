from django.db import models

from datetime import datetime, timedelta
from math import log

# Not using this for now, will make sure use it soon
class TopicManager(models.Manager):

    """
	def epoch_seconds(date):
        
        epoch = datetime(1970, 1, 1)
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
    """


    """    
    def score(arrow_ups, arrow_downs):
        return (arrow_ups - arrow_downs)
    """



    def rank(self, *args, **kwargs):
    	qs = self.get_query_set().filter(*args, **kwargs)
    	return sorted(qs, key=self.trending())    









