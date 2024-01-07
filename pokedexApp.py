from flask import Flask, request, redirect
from pokedex import fetchPokemon
from flask import render_template
from PokemonIRModel import setUpModel, identifyPokemon
import os
from cache.pkmCache import populatePkmCache

app = Flask(__name__)



def nameToId(n):
    name_to_id_map = {}
    for i in range(1,n+1):
        pkmname = PKMCache.get(i).name
        name_to_id_map[pkmname] = i
    return name_to_id_map



PKMCache = populatePkmCache()
nameToIdMap = nameToId(1017)
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

@app.route('/pokemon/<id>')
def getPokemon(id):
    errorholder = []
    print(id)
    try:
        try:
            pokemon = PKMCache.get(int(id))
        except ValueError:
            print("Value Error ----------")
            pkmId = nameToIdMap.get(id)
            pokemon = PKMCache.get(pkmId)

        data = {'name' : pokemon.name,
                 'id' : pokemon.id,
                 'gen': pokemon.gen,
                 'entry' : pokemon.entry,
                 'genus' : pokemon.species,
                 'image' : 'https://th.bing.com/th/id/R.0d045617037f9cef063d1a9dfe2646b7?rik=EswZh150nqhxsg&riu=http%3a%2f%2fwww.snut.fr%2fwp-content%2fuploads%2f2015%2f07%2fimage-de-fleur-6.jpg&ehk=M9uLBYMHQgtcByG2fGYQSKyylapb%2bfCApnNYShcBdfE%3d&risl=&pid=ImgRaw&r=0',
                 'errorholder' : errorholder
                }
        links = {'prev' : pokemon.id-1,
                 'next' : pokemon.id+1
                 }

        return render_template('pokedexentry.html', data = data, links = links)
    except Exception as e:
        print(f'Error: {e}')
        errorholder.append(f'Pokemon with the name or id: "{id}" does not exsist')
        return render_template('index.html', error=errorholder)
        

if __name__ == '__main__':
    #try:
        #IRmodel, IRmodelClasses = setUpModel()
        #PKMCache = populatePkmCache()
        #nameToIdMap = nameToId(len(PKMCache._cache_instance))
   # except:
       # print('pass')
       # pass
    app.run(debug=True)