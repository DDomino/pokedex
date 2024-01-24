import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
from cache.cache_module import PkdexCache
from DTOs.generationDTO import generationDTO

def populateGenerationCache():
    cache = PkdexCache(max_size=100)
    conn = getDBConnection()
    cursor = conn.cursor()
    query = 'Select * from generations'
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        id, generationId, name = row
        generation = generationDTO.create_object(generationId, name)
        cache.set(generationId, generation)
    return cache