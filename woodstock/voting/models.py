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
    slug = models.SlugField(blank=True, max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(default='')
    city = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='')
    ircname = models.CharField(max_length=50, default='')
    tracking_groups = models.ManyToManyField(
        MozillianGroup, related_name='mozillians_tracking')
    avatar_url = models.URLField(max_length=400, default='')
    bio = models.TextField(blank=True, default='')
    username = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['country', 'full_name']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuslug(self.full_name, instance=self)
        super(MozillianProfile, self).save(*args, **kwargs)

    def get_next_entry(self):
        qs = MozillianProfile.objects.all()
        length = qs.count()
        for index, item in enumerate(qs):
            if (item == self) and (index <= length-2):
                return qs[index+1]
        return False

    def get_previous_entry(self):
        qs = MozillianProfile.objects.all()
        for index, item in enumerate(qs):
            if (item == self) and (index > 0):
                return qs[index-1]
        return False

    @property
    def positive(self):
        return self.votes.filter(vote=1).count()

    @property
    def stellar(self):
        return self.votes.filter(vote=2).count()

    @property
    def negative(self):
        return self.votes.filter(vote=-1).count()

    @property
    def skip(self):
        return self.votes.filter(vote=0).count()


class Vote(models.Model):
    """Vote relational model."""
    voter = models.ForeignKey(User, related_name='user_votes')
    nominee = models.ForeignKey(MozillianProfile, related_name='votes')
    vote = models.IntegerField(default=0, choices=((0, 'Skip'),
                                                   (1, 'Probably'),
                                                   (2, 'Definitely'),
                                                   (-1, 'No')))

    def __unicode__(self):
        return '%s %s' % (self.voter, self.nominee)
