import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
import requests
import json
from DTOs.generationDTO import generationDTO
from multiprocessing.dummy import Pool as ThreadPool


NUMBER_OF_GENERATIONS = 43 #Current numbers of versions

def getGeneration(generationUrl):
    print("Fetching data from:", generationUrl)
    
    response = requests.get(generationUrl)
    
    if response.status_code == 200:
        generationData = json.loads(response.text)
        id = generationData['id']
        name = generationData['name']
        print(f"Successfully fetched generation {id}: {name}")
        return generationDTO.create_object(id, name)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def getAllGenerations():
    generations = []
    urls = []
    pool = ThreadPool()
    for i in range(1,NUMBER_OF_GENERATIONS+1):
        generationUrl = 'https://pokeapi.co/api/v2/version/'+str(i)
        urls.append(generationUrl)
    generationList = pool.map(getGeneration, urls)
    pool.close()
    pool.join()
    generations.extend(generationList)
    return generations

def insertGeneration(generations):
    conn = getDBConnection()
    cursor = conn.cursor()
    for generation in generations:
        try:
            object_to_insert=(generation.id, generation.name,)
            query = "INSERT INTO generations (generationid, generationname) VALUES (%s, %s)"
            cursor.execute(query, object_to_insert)
            conn.commit()
        except:
            pass
    cursor.close()
    conn.close()

def populateGenerations():
    generations = getAllGenerations()
    insertGeneration(generations)


populateGenerations()

