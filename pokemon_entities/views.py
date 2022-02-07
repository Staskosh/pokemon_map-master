import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']
    pokemons_with_coordinates = {}
    for pokemon in pokemons:
        coordinates = []
        for pokemon_entity in pokemon['entities']:
            coordinates.append([pokemon_entity['lat'], pokemon_entity['lon']])
        pokemons_with_coordinates[pokemon['title_ru']] = coordinates
    for pokemon_title, pokemon_coordinates in pokemons_with_coordinates.items():
        pokemon = Pokemon.objects.get(title_ru__contains=pokemon_title)
        for pokemon_coordinate in pokemon_coordinates:
            PokemonEntity.objects.create(
                pokemon = pokemon,
                lat = pokemon_coordinate[0],
                lon = pokemon_coordinate[1]
            )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemons_db = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_db:
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title_ru,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image,
                'title_ru': pokemon.title_ru,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']
    pokemons_db = Pokemon.objects.all()
    for pokemon in pokemons_db:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    requested_pokemon_entities = PokemonEntity.objects.filter(pokemon__title_ru__contains=requested_pokemon)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemon = Pokemon.objects.get(title_ru__contains=requested_pokemon)
    if pokemon.image:
        pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
        }
        if pokemon.previous_evolution:
            pokemon_on_page['previous_evolution'] =  pokemon.previous_evolution

        for pokemon_initial in pokemons:
            if pokemon_initial['title_ru'] == pokemon.title_ru:
                if 'next_evolution' in pokemon_initial:
                    evolution_to = pokemon_initial['next_evolution']
                    related_pokemon = Pokemon.objects.select_related().get(title_ru__contains=evolution_to['title_ru'])
                    pokemon_on_page['next_evolution'] = related_pokemon

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page,
    })
