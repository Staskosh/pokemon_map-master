import json

from django.core.management.base import BaseCommand
from pokemon_entities.models import Pokemon, PokemonEntity


class Command(BaseCommand):
    def handle(self, *args, **options):
        PokemonEntity.objects.all().delete()
        Pokemon.objects.all().delete()
        with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
            pokemons = json.load(database)['pokemons']
        pokemons_with_coordinates = {}
        for pokemon in pokemons:
            Pokemon.objects.create(
                title_ru=pokemon['title_ru'],
                title_en=pokemon['title_en'],
                title_jp=pokemon['title_jp'],
                description=pokemon['description']
            )
            if 'previous_evolution' in pokemon:
                actual_pokemon = Pokemon.objects.get(title_ru__contains=pokemon['title_ru'])
                actual_pokemon.previous_evolution = Pokemon.objects.get(title_ru__contains=pokemon['previous_evolution']['title_ru'])
                actual_pokemon.save()

            coordinates = []
            for pokemon_entity in pokemon['entities']:
                coordinates.append([pokemon_entity['lat'], pokemon_entity['lon']])
            pokemons_with_coordinates[pokemon['title_ru']] = coordinates
        for pokemon_title, pokemon_coordinates in pokemons_with_coordinates.items():
            pokemon = Pokemon.objects.get(title_ru__contains=pokemon_title)
            for pokemon_coordinate in pokemon_coordinates:
                PokemonEntity.objects.create(
                    pokemon=pokemon,
                    lat=pokemon_coordinate[0],
                    lon=pokemon_coordinate[1]
                )