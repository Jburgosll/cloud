from django.shortcuts import render

from .models import Movie

# Datos de respaldo: se usan solo mientras no haya películas cargadas en la
# base de datos (por ejemplo, antes de subir el primer poster vía el admin).
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
    for key, label in Movie.CATEGORY_CHOICES:
        movies = Movie.objects.filter(category=key)
        if movies.exists():
            rows.append({
                "title": label,
                "items": [
                    {
                        "title": movie.title,
                        "image_url": movie.poster.url if movie.poster else None,
                        "color": f"c{(movie.pk % 6) + 1}",
                    }
                    for movie in movies
                ],
            })
    if not rows:
        rows = ROWS

    return render(request, "catalog/home.html", {"hero": hero, "rows": rows})
