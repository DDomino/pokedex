import requests
import json
import os
from optparse import OptionParser
from multiprocessing.dummy import Pool as ThreadPool
 
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def createUrls(number):
    urls = []
    for i in range(1, number+1):
        urls.append('https://pokeapi.co/api/v2/pokemon/'+str(i))
    return urls

index = 0
testnumber = 0

def poolFunction(url):
        res = requests.get(url)
        response = json.loads(res.text)
        name = response['name']
        spritesKeyValue = response['sprites']
        spriteUrlList = getSpriteUrls(spritesKeyValue)
        savePokemonImages(spriteUrlList, name)


def getPokemonSprites(numberOfPokemonToGet):
    pool = ThreadPool()
    urls = createUrls(numberOfPokemonToGet)
    printProgressBar(0, numberOfPokemonToGet, prefix='Progress', suffix='Complete', length=50)
    pool.map(poolFunction, urls)
    pool.close()
    pool.join()
    printProgressBar(index, numberOfPokemonToGet, prefix='Progress', suffix='Complete', length=50)

def getSpriteUrls(sprites):
    spriteUrls = []
    spritesDefault = sprites
    for key, value in spritesDefault.items():
        if key == 'front_default' or key == 'back_default':
            spriteUrls.append(value)
    spritesByVersion = sprites['versions']
    for key,value in spritesByVersion.items():
        for k,v in value.items():
            if 'animated' not in v:
                for x, y in v.items():
                    spriteUrls.append(y)
    spritesByDreamWorld = sprites['other']['dream_world']
    for key, value in spritesByDreamWorld.items():
        spriteUrls.append(value)
    spritesByHome = sprites['other']['home']
    for key,value in spritesByHome.items():
        spriteUrls.append(value)
    officialArt = sprites['other']['official-artwork']
    for key,value in officialArt.items():
        spriteUrls.append(value)
    return spriteUrls        


def savePokemonImages(urlList, name):
    new_directory = './pokemon/'+name+'/'
    os.makedirs(new_directory)
    directory_path = new_directory
    imageIndex = 1
    for url in urlList:
        if url != None:
            if '.gif' not in url:
                fileExt = ''
                res = requests.get(url)
                image_data = res.content
                if 'dream-world' in url:
                    fileExt = '.svg'
                else:
                    fileExt = '.png'
                file_name = str(imageIndex)+fileExt
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, 'wb') as file:
                    file.write(image_data)
                imageIndex+=1
            else:
                print('gif')

def getSprites(options = None):
    numberOfPokemon = int(options.pokemonToGet)
    getPokemonSprites(numberOfPokemon)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-g', '--get', dest = 'pokemonToGet')
    (options, args) = parser.parse_args()
    getSprites(options)