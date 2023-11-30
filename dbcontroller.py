from dbconnector import getDBConnection
import requests
import json
from pokemonDTO import pokemonDTO
from abilityDTO import abilityDTO
from typeDTO import typeDTO

MAX_NUMBER_OF_ABILITIES = 3
MAX_NUMBER_OF_TYPES = 2 
GET_NUMBER_OF_ABILITIES = 303
GET_NUMBER_OF_POKEMON = 1017
NUMBER_OF_TYPES = 18

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

def getPokemonGenus(pokeDexEntries, DexLang):
            pokeGenuses = pokeDexEntries['genera']
            for x in pokeGenuses:
                language = x['language']['name']
                if language == DexLang:
                    genus = x['genus'].replace('\n', ' ')
                    return genus.replace('é', 'e')

def getAbilities(n):
    abilities = []
    for i in range(1, n+1):
        print('Fetched abilityid: ' + str(i))
        ability_url = 'https://pokeapi.co/api/v2/ability/' + str(i)
        ability_data = json.loads(requests.get(ability_url).text)
        id = ability_data['id']
        name = ability_data['name']
        abEffect = ''
        effects = ability_data['effect_entries']
        for effect in effects:
            lang = effect['language']['name']
            if lang == 'en':
                abEffect  = effect['effect'].replace('é', 'e').replace('\n', ' ')
        ability = abilityDTO.ability(id, name, abEffect)
        abilities.append(ability)
    return abilities

def getTypes(n):
    types = []
    for i in range(1, n+1):
        print('Fetching TypeId: ' + str(i))
        type_url = 'https://pokeapi.co/api/v2/type/' + str(i)
        type_data = json.loads(requests.get(type_url).text)
        id = type_data['id']
        name = type_data['name']
        type = typeDTO.type(id, name)
        types.append(type)
    return types

def getPokemon(n):
    print("Starting creating pokemon list")
    pkm = []
    for i in range(1, n+1):
        print('Fetching pokemonId: ' + str(i))
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/' + str(i)
        species_url = 'https://pokeapi.co/api/v2/pokemon-species/'+str(i)
        pokemon_data = json.loads(requests.get(pokemon_url).text)
        pokemon_species_data = json.loads(requests.get(species_url).text)
        pokeGenus = getPokemonGenus(pokemon_species_data, 'en')
        id = pokemon_data['id']
        name = pokemon_data['name']
        height = pokemon_data['height']*10 #in cm
        weight = pokemon_data['weight']/10 # in kg
        abilities = getAbilitiesForPokemon(pokemon_data['abilities'])
        types = getPokemonTypes(pokemon_data['types'])
        pkm.append(pokemonDTO.create_object(id, name, pokeGenus ,height, weight, abilities[0], abilities[1], abilities[2], types[0], types[1]))
    return pkm

def insertTypes(types):
    conn = getDBConnection()
    cursor = conn.cursor()
    for type in types:
        print('Inserting Type: ' + type.name)
        object_to_insert = (type.typeId, type.name,)
        insert_query = 'INSERT INTO types (typeid, type) VALUES (%s,%s);'
        cursor.execute(insert_query, object_to_insert)
        conn.commit()
    cursor.close()
    conn.close()


def insertPokemon(pokemon):
    conn = getDBConnection()
    cursor = conn.cursor()
    for pkm in pokemon:
        print('Inserting Pokemon: ' + pkm.name)
        object_to_insert = (
            pkm.id, pkm.name, pkm.species, pkm.height, pkm.weight,
            pkm.abilityone, pkm.abilitytwo, pkm.abilitythree, pkm.typeone, pkm.typetwo,)
        insert_query = 'INSERT INTO pokemon (pokedexid, pokemonname, pokemonspecies, pokemonheight, pokemonweight, pokemonabilityone, pokemonabilitytwo, pokemonabilitythree, typeone, typetwo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(insert_query, object_to_insert)
        conn.commit()
    cursor.close()
    conn.close()

def insertAbility(abilities):
    conn = getDBConnection()
    cursor = conn.cursor()
    for abillity in abilities:
        print('Inserting Ability: ' + abillity.name)
        object_to_insert=(
            abillity.id, abillity.name, abillity.effect,
        )
        insert_query = 'INSERT INTO abilities (abilityid, abilityname, abilityeffect) VALUES (%s,%s,%s);'
        cursor.execute(insert_query, object_to_insert)
        conn.commit()
    cursor.close()
    conn.close()


def populateDatabase():
    pkm = getPokemon(GET_NUMBER_OF_POKEMON)
    abilities = getAbilities(GET_NUMBER_OF_ABILITIES)
    types = getTypes(NUMBER_OF_TYPES)
    insertPokemon(pkm)
    insertAbility(abilities)
    insertTypes(types)
    print('Done')

