from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_hero', 'order', 'poster')
    list_filter = ('category', 'is_hero')
    search_fields = ('title',)
