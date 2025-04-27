# tribes/admin.py
from django.contrib import admin
from .models import People

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'region', 'description')  # Отображаемые поля
    list_filter = ('region',)  # Фильтр по региону
    search_fields = ('name',)  # Поиск по имени