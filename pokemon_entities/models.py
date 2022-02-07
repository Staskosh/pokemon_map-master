from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название на русском')
    title_en = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название на японском'
                                )
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.CASCADE,
                                           related_name="next_evolution",
                                           blank=True,
                                           null=True,
                                           verbose_name='Предыдущая эволюция'
                                           )
    description = models.TextField(blank=True,
                                   verbose_name='Описание'
                                   )
    image = models.ImageField(upload_to='pokemons',
                              verbose_name='Картинка'
                              )

    def __str__(self):
        return f'{self.title_ru}'

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                blank=True,
                                verbose_name='Покемон'
                                )
    lat = models.FloatField(blank=True,
                            null=True,
                            verbose_name='Координата широты'
                            )
    lon = models.FloatField(blank=True,
                            null=True,
                            verbose_name='Координата высоты'
                            )
    appeared_at = models.DateTimeField(blank=True,
                                       null=True,
                                       verbose_name='Время появления'
                                       )
    disappeared_at = models.DateTimeField(blank=True,
                                          null=True,
                                          verbose_name='Время исчезания'
                                          )
    level = models.IntegerField(blank=True,
                                null=True,
                                verbose_name='Уровень покемона'
                                )
    health = models.IntegerField(blank=True,
                                 null=True,
                                 verbose_name='Здоровье покемона'
                                 )
    strength = models.IntegerField(blank=True,
                                   null=True,
                                   verbose_name='Сила'
                                   )
    defence = models.IntegerField(blank=True,
                                  null=True,
                                  verbose_name='Защита'
                                  )
    stamina = models.IntegerField(blank=True,
                                  null=True,
                                  verbose_name='Выносливость')
