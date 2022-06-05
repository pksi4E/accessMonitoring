from django import forms

from .models import Website

class WebsiteForm (forms.ModelForm):
	""" Formularz modelu Website służący do EDYCJI wpisu. """
	class Meta:
		model = Website
		fields = ['site_url', 'time_interval']
		labels = {'site_url': 'URL:', 'time_interval': 'Time interval (min):'}
		widgets = {'time_interval': forms.NumberInput(attrs={'min': 1})}