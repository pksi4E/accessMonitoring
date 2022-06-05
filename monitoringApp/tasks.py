import sys
from time import sleep
from django.core.management import call_command
from celery import shared_task
from celery.schedules import crontab
from celery_progress.backend import ProgressRecorder

from .models import Website, WebsitesHistory
import urllib

@shared_task
def mark_error (website_id):
	website = Website.objects.get(id=website_id)
	website.is_error = True
	website.save()
	return

@shared_task
def mark_no_error (website_id):
	website = Website.objects.get(id=website_id)
	website.is_error = False
	website.save()
	return

@shared_task(name='check_website_status_task')
def get_website_HTTPstatus(website_id):
	""" Wczytuje website_id i zwraca status HTTP wskazanej strony
		łącząc się z nią poprzez bibliotekę urllib. """
	website = Website.objects.get(id=website_id)
	try:
		req = urllib.request.urlopen('http://' + website.site_url)
		website_status = req.code
	except urllib.error.HTTPError as e:
		website_status = e.code
		print('Error!' + str(e.code))
	return website_status

@shared_task(name='update_website_status_task')
def update_website_status (website_id):
	chain = get_website_HTTPstatus.s(website_id)
	status = chain()
	if status == 404:
		mark_error.delay(website_id)

		# Adding error to the monitoring history list
		website_hist = WebsitesHistory.objects.create(
			site_url=Website.objects.get(id=website_id),
			error_type=status)
		website_hist.save()

	elif status == 200:
		mark_no_error.delay(website_id)
	return f"Website with id {website_id} status updated to {str(status)}!!!"