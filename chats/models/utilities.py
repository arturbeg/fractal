import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_label_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a label field and a name character (char) field.
    
    """
    if new_slug is not None:
        label = new_slug
    else:
        label = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(label=label).exists()
    if qs_exists:
        new_slug = "{label}-{randstr}".format(
                    label=label,
                    randstr=random_string_generator(size=4)
                )
        return unique_label_generator(instance, new_slug=new_slug)
    return label
