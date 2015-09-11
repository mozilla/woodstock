from django.contrib import admin

from import_export.admin import ExportMixin, ImportExportMixin
from import_export import fields, resources

from woodstock.voting.models import MozillianGroup, MozillianProfile, Vote


class MozillianGroupResouce(resources.ModelResource):
    negative_votes = fields.Field()
    skip_votes = fields.Field()
    positive_votes = fields.Field()
    stellar_votes = fields.Field()
    total_votes = fields.Field()

    class Meta:
        model = MozillianProfile

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


class MozillianProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    """Mozillian profiles under /admin."""

    resource_class = MozillianGroupResouce
    model = MozillianProfile
    search_fields = ['full_name', 'country']
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


admin.site.register(MozillianGroup, MozillianGroupAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(MozillianProfile, MozillianProfileAdmin)
