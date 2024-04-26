from django.contrib import admin
from django.utils import timezone
from Auth.models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'email', 'username', 'first_name', 'last_name', 'last_login', 'otp_created_at', 'date_joined')
    search_fields = ('user_type',)
    exclude = ('otp', 'otp_created_at', 'username', 'user_permissions', 'groups')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('last_login', None)
        form.base_fields.pop('date_joined', timezone.now())
        return form


admin.site.register(CustomUser, CustomUserAdmin)
