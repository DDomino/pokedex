import requests
import json
import pyttsx3
from random import randrange
from optparse import OptionParser
from PokemonIRModel import setUpModel
from PokemonIRModel import identifyPokemon
from pokemonDTO import create_object
from PIL import Image

spiciesPrefix = ''

def printPokeDexText(pokeId, pokeName, PokeDexEntry, generation, genus):
    genus = genus if genus != '' else 'Unknown'
    spiciesPrefix = 'The ' if genus != 'Unknown' else ''
    info = 'PokeDex Index: ' + str(pokeId) + '\n' + 'Pokemon Name: ' + pokeName + '\n' + 'Pokemon Genus: ' + spiciesPrefix + genus + '\n' + '------------------- \n'+ 'Generation: '+generation + '\n' + '------------------- \n'+ 'DexEntry:\n'+ PokeDexEntry + '\n'+ '==================='
    return info

def discoverPokemon(pokeId, pokeName, pokeDexEntry, generation, genus):
    info = printPokeDexText(pokeId, pokeName, pokeDexEntry, generation, genus)
    spiciesPrefix = 'The ' if genus != '' else ''
    return info

def getRandomDexEntry(pokeDexEntries, DexLang):
    searching = True
    while(searching):
        rnIndex = randrange(len(pokeDexEntries))
        x = pokeDexEntries[rnIndex]
        language = x['language']['name']
        if language == DexLang:
            newGeneration = x['version']['name']
            entry = x['flavor_text'].replace('\n', ' ')
            searching = False
    return entry, newGeneration


def getFullPokedexEntry(pokeDexEntries, DexLang):
        fullDescription = ''
        for entry in pokeDexEntries:
            language = entry['language']['name']
            if language == DexLang:
                fullDescription += entry['flavor_text'].replace('\n', ' ') + ' '
        #return 'lol' #fullDescription
        return 'Pikachu, a remarkable Pokémon, is distinguished by its bright yellow fur and distinctive features. It keeps its tail raised to stay vigilant, and if provoked, it wont hesitate to bite. This intelligent Pokémon possesses electricity-storing pouches on its cheeks, which can generate powerful electric shocks and even cause lightning storms when multiple Pikachus gather. Its known for roasting hard berries with electricity to make them tender enough to eat. pikachus tail-raising habit sometimes exposes it to lightning strikes. When angered, it immediately discharges the energy stored in its cheek pouches. Interestingly, these pouches become electrically charged during the night while Pikachu sleeps, occasionally leading to discharges when it wakes up groggy. In a unique greeting ritual, Pikachu touch their tails together to exchange electricity. They are known to use electric shocks to revive weakened fellow Pikachus. Its their nature to store electricity, and they can feel stressed if unable to fully discharge it. Forests inhabited by Pikachu can be hazardous due to frequent lightning strikes caused by their electric powers. Despite their adorable appearance, Pikachu should be approached with caution, as their electric sacs can deliver a tingly shock upon contact.', 'Full Description'

def getPokeDexEntryByGen(pokeDexEntries, generation, DexLang):
        for x in pokeDexEntries: 
            if generation == x['version']['name']:
                language = x['language']['name']
                if language == DexLang:
                    return x['flavor_text'].replace('\n', ' ')
                
def getPokemonGenus(pokeDexEntries, DexLang):
            pokeGenuses = pokeDexEntries['genera']
            for x in pokeGenuses:
                language = x['language']['name']
                if language == DexLang:
                    return x['genus'].replace('\n', ' ')

def fetchPokemon(id, generation, DexLang):

    idAsString = str(id)
    requestUrlPoke = 'https://pokeapi.co/api/v2/pokemon/'+idAsString
    requestUrlDex = 'https://pokeapi.co/api/v2/pokemon-species/'+idAsString
    baseUrl = 'http://127.0.0.1:5000/pokemon/'
    try:
        resPoke = requests.get(requestUrlPoke)
        resDex = requests.get(requestUrlDex)
        pokemonDex = json.loads(resDex.text)
        pokemonData = json.loads(resPoke.text)
        pokeId = id if  pokemonData['id'] == id else pokemonData['id']
        pokeName = pokemonData['name']
        PokeDXEntries = pokemonDex['flavor_text_entries']
        pokeGenus = getPokemonGenus(pokemonDex, DexLang)
        singleEntry = ''
        if generation == 'full':
             fullDexentry = getFullPokedexEntry(PokeDXEntries, DexLang)
             discoverPokemon(pokeId, pokeName, fullDexentry, '', pokeGenus)
        elif generation == 'all':
            getAllDexentries(pokeId, pokeName, PokeDXEntries, DexLang)
        elif generation == 'random':
            singleEntry, newGeneration = getRandomDexEntry(PokeDXEntries, DexLang)
            image = 'https://pngimg.com/uploads/pokemon/pokemon_PNG1.png'
            prev = baseUrl+str(pokeId-1)
            next = baseUrl+str(pokeId+1)
            pokemon = create_object(pokeId, pokeName, singleEntry, newGeneration, pokeGenus, image, prev, next)
            return pokemon
        else:
            dexEntry = getPokeDexEntryByGen(PokeDXEntries, generation, DexLang)
            if dexEntry == None:
                dexEntry = 'This is the first time this pokemon is registered in this region'
                pokeName = 'Unknown Pokemon'
                pokeGenus = ''
            discoverPokemon(pokeId, pokeName, dexEntry, generation, pokeGenus)
    except:
        print('Unknown Pokemon')
    return create_object('','','','','', '', '', '')

     