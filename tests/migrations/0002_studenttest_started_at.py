# Generated by Django 3.0.6 on 2020-06-25 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttest',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
