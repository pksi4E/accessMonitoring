from django.db import models

class Website (models.Model):
	site_url = models.CharField(max_length=300)
	time_interval = models.IntegerField(min) # in seconds
	is_error = models.BooleanField(default=False)
	
	def __str__ (self):
		return f"{self.site_url}"

class WebsitesHistory (models.Model):
	site_url = models.ForeignKey(Website, on_delete=models.CASCADE)
	error_type = models.IntegerField()
	error_begin_date = models.DateTimeField(auto_now_add=True)