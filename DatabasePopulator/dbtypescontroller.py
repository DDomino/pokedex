import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from DTOs.typeDTO import typeDTO
from dbconnector import getDBConnection
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

NUMBER_OF_TYPES = 18 #Current nr of types in exsistance 18

def getType(typeUrl):
    type_data = json.loads(requests.get(typeUrl).text)
    id = type_data['id']
    name = type_data['name']
    return typeDTO.type(id, name)

def getAllTypes():
    types = []
    urls = []
    pool = ThreadPool()
    for i in range(1, NUMBER_OF_TYPES+1):
        print('Fetching TypeId: ' + str(i))
        urls.append('https://pokeapi.co/api/v2/type/' + str(i))
    type_list = pool.map(getType, urls)
    pool.close()
    pool.join()
    types.extend(type_list)
    return types

def insertTypes(types):
    conn = getDBConnection()
    cursor = conn.cursor()
    for type in types:
        try:
            print('Inserting Type: ' + type.name)
            object_to_insert = (type.typeId, type.name,)
            insert_query = 'INSERT INTO types (typeid, type) VALUES (%s,%s);'
            cursor.execute(insert_query, object_to_insert)
            conn.commit()
        except:
            print(type.name, ' exsist in table types')
            pass
    cursor.close()
    conn.close()

def populateTypes():
    types = getAllTypes()
    insertTypes(types)