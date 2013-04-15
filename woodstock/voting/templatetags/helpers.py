from django import template

register = template.Library()


@register.filter
def get_mozillian_groups(user):
    """Get all the groups of a Mozillian."""
    return user.tracking_groups.all()


@register.filter
def get_next(user):
    """Get next Mozillian from the db."""
    if user.get_next_entry():
        return user.get_next_entry().slug
    return False


@register.filter
def get_previous(user):
    """Get previous Mozillian from the db."""
    if user.get_previous_entry():
        return user.get_previous_entry().slug
    return False


@register.filter
def get_country(key, countries):
    """Get the country from the country code."""
    try:
        return countries[key]
    except KeyError:
        return key
