from flask import Flask, request, redirect
from pokedex import fetchPokemon
from flask import render_template
from PokemonIRModel import setUpModel, identifyPokemon
import os

app = Flask(__name__)

UPLOADR_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOADR_FOLDER
IRmodel = None
IRmodelClasses = []

@app.route('/pokemon')
def goToIndex():
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
       filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
       file.save(filename)
       file.close()
       pokemonName = identifyPokemon(IRmodel, filename, IRmodelClasses) 
       return redirect('/pokemon/'+pokemonName)

@app.route('/pokemon/<name>')
def getPokemon(name):
    pokemon = fetchPokemon(name, 'random', 'en')
    data = { 'name' : pokemon.name,
             'id' : pokemon.id,
             'gen': pokemon.gen,
             'entry' : pokemon.entry,
             'genus' : pokemon.genus,
             'image' : pokemon.image,
            }
    links = {'prev' : pokemon.prev,
             'next' : pokemon.next
             }
    return render_template('pokedexentry.html', data = data, links = links)
    
if __name__ == '__main__':
    IRmodel, IRmodelClasses = setUpModel()
    app.run(debug=True)