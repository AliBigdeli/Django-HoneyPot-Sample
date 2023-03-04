from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .app_settings import HONEYPOT_LOGIN_TRYOUT

class LoginAttempt(models.Model):
    username = models.CharField(_("username"), max_length=255, blank=True, null=True)
    password = models.CharField(_("password"), max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    path = models.TextField(_("path"), blank=True, null=True)
    created_date = models.DateTimeField(_("created_date"), auto_now_add=True)

    class Meta:
        verbose_name = _("login attempt")
        verbose_name_plural = _("login attempts")
        ordering = ('-created_date',)

    def __str__(self):
        return self.username


class BlackList(models.Model):
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    created_date = models.DateTimeField(_("created_date"), auto_now_add=True)
    
    class Meta:
        ordering = ('-created_date',)
        
    def __str__(self):
        return self.ip_address

@receiver(post_save, sender=LoginAttempt)
def create_blacklist(sender, instance, created, **kwargs):
    if created and LoginAttempt.objects.filter(ip_address = instance.ip_address).count() >= HONEYPOT_LOGIN_TRYOUT:
        BlackList.objects.get_or_create(ip_address=instance.ip_address)


@receiver(post_delete, sender=BlackList)
def remove_all_related_attempts(sender,instance,**kwargs):
    LoginAttempt.objects.filter(ip_address = instance.ip_address).delete()
