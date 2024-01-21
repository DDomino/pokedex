from flask import Flask, request, redirect
from flask import render_template
from PokemonIRModel import setUpModel, identifyPokemon
import os
from cache.pkmCache import populatePkmCache
from cache.abilityCache import populateAbilityCache
from cache.typeCache import populateTypeCache
from cache.dexEntryCache import populateDexEntryCache


app = Flask(__name__)



def nameToId(n):
    print("Create Name to Id Map")
    name_to_id_map = {}
    for i in range(1,n+1):
        pkmname = PKMCache.get(i).name.lower()
        name_to_id_map[pkmname] = i
    return name_to_id_map



PKMCache = None
abilityCache = None
typeCache = None
dexEntryCache = None
generations = {"red", "blue", "yellow"}

nameToIdMap = None

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
    abilities = []
    types = []
    entries = {}
    try:
        if id.isnumeric():
            pokemon = PKMCache.get(int(id))
        else:
            pkmId = nameToIdMap.get(id.lower())
            pokemon = PKMCache.get(pkmId)

        typeOne = '-' if typeCache.get(pokemon.typeone) == None else typeCache.get(pokemon.typeone).name
        typeTwo = '-' if typeCache.get(pokemon.typetwo) == None else typeCache.get(pokemon.typetwo).name

        abtOne = '-' if abilityCache.get(pokemon.abilityone) == None else abilityCache.get(pokemon.abilityone).name
        abtTwo = '-' if abilityCache.get(pokemon.abilitytwo) == None else abilityCache.get(pokemon.abilitytwo).name
        abtThree = '-' if abilityCache.get(pokemon.abilitythree) == None else abilityCache.get(pokemon.abilitythree).name

        types.append(typeOne)
        types.append(typeTwo)
        abilities.append(abtOne.capitalize())
        abilities.append(abtTwo.capitalize())
        abilities.append(abtThree.capitalize())

        entriesList = dexEntryCache.get(pokemon.id)
#        for gen in generations:
#           entries[gen] = entriesList.get(gen).entry

        data = {'name' : pokemon.name,
                 'id' : pokemon.id,
                 'gen': pokemon.gen,
                 'entry' : pokemon.entry,
                 'genus' : pokemon.species,
                 'image' : 'https://th.bing.com/th/id/R.0d045617037f9cef063d1a9dfe2646b7?rik=EswZh150nqhxsg&riu=http%3a%2f%2fwww.snut.fr%2fwp-content%2fuploads%2f2015%2f07%2fimage-de-fleur-6.jpg&ehk=M9uLBYMHQgtcByG2fGYQSKyylapb%2bfCApnNYShcBdfE%3d&risl=&pid=ImgRaw&r=0',
                 'errorholder' : errorholder
                }
        abilitiesArray = abilities
        typesArray = types
        entriesArray = entries
        links = {'prev' : pokemon.id-1,
                 'next' : pokemon.id+1
                 }
        return render_template('pokedexentry.html', data = data, entriesArray = entriesArray, links = links, abilitiesArray = abilitiesArray, typesArray = typesArray)
    except Exception as e:
        print(f'Error: {e}')
        errorholder.append(f'Pokemon with the name or id: "{id}" does not exsist')
        return render_template('index.html', error=errorholder)
        

if __name__ == '__main__':
    try:
        #IRmodel, IRmodelClasses = setUpModel()
        PKMCache = populatePkmCache()
        abilityCache = populateAbilityCache()
        typeCache = populateTypeCache()
        dexEntryCache = populateDexEntryCache()
        nameToIdMap = nameToId(len(PKMCache._cache_instance))
    except:
        pass
    app.run(debug=True)