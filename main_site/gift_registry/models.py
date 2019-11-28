from hashlib import sha1

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.text import wrap
from django.utils.translation import gettext_lazy as _


# Dictionary settings inspired by:
# PyCon 2011: Pluggable Django Patterns
# http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-pluggable-django-patterns-4900929

# Required settings: You must supply these in a project settings dictionary
# called GIFT_REGISTRY_SETTINGS.
required_settings = [
    'EVENT_NAME',
]

for field in required_settings:
    if field not in settings.GIFT_REGISTRY_SETTINGS:
        raise ImproperlyConfigured("GIFT_REGISTRY_SETTINGS['%s'] is required in settings." % field)


class Event(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = models.SlugField(verbose_name=_("Slug"))
    user = models.ForeignKey(User, verbose_name=_("User"),
                             related_name="events")

    class Meta:
        ordering = ['name']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return "{} - {}".format(self.name, self.user)


class Gift(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("Event"),
                              related_name='gifts')
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    desc = models.TextField(
        verbose_name=_("Description"), blank=True, default='',
        help_text=_('Specific details of this item, such as preferred model.'))
    url = models.URLField(verbose_name=_("url"),
        blank=True, default='', help_text=_('A website showing the item.'))
    image = models.ImageField(verbose_name=_("Image"),
        null=True, blank=True,
        upload_to='images/',
        help_text=_('A photo or illustration.'))
    one_only = models.BooleanField(
        verbose_name=_("One only"),
        default=True,
        help_text=_(
            'When checked, remove item from list someone has chosen it. For '
            'some items, you may be happy to receive multiple.'))
    live = models.BooleanField(
        _("Live"),
        default=True,
        help_text=_('Make this item visible to public.'))

    class Meta:
        ordering = ['title']
        verbose_name = _("Gift")
        verbose_name_plural = _("Gifts")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gift_detail', args=[self.id])

    def bookable(self):
        return not self.one_only or self.giver_set.count() <= 0

    def count_givers(self):
        return self.giver_set.count()


class Giver(models.Model):
    gift = models.ForeignKey(Gift)
    email = models.EmailField()

    class Meta:
        ordering = ['id']
        unique_together = ('gift', 'email')
        verbose_name = _("Giver")
        verbose_name_plural = _("Givers")

    def __unicode__(self):
        return self.email

    def secret_key(self):
        """Calculate secret unique identifier for this object.

        Based on Django settings SECRET_KEY. Perhaps it should take an
        additional parameter such as the app name and class name so its not
        the same for the same pk between classes."""
        return sha1(str(self.pk).encode('utf-8') + settings.SECRET_KEY.encode('utf-8')).hexdigest()

    def email_confirmation(self, email):
        body = wrap(render_to_string('gift_registry/email_thanks.txt',
                                     {'gift': self.gift,
                                      'giver': self,
                                      'site': Site.objects.get_current()}), 70)
        send_mail(
            settings.GIFT_REGISTRY_SETTINGS['EVENT_NAME'], body,
            settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

    def save(self, *args, **kwargs):
        create = True if not self.pk else False
        email = self.email
        self.email = sha1(self.email.encode('utf-8')).hexdigest()
        super(Giver, self).save(*args, **kwargs)
        if create:
            self.email_confirmation(email)
