import csv

from django.contrib import admin
from django.http import HttpResponse

from woodstock.voting.models import MozillianGroup, MozillianProfile, Vote


def export_as_csv_action(description=None, fields=None, exclude=None,
                         header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row

    Based on snippet http://djangosnippets.org/snippets/2020/
    """

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = ('attachment; filename=%s.csv' %
                                           unicode(opts).replace('.', '_'))

        writer = csv.writer(response, delimiter=';')
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8')
                             for field in field_names])
        return response

    export_as_csv.short_description = (description or 'Export to CSV file')
    return export_as_csv


class MozillianProfileAdmin(admin.ModelAdmin):
    """Mozillian profiles under /admin."""

    search_fields = ['full_name', 'country']
    list_display = ['full_name', 'email', 'city', 'country', 'negative',
                    'skip', 'positive', 'stellar']
    actions = [export_as_csv_action(fields=('full_name', 'email', 'city',
                                            'country', 'positive', 'negative',
                                            'stellar', 'skip'),
                                    header=True)]

    def negative(self, obj):
        return obj.votes.filter(vote=-1).count()

    def skip(self, obj):
        return obj.votes.filter(vote=0).count()

    def positive(self, obj):
        return obj.votes.filter(vote=1).count()

    def stellar(self, obj):
        return obj.votes.filter(vote=2).count()


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['voter', 'nominee', 'vote']


class MozillianGroupAdmin(admin.ModelAdmin):
    model = MozillianGroup


admin.site.register(MozillianGroup, MozillianGroupAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(MozillianProfile, MozillianProfileAdmin)
