import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

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
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = pokemon.image

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = requested_pokemon.entities.first()
    add_pokemon(
        folium_map, pokemon_entities.lat,
        pokemon_entities.lon,
        request.build_absolute_uri(pokemon_entities.pokemon.image.url)
    )
    if requested_pokemon.image:
        pokemon_on_page = {
            'pokemon_id': requested_pokemon.id,
            'img_url': request.build_absolute_uri(requested_pokemon.image.url),
            'title_ru': requested_pokemon.title_ru,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
            'description': requested_pokemon.description,
        }
    if requested_pokemon.previous_evolution:
        pokemon_on_page['previous_evolution'] = requested_pokemon.previous_evolution

    if requested_pokemon.next_evolution.first():
        pokemon_on_page['next_evolution'] = requested_pokemon.next_evolution.first()

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page,
    })
