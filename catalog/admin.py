from django.contrib import admin

from .models import Catalog, Movie


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'catalog', 'is_hero', 'order', 'poster')
    list_filter = ('catalog', 'is_hero')
    search_fields = ('title',)
