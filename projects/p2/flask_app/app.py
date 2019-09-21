from flask import Flask, render_template
from model import PokeClient
app = Flask(__name__)

poke_client = PokeClient()

@app.route('/')
def index():

    pokemon_list = poke_client.get_pokemon_list()
    
    return render_template('index.html', pokemon_list=pokemon_list)

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """
    
    pokemon = poke_client.get_pokemon_info(pokemon_name)
    
    return render_template('pokemon_info.html', pokemon=pokemon)

@app.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    
    context = dict()
    
    context["ability_name"] = ability_name
    context["pokemon_list"] = pokemon_list = poke_client.get_pokemon_with_ability(ability_name)
    
    return render_template('pokemon_with_ability.html', context=context)
