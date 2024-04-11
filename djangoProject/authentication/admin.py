from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'country', 'city', 'registration_date')  
    search_fields = ('user__username', 'user__email', 'country', 'city')  
    list_filter = ('country', 'city', 'registration_date')  
    ordering = ('-registration_date',)  
