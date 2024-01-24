from flask import Flask, request, redirect
from flask import render_template
from PokemonIRModel import setUpModel, identifyPokemon
import os
from cache.pkmCache import populatePkmCache
from cache.abilityCache import populateAbilityCache
from cache.typeCache import populateTypeCache
from cache.dexEntryCache import populateDexEntryCache
from cache.generationCache import populateGenerationCache
import re
import json


app = Flask(__name__)

allGenerations = []
PKMCache = None
abilityCache = None
typeCache = None
dexEntryCache = None
generationCache = None

nameToIdMap = None

UPLOADR_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOADR_FOLDER
IRmodel = None
IRmodelClasses = []

def nameToId(n):
    print("Create Name to Id Map")
    name_to_id_map = {}
    for i in range(1,n+1):
        pkmname = PKMCache.get(i).name.lower()
        name_to_id_map[pkmname] = i
    return name_to_id_map

# Function to remove control characters
def remove_control_characters(input_string):
    control_chars = ''.join([chr(i) for i in range(32) if i != 10 and i != 13])  # Exclude newline and carriage return
    control_char_pattern = re.compile('[%s]' % re.escape(control_chars))
    return control_char_pattern.sub('', input_string)

def listOfGenerations():
    temp = []
    loopRange = len(generationCache._cache_instance)
    for i in range(1, loopRange+1):
        temp.append(generationCache.get(i).name)
    return temp




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
        if dexEntryCache.get(pokemon.id):
            entriesList = dexEntryCache.get(pokemon.id)
            for gen in allGenerations:
                entry = entriesList.get(gen)
                if entry is not None:
                    originalString = entriesList.get(gen).entry
                    newString = originalString.replace('\x0c', " ")
                    entries[gen] = newString
            json_string = json.dumps(entries)
            cleansed_json_string = remove_control_characters(json_string)
            entries = json.loads(cleansed_json_string)


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
        return render_template('pokedexentry.html', data = data, generations = allGenerations, entriesArray = entriesArray, links = links, abilitiesArray = abilitiesArray, typesArray = typesArray)
    except Exception as e:
        print(f'Error: {e}')
        errorholder.append(f'Pokemon with the name or id: "{id}" does not exsist')
        return render_template('index.html', error=errorholder)
        

if __name__ == '__main__':
   # try:
        #IRmodel, IRmodelClasses = setUpModel()
        PKMCache = populatePkmCache()
        abilityCache = populateAbilityCache()
        typeCache = populateTypeCache()
        dexEntryCache = populateDexEntryCache()
        generationCache = populateGenerationCache()
        allGenerations = listOfGenerations()
        nameToIdMap = nameToId(len(PKMCache._cache_instance))
    #except Exception as e:
        #print("ERROR!  " + str(e))
        app.run(debug=True)