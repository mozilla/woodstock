from django.contrib.auth.models import User
from django.db import models


class MozillianGroups(models.Model):
    """Mozillians tracking groups."""
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class MozillianProfile(models.Model):
    """Mozillians User Profile"""
    full_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    is_vouched = models.BooleanField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    ircname = models.CharField(max_length=50, default='')
    tracking_groups = models.ManyToManyField(
        MozillianGroups, related_name='mozillians_tracking')
    avatar_url = models.URLField(max_length=400, default='')
    bio = models.TextField(blank=True, default='')


class Vote(models.Model):
    voter = models.ForeignKey(User)
    nominee = models.ForeignKey(MozillianProfile)
    vote = models.IntegerField(default=0)
