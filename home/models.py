''' Basic database structure for site monitoring '''
import uuid
from django.db import models


# Tracks site visit numbers
class SiteVisits(models.Model):
    ''' A table to track site visit numbers '''
    date = models.DateField()
    site_visits = models.BigIntegerField()


# Tracks what a user has clicked on in this session
class SiteActionsTaken(models.Model):
    ''' A table to track what a user has clicked on '''
    session_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.CharField(max_length=50)
    actions_taken = models.TextField()
