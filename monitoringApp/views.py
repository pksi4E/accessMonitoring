import sys, os
sys.path.insert(0, os.path.abspath('..'))
import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .models import Website, WebsitesHistory
from .forms import WebsiteForm
from .tasks import mark_error, mark_no_error, get_website_HTTPstatus, update_website_status

from accessMonitoring.celery import app
from django_celery_beat.models import PeriodicTask, IntervalSchedule

def index (request):
	# przekierowanie do strony z monitoringiem
	return monitoring(request)

def monitoring (request):
	context = {'websites': Website.objects.all()}
	return render(request, 'monitoringApp/monitoring.html', context)

def add_website (request):
	if request.method != 'POST':
		form = WebsiteForm()
	else:
		form = WebsiteForm(data=request.POST)
		if form.is_valid():
			form.save()
			website = Website.objects.last()

			### Dynamically add task to the scheduler

			schedule = IntervalSchedule.objects.create(
				every=website.time_interval,
				period=IntervalSchedule.MINUTES)
			task = PeriodicTask.objects.create(
				interval=schedule,
				name=str(website.site_url) + '_TASK',
				task='update_website_status_task',
				args=json.dumps([website.id]))
			task.save()

			return redirect('monitoring:monitoring_url')
	context = {'form': form}
	return render(request, 'monitoringApp/add_website.html', context)


def modify_website (request, website_id):
	website = Website.objects.get(id=website_id)
	if request.method != 'POST':
		form = WebsiteForm(instance=website)
	else:
		form = WebsiteForm(request.POST, instance=website)
		if form.is_valid():
			form.save()
			mark_error.delay(website_id=website_id)
			return redirect('monitoring:monitoring_url')
	context = {'form': form, 'website': website}
	return render(request, 'monitoringApp/modify_website.html', context)

def delete_website (request, website_id):
	website = Website.objects.get(id=website_id)
	if request.method == 'POST':
		# delete website from the list
		website.delete()
		return redirect('monitoring:monitoring_url')
	context = {'website': website}
	return render(request, 'monitoringApp/delete_website.html', context)

def with_errors (request):
	""" Widok z listą wszystkich stron opatrzonych błędem dostępu.
		Wszystkie strony z bazy z atrybutem is_error=True. """
	websites = Website.objects.filter(is_error=True)
	context = {'error_websites': websites}
	return render(request, 'monitoringApp/with_errors.html', context)

def website_history (request, website_id):
	website = Website.objects.get(id=website_id)
	history = WebsitesHistory.objects.filter(site_url=website)
	context = {'website': website, 'history': history}
	return render(request, 'monitoringApp/website_history.html', context)