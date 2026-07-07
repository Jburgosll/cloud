from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CatalogForm, MovieForm
from .models import Catalog, Movie

# Datos de respaldo: se usan solo mientras no haya películas cargadas en la
# base de datos (por ejemplo, antes de subir el primer poster desde el panel).
HERO = {
    "title": "Stranger Things",
    "description": "Cuando un niño desaparece, un pequeño pueblo descubre un misterio que "
                   "involucra experimentos secretos, fuerzas sobrenaturales aterradoras y una niña muy extraña.",
    "color": "hero-bg",
}

ROWS = [
    {
        "title": "Populares en Netflix",
        "items": [
            {"title": "Dark", "color": "c1"},
            {"title": "Ozark", "color": "c2"},
            {"title": "Narcos", "color": "c3"},
            {"title": "La Casa de Papel", "color": "c4"},
            {"title": "El Juego del Calamar", "color": "c5"},
            {"title": "Wednesday", "color": "c6"},
        ],
    },
    {
        "title": "Tendencias ahora",
        "items": [
            {"title": "Bridgerton", "color": "c2"},
            {"title": "The Crown", "color": "c3"},
            {"title": "You", "color": "c4"},
            {"title": "Black Mirror", "color": "c5"},
            {"title": "Mindhunter", "color": "c6"},
            {"title": "Dark", "color": "c1"},
        ],
    },
    {
        "title": "Mi lista",
        "items": [
            {"title": "Narcos", "color": "c3"},
            {"title": "Wednesday", "color": "c6"},
            {"title": "Ozark", "color": "c2"},
            {"title": "You", "color": "c4"},
            {"title": "El Juego del Calamar", "color": "c5"},
            {"title": "La Casa de Papel", "color": "c4"},
        ],
    },
]


def home(request):
    hero_movie = Movie.objects.filter(is_hero=True).first()
    if hero_movie:
        hero = {
            "title": hero_movie.title,
            "description": hero_movie.description,
            "image_url": hero_movie.poster.url if hero_movie.poster else None,
            "color": "hero-bg",
        }
    else:
        hero = HERO

    rows = []
    for catalog in Catalog.objects.prefetch_related('movies'):
        movies = catalog.movies.all()
        if movies:
            rows.append({
                "title": catalog.name,
                "items": [
                    {
                        "title": movie.title,
                        "description": movie.description,
                        "image_url": movie.poster.url if movie.poster else None,
                        "color": f"c{(movie.pk % 6) + 1}",
                    }
                    for movie in movies
                ],
            })
    if not rows:
        rows = ROWS

    return render(request, "catalog/home.html", {"hero": hero, "rows": rows})


# ---------------------------------------------------------------------------
# Panel de administración (simulación, sin usuarios): catálogos y películas
# ---------------------------------------------------------------------------

def panel(request):
    catalog_form = CatalogForm()
    movie_form = MovieForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_catalog':
            catalog_form = CatalogForm(request.POST)
            if catalog_form.is_valid():
                catalog = catalog_form.save()
                messages.success(request, f'Catálogo "{catalog.name}" creado.')
                return redirect('panel')
        elif action == 'add_movie':
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                movie = movie_form.save()
                messages.success(request, f'Película "{movie.title}" agregada.')
                return redirect('panel')

    return render(request, 'catalog/panel.html', {
        'catalog_form': catalog_form,
        'movie_form': movie_form,
        'catalogs': Catalog.objects.prefetch_related('movies'),
        'movies': Movie.objects.select_related('catalog'),
    })


@require_POST
def delete_catalog(request, pk):
    catalog = get_object_or_404(Catalog, pk=pk)
    name = catalog.name
    catalog.delete()
    messages.success(request, f'Catálogo "{name}" eliminado (junto con sus películas).')
    return redirect('panel')


@require_POST
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    title = movie.title
    movie.delete()
    messages.success(request, f'Película "{title}" eliminada.')
    return redirect('panel')
