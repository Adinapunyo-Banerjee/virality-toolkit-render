from django.contrib import admin

# Register your models here.
from .models import User

# Register your models here.
class HomeAdmin(admin.ModelAdmin):                                      # This is to show custom fields in admin section
    list_display = ('email', 'mobile', 'isPremium', 'totalPredictions')
    search_fields = ('email', 'first_name')


admin.site.register(User, HomeAdmin)