from django.shortcuts import render

from .models import Website

def index (request):
	context = {
		'websites': Website.objects.all() #typ:QuerySet
	}
	return render(request, 'monitoringApp/index.html', context)
