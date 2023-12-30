import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
from dbconnector import getDBConnection
import requests
import json
from DTOs.abilityDTO import abilityDTO
from multiprocessing.dummy import Pool as ThreadPool

GET_NUMBER_OF_ABILITIES = 303 # Current nr of abilities in exsistance 303

def getAbility(abilityUrl):
    ability_data = json.loads(requests.get(abilityUrl).text)
    id = ability_data['id']
    print('Fetched abilityid: ' + str(id))
    name = ability_data['name']
    abEffect = ''
    effects = ability_data['effect_entries']
    for effect in effects:
        lang = effect['language']['name']
        if lang == 'en':
            abEffect  = effect['effect'].replace('é', 'e').replace('\n', ' ')
    return abilityDTO.ability(id, name, abEffect)

def getAllAbilities():
    abilities = []
    urls = []
    pool = ThreadPool()
    for i in range(1, GET_NUMBER_OF_ABILITIES+1):
        ability_url = 'https://pokeapi.co/api/v2/ability/' + str(i)
        urls.append(ability_url)
    ability_list = pool.map(getAbility, urls)
    pool.close()
    pool.join()
    abilities.extend(ability_list)
    return abilities

def insertAbility(abilities):
    conn = getDBConnection()
    cursor = conn.cursor()
    for ability in abilities:
        try:
            print('Inserting Ability: ' + ability.name)
            object_to_insert=(
                ability.id, ability.name, ability.effect,
            )
            insert_query = 'INSERT INTO abilities (abilityid, abilityname, abilityeffect) VALUES (%s,%s,%s);'
            cursor.execute(insert_query, object_to_insert)
            conn.commit()
        except:
            print(ability.name, ability.id, ' exsist in table Abilities')
            pass
    cursor.close()
    conn.close()

def populateAbilities():
    abilities = getAllAbilities()
    insertAbility(abilities)