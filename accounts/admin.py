from django.contrib import admin
from . models import User 

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role','phone_number', 'days_since_joined', 'is_active',)
    list_filter = ('created','is_staff')
    search_fields = ('email',)
    readonly_fields = ('password',)

    def days_since_joined(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return (now - obj.created).days
    days_since_joined.short_description = 'Days since joined'

admin.site.register(User, UserAdmin)
