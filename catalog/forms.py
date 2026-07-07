from django import forms

from .models import Catalog, Movie


class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Populares en Netflix'}),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'catalog', 'poster', 'is_hero', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título de la película'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sinopsis...'}),
        }
