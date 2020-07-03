# Generated by Django 3.0.6 on 2020-07-02 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200630_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='phone_number',
            field=models.CharField(default=9012345678, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]