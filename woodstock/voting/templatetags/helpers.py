from django import template

register = template.Library()


@register.filter
def get_vote(mozillian, voter):
    """Get the vote of a user."""
    vote = mozillian.votes.filter(voter=voter)
    if vote.exists():
        return vote[0].get_vote_display()
    return ''
