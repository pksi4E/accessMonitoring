from django.contrib import admin
from django.urls import path

from . import views

app_name = 'monitoring'
urlpatterns = [
	path('', views.index, name="index_url"),
	path('monitoring/', views.monitoring, name='monitoring_url'),
	path('monitoring/add/', views.add_website, name='add_website_url'),
	path('monitoring/modify/<int:website_id>/', views.modify_website, name='modify_website_url'),
	path('monitoring/delete/<int:website_id>/', views.delete_website, name='delete_website_url'),
	path('monitoring/witherrors/', views.with_errors, name='with_errors_url'),
	path('monitoring/history/<int:website_id>/', views.website_history, name='website_history_url'),
]