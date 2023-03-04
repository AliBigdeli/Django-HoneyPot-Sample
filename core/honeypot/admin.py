from django.contrib import admin
from .models import LoginAttempt,BlackList

# Register your models here.
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "ip_address",
        "path",
        "created_date",
    ]

admin.site.register(LoginAttempt,LoginAttemptAdmin)
admin.site.register(BlackList)
