from tokenize import blank_re
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('User Email Address')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    event_manager = models.CharField(max_length=50)
    attendees = models.ManyToManyField(User, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    venue_image = models.ImageField(null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        return self.event_name

        