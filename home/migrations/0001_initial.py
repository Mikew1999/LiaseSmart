# Generated by Django 4.0.4 on 2022-05-01 20:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteActionsTaken',
            fields=[
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=50)),
                ('actions_taken', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteVisits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('site_visits', models.BigIntegerField()),
            ],
        ),
    ]
