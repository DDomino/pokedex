import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
from cache.cache_module import PkdexCache
from DTOs.abilityDTO import abilityDTO

def populateAbilityCache():
    cache = PkdexCache(max_size=1000)
    conn = getDBConnection()
    cursor = conn.cursor()
    query = 'Select abilityid, abilityname, abilityeffect from abilities;'
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        abilityid, ablityname, abilityeffect = row
        ability = abilityDTO.ability(abilityid, ablityname, abilityeffect)
        cache.set(abilityid, ability)
    return cache
    

