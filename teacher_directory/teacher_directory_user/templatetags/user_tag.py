from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag()
def get_url(slug,second_slug):
    print(slug,second_slug)
    print(reverse('manage-teacher',args=[slug,second_slug]))
    return slug
    # return reverse('manage-teacher',args=[slug,second_slug])