# Generated by Django 3.1.1 on 2021-05-14 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regguide', '0017_auto_20210510_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetablesubject',
            name='room',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='timetablesubject',
            name='term',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='timetablesubject',
            name='yaer',
            field=models.IntegerField(null=True),
        ),
    ]
