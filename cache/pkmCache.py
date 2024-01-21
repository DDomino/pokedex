import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
from cache.cache_module import PkdexCache
from DTOs.pokemonDTO import pokemonDTO


def populatePkmCache():
    print("In populate Pokemon")
    cache = PkdexCache(max_size=3000)
    conn = getDBConnection()
    cursor = conn.cursor()
    query = 'Select * from pokemon;'
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        id, pokedexid, pokemonname,pokemonspecies,pokemonheight, pokemonweight, pokemonabilityone, pokemonabilitytwo, pokemonabilitythree, typeone, typetwo = row 
        pokemon = pokemonDTO.create_object(pokedexid, pokemonname, pokemonspecies, pokemonheight, pokemonweight, pokemonabilityone, pokemonabilitytwo, pokemonabilitythree, typeone, typetwo, None, None, None)
        cache.set(pokedexid, pokemon)
    return cache
    

