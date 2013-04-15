from django.contrib import admin
from woodstock.voting.models import MozillianGroup, MozillianProfile, Vote


class MozillianProfileAdmin(admin.ModelAdmin):
    """Mozillian profiles under /admin."""

    search_fields = ['full_name', 'country']
    list_display = ['full_name', 'email', 'city', 'country', 'no',
                    'skip', 'probably', 'definitely']

    def no(self, obj):
        number = Vote.objects.filter(nominee=obj, vote=-1).count()
        return number

    def skip(self, obj):
        number = Vote.objects.filter(nominee=obj, vote=0).count()
        return number

    def probably(self, obj):
        number = Vote.objects.filter(nominee=obj, vote=1).count()
        return number

    def definitely(self, obj):
        number = Vote.objects.filter(nominee=obj, vote=2).count()
        return number


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['voter', 'nominee', 'vote']


class MozillianGroupAdmin(admin.ModelAdmin):
    model = MozillianGroup


admin.site.register(MozillianGroup, MozillianGroupAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(MozillianProfile, MozillianProfileAdmin)
