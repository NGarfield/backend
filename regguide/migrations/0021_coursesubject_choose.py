# Generated by Django 3.1.1 on 2021-05-18 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regguide', '0020_conditionjson_choose'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesubject',
            name='choose',
            field=models.IntegerField(null=True),
        ),
    ]
