from django.db import models


class Movie(models.Model):
    CATEGORY_CHOICES = [
        ('popular', 'Populares en Netflix'),
        ('trending', 'Tendencias ahora'),
        ('mylist', 'Mi lista'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='popular')
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    is_hero = models.BooleanField(
        default=False,
        help_text='Si se activa, esta película se muestra en el banner principal.',
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
