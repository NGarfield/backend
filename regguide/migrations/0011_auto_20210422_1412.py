# Generated by Django 3.1.1 on 2021-04-22 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regguide', '0010_coursesubject'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateSystem',
            fields=[
                ('id_date', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('system_yaer', models.IntegerField()),
                ('system_term', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='term_of_entry',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='yaer_of_entry',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
