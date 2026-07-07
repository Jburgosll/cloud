from django.db import migrations, models
import django.db.models.deletion

# Las antiguas categorías fijas del modelo Movie; se convierten en registros
# de Catalog para que las películas existentes no se pierdan.
OLD_CATEGORIES = [
    ('popular', 'Populares en Netflix'),
    ('trending', 'Tendencias ahora'),
    ('mylist', 'Mi lista'),
]


def forwards(apps, schema_editor):
    Catalog = apps.get_model('catalog', 'Catalog')
    Movie = apps.get_model('catalog', 'Movie')

    for order, (key, label) in enumerate(OLD_CATEGORIES):
        movies = Movie.objects.filter(category=key)
        if movies.exists():
            catalog, _ = Catalog.objects.get_or_create(name=label, defaults={'order': order})
            movies.update(catalog=catalog)

    # Cualquier película con una categoría desconocida va a un catálogo genérico.
    orphans = Movie.objects.filter(catalog__isnull=True)
    if orphans.exists():
        catalog, _ = Catalog.objects.get_or_create(name='Otros', defaults={'order': 99})
        orphans.update(catalog=catalog)


def backwards(apps, schema_editor):
    Movie = apps.get_model('catalog', 'Movie')
    labels_to_keys = {label: key for key, label in OLD_CATEGORIES}
    for movie in Movie.objects.select_related('catalog'):
        movie.category = labels_to_keys.get(movie.catalog.name, 'popular')
        movie.save(update_fields=['category'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Orden')),
            ],
            options={
                'verbose_name': 'Catálogo',
                'verbose_name_plural': 'Catálogos',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='catalog',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='movies',
                to='catalog.catalog',
                verbose_name='Catálogo',
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name='movie',
            name='category',
        ),
        migrations.AlterField(
            model_name='movie',
            name='catalog',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='movies',
                to='catalog.catalog',
                verbose_name='Catálogo',
            ),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='posters/', verbose_name='Poster'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='is_hero',
            field=models.BooleanField(
                default=False,
                help_text='Si se activa, esta película se muestra en el banner principal.',
                verbose_name='Mostrar en el banner',
            ),
        ),
        migrations.AlterField(
            model_name='movie',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Orden'),
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={
                'ordering': ['order', 'title'],
                'verbose_name': 'Película',
                'verbose_name_plural': 'Películas',
            },
        ),
    ]
