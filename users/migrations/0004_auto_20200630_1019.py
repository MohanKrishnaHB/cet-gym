# Generated by Django 3.0.6 on 2020-06-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200630_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='prefered_branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='puc_college',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]