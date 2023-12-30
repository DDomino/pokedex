from dbpokemoncontroller import populatePokemon
from dbabilitycontroller import populateAbilities
from dbdexentrycontroller import populateDexEntries
from dbtypescontroller import populateTypes


def populateDB():
    populatePokemon()
    populateDexEntries()
    populateAbilities()
    populateTypes()

populateDB()