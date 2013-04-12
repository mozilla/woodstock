from django.contrib import admin
from woodstock.voting.models import MozillianGroup, MozillianProfile, Vote

class MozillianProfileAdmin(admin.ModelAdmin):
    """Mozillian profiles under /admin."""

    search_fields = ['full_name', 'country']
    list_display = ['full_name', 'email', 'city', 'country', 'negative', 'skip',
                    'positive', 'stellar']

    def negative(self, obj):
        number = Vote.objects.filter(nominee = obj, vote = -1).count()
        return number
    
    def skip(self, obj):
        number = Vote.objects.filter(nominee = obj, vote = 0).count()
        return number
    
    def positive(self, obj):
        number = Vote.objects.filter(nominee = obj, vote = 1).count()
        return number
        
    def stellar(self, obj):
        number = Vote.objects.filter(nominee = obj, vote = 2).count()
        return number


admin.site.register(MozillianGroup)
admin.site.register(MozillianProfile, MozillianProfileAdmin)
