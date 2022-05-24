from django.db import models

class Website (models.Model):
	site_url = models.CharField(max_length=300)
	time_interval = models.IntegerField() # in seconds

	def __str__ (self):
		return f"{self.site_url[:20]}..."