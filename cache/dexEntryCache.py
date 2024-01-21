import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
from cache.cache_module import PkdexCache
from DTOs.dexentryDTO import dexentryDTO


def populateDexEntryCache():
    cache = PkdexCache(max_size=100000)
    conn = getDBConnection()
    cursor = conn.cursor()
    query = 'Select * from dexentries;'
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        id, pokemonId, generation, dexEntry, language = row
        dexEntry = dexentryDTO.create_object(pokemonId, generation, dexEntry, language)
        if cache.get(pokemonId):
            internalCache = cache.get(pokemonId)
            internalCache.set(generation, dexEntry)
        else:
            internalCache = PkdexCache(100)
            internalCache.set(generation, dexEntry)
            cache.set(pokemonId, internalCache)
    print("Populated entryDexCache")
    return cache

            