# Generated by Django 3.2.13 on 2022-06-05 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoringApp', '0003_auto_20220605_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='websiteshistory',
            name='error_type',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='websiteshistory',
            name='error_begin_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
