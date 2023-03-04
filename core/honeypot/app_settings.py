from django.conf import settings


HONEYPOT_LOGIN_TRYOUT = getattr(settings, "HONEYPOT_LOGIN_TRYOUT", 5)
