from django.db import models


class Catalog(models.Model):
    """Categoría/fila del home (ej. "Populares en Netflix", "Tendencias ahora")."""

    name = models.CharField('Nombre', max_length=100, unique=True)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catálogo'
        verbose_name_plural = 'Catálogos'

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción', blank=True)
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name='movies',
        verbose_name='Catálogo',
    )
    poster = models.ImageField('Poster', upload_to='posters/', blank=True, null=True)
    is_hero = models.BooleanField(
        'Mostrar en el banner',
        default=False,
        help_text='Si se activa, esta película se muestra en el banner principal.',
    )
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Película'
        verbose_name_plural = 'Películas'

    def __str__(self):
        return self.title
