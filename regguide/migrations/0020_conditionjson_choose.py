# Generated by Django 3.1.1 on 2021-05-17 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regguide', '0019_datesystem_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditionjson',
            name='choose',
            field=models.IntegerField(null=True),
        ),
    ]
