import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
import requests
import json
from DTOs.typeDTO import typeDTO
from DTOs.dexentryDTO import dexentryDTO
from multiprocessing.dummy import Pool as ThreadPool

GET_NUMBER_OF_ENTRIES_FOR_POKEMON = 1017 #Current nr of pokemon in exsistance 1017

def getDexEntry(entryUrl):
    entries = []
    pokedexeEntries = json.loads(requests.get(entryUrl).text)
    allentries = pokedexeEntries['flavor_text_entries']
    for entry in allentries:
        if entry['language']['name'] == 'en':
            pokemonId = pokedexeEntries['id']
            generation = entry['version']['name']
            language = entry['language']['name']
            dexentry = entry['flavor_text'].replace('\n', ' ')
            newEntry = dexentryDTO.create_object(pokemonId, generation, dexentry, language)
            entries.append(newEntry)
    return entries

def getAllDexEntries():
    print("Starting fetch of pokedex entries")
    entries = []
    urls = []
    pool = ThreadPool()
    for i in range(1, GET_NUMBER_OF_ENTRIES_FOR_POKEMON+1):
        urls.append('https://pokeapi.co/api/v2/pokemon-species/'+str(i))
    entry_list = pool.map(getDexEntry, urls)
    pool.close()
    pool.join()
    entries.extend(entry_list)
    return entries

def insertDexEntries(dexEntries):
    conn = getDBConnection()
    cursor = conn.cursor()
    for entriesByPkm in dexEntries:
        for entry in entriesByPkm:
            try:
                print('Inserting Dexentry for pokemonid: ' + str(entry.pokemonId) + ' lang: ' + entry.language)
                object_to_insert=(entry.pokemonId, entry.generation, entry.entry, entry.language,)
                insert_query = 'INSERT INTO dexentries (pokemonid, generation, dexentry, language) VALUES (%s, %s, %s, %s);'
                cursor.execute(insert_query, object_to_insert)
                conn.commit()
            except:
               print(entry.pokemonId, entry.language,' exsist in the table dexentries') 
               pass
    cursor.close()
    conn.close()

def populateDexEntries():
    entries = getAllDexEntries()
    insertDexEntries(entries)