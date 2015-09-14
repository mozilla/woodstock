import re

from django.contrib import admin
from django.core.validators import EmailValidator
from django.forms import ValidationError

from import_export.admin import ExportMixin, ImportExportMixin
from import_export import fields, resources

from woodstock.voting.models import (Application, Event, PreferredEvent,
                                     MozillianGroup, MozillianProfile, Vote)


RGX = re.compile('.+/u/(.+)/')


class ApplicationResource(resources.ModelResource):

    class Meta:
        model = Application
        fields = ('entry_id', 'number_of_events', 'event', 'reasoning',
                  'contributions', 'learning_areas', 'recommendation_letter',
                  'ideas', 'commitments', 'functional_team', 'team_contact',
                  'participation_opportunities', 'tracking_communities',
                  'community_record', 'community_impact', 'other', 'date',
                  'application_complete',)
        skip_unchanged = True
        report_skipped = True


class EventResource(resources.ModelResource):

    class Meta:
        model = Event
        fields = ('name',)
        skip_unchanged = True
        report_skipped = True


class PreferredEventResource(resources.ModelResource):

    class Meta:
        model = PreferredEvent
        fields = ('event', 'application', 'preferred',)
        skip_unchanged = True
        report_skipped = True


class MozillianGroupResouce(resources.ModelResource):
    negative_votes = fields.Field()
    skip_votes = fields.Field()
    positive_votes = fields.Field()
    stellar_votes = fields.Field()
    total_votes = fields.Field()

    class Meta:
        model = MozillianProfile
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('mozillian_username',)
        fields = ('mozillian_username', 'email',)

    def dehydrate_negative_votes(self, mozillianprofile):
        return mozillianprofile.votes.filter(vote=-1).count()

    def dehydrate_skip_votes(self, mozillianprofile):
        return mozillianprofile.votes.filter(vote=0).count()

    def dehydrate_positive_votes(self, mozillianprofile):
        return mozillianprofile.votes.filter(vote=1).count()

    def dehydrate_stellar_votes(self, mozillianprofile):
        return mozillianprofile.votes.filter(vote=2).count()

    def total_votes(self, mozillianprofile):
        negatives = mozillianprofile.votes.filter(vote=-1).count()
        positives = (mozillianprofile.votes.filter(vote=1).count() +
                     mozillianprofile.votes.filter(vote=2).count())
        return (positives - negatives)

    # Import section
    def before_import(self, dataset, dry_run, **kwargs):
        """Override method for custom functionality."""

        # Normalize dataset
        if dataset.headers:
            dataset.headers = [unicode(header).lower().strip()
                               for header in dataset.headers]

    def get_or_init_instance(self, instance_loader, row):
        """Override method for custom functionality."""

        # If ther isn't a username or the application is not complete,
        # do not return an instance.
        if ('mozillian_username' not in row or
            'application_complete' not in row or
                row['application_complete'] == u'0'):
            row['mozillian_username'] = ''

        # Normalize usernames
        match = RGX.match(row['mozillian_username'])
        if match:
            row['mozillian_username'] = match.groups()[0]

        # Validate email
        email_validator = EmailValidator()
        try:
            email_validator(row['email'])
        except ValidationError:
            row['email'] = ''

        return (super(MozillianGroupResouce, self)
                .get_or_init_instance(instance_loader, row))

    def skip_row(self, instance, original):
        if instance and (instance.mozillian_username == '' or
                         instance.email == ''):
            return True
        return super(MozillianGroupResouce, self).skip_row(instance, original)

    def save_instance(self, instance, dry_run):
        if not dry_run:
            # TODO: Get the rest of the info from mozillians.org
            # Probably we need to check if there are any changes to the profile
            # and update it
            super(MozillianGroupResouce, self).save_instance(instance, dry_run)


class MozillianProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    """Mozillian profiles under /admin."""

    resource_class = MozillianGroupResouce
    model = MozillianProfile
    search_fields = ('full_name', 'country', 'mozillian_username', 'email',)
    list_display = ['mozillian_username', 'full_name', 'email', 'city',
                    'country', 'negative', 'skip', 'positive', 'stellar']

    def negative(self, obj):
        return obj.votes.filter(vote=-1).count()

    def skip(self, obj):
        return obj.votes.filter(vote=0).count()

    def positive(self, obj):
        return obj.votes.filter(vote=1).count()

    def stellar(self, obj):
        return obj.votes.filter(vote=2).count()


class VoteResource(resources.ModelResource):
    voter = fields.Field()

    class Meta:
        model = Vote
        fields = ['voter', 'nominee__full_name', 'vote']

    def dehydrate_voter(self, vote):
        return '%s %s' % (vote.voter.first_name, vote.voter.last_name)


class VoteAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = VoteResource
    model = Vote
    list_display = ['voter', 'nominee', 'vote']


class MozillianGroupAdmin(ExportMixin, admin.ModelAdmin):
    model = MozillianGroup


class ApplicationAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ApplicationResource
    model = Application
    search_fields = ('entry_id', 'event__name',)


class EventAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = EventResource
    model = Event


class PreferredEventAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = PreferredEventResource
    model = PreferredEvent


admin.site.register(MozillianGroup, MozillianGroupAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(MozillianProfile, MozillianProfileAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PreferredEvent, PreferredEventAdmin)
