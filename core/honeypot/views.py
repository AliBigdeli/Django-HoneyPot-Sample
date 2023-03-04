from django.urls import reverse_lazy
from django.views.generic import FormView,RedirectView
from django.contrib import messages

from .models import LoginAttempt
from .forms import LoginForm
from .app_settings import HONEYPOT_LOGIN_TRYOUT


class RedirectToLogin(RedirectView):
    pattern_name = "honeypot:login"

# Create your views here.
class LoginView(FormView):
    form_class = LoginForm
    template_name = "honeypot/login.html"
    success_url = reverse_lazy("honeypot:login")
    
    def form_valid(self, form):
        if LoginAttempt.objects.filter(ip_address = self.get_client_ip()).count() >= HONEYPOT_LOGIN_TRYOUT:
            messages.error(self.request, 'Please enter the correct email address and password for a staff account. Note that both fields may be case-sensitive.')
        else:
            messages.error(self.request, 'Please enter the correct email address and password for a staff account. Note that both fields may be case-sensitive.')
            form.instance.user_agent = self.request.META.get('HTTP_USER_AGENT')
            form.instance.ip_address = self.get_client_ip()
            form.instance.session_key = self.request.session.session_key
            form.instance.path = self.request.path
            form.save()
        return super().form_valid(form)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_REMOTE_ADDR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip