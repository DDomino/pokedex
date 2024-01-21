import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from  dbconnector import getDBConnection
import requests
import json
from DTOs.pokemonDTO import pokemonDTO
from multiprocessing.dummy import Pool as ThreadPool

GET_NUMBER_OF_POKEMON = 1017 #Current nr of pokemon in exsistance 1017
MAX_NUMBER_OF_ABILITIES = 3
MAX_NUMBER_OF_TYPES = 2 

def createPokemon(id, name, pokeGenus ,height, weight, ability1, ability2, ability3, type1, types2):
    return pokemonDTO.create_object(id, name, pokeGenus ,height, weight,ability1, ability2,ability3, type1, types2, None, None, None)

def getAbilitiesForPokemon(pokemonAbilities):
    index = 0
    abilityindex = []
    for i in range(0, MAX_NUMBER_OF_ABILITIES):
        abilityindex.append(None)
    try:
        for ability in pokemonAbilities:
            if index > 3:
                raise IndexError("The number of abilities esceeds the number of columns")
            ability_is_hidden = False
            if ability['is_hidden']:
                ability_is_hidden = True
            aIndex = ability['ability']['url']
            aIndex = aIndex.split('/')
            aIndex = aIndex[-2]
            if ability_is_hidden:
                abilityindex[-1] = aIndex
            else:
                abilityindex[index] = aIndex
            index += 1
        return abilityindex
    except IndexError as IE:
        print(f"Caught an IndexError: {IE}")

def getPokemonGenus(pokeDexEntries, DexLang):
            pokeGenuses = pokeDexEntries['genera']
            for x in pokeGenuses:
                language = x['language']['name']
                if language == DexLang:
                    genus = x['genus'].replace('\n', ' ')
                    return genus.replace('é', 'e')        

def getPokemonTypes(pokemonTypes):
    index = 0
    typeIndexs = []
    for i in range(0, MAX_NUMBER_OF_TYPES):
        typeIndexs.append(None)
    for type in pokemonTypes:
        tIndex = type['type']['url']
        tIndex = tIndex.split('/')
        tIndex = tIndex[-2]
        typeIndexs[index] = tIndex
        index += 1
    return typeIndexs

def getPokemon(pokemonUrl, speciesUrl):
    pokemon_data = json.loads(requests.get(pokemonUrl).text)
    pokemon_species_data = json.loads(requests.get(speciesUrl).text)
    pokeGenus = getPokemonGenus(pokemon_species_data, 'en')
    id = pokemon_data['id']
    name = pokemon_data['name']
    height = pokemon_data['height']*10 #in cm
    weight = pokemon_data['weight']/10 # in kg
    abilities = getAbilitiesForPokemon(pokemon_data['abilities'])
    types = getPokemonTypes(pokemon_data['types'])
    return createPokemon(id, name, pokeGenus ,height, weight, abilities[0], abilities[1], abilities[2], types[0], types[1])

def getAllPokemon():
    print("Starting fetch of pokemon")
    pkm  = []
    pool = ThreadPool()
    params = [('https://pokeapi.co/api/v2/pokemon/' + str(i), 'https://pokeapi.co/api/v2/pokemon-species/'+str(i)) for i in range(1,GET_NUMBER_OF_POKEMON+1)]
    pokemon_list = pool.starmap(getPokemon, params)
    pool.close()
    pool.join()
    pkm.extend(pokemon_list)
    return pkm

def insertPokemon(pokemon):
    conn = getDBConnection()
    cursor = conn.cursor()
    for pkm in pokemon:
        try:
            print('Inserting Pokemon: ' + pkm.name)
            object_to_insert = (
                pkm.id, pkm.name, pkm.species, pkm.height, pkm.weight,
                pkm.abilityone, pkm.abilitytwo, pkm.abilitythree, pkm.typeone, pkm.typetwo,)
            insert_query = 'INSERT INTO pokemon (pokedexid, pokemonname, pokemonspecies, pokemonheight, pokemonweight, pokemonabilityone, pokemonabilitytwo, pokemonabilitythree, typeone, typetwo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(insert_query, object_to_insert)
            conn.commit()
        except:
            print(pkm.name, pkm.id, ' exsist in table pokemon' )
            pass
    cursor.close()
    conn.close()

def populatePokemon():
    pokemon = getAllPokemon()
    insertPokemon(pokemon)