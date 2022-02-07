from django.contrib import admin
from pokemon_entities.models import Pokemon, PokemonEntity

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title_ru',)


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lon')
