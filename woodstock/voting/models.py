from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug


class MozillianGroup(models.Model):
    """Mozillians tracking groups."""
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MozillianProfile(models.Model):
    """Mozillians User Profile"""

    full_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, max_length=100)
    email = models.EmailField(default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    ircname = models.CharField(max_length=50, default='')
    tracking_groups = models.ManyToManyField(
        MozillianGroup, related_name='mozillians_tracking')
    avatar_url = models.URLField(max_length=400, default='')
    bio = models.TextField(blank=True, default='')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name', 'country']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuslug(self.full_name, instance=self)
        super(MozillianProfile, self).save(*args, **kwargs)

    def get_next_entry(self):
        next_entry = (MozillianProfile.objects
                      .filter(id__gt=self.id))
        if next_entry:
            return next_entry[0]
        return False

    def get_previous_entry(self):
        previous_entry = (MozillianProfile.objects
                          .filter(id__lt=self.id))
        if previous_entry:
            return previous_entry[0]
        return False


class Vote(models.Model):
    """Vote relational model."""

    voter = models.ForeignKey(User)
    nominee = models.ForeignKey(MozillianProfile)
    vote = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s' % (self.voter, self.nominee)
