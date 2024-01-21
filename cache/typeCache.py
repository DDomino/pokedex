import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
from cache.cache_module import PkdexCache
from DTOs.typeDTO import typeDTO


def populateTypeCache():
    print("In Populate Type Cache")
    cache = PkdexCache(max_size=100)
    conn = getDBConnection()
    cursor = conn.cursor()
    query = 'Select * from types;'
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        id, typeId, name = row
        type = typeDTO.type(typeId, name)
        cache.set(typeId, type)
    print("Done with typeCache")
    return cache