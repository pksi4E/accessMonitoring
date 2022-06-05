# accessMonitoring: Application for monitoring website access 


## What is it?
**accessMonitoring** is a Django application for monitoring website access.

Application uses **sqlite** database.

After downloading all the code and placing it in *accessMonitoring* folder, make sure you have **django-celery-beat** module and **celery** installed,
and in the terminal enter the following commands:

```python
celery --app accessMonitoring beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

```python
celery --app accessMonitoring worker --loglevel=INFO
```

```python
python3 manage.py runserver
```

Application uses **django_celery_beat** for dynamically scheduling tasks.
