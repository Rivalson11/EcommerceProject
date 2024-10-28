
from django.contrib import admin
from .models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')