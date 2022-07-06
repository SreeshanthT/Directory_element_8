from django.shortcuts import get_object_or_404
from django.utils.text import slugify 
import random
import string

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,slugField, new_slug = None, size=4): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(slugField) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = size)) 
              
        return unique_slug_generator(instance,slugField, new_slug = new_slug) 
    return slug 

def get_object_or_none(query, **kwargs):
    try:
        return get_object_or_404(query, **kwargs)
    except:
        return None