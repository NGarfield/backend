# Generated by Django 3.1.1 on 2021-04-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regguide', '0012_deparment_total_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='registersubject',
            name='term',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='registersubject',
            name='yaer',
            field=models.IntegerField(null=True),
        ),
    ]
